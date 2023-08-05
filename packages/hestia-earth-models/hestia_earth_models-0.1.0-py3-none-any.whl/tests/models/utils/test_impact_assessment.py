import unittest

from hestia_earth.models.utils.impact_assessment import _get_impacts_dict


class TestImpactAssessment(unittest.TestCase):
    def test_get_impacts_dict(self):
        impacts = _get_impacts_dict()
        self.assertEqual(len(impacts['fuelOil']['nh3ToAirInputsProduction']), 1)
