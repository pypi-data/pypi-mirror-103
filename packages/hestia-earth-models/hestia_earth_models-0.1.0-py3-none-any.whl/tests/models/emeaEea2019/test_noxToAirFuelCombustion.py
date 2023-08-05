import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.emeaEea2019.noxToAirFuelCombustion import TERM_ID, run, _should_run

class_path = f"hestia_earth.models.emeaEea2019.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/emeaEea2019/{TERM_ID}"


class TestNoxToAirCropResidueBurning(unittest.TestCase):
    @patch(f"{class_path}._get_fuel_values")
    def test_should_run(self, mock_get_fuel_values):
        # no fuel values => no run
        mock_get_fuel_values.return_value = ([], [])
        should_run, *args = _should_run({})
        self.assertEqual(should_run, False)

        # with fuel values => run
        mock_get_fuel_values.return_value = ([0], [0])
        should_run, *args = _should_run({})
        self.assertEqual(should_run, True)

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)
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

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_data_complete(self, _m):
        with open(f"{fixtures_folder}/no-input-data-complete/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/no-input-data-complete/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
