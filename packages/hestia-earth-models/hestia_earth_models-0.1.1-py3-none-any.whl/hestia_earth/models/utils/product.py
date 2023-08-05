from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_term_match, linked_node
from hestia_earth.utils.tools import list_sum

from . import _term_id, _include_methodModel


def _new_product(term, model=None):
    node = {'@type': SchemaType.PRODUCT.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_methodModel(node, model)


def _get_nitrogen_content(product: dict):
    return float(find_term_match(product.get('properties', []), 'nitrogenContent').get('value', '0'))


def _abg_residue_nitrogen(products: list):
    left_on_field = find_term_match(products, 'aboveGroundCropResidueLeftOnField').get('value', [0])
    incorporated = find_term_match(products, 'aboveGroundCropResidueIncorporated').get('value', [0])
    total = find_term_match(products, 'aboveGroundCropResidueTotal')
    return list_sum(left_on_field + incorporated) * _get_nitrogen_content(total) / 100


def _blg_residue_nitrogen(products: list):
    residue = find_term_match(products, 'belowGroundCropResidue')
    return list_sum(residue.get('value', [0])) * _get_nitrogen_content(residue) / 100


def _residue_nitrogen(products: list): return _abg_residue_nitrogen(products) + _blg_residue_nitrogen(products)
