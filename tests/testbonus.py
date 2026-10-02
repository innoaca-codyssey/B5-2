from pathlib import Path
import tempfile
import unittest
from diffing import diff_lines, diff_files
from main import execute
from repository import Repository
from sorting import insertion_sort, merge_sort


class BonusTests(unittest.TestCase):
    def test_diff_common_added_deleted_and_repeated(self):
        result=list(diff_lines(['a\n','b\n','a\n'],['a\n','c\n','a\n','d\n']))
        self.assertEqual([v for marker,v in result if marker!='+'],['a\n','b\n','a\n'])
        self.assertEqual([v for marker,v in result if marker!='-'],['a\n','c\n','a\n','d\n'])
        self.assertIn(('-', 'b\n'),result)
        self.assertIn(('+', 'c\n'),result)

    def test_diff_empty_files_unicode_and_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            a,b=Path(directory)/'a.txt',Path(directory)/'b.txt'
            a.write_text('한글\n');b.write_text('한글\n새 줄\n')
            self.assertIn('+ 새 줄',diff_files(a,b))
            self.assertIn('새 줄',execute(Repository(),f'DIFF "{a}" "{b}"'))
            a.write_text('');b.write_text('')
            self.assertIn('empty files',diff_files(a,b))
            self.assertIn('No such file',execute(Repository(),f'DIFF "{a}" "{b}.missing"'))

    def test_two_sorts_equal_stable_and_input_unchanged(self):
        original=[(3,'a'),(1,'b'),(3,'c'),(2,'d'),(1,'e')]
        expected=[(1,'b'),(1,'e'),(2,'d'),(3,'a'),(3,'c')]
        for sorting in [merge_sort,insertion_sort]:
            self.assertEqual(sorting(original,lambda x:x[0]),expected)
            self.assertEqual(sorting([]),[])
        self.assertEqual(original[0],(3,'a'))


if __name__=='__main__':unittest.main()
