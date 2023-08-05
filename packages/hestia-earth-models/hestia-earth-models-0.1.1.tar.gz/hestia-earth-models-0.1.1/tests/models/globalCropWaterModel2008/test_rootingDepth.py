import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_property, fake_download

from hestia_earth.models.globalCropWaterModel2008.rootingDepth import TERM_ID, run, _should_run, _should_run_product

class_path = 'hestia_earth.models.globalCropWaterModel2008.rootingDepth'
fixtures_folder = f"{fixtures_path}/globalCropWaterModel2008/{TERM_ID}"


class TestRootingDepth(unittest.TestCase):
    def test_should_run(self):
        cycle = {'functionalUnitMeasure': '1 ha'}
        self.assertEqual(_should_run(cycle), True)

        cycle = {'functionalUnitMeasure': 'relative'}
        self.assertEqual(_should_run(cycle), False)

    def test_should_run_product(self):
        product = {}
        # no properties => run
        self.assertEqual(_should_run_product(product), True)

        # product with model => does not run
        prop = {
            'term': {
                '@id': TERM_ID
            }
        }
        product['properties'] = [prop]
        self.assertEqual(_should_run_product(product), False)

    @patch(f"{class_path}.download_hestia", side_effect=fake_download)
    @patch(f"{class_path}._new_property", side_effect=fake_new_property)
    def test_run(self, _m1, _m2):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)

    @patch(f"{class_path}.download_hestia", side_effect=fake_download)
    @patch(f"{class_path}._new_property", side_effect=fake_new_property)
    def test_gap_fill_with_irrigation(self, _m1, _m2):
        with open(f"{fixtures_folder}/with-irrigation/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/with-irrigation/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
