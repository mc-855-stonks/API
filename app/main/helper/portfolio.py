import pandas as pd

def compute_single_asset_returns(df_operations):
    """
    Compute the portfolio return for a single asset portfolio.

    :param df_operations: a pandas.DataFrame in the format
    pd.DataFrame({'date': [...],
                  'close': [...],   # close price at that date
                  'price': [...],   # price paid for each stock operated at that date
                  'amount': [...])  # amount of stocks operated at that date. Note if the operation is a sell,
                                      then amount is negative

    :return: a pd.DataFrame({'date': [...],
                             'returns': [...]})
    """
    cumulated_amount = df_operations['amount'] .cumsum()
    portfolio_value = df_operations['close'] * cumulated_amount
    cash_flow = df_operations['price'] * df_operations['amount']
    cumulated_investment = cash_flow.cumsum()

    returns = portfolio_value - cumulated_investment
    return pd.DataFrame({'date': df_operations['date'],
                         'return': returns})
