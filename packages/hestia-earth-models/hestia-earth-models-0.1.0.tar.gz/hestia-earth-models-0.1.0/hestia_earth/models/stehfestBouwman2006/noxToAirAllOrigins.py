import numpy as np
from hestia_earth.utils.tools import list_average, list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _filter_list_term_unit
from hestia_earth.models.utils.contant import ATOMIC_WEIGHT_CONVERSIONS
from hestia_earth.models.utils.product import _residue_nitrogen
from hestia_earth.models.utils.measurement import _most_relevant_measurement_value

TERM_ID = 'noxToAirAllOrigins'
NOX_FACTORS_BY_CLIMATE_ZONE = {
    '1': 0.5189,
    '2': 0.5189,
    '3': 0.3511,
    '4': 0.0,
    '5': 0.3511,
    '6': 0.0,
    '7': 0.3511,
    '8': 0.0,
    '9': 1.1167,
    '10': 1.1167,
    '11': 1.1167,
    '12': 1.1167,
    '13': 1.1167
}


def _get_total_N(inputs: list): return [list_sum(i.get('value'), 0) for i in inputs]


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    measurements = site.get('measurements', [])
    ecoClimateZone = _most_relevant_measurement_value(measurements, 'ecoClimateZone', end_date)
    ecoClimateZone = str(ecoClimateZone[0]) if len(ecoClimateZone) > 0 else None
    nitrogenContent = list_average(_most_relevant_measurement_value(measurements, 'soilTotalNitrogenContent', end_date))

    inputs = _filter_list_term_unit(cycle.get('inputs', []), 'kg N')

    residue = _residue_nitrogen(cycle.get('products', []))
    logger.debug('residue, value=%s', residue)

    N_total = list_sum(_get_total_N(inputs) + [residue])
    logger.debug('N_total, value=%s', N_total)

    should_run = ecoClimateZone is not None and nitrogenContent is not None and N_total > 0
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run, ecoClimateZone, nitrogenContent, N_total, inputs, residue


def _get_value(ecoClimateZone: str, nitrogenContent: float, N_total: float):
    eco_factor = NOX_FACTORS_BY_CLIMATE_ZONE[ecoClimateZone]
    n_factor = 0 if nitrogenContent / 1000000 < 0.0005 else -1.0211 if nitrogenContent / 1000000 <= 0.002 else 0.7892
    value = min(
        0.025 * N_total,
        np.exp(-0.451 + 0.0061 * N_total + n_factor + eco_factor) -
        np.exp(-0.451 + n_factor + eco_factor)
    ) * ATOMIC_WEIGHT_CONVERSIONS['Conv_Mol_NON_NO']
    logger.info('term=%s, value=%s', TERM_ID, value)
    return value
