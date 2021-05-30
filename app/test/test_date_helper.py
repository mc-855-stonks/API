from unittest import TestCase

import pandas as pd

from app.main.helper.date_helper import get_commercial_end_of_month


class TestDateHelper(TestCase):

    def test_get_commercial_end_of_month(self):
        dates = ['2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08',
                 '2020-03-11', '2020-03-12',
                 '2020-02-08', '2020-02-09', '2020-02-10', '2020-02-11',
                 '2021-02-12', '2021-02-16']

        date_series = pd.Series(pd.to_datetime(dates))

        expected_dates = pd.Series(pd.to_datetime(['2020-01-08', '2020-02-11',
                                                   '2020-03-12', '2021-02-16']))

        commercial_eom = get_commercial_end_of_month(date_series)
        self.assertTrue(commercial_eom.equals(expected_dates))