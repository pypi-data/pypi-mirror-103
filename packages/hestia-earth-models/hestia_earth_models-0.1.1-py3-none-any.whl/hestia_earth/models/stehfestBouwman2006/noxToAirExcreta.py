from hestia_earth.schema import EmissionMethodTier, TermTermType
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils.cycle import _is_term_type_complete
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils import _filter_list_term_type, _filter_list_term_unit
from . import MODEL
from .noxToAirAllOrigins import _should_run, _get_value

TERM_ID = 'noxToAirExcreta'


def _emission(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_2.value
    return emission


def _get_product_value(cycle: dict):
    products = _filter_list_term_unit(cycle.get('products', []), 'kg N')
    products = _filter_list_term_type(products, TermTermType.ANIMALPRODUCT)
    values = [list_sum(p.get('value'), 0) for p in products if len(p.get('value', [])) > 0]
    return 0 if len(products) == 0 and _is_term_type_complete(cycle, {'termType': 'products'}) else list_sum(values)


def _run(cycle: dict, ecoClimateZone: str, nitrogenContent: float, N_total: float):
    noxToAirAllOrigins = _get_value(ecoClimateZone, nitrogenContent, N_total)
    value = _get_product_value(cycle)
    return [_emission(value * noxToAirAllOrigins / N_total)]


def run(cycle: dict):
    should_run, ecoClimateZone, nitrogenContent, N_total, *args = _should_run(cycle)
    return _run(cycle, ecoClimateZone, nitrogenContent, N_total) if should_run else []
