from hestia_earth.schema import EmissionMethodTier
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils.emission import _new_emission
from .utils import _get_fuel_values
from . import MODEL

TERM_ID = 'so2ToAirFuelCombustion'
DIESEL_COMB_SO2 = 0.001
GASOLINE_COMB_SO2 = 0.001


def _emission(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    return emission


def _run(diesel_values: list, gasoline_values: list):
    diesel_value = 2 * list_sum(diesel_values) * DIESEL_COMB_SO2
    gasoline_value = 2 * list_sum(gasoline_values) * GASOLINE_COMB_SO2
    return [_emission(diesel_value + gasoline_value)]


def _should_run(cycle: dict):
    diesel_values, gasoline_values = _get_fuel_values(cycle)
    should_run = len(diesel_values) > 0 or len(gasoline_values) > 0
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run, diesel_values, gasoline_values


def run(cycle: dict):
    should_run, diesel_values, gasoline_values = _should_run(cycle)
    return _run(diesel_values, gasoline_values) if should_run else []
