import unittest
from unittest.mock import patch

from hestia_earth.models.stehfestBouwman2006GisImplementation.noxToAirAllOrigins import TERM_ID, _get_value, _should_run

class_path = f"hestia_earth.models.stehfestBouwman2006GisImplementation.{TERM_ID}"


class TestNh3ToAirCropResidueBurning(unittest.TestCase):
    @patch(f"{class_path}._residue_nitrogen", return_value=0)
    def test_should_run(self, *args):
        # no country => no run
        cycle = {'inputs': [], 'site': {}}
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with country => no run
        cycle['site'] = {'country': {'@id': 'country'}}
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
        country_id = 'GADM-GBR'
        N_total = 7
        self.assertEqual(_get_value(country_id, N_total), 0.027810475)
