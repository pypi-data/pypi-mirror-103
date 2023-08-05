import unittest
from unittest.mock import patch

from hestia_earth.models.emeaEea2019.utils import _get_fuel_values

class_path = 'hestia_earth.models.emeaEea2019.utils'


class TestUtils(unittest.TestCase):
    @patch(f"{class_path}._is_term_type_complete", return_value=True)
    def test_get_fuel_values_no_inputs_complete(self, *args):
        cycle = {'inputs': []}
        self.assertEqual(_get_fuel_values(cycle), ([0], [0]))

    @patch(f"{class_path}._is_term_type_complete", return_value=False)
    def test_get_fuel_values_no_inputs_incomplete(self, *args):
        cycle = {'inputs': []}
        self.assertEqual(_get_fuel_values(cycle), ([], []))

    @patch(f"{class_path}._load_property", return_value='diesel\ngasoline')
    def test_get_fuel_values(self, *args):
        cycle = {'inputs': [
            {
                'term': {'@id': 'diesel'},
                'value': [100]
            },
            {
                'term': {'@id': 'gasoline'},
                'value': [50]
            }
        ]}
        self.assertEqual(_get_fuel_values(cycle), ([100], [50]))
