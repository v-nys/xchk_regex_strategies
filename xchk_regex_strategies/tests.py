import unittest
import datetime
import regex
from unittest.mock import MagicMock
from django.test import TestCase
from xchk_regex_strategies.strats import RegexCheck
from xchk_core.strats import OutcomeAnalysis, OutcomeComponent
from xchk_core.models import SubmissionV2

# tests go here
class RegexMatchingTest(TestCase):

    def test_matching_string(self):
        chk = RegexCheck(pattern=regex.compile(r'a[bc]d+e'))
        # open is called, producing a context manager
        # context_manager has __enter__, which produces file handle
        # file handle's read method is called to produce text
        mock_open = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = 'acdddddddde'
        submission = SubmissionV2(content_uid='some_uid')
        analysis = chk.check_submission(submission=submission,student_path='/student',model_path='/home/model',desired_outcome=True,init_check_number=1,parent_is_negation=False,open=mock_open)
        expected = OutcomeAnalysis(outcome=True,outcomes_components=[OutcomeComponent(component_number=1,outcome=True,desired_outcome=True,rendered_data='',acceptable_to_ancestor=True)])
        self.assertEquals(analysis,expected)

    def test_nonmatching_string_single_line(self):
        chk = RegexCheck(pattern=regex.compile(r'a[bc]d+e'))
        mock_open = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = 'acddddddddf'
        submission = SubmissionV2(content_uid='some_uid')
        analysis = chk.check_submission(submission=submission,student_path='/student',model_path='/home/model',desired_outcome=True,init_check_number=1,parent_is_negation=False,open=mock_open)
        expected = OutcomeAnalysis(outcome=False,outcomes_components=[OutcomeComponent(component_number=1,outcome=False,desired_outcome=True,rendered_data='<p>Je oplossing verschilt van een gekend patroon vanaf regel 1, karakter 11.</p>')])
        self.assertEquals(analysis,expected)

    def test_nonmatching_string_multiple_lines(self):
        chk = RegexCheck(pattern=regex.compile(r'a[bc]d+e\nfghi'))
        mock_open = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = 'acdddddddde\nfgih'
        submission = SubmissionV2(content_uid='some_uid')
        analysis = chk.check_submission(submission=submission,student_path='/student',model_path='/home/model',desired_outcome=True,init_check_number=1,parent_is_negation=False,open=mock_open)
        expected = OutcomeAnalysis(outcome=False,outcomes_components=[OutcomeComponent(component_number=1,outcome=False,desired_outcome=True,rendered_data='<p>Je oplossing verschilt van een gekend patroon vanaf regel 2, karakter 3.</p>')])
        self.assertEquals(analysis,expected)

if __name__ == '__main__':
    unittest.main()
