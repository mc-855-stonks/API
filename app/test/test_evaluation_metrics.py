import random
from unittest import TestCase

from app.main.helper.evaluation_metrics import alpha_beta_metrics, sharpe_ratio
import pandas as pd
import numpy as np

class TestPerformanceMetrics(TestCase):
    def test_alpha_beta_metrics(self):
        x = [x for x in range(10)]
        y = [3 * x + 1 for x in range(10)]
        alpha, beta = alpha_beta_metrics(portfolio_returns=y, market_returns=x)

        self.assertAlmostEqual(alpha, 1, delta=1e-5)
        self.assertAlmostEqual(beta, 3, delta=1e-5)

    def test_sharpe(self):
        mean = 0.001
        std = 5
        portfolio_return = pd.Series([random.gauss(mean, std) for _ in range(10)])
        risk_free_rate = 1.03

        expected_vol = portfolio_return.std()*np.sqrt(252)
        expected_sharpe = (portfolio_return.mean()*252 - risk_free_rate)/expected_vol

        sharpe, vol = sharpe_ratio(portfolio_return, risk_free_rate, days_per_period=252)
        self.assertAlmostEqual(sharpe, expected_sharpe, delta=1e-5)
        self.assertAlmostEqual(vol, expected_vol, delta=1e-5)