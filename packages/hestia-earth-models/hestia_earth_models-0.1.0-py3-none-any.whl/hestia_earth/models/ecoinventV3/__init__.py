from functools import reduce
from hestia_earth.schema import EmissionMethodTier

from hestia_earth.models.log import logger
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.impact_assessment import _get_impacts_dict

MODEL = 'ecoinventV3'
TERM_IDS = [
    '11DichlorotetrafluoroethaneToAirInputsProduction',
    '112TrichlorotrifluoroethaneToAirInputsProduction',
    '1112TetrafluoroethaneToAirInputsProduction',
    'bromochlorodifluoromethaneToAirInputsProduction',
    'ch4ToAirInputsProductionFossil',
    'ch4ToAirInputsProductionNonFossil',
    'chlorodifluoromethaneToAirInputsProduction',
    'co2ToAirInputsProduction',
    'dichlorodifluoromethaneToAirInputsProduction',
    'n2OToAirInputsProduction',
    'nh3ToAirInputsProduction',
    'noxToAirInputsProduction',
    'so2ToAirInputsProduction'
]


def _get_input_value(input: dict, impacts: dict, emission: str):
    impact = impacts[input.get('term').get('@id')]
    return sum(input.get('value', [])) * sum(impact.get(emission, [0]))


def _get_value(cycle: dict, emission: str):
    impacts = _get_impacts_dict()
    inputs = list(filter(lambda i: i.get('term', {}).get('@id') in impacts, cycle.get('inputs', [])))
    return reduce(lambda prev, i: prev + _get_input_value(i, impacts, emission), inputs, 0), inputs


def _emission(cycle: dict, term_id: str):
    value, inputs = _get_value(cycle, term_id)
    logger.info('term=%s, value=%s', term_id, value)
    emission = _new_emission(term_id, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.BACKGROUND.value
    emission['inputs'] = list(map(lambda i: i.get('term'), inputs))
    return emission


def run(model: str, data):
    run_all_models = model is None or model == '' or model == 'null' or model == 'all'
    return list(map(lambda x: _emission(data, x), TERM_IDS)) if run_all_models else [_emission(data, model)]
