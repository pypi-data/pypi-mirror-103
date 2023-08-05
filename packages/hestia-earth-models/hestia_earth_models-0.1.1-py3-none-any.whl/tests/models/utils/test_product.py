import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, TERM

from hestia_earth.models.utils.product import _new_product
from hestia_earth.models.utils.product import _residue_nitrogen, _abg_residue_nitrogen, _blg_residue_nitrogen

class_path = 'hestia_earth.models.utils.product'
fixtures_folder = f"{fixtures_path}/utils/product"


class TestProduct(unittest.TestCase):
    @patch(f"{class_path}._include_methodModel", side_effect=lambda n, x: n)
    @patch(f"{class_path}.download_hestia", return_value=TERM)
    def test_new_product(self, *args):
        # with a Term as string
        product = _new_product('term')
        self.assertEqual(product, {
            '@type': 'Product',
            'term': TERM
        })

        # with a Term as dict
        product = _new_product(TERM)
        self.assertEqual(product, {
            '@type': 'Product',
            'term': TERM
        })

    def test_residue_nitrogen_no_products(self):
        self.assertEqual(_residue_nitrogen({}), 0)

    @patch(f"{class_path}._abg_residue_nitrogen", return_value=20)
    @patch(f"{class_path}._blg_residue_nitrogen", return_value=30)
    def test_residue_nitrogen(self, *args):
        self.assertEqual(_residue_nitrogen([]), 50)

    def test_abg_residue_nitrogen_no_products(self):
        self.assertEqual(_abg_residue_nitrogen([]), 0)

    def test_abg_residue_nitrogen(self):
        with open(f"{fixtures_folder}/products-cropResidue.jsonld", encoding='utf-8') as f:
            products = json.load(f)

        self.assertEqual(_abg_residue_nitrogen(products), 0.8445757894736851)

    def test_blg_residue_nitrogen_no_products(self):
        self.assertEqual(_blg_residue_nitrogen([]), 0)

    def test_blg_residue_nitrogen(self):
        with open(f"{fixtures_folder}/products-cropResidue.jsonld", encoding='utf-8') as f:
            products = json.load(f)

        self.assertEqual(_blg_residue_nitrogen(products), 13.606542431999996)
