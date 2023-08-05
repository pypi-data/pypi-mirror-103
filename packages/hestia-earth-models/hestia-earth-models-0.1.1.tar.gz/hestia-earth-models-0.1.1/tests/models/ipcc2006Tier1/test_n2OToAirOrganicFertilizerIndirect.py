import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.ipcc2006Tier1.n2OToAirOrganicFertilizerIndirect import TERM_ID, run, _should_run

class_path = f"hestia_earth.models.ipcc2006Tier1.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/ipcc2006Tier1/{TERM_ID}"


class TestN2OToAirOrganicFertilizerIndirect(unittest.TestCase):
    def test_should_run(self):
        # no inputs => no run
        cycle = {'inputs': []}
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with kg N inputs => no run
        cycle['inputs'] = [{
            'term': {
                'units': 'kg N',
                'termType': 'organicFertilizer'
            },
            'value': [100]
        }]
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with no3 emission => run
        cycle['emissions'] = [{
            'term': {
                '@id': 'no3ToGroundwaterOrganicFertilizer'
            },
            'value': [100]
        }]
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, True)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
