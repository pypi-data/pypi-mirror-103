from functools import reduce

from hestia_earth.models.data.impact_assessments import _load_impacts


def _get_impacts_dict():
    def merge_emission(prev: dict, emission: dict):
        key = emission.get('term', {}).get('@id')
        prev[key] = prev.get(key, []) + [float(emission.get('value'))]
        return prev

    def merge_impact(prev: dict, impact: dict):
        key = impact.get('product', {}).get('@id')
        prev[key] = reduce(merge_emission, impact.get('emissionsResourceUse', []), prev.get(key, {}))
        return prev

    impacts = _load_impacts()
    return reduce(merge_impact, impacts, {})
