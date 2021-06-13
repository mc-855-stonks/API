from collections import defaultdict
from datetime import datetime

from app.main.helper import date_helper
from app.main.helper.utils import create_response
import pandas as pd

from app.main.service.portfolio_performance_services import get_portfolio_daily_returns
from app.main.service.stock_history_service import filter_historical_data


class BenchmarkService:
    BC_DATA_URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'
    map_indicator_to_code = {'CDI': 12,   # Interest rate - CDI
                             'IPCA': 433} # Broad National Consumer Price Index (IPCA)

    @staticmethod
    def __get_BC_data(indicator, start=None, end=None):
        """

        :param indicator: indicator for which you want to get data, it can CDI or IPCA
        :param start: (datetime) start date
        :param end: (datetime) end date
        :return: pd.DataFrame
        """
        if not BenchmarkService.map_indicator_to_code.get(indicator):
            return create_response('fail', 'Indicator {} not found'.format(indicator), 404)

        indicator = BenchmarkService.map_indicator_to_code[indicator]
        url = BenchmarkService.BC_DATA_URL.format(indicator)
        if start is not None:
            start = start.strftime('%d/%m/%Y')
            end = end.strftime('%d/%m/%Y')
            url = '{}&dataInicial={}&dataFinal={}'.format(url, start, end)

        df = pd.read_json(url)
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df.rename(columns={'data': 'date', 'valor': 'value'}, inplace=True)
        df.sort_values(by='date', inplace=True)
        return df


    @staticmethod
    def __get_CDI_data(months=12):
        """

        :param months: number to compute CDI
        :return: df.DataFrame({'date':[...], # daily values
                               'value':[...]})
        """
        today = date_helper.get_today_date()
        start = date_helper.add_months(today, -months)

        return BenchmarkService.__get_BC_data('CDI', start=start, end=today)


    @staticmethod
    def __get_IPCA_data(months=12):
        """

        :param months: number to compute IPCA
        :return: df.DataFrame({'date':[...], # monthly values
                               'value':[...]})
        """
        today = date_helper.get_today_date()
        start = date_helper.add_months(today, -months)

        df_ipca = BenchmarkService.__get_BC_data('IPCA', start=start, end=today)

        return df_ipca

    @staticmethod
    def __get_IBOVESPA_data(months=12):
        """

        :param months:
        :return: a list of StockHistory
        """
        today = date_helper.get_today_date()
        start = date_helper.add_months(today, -months)

        params = {'tickers': 'BOVA11',
                  'since': start}
        ibov = filter_historical_data(params)
        result = {'date':[], 'ibov':[]}
        for item in ibov:
            result['date'].append(item.date)
            result['ibov'].append(item.close)

        return pd.DataFrame(result)

    @staticmethod
    def get_benchmarks(months, pct=True):
        """

        :param months:
        :param pct: if pct==True return results in %, otherwise return raw values
        :return: df.DataFrame({'date':[...],
                                'ibov':[...],
                                'cdi':[...]})
        """
        df_cdi = BenchmarkService.__get_CDI_data(months)
        df_ibov = BenchmarkService.__get_IBOVESPA_data(months)
        df_ibov['date'] = pd.to_datetime(df_ibov['date'], dayfirst=True)

        df_cdi.rename(columns={'value': 'cdi'}, inplace=True)

        if pct:
            df_ibov['ibov'] = df_ibov['ibov'].pct_change().fillna(0)
            df_cdi['cdi'] = df_cdi['cdi'].pct_change().fillna(0)

        return df_ibov.merge(df_cdi, on='date', how='inner')


def __group_row_by_month(df):
    result = defaultdict(lambda: [])

    for row in df.iterrows():
        date = str(row[1]['date'].strftime('%Y-%m-%d'))
        ibov = row[1]['ibov']
        cdi = row[1]['cdi']
        return_ = row[1]['return']

        year, month, day = date.split('-')
        result['{}-{}'.format(year, month)].append({'date': date,
                                                    'ibov': ibov,
                                                    'cdi': cdi,
                                                    'return': return_})

    result = sorted(list(result.items()), key=lambda x: x[0])
    return [sorted(values, key=lambda item: item['date']) for _, values in result]


def get_portfolio_benchmarks(user_id, n_months):
    """

    :param user_id: user id
    :param n_months: number of months for which portfolio is to be computed

    :return: [[{'date': '2021-01-04',
                'ibov': 0.22,
                'cdi': 0.01,
                'return': 0.13}, ... ],
            [{'date': '2021-02-03',
                'ibov': 0.10,
                'cdi': 0.02,
                'return': 0.19}, ... ]
                ...]
    """
    df_returns = get_portfolio_daily_returns(user_id, n_months)
    df_returns['return'] = df_returns['return'].pct_change().fillna(0)
    df_returns['date'] = pd.to_datetime(df_returns['date'], dayfirst=True)

    df_benchmarks = BenchmarkService.get_benchmarks(n_months)
    df_returns = df_returns.merge(df_benchmarks, on='date', how='inner')

    return __group_row_by_month(df_returns)