import unittest, os
import sys
sys.path.append('../Initial_project')
from source import FileManager


class FileManagerTest(unittest.TestCase):
    def setUp(self):
        self.base_address = os.path.dirname(__file__)
        self.user_file_manager = FileManager()

    def test_delete_unavailable_file(self):
        self.user_file_manager.delete('test.txt', self.base_address + '/fmt')


if __name__ == '__main__':
    unittest.main()