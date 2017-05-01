import os
import unittest
import random

from files_in_there_but_not_here import FilesystemWalker

random.seed(0)

@unittest.skip('not yet written')
class SplitPathFileTest(unittest.TestCase):

    def test_sample(self):
        self.assertTrue(True, 'Dummy test')


class FilesystemWalkerTest(unittest.TestCase):
    dir1 = '/home/kp/Documents/class/cs6402 - Advanced Topics in Data Mining (copy 1)/'
    dir2 = '/home/kp/Documents/class/cs6402 - Advanced Topics in Data Mining/'
    def test_sample(self):
        # create two directories containing some files
        target_directory = FilesystemWalker(FilesystemWalkerTest.dir1,
                                            cache_files=True)
        other_directory = FilesystemWalker(FilesystemWalkerTest.dir2,
                                           cache_files=True)
        for f in other_directory:
            print(f)

@unittest.skip('not yet written')
class SameSizedFilesTest(unittest.TestCase):

    def test_sample(self):
        self.assertTrue(True, 'Dummy test')


@unittest.skip('not yet written')
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
    #unittest.main()
    dir1 = '/home/kp/Documents/class/cs6402 - Advanced Topics in Data Mining (copy 1)/'
    dir2 = '/home/kp/Documents/class/cs6402 - Advanced Topics in Data Mining/'

    target_directory = FilesystemWalker(dir1, cache_files=True)
    other_directory = FilesystemWalker(dir2, cache_files=True)

    for file in other_directory:
        if file in target_directory:
            pass

        else:
            print(file)
            print('='*80)