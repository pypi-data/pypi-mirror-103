from hestia_earth.schema import EmissionMethodTier
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils.emission import _new_emission
from .constant import COEFF_NO3N_N03, COEFF_NH3N_NH3, COEFF_NOXN_NOX, COEFF_NH3NOX_N20, COEFF_NO3N_N20
from . import MODEL

TERM_ID = 'n2OToAirCropResidueDecompositionIndirect'
NO3_TERM_ID = 'no3ToGroundwaterCropResidueDecomposition'
NH3_TERM_ID = 'nh3ToAirCropResidueDecomposition'
NOX_TERM_ID = 'noxToAirCropResidueDecomposition'


def _emission(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    return emission


def _run(cycle: dict, no3: list):
    nh3 = list_sum(find_term_match(cycle.get('emissions'), NH3_TERM_ID).get('value', [0]))
    nox = list_sum(find_term_match(cycle.get('emissions'), NOX_TERM_ID).get('value', [0]))
    no3 = list_sum(no3)
    value = COEFF_NH3NOX_N20 * (
        0 if nox == 0 or nh3 == 0 else nh3 / COEFF_NH3N_NH3 + nox / COEFF_NOXN_NOX
    ) + COEFF_NO3N_N20 * no3 / COEFF_NO3N_N03

    return [_emission(value)]


def _should_run(cycle: dict):
    no3 = find_term_match(cycle.get('emissions', []), NO3_TERM_ID).get('value', [])
    should_run = len(no3) > 0
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run, no3


def run(cycle: dict):
    should_run, no3 = _should_run(cycle)
    return _run(cycle, no3) if should_run else []
