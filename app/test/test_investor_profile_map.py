from unittest import TestCase

from app.main.helper import utils


class TestInvestorProfileMap(TestCase):
    def test_get_investor_profile_given_conservator(self):
        self.assertEqual(utils.get_investor_profile(1), 'Conservador')

    def test_get_investor_profile_given_moderate(self):
        self.assertEqual(utils.get_investor_profile(2), 'Moderado')

    def test_get_investor_profile_given_risky(self):
        self.assertEqual(utils.get_investor_profile(3), 'Arrojado')

    def test_get_investor_profile_id_given_conservator(self):
        self.assertEqual(utils.get_investor_profile_id('conservador'), 1)

    def test_get_investor_profile_id_given_moderate(self):
        self.assertEqual(utils.get_investor_profile_id('moderado'), 2)

    def test_get_investor_profile_id_given_risky(self):
        self.assertEqual(utils.get_investor_profile_id('arrojado'), 3)