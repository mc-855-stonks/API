import datetime
from datetime import datetime

import dateutil
import numpy as np


def get_today_date():
    return datetime.now()


def add_months(date, n_months):
    return date + dateutil.relativedelta.relativedelta(months=n_months)


def date_to_str(date, pattern='%Y-%m-%d'):
    """

    :param date: a datetime object
    :param pattern: date pattern
    :return: string with formatted date
    """
    return date.strftime(pattern)


def str_to_date(string, pattern='%Y-%m-%d'):
    """

    :param string: string with date in format Y-m-d
    :param pattern: date pattern
    :return: datetime
    :raise ValueError in case of invalid date format
    """

    return datetime.strptime(string, pattern)


def get_commercial_end_of_month(date_series):
    """
    Given a list of dates, get the last day of each year-month

    :param date_series: a pd.Series datetime64
    :return: a pd.Series datetime64
    """
    group = date_series.groupby(by=[date_series.dt.year, date_series.dt.month])
    eom = date_series[group.apply(lambda s: np.max(list(s.index)))]
    eom = eom.reset_index(drop=True)
    return eom



def interpolate_monthly_data_to_daily_data(df):
    """

    :param df: pd.DataFrame({'date':[...], # monthly data
                            ...})

    :return: pd.DataFrame({'date':[...], # daily data
                            ...})
    """
    return df.set_index('date').resample('D').interpolate().reset_index()
