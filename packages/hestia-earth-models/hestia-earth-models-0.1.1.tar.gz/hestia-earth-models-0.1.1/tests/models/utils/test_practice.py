import unittest
from unittest.mock import patch
from tests.utils import TERM

from hestia_earth.models.utils.practice import _new_practice


class TestPractice(unittest.TestCase):
    @patch('hestia_earth.models.utils.practice._include_methodModel', side_effect=lambda n, x: n)
    @patch('hestia_earth.models.utils.practice.download_hestia', return_value=TERM)
    def test_new_practice(self, *args):
        # with a Term as string
        practice = _new_practice('term')
        self.assertEqual(practice, {
            '@type': 'Practice',
            'term': TERM
        })

        # with a Term as dict
        practice = _new_practice(TERM)
        self.assertEqual(practice, {
            '@type': 'Practice',
            'term': TERM
        })
