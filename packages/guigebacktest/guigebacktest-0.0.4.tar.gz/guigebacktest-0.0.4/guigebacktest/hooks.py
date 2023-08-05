# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import empyrical as ey
import math

class Base(ABC):
    def initialize(self):
        pass

    def finish(self):
        pass

    @abstractmethod
    def run(self, tick):
        pass


class Stat(Base):
    def __init__(self):
        self._date_hist = []
        self._cash_hist = []
        self._stk_val_hist = []
        self._ast_val_hist = []
        self._returns_hist = []
        self._position_hist = []

        self._s_cash_hist = pd.Series()
        self._s_stk_val_hist = pd.Series()
        self._s_ast_val_hist = pd.Series()
        self._s_returns_hist = pd.Series()
        self._s_position_hist = pd.Series()

    def run(self, tick):
        self._date_hist.append(tick)
        self._cash_hist.append(self.ctx.broker.cash)
        self._stk_val_hist.append(self.ctx.broker.stock_value)
        self._ast_val_hist.append(self.ctx.broker.assets_value)
        self._position_hist.append(len(self.ctx.broker.position))


    @property
    def data(self):
        df = pd.DataFrame({"cash": self._cash_hist,
                           "stock_value": self._stk_val_hist,
                           "assets_value": self._ast_val_hist,
                           "pos_count": self._position_hist}, index=self._date_hist)
        df.index.name = "date"
        return df

    def get_dropdown(self):
        high_val = -1
        low_val = None
        high_index = 0
        low_index = 0
        dropdown_lst = []
        dropdown_index_lst = []

        for idx, val in enumerate(self._ast_val_hist):
            if val >= high_val:
                if high_val == low_val or high_index >= low_index:
                    high_val = low_val = val
                    high_index = low_index = idx
                    continue

                dropdown = (high_val - low_val) / high_val
                dropdown_lst.append(dropdown)
                dropdown_index_lst.append((high_index, low_index))

                high_val = low_val = val
                high_index = low_index = idx

            if low_val is None:
                low_val = val
                low_index = idx

            if val < low_val:
                low_val = val
                low_index = idx

        if low_index > high_index:
            dropdown = (high_val - low_val) / high_val
            dropdown_lst.append(dropdown)
            dropdown_index_lst.append((high_index, low_index))

        return dropdown_lst, dropdown_index_lst

    @property
    def max_dropdown(self):
        """最大回撤率"""
        dropdown_lst, dropdown_index_lst = self.get_dropdown()
        if len(dropdown_lst) > 0:
            return max(dropdown_lst)
        else:
            return 0

    @property
    def max_dropdown_len(self):
        """最大回撤区间"""
        dropdown_lst, dropdown_index_lst = self.get_dropdown()
        if len(dropdown_lst) > 0:
            m = max(dropdown_lst)

            for i in range(len(dropdown_lst)):
                if math.isclose(dropdown_lst[i],m,rel_tol=1e-5):
                    return dropdown_index_lst[i][1] - dropdown_index_lst[i][0]
        else:
            return 0

    @property
    def annual_return(self):
        """
        年化收益率

        y = (v/c)^(D/T) - 1

        v: 最终价值
        c: 初始价值
        D: 有效投资时间(365)
        注: 虽然投资股票只有250天，但是持有股票后的非交易日也没办法投资到其他地方，所以这里我取365

        参考: https://wiki.mbalib.com/zh-tw/%E5%B9%B4%E5%8C%96%E6%94%B6%E7%9B%8A%E7%8E%87
        """
        # D = 365
        D = 252
        c = self._ast_val_hist[0]
        v = self._ast_val_hist[-1]
        # days = (self._date_hist[-1] - self._date_hist[0]).days
        days = len(self._date_hist)

        ret = (v / c) ** (D / days) - 1
        return ret

    @property
    def cum_ret(self):
        """累计收益率"""
        ret_lst = pd.Series(self._ast_val_hist).pct_change().cumsum()

        return ret_lst

    @property
    def total_returns(self):
        init_val = self._ast_val_hist[0]
        final_val = self._ast_val_hist[-1]
        return (final_val - init_val) / init_val

    @property
    def max_returns(self):
        init_val = self._ast_val_hist[0]
        max_val = max(self._ast_val_hist)
        return (max_val - init_val) / init_val

    @property
    def min_returns(self):
        init_val = self._ast_val_hist[0]
        min_val = min(self._ast_val_hist)
        return (min_val - init_val) / init_val

    @property
    def sharpe(self, rf=0.04):
        return self.get_sharpe(rf)

    def get_sharpe(self, rf=0.04):
        """夏普比率
                计算公式: SharpeRatio = (E(Rp) - Rf) / op

                E(Rp): 投资预期报酬率
                Rf: 无风险利率
                op: 投资组合的波动率(标准差)

                参卡:https://wiki.mbalib.com/zh-tw/%E5%A4%8F%E6%99%AE%E6%AF%94%E7%8E%87
                ---------
                Parameters:
                  rf:float
                        无风险利率，默认为4%
                ----
                """
        # # 有可能返回nan, 而nan 类型是float，bool值为True
        # return_std = (pd.Series(self._ast_val_hist, index=self._date_hist)
        #               .pct_change()
        #               .groupby(pd.Grouper(freq="W"))
        #               .sum().std())

        # 有可能返回nan, 而nan 类型是float，bool值为True
        return_std = (pd.Series(self._ast_val_hist, index=self._date_hist)
                      .pct_change()
                      .std())
        # 年化
        return_std = return_std * 252 ** 0.5

        # 防止return_sd == 0, 所以加上一个很小的数1e-5 == 0.00001
        ratio = (self.annual_return - rf) / (return_std + 1e-5)
        return ratio

    @property
    def win_ratio(self):
        return

    @property
    def profit_loss_ratio(self):
        return

    @property
    def annual_volatility(self):
        s = pd.Series(self._ast_val_hist, index=self._date_hist)
        rs = s.pct_change()
        std_return = rs.std()
        out = np.multiply(std_return, 252 ** (1.0 / 2))
        return out

    @property
    def ey_max_drawdown(self):
        s = pd.Series(self._ast_val_hist, index=self._date_hist)
        rs = s.pct_change()
        return ey.max_drawdown(rs)

    @property
    def ey_annual_return(self):
        s = pd.Series(self._ast_val_hist, index=self._date_hist)
        rs = s.pct_change()
        return ey.annual_return(rs,period='daily', annualization=None)

    @property
    def ey_sortino_ratio(self):
        s = pd.Series(self._ast_val_hist, index=self._date_hist)
        rs = s.pct_change()
        return ey.sortino_ratio(rs, period='daily', annualization=None)

    @property
    def ey_sharpe_ratio(self,rf = 0.04):
        return self.get_ey_sharpe_ratio(rf)

    def get_ey_sharpe_ratio(self,rf = 0.04):
        # rs = pd.DataFrame([self._ast_val_hist])
        # rs = rs.T  # 转置之后得到想要的结果
        # rs.rename(columns={0: 'returns'}, inplace=True)
        rs = pd.DataFrame({'returns':self._ast_val_hist} ,index=self._date_hist)
        # 计算每日回报率
        stock_returns = rs.pct_change()
        # 每日超额回报
        excess_returns = pd.DataFrame()
        risk_free = 0.04 / 252.0
        excess_returns["returns"] = stock_returns["returns"] - risk_free

        # print(excess_returns.describe())
        # 超额回报的均值
        avg_excess_return = excess_returns.mean()
        # print(avg_excess_return)
        # 超额回报的标准差
        std_excess_return = excess_returns.std()
        # print(std_excess_return)
        # 计算夏普比率
        # 日夏普比率
        daily_sharpe_ratio = avg_excess_return.div(std_excess_return)
        # 年化夏普比率
        annual_factor = np.sqrt(252)
        annual_sharpe_ratio = daily_sharpe_ratio.mul(annual_factor)
        # print("年化夏普比率\n", annual_sharpe_ratio)

        result = ey.sharpe_ratio(stock_returns["returns"], risk_free=risk_free)
        # print("empyrical计算结果\n", result)
        return result

    @property
    def ey_annual_volatility(self):
        s = pd.Series(self._ast_val_hist, index=self._date_hist)
        rs = s.pct_change()
        return ey.annual_volatility(rs, period='daily', annualization=None)