from datetime import datetime, timedelta, date
import warnings
import numpy as np
import pandas as pd
from pandas._libs.tslibs.offsets import Week
from workalendar.europe import EuropeanCentralBank
from pandas.tseries.offsets import BDay, BMonthEnd, BQuarterEnd, BYearEnd

cal = EuropeanCentralBank()


class Indicators:

    def __init__(self, price_serie, bench_serie=0, computation_date=0, risk_free_rate=0 ,nb_days=0):
        '''Class constructor//
        To get a full access to all methods you need to create an instance with :
        //price_serie : pd.serie(datetime index,asset price)
        //bench_Serie : pd.serie(datetime index,benchmark price)
        //calcul_date : datetime or date
        //risk_free_rate : float (example 0.05 for 5%)
        //nb_days : int (For rolling methods)'''
        self.nav = price_serie
        self.bench = bench_serie
        self.computation_date = computation_date
        self.rf = risk_free_rate
        self.roll_nb_days = nb_days

    '''
    ####################################################################################################################
    # Data Quality Testing
    ####################################################################################################################
    '''

    def test_benchmark(self):
        '''Test if  benchmark attribute is well formatted'''
        assert isinstance(self.bench, pd.Series), "bench_serie must be a pandas.series"
        assert self.bench.index.dtype == 'datetime64[ns]', "Index of your bench_serie must be datetime64[ns]"
        assert self.bench.dtype == 'float64', "bench_serie values must be float64"

    def test_nav(self):
        '''Test if  nav attribute is well formatted'''
        assert isinstance(self.nav, pd.Series), "price_serie must be a pandas.series"
        assert self.nav.index.dtype == 'datetime64[ns]', "Index of your price_serie must be datetime64[ns]"
        assert self.nav.dtype == 'float', "price_serie values must be float"

    def test_computation_date(self):
        '''Test if  computation_date attribute is well formatted'''
        if not self.computation_date:
            raise RuntimeError("This method is not available without instanciate a calcul_date")
        else:
            assert isinstance(self.computation_date,
                              (date, datetime)), "calcul_date must be a datetime or a date class instance"

    def test_risk_free_rate(self):
        '''Test if  rf attribute is well formatted'''
        if self.rf == 0:
            warnings.warn("This method runs better with instanciate a risk_free_rate", UserWarning)
        else:
            assert isinstance(self.rf, (float)), "risk_free_rate must be float"

    def test_nb_days(self):
        '''Test if  number days attribute is well formatted'''
        if self.roll_nb_days == 0:
            raise RuntimeError("This method is not available without instanciate a nb_days")
        else:
            assert isinstance(self.roll_nb_days, (int)), "nb_days must be float"
            assert self.roll_nb_days > 2, "nb_days must be > 2"

    '''
    ####################################################################################################################
    # Getter
    ####################################################################################################################
    '''

    def get_risk_free_rate(self):
        '''Return risk free rate'''
        self.test_risk_free_rate()
        return self.rf

    def get_nav(self):
        '''Return nav price serie'''
        self.test_nav()
        return self.nav

    def get_benchmark(self):
        '''Return benchmark price serie'''
        self.test_benchmark()
        return self.bench

    def get_computation_date(self):
        '''Return computation date'''
        self.test_computation_date()
        return self.computation_date

    def get_nav_returns(self):
        '''Return nav daily returns'''
        return (self.get_nav().pct_change() * 100).dropna()

    def get_bench_returns(self):
        '''Return benchmark daily returns'''
        return (self.get_benchmark().pct_change() * 100).dropna()

    def get_nb_days(self):
        '''Return the number of days for rolling methods'''
        self.test_nb_days()
        return self.roll_nb_days

    '''
    ####################################################################################################################
    # Rolling/Dynamic Indicators Computation
    ####################################################################################################################
    '''

    def calculate_rolling_volatility(self, data=False):
        '''Return a rolling volatility pd.Serie'''
        self.test_nb_days()
        if data:
            rolling_vol = self.get_nav_returns().rolling(window=self.get_nb_days()).std() * np.sqrt(252)
        else:
            rolling_vol = self.get_bench_returns().rolling(window=self.get_nb_days()).std() * np.sqrt(252)
        return rolling_vol.dropna()

    def calculate_moving_average(self, data=False):
        '''Return a moving average pd.Serie'''
        self.test_nb_days()
        if data:
            moving_average = self.get_nav().rolling(window=self.get_nb_days()).mean()
        else:
            moving_average = self.get_benchmark().rolling(window=self.get_nb_days()).mean()
        return moving_average

    def calculate_rolling_beta(self):
        '''Return a rolling beta pd.Serie'''
        self.test_nb_days()
        return_serie = self.get_nav_returns()
        bench_return_serie = self.get_bench_returns()
        df_returns = pd.DataFrame(return_serie, columns=['Fund'])
        df_returns['Benchmark'] = bench_return_serie
        covar = df_returns.rolling(self.get_nb_days()).cov().unstack()['Fund']['Benchmark']
        variance = df_returns['Benchmark'].rolling(self.get_nb_days()).var()
        return (covar / variance).dropna()

    def calculate_last_beta(self):
        '''Return the last beta with window period calculation'''
        beta_serie = self.calculate_rolling_beta()
        last_beta = float(beta_serie.tail(n=1).values)
        return last_beta

    '''
    ####################################################################################################################
    # Static (As Of Date) Indicators Computation
    ####################################################################################################################
    '''

    def calculate_historical_beta(self):
        '''Return Historical beta (float)'''
        return_serie = self.get_nav_returns()
        bench_return_serie = self.get_bench_returns()
        df_returns = pd.DataFrame(return_serie, columns=['Fund'])
        df_returns['Benchmark'] = bench_return_serie
        covar = df_returns.cov().unstack()['Fund']['Benchmark']
        variance = df_returns['Benchmark'].var()
        return (covar / variance)

    def calculate_historical_high_water_mark(self):
        '''Return a pd.Serie representing the HWM evolution'''
        return self.get_nav().cummax()

    def calculate_high_water_mark(self):
        '''Return the HWM (float)'''
        return self.get_nav().max()

    def calculate_annualised_returns(self, data=False):
        '''Return annualised returns (float)'''
        if data:
            return self.get_bench_returns().mean() * 252
        return self.get_nav_returns().mean() * 252

    def calculate_annualised_volatility(self, data=False):
        '''Return Annualised volatility (float)'''
        if data:
            return self.get_bench_returns().std() * np.sqrt(252)
        return self.get_nav_returns().std() * np.sqrt(252)

    def calculate_max_drawdown(self, data=False):
        '''Return maximum drawdown (float)'''
        if data:
            self.test_benchmark()
            return abs((self.bench / self.bench.cummax() - 1).cummin().min())
        self.test_nav()
        return abs((self.nav / self.nav.cummax() - 1).cummin().min())

    def calculate_time_to_recover(self, data=False):
        '''Return number of days needed to recover the max DD (str)'''
        if data:
            self.test_benchmark()
            serie = self.bench
        else:
            self.test_nav()
            serie = self.nav
        mdd_serie = (serie / serie.cummax() - 1)
        date_mdd_reached = mdd_serie[mdd_serie == -self.calculate_max_drawdown(data)].index.date[0]
        mdd_serie = mdd_serie.truncate(before=date_mdd_reached, axis=0)
        print(mdd_serie)
        i = 0
        while i < len(mdd_serie):
            if mdd_serie.iloc[i] < 0:
                i += 1
            else:
                break
        if i == len(mdd_serie):
            return "In Progress"
        return str(i + 1) + " Days"

    def calculate_mean_return(self, data=False):
        '''Return returns mean (float) '''
        if data:
            return self.get_bench_returns().mean()
        return self.get_nav_returns().mean()

    def calculate_std_return(self, data=False):
        '''Return  returns standard deviation (float)'''
        if data:
            return self.get_bench_returns().std()
        return self.get_nav_returns().std()

    def calculate_skew_return(self, data=False):
        '''Return  returns skewness (float)'''
        if data:
            return self.get_bench_returns().skew()
        return self.get_nav_returns().skew()

    def calculate_kurt_return(self, data=False):
        '''Return  returns kurtosis (float)'''
        if data:
            return self.get_bench_returns().kurt()
        return self.get_nav_returns().kurt()

    def calculate_min_return(self, data=False):
        '''Return  returns minimum (float)'''
        if data:
            return self.get_bench_returns().min()
        return self.get_nav_returns().min()

    def calculate_max_return(self, data=False):
        '''Return  returns maximum (float)'''
        if data:
            return self.get_bench_returns().max()
        return self.get_nav_returns().max()

    def calculate_median_return(self, data=False):
        '''Return  returns median (float)'''
        if data:
            return self.get_bench_returns().median()
        return self.get_nav_returns().median()

    def calculate_twentyfive_return(self, data=False):
        '''Return  returns 25% quartile (float)'''
        if data:
            return np.percentile(self.get_bench_returns(), 25)
        return np.percentile(self.get_nav_returns(), 25)

    def calculate_seventyfive_return(self, data=False):
        '''Return  returns 75% quartile (float)'''
        if data:
            return np.percentile(self.get_bench_returns(), 75)
        return np.percentile(self.get_nav_returns(), 75)

    '''
    ####################################################################################################################
    # Performance Ratio 
    ####################################################################################################################
    '''

    def calculate_sharpe_ratio(self):
        '''Return  Sharpe Ratio (float)'''
        return (self.calculate_annualised_returns() - self.get_risk_free_rate()) / self.calculate_annualised_volatility()

    def calculate_jensen_alpha(self):
        '''Return  Jensen aAlpha (float)'''
        return self.calculate_annualised_returns() - (self.get_risk_free_rate() + self.calculate_historical_beta() * (
                self.calculate_annualised_returns(data=True) - self.get_risk_free_rate()))

    def calculate_tracking_error(self):
        '''Return  TE Ratio (float)'''
        port = self.get_nav_returns()
        bench = self.get_bench_returns()
        return (port - bench).std()

    def calculate_information_ratio(self):
        '''Return  Information Ratio (float)'''
        port = self.calculate_annualised_returns()
        bench = self.calculate_annualised_returns(data=True)
        tracking_error = self.calculate_tracking_error()
        return (port - bench) / tracking_error

    def calculate_treynor_ratio(self):
        '''Return  Treynor Ratio (float)'''
        beta = self.calculate_historical_beta()
        port = self.calculate_annualised_returns()
        bench = self.calculate_annualised_returns(data=True)
        return (port - bench) / beta

    def calculate_calmar_ratio(self):
        '''Return  Calmar Ratio (float)'''
        return (self.calculate_annualised_returns() - self.get_risk_free_rate()) / self.calculate_max_drawdown()

    def calculate_sterling_ratio(self, ):
        '''Return  Sterling Ratio (float)'''
        return (self.calculate_annualised_returns() - self.get_risk_free_rate()) / abs(
            (self.nav / self.nav.cummax() - 1).cummin().mean()) * 100

    def calculate_sortino_ratio(self):
        '''Return  Sortino Ratio (float)'''
        asset_negative_returns = self.get_nav_returns()
        asset_negative_returns = asset_negative_returns[asset_negative_returns < 0].std() * np.sqrt(252)
        return (self.calculate_annualised_returns() - self.get_risk_free_rate()) / asset_negative_returns

    '''
    ####################################################################################################################
    # Historical Performance
    ####################################################################################################################
    '''

    def calculate_daily_perf(self):
        '''Return Daily Performance (float)'''
        date = self.get_computation_date()-BDay()
        while not cal.is_working_day(date):
            date = date - timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[date] - 1) * 100

    def calculate_weekly_perf(self):
        '''Return one week Performance (float)'''
        date = self.get_computation_date()-timedelta(days=7)
        while not cal.is_working_day(date):
            date = date - timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[date] - 1) *100

    def calculate_wtd_perf(self):
        '''Return wtd  Performance (float)'''
        date = self.get_computation_date() - Week(weekday=5)
        while not cal.is_working_day(date):
            date = date - timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[date] - 1) * 100

    def calculate_mtd_perf(self):
        '''Return mtd Performance (float)'''
        date = self.get_computation_date()-BMonthEnd()
        while not cal.is_working_day(date):
            date = date -timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[date] - 1) *100

    def calculate_month_perf(self):
        '''Return one month Performance (float)'''
        year = self.get_computation_date().year
        month = self.get_computation_date().month
        day = self.get_computation_date().day
        if month == 1:
            one_month = datetime(year - 1, month + 11, day)
        else:
            one_month = datetime(year, month - 1, day)
        while not cal.is_working_day(one_month):
            one_month = one_month - timedelta(days=1)

        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[one_month] - 1) *100

    def calculate_three_month_perf(self):
        '''Return three month Performance (float)'''
        year = self.get_computation_date().year
        month = self.get_computation_date().month
        day = self.get_computation_date().day
        if month <=3:
            for i in range(1,3,1):
                if month == i:
                    three_month = datetime(year - 1, 9+i, day)
        else:
            three_month = datetime(year, month - 3, day)
        while not cal.is_working_day(three_month):
            three_month = three_month - timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[three_month] - 1) *100

    def calculate_six_month_perf(self):
        '''Return six month Performance (float)'''
        year = self.get_computation_date().year
        month = self.get_computation_date().month
        day = self.get_computation_date().day
        if month <=6:
            for i in range(1,6,1):
                if month == i:
                    six_month = datetime(year - 1, 6+i, day)
        else:
            six_month = datetime(year, month - 6, day)
        while not cal.is_working_day(six_month):
            six_month = six_month - timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[six_month] - 1) *100

    def calculate_one_year_perf(self):
        '''Return one year Performance (float)'''
        year = self.get_computation_date().year
        month = self.get_computation_date().month
        day = self.get_computation_date().day
        one_year = datetime(year - 1, month, day)
        while not cal.is_working_day(one_year):
            one_year = one_year - timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[one_year] - 1) *100

    def calculate_ytd_perf(self):
        '''Return Ytd Performance (float)'''
        date = self.get_computation_date()-BYearEnd()
        while not cal.is_working_day(date):
            date = date -timedelta(days=1)
        return (float(self.get_nav().tail(n=1)) / self.get_nav().loc[date] - 1) *100

    def calculate_since_inception_perf(self):
        '''Return Since inception Performance (float)'''
        return (float(self.get_nav().tail(n=1)) / float(self.get_nav().head(n=1)) - 1) * 100

    def calculate_annualised_since_inception_perf(self):
        '''Return Annualised since inception Performance (float)'''
        return (((1+(float(self.get_nav().tail(n=1)) / 100 - 1))**(252/len(self.get_nav())))-1)*100