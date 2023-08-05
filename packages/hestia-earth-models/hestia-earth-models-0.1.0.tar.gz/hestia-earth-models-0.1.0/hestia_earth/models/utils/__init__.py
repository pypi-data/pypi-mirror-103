from os.path import dirname, abspath
import sys
from functools import reduce
from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import download_hestia, find_node_exact
from hestia_earth.utils.model import linked_node

CURRENT_DIR = dirname(abspath(__file__)) + '/'
sys.path.append(CURRENT_DIR)


def _term_id(term): return term.get('@id') if isinstance(term, dict) else term


def _include_methodModel(node: dict, term_id: str):
    term = download_hestia(term_id)
    return {**node, **({} if term.get('@id') is None else {'methodModel': linked_node(term)})}


def _include_source(node: dict, biblio_title: str):
    source = find_node_exact(SchemaType.SOURCE, {'bibliography.title': biblio_title}) if biblio_title else None
    return {**node, **({} if source is None else {'source': linked_node({'@type': SchemaType.SOURCE.value, **source})})}


def _run_in_serie(data: dict, models: list): return reduce(lambda prev, model: model(prev), models, data)


def _load_calculated_node(node, type: str):
    # TODO: update api to fallback from dataState to original
    try:
        try:
            return download_hestia(node.get('@id'), type, 'recalculated')
        except Exception:
            return download_hestia(node.get('@id'), type, 'gapFilled')
    except Exception:
        return download_hestia(node.get('@id'), type)


def _filter_list_term_type(values: list, term_type: TermTermType):
    return list(filter(lambda i: i.get('term', {}).get('termType') == term_type.value, values))


def _filter_list_term_unit(values: list, unit: str):
    return list(filter(lambda i: i.get('term', {}).get('units') == unit, values))
