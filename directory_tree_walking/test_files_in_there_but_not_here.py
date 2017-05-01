import os
import unittest
import random
random.seed(0)


class SplitPathFileTest(unittest.TestCase):

    def test_sample(self):
        self.assertTrue(True, 'Dummy test')


class FilesystemWalkerTest(unittest.TestCase):

    def test_sample(self):
        self.assertTrue(True, 'Dummy test')


class SameSizedFilesTest(unittest.TestCase):

    def test_sample(self):
        self.assertTrue(True, 'Dummy test')


class FileSynchronizerScriptBuilderTest(unittest.TestCase):

    def test_sample(self):
        pass


def create_temp_file(directory, size):
    os.makedirs(directory, exist_ok=True)
    filename = str(random.randint(0, 100001))
    file = os.path.join(directory, filename)

    with open(file, 'w') as f:
        for i in range(size):
            f.write('0')

    return file


if __name__ == '__main__':
    unittest.main()
