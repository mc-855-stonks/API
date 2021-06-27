from collections import defaultdict
from operator import or_, and_

import pandas as pd

from app.main import db
from app.main.helper import date_helper, utils, portfolio, evaluation_metrics
from app.main.model.operation import Operation
from app.main.model.stock_history import StockHistory


def __select_end_of_month_values(df_returns):
    end_of_month_series = date_helper.get_commercial_end_of_month(
        df_returns['date'])
    df_end_of_month = df_returns[df_returns['date'].isin(end_of_month_series)]
    if df_end_of_month['date'].iloc[-1] != df_returns['date'].iloc[-1]:
        df_end_of_month = df_end_of_month.append(
            df_returns.iloc[-1:, :]).reset_index().drop(columns=['index'])
    return df_end_of_month


def __get_map_stock_id_to_data(joined_data):
    map_ticker_to_data = defaultdict(lambda: {'date': [],
                                              'close': [],
                                              'price': [],
                                              'amount': []})
    for item in joined_data:
        date, stock_id, close, price, amount, side_id = item
        if side_id == utils.get_side_id('sell'):
            amount = -amount

        map_ticker_to_data[stock_id]['date'].append(date)
        map_ticker_to_data[stock_id]['close'].append(close)
        map_ticker_to_data[stock_id]['price'].append(price)
        map_ticker_to_data[stock_id]['amount'].append(amount)
    return map_ticker_to_data


def __find_first_non_zero(series):
    for i, x in enumerate(series):
        if x != 0:
            return i
    return -1


def __join_historical_data_operation(start_date, user_id):
    subquery = db.session.query(Operation.stock_id).filter_by(
        user_id=user_id).subquery()
    filtered_data = db.session.query(StockHistory.date, StockHistory.stock_id, StockHistory.close,
                                     Operation.price, Operation.amount, Operation.side_id) \
        .join(Operation, Operation._date == StockHistory.date, isouter=True) \
        .filter(StockHistory.date >= start_date,
                StockHistory.stock_id.in_(subquery),
                or_(and_(Operation.stock_id == StockHistory.stock_id, Operation.user_id == user_id),
                    Operation.stock_id == None)).all()

    return filtered_data


def __sum_dataframe(df_returns1, df_returns2):
    if df_returns2 is None:
        return df_returns1

    df = pd.merge(df_returns1, df_returns2, on='date',
                  how='outer', suffixes=('_1', '_2')).fillna(0)
    df['return'] = df['return_1'] + df['return_2']
    return df.drop(columns=['return_1', 'return_2'])


def compute_percentage_returns(df_returns):
    """

    :param df_returns: pd.DataFrame({'date':[...],    # daily
                                     'return':[..]})  # values in R$

    :return: pd.DataFrame({'date':[...],   # daily
                           'return':[..]}) # values in %
    """
    df_returns['return_pct'] = df_returns['return'].pct_change()
    df_returns['return_pct'].loc[0] = 0
    return df_returns


def get_portfolio_daily_returns(user_id, n_months):
    """

    :param user_id: user id
    :param n_months: number of months for which portfolio is to be computed

    :return: pd.DataFrame({'date':[...],   # daily
                           'return':[..]}) # values in R$
    """
    today = date_helper.get_today_date()
    start_date = date_helper.date_to_str(
        date_helper.add_months(today, n_months=-n_months))
    joined_data = __join_historical_data_operation(start_date, user_id)
    map_stock_id_to_data = __get_map_stock_id_to_data(joined_data)

    df_returns = None
    for stock_id, data in map_stock_id_to_data.items():
        df = pd.DataFrame(data).sort_values(by=['date']).fillna(0)
        df_single_returns = portfolio.compute_single_asset_returns(df)
        df_returns = __sum_dataframe(df_single_returns, df_returns)
    return df_returns


def get_portfolio_monthly_returns(df_returns):
    """
    :param df_returns: pd.DataFrame({'date':[...], # daily
                           'return':[..]})         # values in R$

    :return: pd.DataFrame({'date':[...],   # monthly
                           'return':[..]}) # values in R$
    """
    if df_returns is None or len(df_returns) == 0:
        return []

    df_returns['date'] = pd.to_datetime(df_returns['date'])

    df_returns = __select_end_of_month_values(df_returns)
    index = __find_first_non_zero(df_returns['return'])
    df_returns = df_returns.iloc[index:, :]

    df_returns['date'] = df_returns['date'].dt.strftime('%Y-%m')
    df_returns.sort_values(by=['date'], ascending=False, inplace=True)
    return utils.dataframe_to_json(df_returns)


def compute_portfolio_performance(user_id, n_months=12):
    """TODO: terminar de criar o método que calcula os rendimento do portfolio"""
    df_returns = get_portfolio_daily_returns(
        user_id=user_id, n_months=n_months)
    df_returns = compute_percentage_returns(df_returns)

    returns = get_portfolio_monthly_returns(df_returns)

    return {'returns': returns}


def get_portfolio_last_day_returns(df_returns):
    """
    :param df_returns: pd.DataFrame({'date':[...], # daily
                           'return':[..]})         # values in R$

    :return: pd.DataFrame({'date':[...],   # monthly
                           'return':[..]}) # values in R$
    """
    if df_returns is None or len(df_returns) == 0:
        return 0

    df_returns['date'] = pd.to_datetime(df_returns['date'])

    index = __find_first_non_zero(df_returns['return'])
    df_returns = df_returns.iloc[index:, :]

    df_returns['date'] = df_returns['date'].dt.strftime('%Y-%m')
    df_returns.sort_values(by=['date'], ascending=False, inplace=True)
    if len(df_returns) == 0:
        return 0

    return df_returns.iloc[0]
