#!/usr/bin/env python3

import io
import os
import sys
import unittest
from unittest.mock import patch

import filterfollow # pip install -e filterfollow - Or install into venv.


#%%
class TestFilterFollow(unittest.TestCase):
    '''
    Test the FilterFollow class
    '''

    def file2str(self,testfile):
        '''
        Return content of testfile as a str. The file need to be in the testfile
        directory.
        '''
        with open(self.get_test_file_path(testfile)) as mfile:
            return mfile.read()

    def get_test_file_path(self, testfile):
        '''
        Get the full path a file, testfile, in the testfiles subfolder.
        '''
        return os.path.join(os.path.dirname(__file__),"testfiles", testfile)

    # def test_helloworld(self):
    #     '''
    #     If this test run. The tests are up and running.
    #     '''
    #     pass

    def test_from_file_basic_simple(self):
        '''
        Basic test against the readme test file.
        '''
        infile = self.get_test_file_path("testfile_02_from_readme.txt")
        expfile = self.get_test_file_path("testfile_02_01_exp_basic_simple.txt")

        exp = self.file2str(expfile)

        ff = filterfollow.FilterFollow(filename=infile,
                                       startpattern="^PATTERN1",
                                       endpattern="^PATTERN2",
                                       includestarting=True)
        ret = "".join(ff.run())

        self.assertEqual(exp,ret)

    def test_from_file_extended_simple(self):
        '''
        Including end pattern to test against the readme test file.
        '''
        infile = self.get_test_file_path("testfile_02_from_readme.txt")
        expfile = self.get_test_file_path("testfile_02_02_exp_extended_includeclosing.txt")

        with open(expfile) as mfile:
            exp = mfile.read()

        ff = filterfollow.FilterFollow(filename=infile,
                                       startpattern="^PATTERN1",
                                       endpattern="^PATTERN2",
                                       includestarting=True,
                                       includeclosing=True)
        ret = "".join(ff.run())

        self.assertEqual(exp, ret)

    def test_from_file_extended_excludestarting(self):
        '''
        Exclude starting pattern to test against the readme test file.
        '''
        infile = self.get_test_file_path("testfile_02_from_readme.txt")
        expfile = self.get_test_file_path("testfile_02_03_exp_extended_excludestarting.txt")

        with open(expfile) as mfile:
            exp = mfile.read()

        ff = filterfollow.FilterFollow(filename=infile,
                                       startpattern="^PATTERN1",
                                       endpattern="^PATTERN2",)
        ret = "".join(ff.run())

        self.assertEqual(exp, ret)

    def test_from_file_extended_excludestarting_includeclosing(self):
        '''
        Exclude starting pattern to test against the readme test file.
        '''
        infile = self.get_test_file_path("testfile_02_from_readme.txt")
        expfile = self.get_test_file_path("testfile_02_04_exp_excludestarting_includeclosing.txt")

        with open(expfile) as mfile:
            exp = mfile.read()

        ff = filterfollow.FilterFollow(filename=infile,
                                       startpattern="^PATTERN1",
                                       endpattern="^PATTERN2",
                                       includeclosing=True,)
        ret = "".join(ff.run())

        self.assertEqual(exp, ret)

    # Need to send KeyboardInterrupt to stop the read. And then debug the test.
    # def test_from_file_basic_stdin(self):
    #     '''
    #     Basic test against the readme test file.
    #     '''
    #     infile = "testfile_02_from_readme.txt"
    #     expfile = self.get_test_file_path("testfile_02_01_exp_basic_simple.txt")
    #
    #     exp = self.file2str(expfile)
    #     with patch("sys.stdin",io.StringIO(self.file2str(infile))) as mthing:
    #         ff = filterfollow.FilterFollow(startpattern="^PATTERN1",
    #                                        endpattern="^PATTERN2")
    #         ret = "".join(ff.run())
    #
    #     self.assertEqual(exp,ret)
