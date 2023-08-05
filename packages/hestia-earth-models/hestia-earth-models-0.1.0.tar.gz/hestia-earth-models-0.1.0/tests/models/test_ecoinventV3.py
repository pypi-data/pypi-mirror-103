import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.ecoinventV3 import run, TERM_IDS

class_path = 'hestia_earth.models.ecoinventV3'
fixtures_folder = f"{fixtures_path}/ecoinventV3"


class TestEcoinventV3(unittest.TestCase):
    @patch(f"{class_path}._emission", return_value={})
    def test_run_all_models(self, mock):
        run(None, {})
        self.assertEqual(mock.call_count, len(TERM_IDS))

        mock.reset_mock()
        run('', {})
        self.assertEqual(mock.call_count, len(TERM_IDS))

        mock.reset_mock()
        run('null', {})
        self.assertEqual(mock.call_count, len(TERM_IDS))

        mock.reset_mock()
        run('all', {})
        self.assertEqual(mock.call_count, len(TERM_IDS))

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_nh3ToAirInputsProduction(self, *args):
        term_id = 'nh3ToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_co2ToAirInputsProduction(self, *args):
        term_id = 'co2ToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_n2OToAirInputsProduction(self, *args):
        term_id = 'n2OToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_ch4ToAirInputsProductionFossil(self, *args):
        term_id = 'ch4ToAirInputsProductionFossil'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_ch4ToAirInputsProductionNonFossil(self, *args):
        term_id = 'ch4ToAirInputsProductionNonFossil'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_noxToAirInputsProduction(self, *args):
        term_id = 'noxToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_so2ToAirInputsProduction(self, *args):
        term_id = 'so2ToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_bromochlorodifluoromethaneToAirInputsProduction(self, *args):
        term_id = 'bromochlorodifluoromethaneToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_chlorodifluoromethaneToAirInputsProduction(self, *args):
        term_id = 'chlorodifluoromethaneToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_dichlorodifluoromethaneToAirInputsProduction(self, *args):
        term_id = 'dichlorodifluoromethaneToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_112TrichlorotrifluoroethaneToAirInputsProduction(self, *args):
        term_id = '112TrichlorotrifluoroethaneToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_11DichlorotetrafluoroethaneToAirInputsProduction(self, *args):
        term_id = '11DichlorotetrafluoroethaneToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_1112TetrafluoroethaneToAirInputsProduction(self, *args):
        term_id = '1112TetrafluoroethaneToAirInputsProduction'

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/{term_id}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(term_id, cycle)
        self.assertEqual(result, expected)
