from hestia_earth.schema import EmissionMethodTier, TermTermType
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils.cycle import _is_term_type_complete
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils import _filter_list_term_type
from . import MODEL
from .noxToAirAllOrigins import _should_run, _get_value

TERM_ID = 'noxToAirOrganicFertilizer'


def _emission(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_2.value
    return emission


def _get_input_value(cycle: dict, inputs: list):
    inputs = _filter_list_term_type(inputs, TermTermType.ORGANICFERTILIZER)
    values = [list_sum(i.get('value'), 0) for i in inputs if len(i.get('value', [])) > 0]
    return 0 if len(inputs) == 0 and _is_term_type_complete(cycle, {'termType': 'fertilizer'}) else list_sum(values)


def _run(cycle: dict, ecoClimateZone: str, nitrogenContent: float, inputs: list, N_total: float):
    noxToAirAllOrigins = _get_value(ecoClimateZone, nitrogenContent, N_total)
    value = _get_input_value(cycle, inputs)
    return [_emission(value * noxToAirAllOrigins / N_total)]


def run(cycle: dict):
    should_run, ecoClimateZone, nitrogenContent, N_total, inputs, *args = _should_run(cycle)
    return _run(cycle, ecoClimateZone, nitrogenContent, inputs, N_total) if should_run else []
