from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.model import linked_node

from . import _term_id, _include_methodModel


def _new_property(term, model=None):
    node = {'@type': SchemaType.PROPERTY.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_methodModel(node, model)


def _find_term_property(term_id: str, property: str):
    term = download_hestia(term_id)
    return find_term_match(term.get('defaultProperties', []), property, None)


def _get_property_by_key(node: dict, property: str):
    prop = find_term_match(node.get('properties', []), property, None)
    return _find_term_property(node.get('term', {}).get('@id'), property) if prop is None else prop
