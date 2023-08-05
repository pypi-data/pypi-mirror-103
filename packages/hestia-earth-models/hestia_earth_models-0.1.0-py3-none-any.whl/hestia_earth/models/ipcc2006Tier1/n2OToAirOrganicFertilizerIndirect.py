from hestia_earth.schema import EmissionMethodTier, TermTermType
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _filter_list_term_unit, _filter_list_term_type
from hestia_earth.models.utils.cycle import _is_term_type_complete
from hestia_earth.models.utils.emission import _new_emission
from .constant import COEFF_NO3N_N03, COEFF_NH3N_NH3, COEFF_NOXN_NOX, COEFF_NH3NOX_N20, COEFF_NO3N_N20
from . import MODEL

TERM_ID = 'n2OToAirOrganicFertilizerIndirect'
NO3_TERM_ID = 'no3ToGroundwaterOrganicFertilizer'
NH3_TERM_ID = 'nh3ToAirOrganicFertilizer'
NOX_TERM_ID = 'noxToAirOrganicFertilizer'


def _emission(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    return emission


def _get_N_total(cycle: dict, inputs: list):
    values = [list_sum(p.get('value'), 0) for p in inputs if len(p.get('value', [])) > 0]
    return 0 if len(inputs) == 0 and _is_term_type_complete(cycle, {'termType': 'fertilizer'}) else list_sum(values)


def _run(cycle: dict, inputs: list, no3: list):
    nh3 = list_sum(find_term_match(cycle.get('emissions'), NH3_TERM_ID).get('value', [0]))
    nox = list_sum(find_term_match(cycle.get('emissions'), NOX_TERM_ID).get('value', [0]))
    no3 = list_sum(no3)
    N_total = _get_N_total(cycle, inputs)
    value = COEFF_NH3NOX_N20 * (
        N_total * 0.2 if nox == 0 or nh3 == 0 else nh3 / COEFF_NH3N_NH3 + nox / COEFF_NOXN_NOX
    ) + COEFF_NO3N_N20 * no3 / COEFF_NO3N_N03

    return [_emission(value)]


def _should_run(cycle: dict):
    inputs = _filter_list_term_unit(cycle.get('inputs'), 'kg N')
    inputs = _filter_list_term_type(inputs, TermTermType.ORGANICFERTILIZER)
    no3 = find_term_match(cycle.get('emissions', []), NO3_TERM_ID).get('value', [])
    should_run = len(inputs) > 0 and len(no3) > 0
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run, inputs, no3


def run(cycle: dict):
    should_run, inputs, no3 = _should_run(cycle)
    return _run(cycle, inputs, no3) if should_run else []
