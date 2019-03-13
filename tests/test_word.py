# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-03-12 21:43:53
# @Last Modified time: 2019-03-13 10:47:43
import unittest
import chardet
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class TestWord(unittest.TestCase):

    def test_coding(self):
        with open(os.path.join(basedir, '..', 'words.txt'), 'rb') as f:
            code = chardet.detect(f.read())['encoding']
            self.assertEqual(code, 'utf-8')

    def test_duplicate_word(self):
        with open(os.path.join(basedir, '..', 'words.txt'), 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), len(set(lines)))

    def test_split(self):
        with open(os.path.join(basedir, '..', 'words.txt'), 'r') as f:
            lines = f.readlines()
            for line in lines:
                ss = line.split(' ')
                self.assertEqual(2, len(ss))


if __name__ == '__main__':
    unittest.main()
