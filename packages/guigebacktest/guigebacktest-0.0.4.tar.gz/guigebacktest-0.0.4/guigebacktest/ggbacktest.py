# -*- coding: utf-8 -*-
import math
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from guigebacktest.config import config
from guigebacktest.backtest import BackTest
from guigebacktest.broker import BackTestBroker
from guigebacktest.utils import mkdir


plt.style.use("ggplot")
plt.rcParams['font.sans-serif'] = ['simhei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题


class GGBackTest(BackTest):
    def __init__(self):
        self.price_df = self.load_price_table()
        feed = self.get_feed()
        trade_cal = self.get_trade_cal()
        cash = 100000
        super(GGBackTest, self).__init__(feed=feed, cash=cash,
                                         broker=BackTestBroker(cash=cash, cm_rate=0.0, deal_price="close"),
                                         trade_cal=trade_cal, enable_stat=True)

    def initialize(self):
        self.info("initialize")
        self.right_df = self.load_right_table()
        self.last_dt = None
        self.net_price_lst = {}
        self.stock_values = pd.DataFrame(columns=self.feed.keys(), index=['date'])
        self.costs = {}
        self.net_price_lst = {}

        print("初始化完成")

    def on_order_ok(self, order):
        """当订单执行成功后调用"""
        print("订单执行成功", order)
        if order['done'] == True:
            str_date = order['date'].strftime('%Y-%m-%d')
            code = order['code']
            if str_date not in self.costs.keys():
                self.costs[str_date] = {}
            self.costs[str_date][code] = {'cost': order['price'] *  order['shares'], 'buysell': order['type']}

    def on_order_timeout(self, order):
        """当订单超时后调用"""
        print("订单超时", order)

    def finish(self):
        """在回测结束后调用"""
        self.caculate_net_price()
        print("回测结束")

    def on_tick(self, dt):
        self.save_stock_values(dt)

        position = self.ctx.broker.position

        str_date = dt.strftime('%Y-%m-%d')
        # 获取权重表的某日的所有资产的权重分配（一行）
        rights = self.right_df.loc[str_date]
        # 第一天交易
        first_day = self.right_df.index[0]
        is_first = str_date == first_day

        # 权重没发生变化说明没有交易
        if not is_first:
            pre_date = self.last_dt
            pre_str_date = pre_date.strftime('%Y-%m-%d')
            pre_rights = self.right_df.loc[pre_str_date]
            if str(pre_rights.values) == str(rights.values):
                return

        total_value = self.ctx.broker.assets_value
        total_value_availble = total_value * (1 - 0.02)
        buys = {}
        sells = {}

        tick_data = self.ctx["tick_data"]
        print(tick_data)
        print(dt)

        for code, hist in tick_data.items():
            # print(code, hist)
            close = hist['close']
            right_rate = rights[code]
            right_rate = right_rate - config.COMMISSION  # 预留资金以应付佣金和计算误差
            target_value = total_value_availble * right_rate

            self_value = self.ctx.broker.get_stock_value(code)
            pos = self.ctx.broker.get_shares(code)

            if is_first:
                size = int(target_value / close // 100 * 100)
                if size > 0:
                    buys[code] = {"size": size}
                    print(
                        "%s %f  code:%s close:%f    value:%f    position value:%f   position:%f buysell size:%f " % (
                            str_date, total_value, code, close, self_value, pos * close, pos, size))
            else:
                size = int(abs((self_value - target_value) / close // 100 * 100))
                if size > 0:
                    # 持仓过多，要卖
                    multi = 1
                    if self_value > target_value:
                        sells[code] = {"size": size}
                        multi = - 1
                    else:
                        buys[code] = {"size": size}

                    print(
                        "%s %f    code:%s close:%f    value:%f    position value:%f   position:%f buysell size:%f " % (
                            str_date, total_value, code, close, self_value, pos * close, pos, size * multi))

        # 先买后卖
        for symbol, value in sells.items():
            self.ctx.broker.sell(symbol, value["size"])

        for symbol, value in buys.items():
            self.ctx.broker.buy(symbol, value["size"])

        # 记录上个交易日
        self.last_dt = dt

    # 加载权重表
    def load_right_table(self):
        return pd.read_csv(config.DATA_INPUT_PATH + 'right.csv', header=0, index_col="date")

    def save_stock_values(self, dt):
        str_date = dt.strftime('%Y-%m-%d')
        position = self.ctx.broker.position
        tick_data = self.ctx["tick_data"]
        vs = []
        for code, hist in tick_data.items():
            close = hist['close']
            if code in position.keys():
                cc = 0
                for p in position[code]:
                    c = p['shares'] * close
                    cc = cc + c
                vs.append(cc)
            else:
                vs.append(0)
        self.stock_values.loc[str_date] = vs

    def caculate_net_price(self):
        is_first_date = True
        rate_lst = {}
        accumulate_val = 100
        trade_dates = self.right_df.index.values
        trade_dates_len = len(trade_dates)
        last_date = trade_dates[-1]
        for date in self.right_df.index.values:
            # 最后一天不计算
            if date == last_date:
                break

            # 得到下一个交易日'
            next_i = 0
            for i, d in enumerate(trade_dates):
                if d == date and date != last_date:
                    next_i = i + 1
                    break

            next_date = trade_dates[next_i]

            rights = self.right_df.loc[date]
            next_values = self.stock_values.loc[next_date]
            if is_first_date:
                is_first_date = False
                cur_values = rights.to_dict()
                for c, v in cur_values.items():
                    cur_values[c] = 0.0
            else:
                cur_values = self.stock_values.loc[date]

            total_rate = 0.0
            for code, right in rights.items():
                cur_val = cur_values[code]
                next_val = next_values[code]
                v1 = cur_val
                if date in self.costs.keys():
                    if code in self.costs[date].keys():
                        cost = self.costs[date][code]
                        if cost['buysell'] == 'buy':
                            v1 = cur_val + cost['cost']
                        else:
                            v1 = cur_val - cost['cost']
                # 计算收益率
                if math.isclose(v1, 0.00001, abs_tol=0.00001):
                    rate = 0
                else:
                    rate = (next_val - v1) / v1
                # 每天收益率*权重
                rate_r = rate * right
                # 每天总收益率
                total_rate = total_rate + rate_r
            rate_lst[next_date] = total_rate
            accumulate_val = accumulate_val * (1 + total_rate)
            self.net_price_lst[next_date] = accumulate_val
        print("caculate_net_price ok")

    def output(self):
        print("最大回撤率: {:.3f}% ".format(self.stat.max_dropdown * 100))
        print("最大回撤时长: {} ".format(self.stat.max_dropdown_len))
        print("策略总收益率： {:.3f}%".format(self.stat.total_returns * 100))
        print("年化收益率: {:.3f}%".format(self.stat.annual_return * 100))
        print("夏普比率: {:.3f}".format(self.stat.sharpe))
        print("最大收益率: {:.3f}%".format(self.stat.max_returns * 100))
        print("年化波动率: {:.3f}%".format(self.stat.annual_volatility * 100))

        print("ey 最大回撤率: {:.3f}%".format(self.stat.ey_max_drawdown * 100))
        print("ey 年化收益率: {:.3f}%".format(self.stat.ey_annual_return * 100))
        print("ey sortino ratio: {:.3f}%".format(self.stat.ey_sortino_ratio * 100))
        print("ey 夏普比率: {:.3f}".format(self.stat.ey_sharpe_ratio))
        print("ey 年化波动率: {:.3f}%".format(self.stat.ey_annual_volatility * 100))

        mkdir(config.DATA_OUTPUT_PATH)
        dic = {"最大回撤率": [round(self.stat.max_dropdown * 100, 3)],
               "最大回撤时长": [self.stat.max_dropdown_len],
               "策略总收益率": [round(self.stat.total_returns * 100, 3)],
               "年化收益率": [round(self.stat.annual_return * 100, 3)],
               "夏普比率": [round(self.stat.sharpe, 3)],
               "最大收益率": [round(self.stat.max_returns * 100, 3)],
               "年化波动率": [round(self.stat.annual_volatility * 100, 3)],

               # "ey 最大回撤率": [round(self.stat.ey_max_drawdown * 100, 3)],
               # "ey 年化收益率": [round(self.stat.ey_annual_return * 100, 3)],
               "ey sortino ratio": [round(self.stat.ey_sortino_ratio * 100, 3)],
               # "ey 夏普比率": [round(self.stat.ey_sharpe_ratio, 3)],
               # "ey 年化波动率": [round(self.stat.ey_annual_volatility * 100, 3)],
               }
        df0 = pd.DataFrame.from_dict(dic)
        df0.to_csv(config.DATA_OUTPUT_PATH + "result.csv", index=False)

        df1 = pd.DataFrame.from_dict([self.net_price_lst]).T
        df1.columns = ['value']
        df1.to_csv(config.DATA_OUTPUT_PATH + "net_price.csv")

        self.display()

    def display(self):
        title = "最大回撤率: {:.3f}% 最大回撤时长: {} 年化收益率: {:.3f}% 年化波动率: {:.3f}% 夏普比率: {:.3f} Sortino ratio: {:.3f}%  最大收益率: {:.3f}%\n\n净值曲线走势"
        title = title.format(self.stat.max_dropdown * 100,
                             self.stat.max_dropdown_len,
                             self.stat.annual_return * 100,
                             self.stat.annual_volatility * 100,
                             self.stat.sharpe,
                             self.stat.ey_sortino_ratio * 100,
                             self.stat.max_returns * 100)
        fig = plt.figure(figsize=(18, 15))

        # add_subplot(3, 2, 1)  # 推荐此种写法
        # add_subplot(321)
        # (3, 2, 1)(3, 2, 2)
        # (3, 2, 3)(3, 2, 4)
        # (3, 2, 5)(3, 2, 6)

        # 绘制净价曲线走势图
        rows = 1
        ax_net_price = fig.add_subplot(rows, 1, 1)
        ax_net_price.set_title(title)
        dates = list(self.net_price_lst.keys())
        values = list(self.net_price_lst.values())
        xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
        ax_net_price.plot(xs,values)
        plt.savefig(config.DATA_OUTPUT_PATH+'net_price.png')
        plt.show()


    def get_trade_cal(self):
        # 分析起止日期
        trade_cal = pd.to_datetime(self.price_df['date']) + pd.Timedelta(hours=15)
        return trade_cal

    def load_price_table(self):
        return pd.read_csv(config.DATA_INPUT_PATH + 'price.csv', header=0)

    def get_feed(self):
        feed = {}
        # 分析资产
        codes = list(self.price_df.columns[1:])
        for i in range(len(codes)):
            code = codes[i]
            df1 = pd.DataFrame()
            df1['date'] = pd.to_datetime(self.price_df['date']) + pd.Timedelta(hours=15)
            # df1['date'] = df['date']
            df1[code] = self.price_df.apply(
                lambda x: {'open': x[code], 'high': x[code], 'low': x[code], 'close': x[code]}, axis=1)
            df1.set_index(['date'], inplace=True)
            dic = df1.groupby('date')[code].apply(lambda x: x).to_dict()
            # for (k, v) in dic.items():
            # print("-----", k, str(v))
            # for (kk, vv) in v.items():
            #     print("-----",k,kk, vv)
            feed[code] = dic

        return feed


def run_ggbacktest():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpath', type=str, default='D:/data/input/', help="input faile path")
    parser.add_argument('--outpath', type=str, default='D:/data/output/', help='output faile path')
    parser.add_argument('--operation', type=str, default='right', choices=['right', 'trade'], help="trade action")
    parser.add_argument('--quote', type=str, default='price', choices=['price', 'earning'], help="market data")

    args = parser.parse_args()
    config.DATA_INPUT_PATH = args.inpath
    config.DATA_OUTPUT_PATH = args.outpath
    config.OPERATION_TYPE = args.operation
    config.QUOTE_TYPE = args.quote

    ggtest = GGBackTest()
    ggtest.start()
    ggtest.output()


if __name__ == '__main__':
    run_ggbacktest()

