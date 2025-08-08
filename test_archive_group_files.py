import unittest
from unittest.mock import patch, MagicMock
import errno
import archive_group_files 


class TestArchiveGroupFiles(unittest.TestCase):
    @patch('archive_group_files.grp.getgrnam')
    @patch('archive_group_files.pwd.getpwall')
    def test_get_group_members_includes_primary_and_secondary(self, mock_getpwall, mock_getgrnam):
        # Setup mock group info
        mock_group = MagicMock()
        mock_group.gr_mem = ['user1', 'user2']
        mock_group.gr_gid = 1000
        mock_getgrnam.return_value = mock_group

        # Setup mock users list (primary group)
        user_primary = MagicMock(pw_name='user3', pw_gid=1000)
        user_other = MagicMock(pw_name='user4', pw_gid=2000)
        mock_getpwall.return_value = [user_primary, user_other]

        result = archive_group_files.get_group_members('developers', logger=MagicMock())
        self.assertIn('user1', result)
        self.assertIn('user2', result)
        self.assertIn('user3', result)
        self.assertNotIn('user4', result)

    @patch('archive_group_files.shutil.move')
    @patch('archive_group_files.shutil.copy2')
    @patch('archive_group_files.os.unlink')
    def test_safe_move_cross_device(self, mock_unlink, mock_copy2, mock_move):
        # Simulate EXDEV error on move, fallback to copy + unlink
        mock_move.side_effect = OSError(errno.EXDEV, "Cross-device link")

        src = '/path/srcfile'
        dst = '/path/dstfile'

        archive_group_files.safe_move(src, dst)

        mock_copy2.assert_called_once_with(src, dst)
        mock_unlink.assert_called_once_with(src)

    @patch('archive_group_files.safe_move')
    @patch('archive_group_files.pwd.getpwnam')
    @patch('archive_group_files.Path.iterdir')
    @patch('archive_group_files.Path.exists')
    @patch('archive_group_files.Path.mkdir')
    def test_process_user_moves_files(self, mock_mkdir, mock_exists, mock_iterdir, mock_getpwnam, mock_safe_move):
        # Setup user info with home directory
        mock_user_info = MagicMock()
        mock_user_info.pw_dir = '/home/testuser'
        mock_getpwnam.return_value = mock_user_info

        # Mock user home directory exists
        mock_exists.return_value = True

        # Mock files in home directory
        mock_file1 = MagicMock()
        mock_file1.is_file.return_value = True
        mock_file1.name = 'file1.txt'
        mock_file2 = MagicMock()
        mock_file2.is_file.return_value = False  # directory or something else
        mock_file2.name = 'dir1'

        mock_iterdir.return_value = [mock_file1, mock_file2]

        # Call process_user
        count = archive_group_files.process_user('testuser', 'developers', logger=MagicMock())

        self.assertEqual(count, 1)
        mock_safe_move.assert_called_once()
