import unittest
from unittest.mock import patch

from hestia_earth.models.stehfestBouwman2006.noxToAirAllOrigins import TERM_ID, _get_value, _should_run

class_path = f"hestia_earth.models.stehfestBouwman2006.{TERM_ID}"


class TestNh3ToAirCropResidueBurning(unittest.TestCase):
    @patch(f"{class_path}._residue_nitrogen", return_value=0)
    @patch(f"{class_path}._most_relevant_measurement_value", return_value=[])
    def test_should_run(self, mock_most_relevant_measurement_value, *args):
        # no measurements => no run
        cycle = {'inputs': [], 'measurements': []}
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with measurements => no run
        mock_most_relevant_measurement_value.return_value = [10]
        cycle['measurements'] = [{}]
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with kg N inputs => run
        cycle['inputs'] = [{
            'term': {
                'units': 'kg N'
            },
            'value': [100]
        }]
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, True)

    def test_get_value(self):
        ecoClimateZone = '5'
        nitrogenContent = 100
        N_total = 7
        self.assertEqual(_get_value(ecoClimateZone, nitrogenContent, N_total), 0.08456876974469733)
