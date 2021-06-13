import pandas as pd

from app.main.helper import evaluation_metrics
from app.main.service.benchmark_service import BenchmarkService
from app.main.service.portfolio_return_services import get_portfolio_daily_returns


def get_performance_metrics(user_id, n_months):
    df_returns = get_portfolio_daily_returns(user_id=user_id, n_months=n_months)
    df_returns = df_returns[df_returns['return'] > 0]
    df_returns['date'] = pd.to_datetime(df_returns['date'], dayfirst=True)

    since_date = df_returns['date'].min()
    df_market = BenchmarkService.get_benchmarks(since_date=since_date)
    df_market['date'] = pd.to_datetime(df_market['date'], dayfirst=True)
    df_merge = df_market.merge(df_returns, on='date', how='inner')
    df_merge['return'] = df_merge['return'].pct_change().fillna(0)
    df_merge['return'] = (df_merge['return'] + 1).cumprod() - 1

    sharpe, vol = evaluation_metrics.sharpe_ratio(df_merge['return'], risk_free_rate=df_merge['cdi'].mean(), days_per_period=len(df_merge))
    alpha, beta = evaluation_metrics.alpha_beta_metrics(df_merge['return'], df_merge['ibov'])

    return {'alpha': alpha,
            'beta': beta,
            'volatility': vol,
            'sharpe': sharpe}