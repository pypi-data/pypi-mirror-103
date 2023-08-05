from hestia_earth.utils.lookup import download_lookup, get_table_value
from hestia_earth.utils.tools import list_sum, safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _filter_list_term_unit
from hestia_earth.models.utils.product import _residue_nitrogen

TERM_ID = 'noxToAirAllOrigins'


def _get_total_N(inputs: list): return [list_sum(i.get('value'), 0) for i in inputs]


def _should_run(cycle: dict):
    country_id = cycle.get('site', {}).get('country', {}).get('@id')

    inputs = _filter_list_term_unit(cycle.get('inputs', []), 'kg N')

    residue = _residue_nitrogen(cycle.get('products', []))
    logger.debug('residue, value=%s', residue)

    N_total = list_sum(_get_total_N(inputs) + [residue])
    logger.debug('N_total, value=%s', N_total)

    should_run = country_id is not None and N_total > 0
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run, country_id, N_total, inputs, residue


def _get_value(country_id: str, N_total: float):
    lookup = download_lookup('region.csv', True)
    value = safe_parse_float(get_table_value(lookup, 'termid', country_id, 'ef_nox'))
    value = value * N_total
    logger.info('term=%s, value=%s', TERM_ID, value)
    return value
