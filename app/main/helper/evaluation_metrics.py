from scipy import stats
import numpy as np


def volatility(return_series, days_per_period=252):
    """
    :param return_series: a pandas.Series with the portfolio daily returns
    :param days_per_period: in general we compute the annualized shape, thus we use 252 working days
    :return: volatility time corrected for the considered period
    """
    # time correctly volatility
    return return_series.std() * np.sqrt(days_per_period)


def sharpe_ratio(portfolio_return, risk_free_rate, days_per_period=252):
    """
    :param portfolio_return: a pandas.Series with the portfolio daily returns
    :param risk_free_rate: a fixed risk free rate, in Brazil CDI is typically used
    :param days_per_period: in general we compute the annualized shape, thus we use 252 working days
    :return: sharpe ratio and volatility time corrected for the considered period
    """
    # the expected return for that period
    expected_return = portfolio_return.mean() * days_per_period
    vol = volatility(portfolio_return, days_per_period)

    sharpe = (expected_return - risk_free_rate) / vol
    return sharpe, vol


def alpha_beta_metrics(portfolio_returns, market_returns):
    """
    :param portfolio_returns:  a pandas.Series with the portfolio daily returns
    :param market_returns: a pandas.Series with the market daily returns
    :return: alpha, beta. They represent the alpha and beta of the portfolio
    """
    result = stats.linregress(market_returns, portfolio_returns)
    alpha = result.intercept
    beta = result.slope

    return alpha, beta
