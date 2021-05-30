from unittest import TestCase

import pandas as pd

from app.main.helper.portfolio import compute_single_asset_returns


class TestPortfolioBasicOperations(TestCase):

    def test_compute_single_asset_returns(self):
        df = pd.DataFrame({'date': [0, 1, 2, 3],
                           'close': [10, 12, 11, 14],   # close price at that date
                           'price': [0, 8, 12, 13],     # price paid for each stock operated at that date
                           'amount': [0, 10, 5, -10]})  # amount of stocks operated at that date


        expected_returns = pd.DataFrame({'date': [0, 1, 2, 3],
                                         'return': [0, 40, 25, 60]})
        returns = compute_single_asset_returns(df)
        self.assertTrue(returns.equals(expected_returns))