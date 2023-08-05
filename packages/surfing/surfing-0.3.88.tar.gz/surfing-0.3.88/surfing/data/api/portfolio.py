from typing import Tuple, List

import pandas as pd
import datetime
from sqlalchemy import func
import numpy as np
from .raw import RawDataApi
from .basic import BasicDataApi
from .derived import DerivedDataApi
from ...util.singleton import Singleton
from ...util.calculator_item import CalculatorBase
from ...util.calculator import Calculator

TRADE_HISTORY_TEMP = [
    {
        'datetime':datetime.date(2018,12,4),
        'fund_weight':[
            {
                'fund_id':'005267!0',
                'weight':0.2,
                'fund_type':'低估价值',
            },
            {
                'fund_id':'166005!0',
                'weight':0.1,
                'fund_type':'成长价值',
            },
            {
                'fund_id':'006551!0',
                'weight':0.1,
                'fund_type':'稳态红利',
            },
            {
                'fund_id':'090010!0',
                'weight':0.15,
                'fund_type':'稳态红利',
            },
            {
                'fund_id':'003396!0',
                'weight':0.15,
                'fund_type':'低估价值',
            },
            {
                'fund_id':'161005!0',
                'weight':0.15,
                'fund_type':'稳态红利',
            },
            {
                'fund_id':'005827!0',
                'weight':0.15,
                'fund_type':'成长价值',
            },
            
        ]
    },
    {
        'datetime':datetime.date(2021,3,2),
        'fund_weight':[
            {
                'fund_id':'005267!0',
                'weight':0.2,
                'fund_type':'低估价值',
            },
            {
                'fund_id':'166005!0',
                'weight':0.2,
                'fund_type':'成长价值',
            },
            {
                'fund_id':'006551!0',
                'weight':0.2,
                'fund_type':'稳态红利',
            },
            {
                'fund_id':'090010!0',
                'weight':0.1,
                'fund_type':'稳态红利',
            },
            {
                'fund_id':'003396!0',
                'weight':0.1,
                'fund_type':'低估价值',
            },
            {
                'fund_id':'161005!0',
                'weight':0.1,
                'fund_type':'稳态红利',
            },
            {
                'fund_id':'118001!0',
                'weight':0.1,
                'fund_type':'成长价值',
            },
            
        ]
    },
]

BENCHMARK_INFO = {
    '稳态红利':'csi_dvi',
    '成长价值':'csi300_value',
    '低估价值':'csi_retval',    
}



class PortfolioDataApi(metaclass=Singleton):

    def get_all_fund_info(self, fund_list=None):
        try:
            if fund_list is not None:
                mutual_fund_list = [_ for _ in fund_list if '!' in _]
                hedge_fund_list = [_ for _ in fund_list if '!' not in _]
                mutual_fund_info = BasicDataApi().get_fund_info(fund_list=mutual_fund_list)[['fund_id','desc_name']]
                hedge_fund_info = RawDataApi().get_hf_fund_info(fund_list=hedge_fund_list)[['fund_id','desc_name']]
            else:
                mutual_fund_info = BasicDataApi().get_fund_info()[['fund_id','desc_name']]
                hedge_fund_info = RawDataApi().get_hf_fund_info()[['fund_id','desc_name']]
            if not mutual_fund_info.empty:
                mutual_fund_info.loc[:,'fund_type'] = '公募'    
            if not hedge_fund_info.empty:
                hedge_fund_info.loc[:,'fund_type'] = '私募'
            df_list = [i for i in [mutual_fund_info, hedge_fund_info] if not i.empty ]
            fund_info = pd.concat(df_list)
            return fund_info

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_all_fund_info')

    def get_all_fund_nav(self, start_date='', end_date='', fund_list: Tuple[str] = ()):
        try:
            if fund_list is not None:
                mutual_fund_list = [_ for _ in fund_list if '!' in _]
                hedge_fund_list = [_ for _ in fund_list if '!' not in _]
                mutual_fund_nav = BasicDataApi().get_fund_nav_with_date(start_date=start_date-datetime.timedelta(days=20),end_date=end_date,fund_list=fund_list)
                hedge_fund_nav = RawDataApi().get_hf_fund_nav(fund_ids=hedge_fund_list, start_date=start_date-datetime.timedelta(days=20), end_date=end_date)
            else:
                mutual_fund_nav = BasicDataApi().get_fund_nav_with_date(start_date=start_date-datetime.timedelta(days=20),end_date=end_date)
                hedge_fund_nav = RawDataApi().get_hf_fund_nav_dt(start_date=start_date-datetime.timedelta(days=20))
            
            if not mutual_fund_nav.empty:
                mutual_fund_nav = mutual_fund_nav.pivot_table(index='datetime',columns='fund_id',values='adjusted_net_value')
            if not hedge_fund_nav.empty:
                hedge_fund_nav = hedge_fund_nav.pivot_table(index='datetime',columns='fund_id',values='nav')
            df_list = [i for i in [mutual_fund_nav, hedge_fund_nav] if not i.empty ]
            fund_nav = pd.concat(df_list, axis=1).sort_index().ffill().loc[start_date:]
            fund_nav.index.name = 'datetime'
            return fund_nav

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_all_fund_nav')

    def trade_history_parse(self, trade_history):
        try:
            fund_type = {}
            order_list = []
            for dic in trade_history:
                dt = dic['datetime']
                _dic = {dt:{}}
                for trade_i in dic['fund_weight']:
                    type_i = trade_i['fund_type'] 
                    fund_id = trade_i['fund_id']
                    weight = trade_i['weight']
                    _dic[dt][fund_id]=weight
                    if type_i not in fund_type:
                        fund_type[type_i] = [fund_id]
                    elif type_i in fund_type and fund_id not in fund_type[type_i]:
                        fund_type[type_i].append(fund_id)
                    else:
                        pass
                order_list.append(_dic)
            return order_list, fund_type

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.trade_history_parse')

    def get_portfolio_nav(self, trade_history):
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            fund_list = set(list([j for dic in order_list for i in dic.values() for j in i.keys()]))
            _begin_date = min([j for i in order_list for j in i.keys()])
            fund_nav = self.get_all_fund_nav(start_date=_begin_date,fund_list=fund_list)
            fund_nav = fund_nav.ffill()
            order_dic = { dt: i[dt] for i in order_list for dt in list(i.keys())}
            date_list = [j for i in order_list for j in i.keys()] + [fund_nav.index[-1]]
            date_pairs = [[dt, date_list[idx+1]] for idx, dt in enumerate(date_list) if dt != date_list[-1]]
            port_amount = 1 
            port_mv_result = []
            port_weight_result = []
            port_type_result = []
            port_share_result = {}
            for dts in date_pairs:
                b_d = dts[0]
                e_d = dts[1]
                fund_wgt_dt = pd.Series({k : v for k, v in order_dic[b_d].items() if v > 0})
                fund_amt_dt = port_amount * fund_wgt_dt
                fund_nav_dt = fund_nav.loc[b_d:e_d,fund_wgt_dt.keys()]
                fund_vol_dt = port_amount * fund_wgt_dt / fund_nav_dt.iloc[0]
                port_share_result[b_d] = fund_vol_dt.to_dict()
                fund_amount_dt = fund_nav_dt * fund_vol_dt
                fund_weight_dt = fund_amount_dt.div(fund_amount_dt.sum(axis=1), axis=0)
                port_weight_result.append(fund_weight_dt)
                port_mv = fund_amount_dt.sum(axis=1).to_frame()
                port_mv.columns = ['组合']
                port_mv = port_mv / port_mv.iloc[0] * port_amount
                port_amount = port_mv['组合'].values[-1]
                port_mv_result.append(port_mv)
                fund_type_result = []
                for fund_type_i, fund_list_i in fund_type.items():
                    fund_mv_type_i = fund_amount_dt[fund_amount_dt.columns.intersection(fund_list_i)].sum(axis=1).rename(fund_type_i).to_frame()
                    fund_type_result.append(fund_mv_type_i)
                fund_type_amt_dt = pd.concat(fund_type_result, axis=1)
                port_type_result.append(fund_type_amt_dt)
            port_mv_result = [i.iloc[:-1] if i.index[-1] != port_mv_result[-1].index[-1] else i for i in port_mv_result]
            port_mv_result = pd.concat(port_mv_result)
            port_mv_result.index.name = 'datetime'
            port_weight_result = [i.iloc[:-1] if i.index[-1] != port_weight_result[-1].index[-1] else i for i in port_weight_result]
            port_weight_result = pd.concat(port_weight_result)
            port_type_result = [i.iloc[:-1] if i.index[-1] != port_type_result[-1].index[-1] else i for i in port_type_result]
            port_type_result = pd.concat(port_type_result)
            data = {
                '净值':port_mv_result,
                '各基净值':fund_nav,
                '各基权重':port_weight_result,
                '大类净值':port_type_result,
                '持有信息':port_share_result,
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_nav')
   
    def get_portfolio_benchmark_info(self):
        try:
            index_info = BasicDataApi().get_index_info(index_list=['hs300','national_debt','csi500','gem','sp500rmb','mmf','hsi'])
            res = []
            for r in index_info.itertuples():
                res.append([r.index_id, r.desc_name])
            return res

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_benchmark_info')

    def get_portfolio_mv(self, fund_nav, index_id, begin_date, end_date, time_para):
        try:
            def print_st(mdd):
                return str(round(mdd * 100,2)) + '%' 
            fund_nav.columns=['组合']
            basic = BasicDataApi()
            index_price = basic.get_index_price_dt(index_list=[index_id],start_date=fund_nav.index[0] - datetime.timedelta(days=10),end_date=fund_nav.index[-1]).pivot_table(index='datetime',columns='index_id',values='close')
            index_info = basic.get_index_info([index_id])
            name_dic = index_info.set_index('index_id').to_dict()['desc_name']
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            df = pd.merge(fund_nav.reset_index(), index_price.reset_index(),how='outer').set_index('datetime').sort_index().ffill().dropna()
            df = df.loc[begin_date:end_date]
            df = df / df.iloc[0]
            df.loc[:,'价格比'] = df.组合 / df[index_id]
            df = df.rename(columns=name_dic)
            mv_df = df[['组合']].rename(columns={'组合':'mv'})
            mv_df.index.name = 'date'
            mdd_details = Calculator.get_mdd_recover_result(mv_df=mv_df)
            mdd1 = print_st(mdd_details['mdd1'])
            mdd1_d1 = str(mdd_details['mdd1_d1'])
            mdd1_d2 = str(mdd_details['mdd1_d2'])
            mdd1_lens = mdd_details['mdd1_lens']
            mdd2 = print_st(mdd_details['mdd2'])
            mdd2_d1 = str(mdd_details['mdd2_d1'])
            mdd2_d2 = str(mdd_details['mdd2_d2'])
            mdd2_lens = mdd_details['mdd2_len']
            bk_stats = Calculator.get_stat_result_from_df(df=mv_df.reset_index(), date_column='date', value_column='mv').__dict__
            ar = print_st(bk_stats['annualized_ret'])
            av = print_st(bk_stats['annualized_vol'])
            sharpe = round(bk_stats['sharpe'],2)
            st1 = f'年化收益: {ar} 年化波动: {av} 夏普比率: {sharpe}'
            st2 = f'最大回撤 {mdd1} {mdd1_d1} : {mdd1_d2}, {mdd1_lens} days'
            st3 = f'第二回撤 {mdd2} {mdd2_d1} : {mdd2_d2}, {mdd2_lens} days'
            sts = [st1, st2, st3]
            mdd_dic_1 = {
                'd1':str(mdd_details['mdd1_d1']),
                'd2':str(mdd_details['mdd1_d2']),
                'v1':df['组合'].loc[mdd_details['mdd1_d1']: mdd_details['mdd1_d2']].min(),
                'v2':df['组合'].loc[mdd_details['mdd1_d1']: mdd_details['mdd1_d2']].max(),
            }
            mdd_dic_2 = {
                'd1':str(mdd_details['mdd2_d1']),
                'd2':str(mdd_details['mdd2_d2']),
                'v1':df['组合'].loc[mdd_details['mdd2_d1']: mdd_details['mdd2_d2']].min(),
                'v2':df['组合'].loc[mdd_details['mdd2_d1']: mdd_details['mdd2_d2']].max(),
            }
            data = {
                'data':df,
                'mdd_1':mdd_dic_1,
                'mdd_2':mdd_dic_2,
                'stats': sts
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_mv')

    def get_portfolio_cur_mdd(self, fund_nav, begin_date, end_date, time_para):
        try:            
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            fund_nav = fund_nav.loc[begin_date:end_date]
            df = fund_nav / fund_nav.cummax() - 1
            df.columns=['历史回撤']
            df_min = df['历史回撤'].min()
            data = {
                '历史回撤': df,
                '最低值': df_min,
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_cur_mdd')

    def get_portfolio_ret_distribution(self, fund_nav, period, begin_date, end_date, time_para):
        try:
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            fund_nav = fund_nav.loc[begin_date:end_date]    
            fund_nav = CalculatorBase.data_resample_weekly_nav(df=fund_nav, rule=period)
            ret = fund_nav.pct_change(1).iloc[1:]
            ret.columns=['收益']
            result = np.histogram(a=ret['收益'],bins=8)
            fre = result[0].tolist()
            _sum = np.sum(fre)
            fre = [ i / _sum for i in fre]
            data = {'分布_频度':fre,
                '分布_收益':result[1].round(3).tolist(),
                '收益':ret
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_cur_mdd')

    def get_portfolio_stats(self, fund_nav, index_id):
        try:
            fund_nav.columns=['组合']
            basic = BasicDataApi()
            index_price = basic.get_index_price_dt(index_list=[index_id],start_date=fund_nav.index[0] - datetime.timedelta(days=10),end_date=fund_nav.index[-1]).pivot_table(index='datetime',columns='index_id',values='close')
            index_info = basic.get_index_info([index_id])
            name_dic = index_info.set_index('index_id').to_dict()['desc_name']
            df = pd.merge(fund_nav.reset_index(), index_price.reset_index(),how='outer').set_index('datetime').sort_index().ffill().dropna()
            df = df / df.iloc[0]
            df = df.rename(columns=name_dic)
            result = []
            for col in df:
                res_status = Calculator.get_benchmark_stat_result(dates=df.index,
                                                                values=df[col],
                                                                benchmark_values=df[name_dic[index_id]],
                                                                frequency = '1W',
                                                                risk_free_rate=0.025, )
                
                indicators_tem={
                    '开始日期': str(res_status.start_date),
                    '截止日期': str(res_status.end_date),
                    '累计收益': str(round((res_status.last_unit_nav-1)*100,2)) + "%",
                    '最近一月收益':str(round(res_status.recent_1m_ret*100 ,2)) + "%",
                    '年化收益率': str(round(res_status.annualized_ret*100 ,2)) + "%",
                    '年化波动率': str(round(res_status.annualized_vol*100 ,2)) + "%",
                    '夏普比率': round(res_status.sharpe,2),
                    '最大回撤': str(round(res_status.mdd*100 ,2)) + "%",
                    '最大回撤开始日期': str(res_status.mdd_date1),
                    '最大回撤结束日期': str(res_status.mdd_date2),
                    '最大回撤持续时长': res_status.mdd_lens,
                    '卡玛比率': round(res_status.ret_over_mdd ,2),
                    '下行标准差': str(round(res_status.downside_std*100 ,2)) + "%",
                    'alpha': str(round(res_status.alpha*100 ,2)) + "%",
                    'beta': round(res_status.beta ,2),
                    '信息比率': round(res_status.ir ,2),
                    'CL模型_alpha': str(round(res_status.alpha_cl*100 ,2)) + "%",
                    'CL模型_beta': str(round(res_status.beta_cl*100 ,2)) + "%",
                    '相对胜率': str(round(res_status.win_rate*100 ,2)) + "%",
                    '绝对胜率': str(round(res_status.win_rate_0*100 ,2)) + "%",
                    'name':col
                }
                if col != '组合':
                    indicators_tem['alpha'] = '-'
                    indicators_tem['beta'] = '-'
                    indicators_tem['信息比率'] = '-'
                    indicators_tem['CL模型_alpha'] = '-'
                    indicators_tem['CL模型_beta'] = '-'
                    indicators_tem['相对胜率'] = '-'
                result.append(indicators_tem)
                # indicators_tem={
                #     '开始日期': str(res_status.start_date),
                #     '截止日期': str(res_status.end_date),
                #     '累计收益': (res_status.last_unit_nav-1)*100,
                #     '最近一月收益':res_status.recent_1m_ret*100,
                #     '年化收益率': res_status.annualized_ret*100,
                #     '年化波动率': res_status.annualized_vol*100,
                #     '夏普比率': res_status.sharpe,
                #     '最大回撤': res_status.mdd*100,
                #     '最大回撤开始日期': str(res_status.mdd_date1),
                #     '最大回撤结束日期': str(res_status.mdd_date2),
                #     '最大回撤持续时长': res_status.mdd_lens,
                #     '卡玛比率': res_status.ret_over_mdd,
                #     '下行标准差': res_status.downside_std*100,
                #     'alpha': res_status.alpha*100,
                #     'beta': res_status.beta,
                #     '信息比率': res_status.ir,
                #     'CL模型_alpha': res_status.alpha_cl*100,
                #     'CL模型_beta': res_status.beta_cl*100,
                #     '相对胜率': res_status.win_rate*100,
                #     '绝对胜率': res_status.win_rate_0*100,
                #     'name':col
                # }
                # result.append(indicators_tem)
            df = pd.DataFrame(result).set_index('name').T
            df.index.name = '指标'
            for col in df:
                df[col] = df[col].where(pd.notnull(df[col]), None)
            return df
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_portfolio_stats')

    def get_rolling_corr(self, fund_navs, frequency, windows, step):
        try:
            fund_navs_period = CalculatorBase.data_resample_weekly_nav(df=fund_navs, rule=frequency)
            fund_ret = fund_navs_period.pct_change(1).iloc[1:]  
            # 弱鸡排列
            col_pair = []
            cols = fund_ret.columns.tolist()
            for idx_i, col_i in enumerate(cols):
                cols_list = cols[idx_i+1:]
                for idx_j, col_j in enumerate(cols_list):
                    col_pair.append([col_i,col_j])

            corr_result_df = []
            for col_pair_i in col_pair:
                df = fund_ret[col_pair_i]
                idx_list = df.reset_index().index.tolist()
                corr_result = []
                b = idx_list[0]
                _result = []
                
                # 计算窗口划分 不包含min_windows概念
                while(1):
                    e = b + windows
                    if e > idx_list[-1]:
                        break
                    else:
                        _result.append([b,e])
                        b += step

                # 计算部分
                for idxs in _result:
                    _df = df.iloc[idxs[0]:idxs[1]]
                    corr_result.append({'datetime':_df.index[-1], f'{col_pair_i[0]}_{col_pair_i[1]}':_df.corr().iloc[1,0]})
                df = pd.DataFrame(corr_result).set_index('datetime')
                corr_result_df.append(df)
            df = pd.concat(corr_result_df,axis=1)
            return df
        
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_rolling_corr')
    
    def get_port_fund_list(self, trade_history):
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            fund_list = []
            for order in order_list:
                for d, fund_wgt in order.items():
                    fund_list.extend(list(fund_wgt))
            fund_list = list(set(fund_list))
            fund_info = self.get_all_fund_info(fund_list)
            result = [[r.fund_id, r.desc_name] for r in fund_info.itertuples()]
            return result
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_list')

    def get_port_fund_pos_date(self,fund_id, trade_history, index_id): 
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            basic = BasicDataApi()
            fund_list = [fund_id]
            fund_info = self.get_all_fund_info(fund_list=fund_list)
            desc_name_dic = fund_info.set_index('fund_id').to_dict()['desc_name']

            begin_date, end_date = RawDataApi().get_date_range(time_para='ALL', begin_date=None, end_date=None)
            fund_nav = self.get_all_fund_nav(fund_list=[fund_id])
            fund_nav = fund_nav.ffill()
            index_price = basic.get_index_price(index_list=[index_id])
            index_price = index_price.pivot_table(columns='index_id',index='datetime',values='close')
            nav_df = fund_nav.join(index_price).ffill().dropna()
            
            result = []
            for order in order_list:
                for d, fund_wgt in order.items():
                    fund_wgt['datetime'] = d
                    result.append(fund_wgt)

            weight_df = pd.DataFrame(result).set_index('datetime')
            pos_con = 1 - weight_df[fund_id].isnull()
            result = []
            is_empty = True
            for r in pos_con.iteritems():
                if is_empty and r[1] == 1:
                    dic = {'begin_date':r[0]}
                    is_empty = False
                elif not is_empty and r[1] == 0:
                    dic['end_date'] = r[0]
                    dic['rise'] =  bool(nav_df.loc[:dic['end_date']].iloc[-1][fund_id] > nav_df.loc[dic['begin_date'],fund_id])
                    dic['begin_date'] = str(dic['begin_date'])
                    dic['end_date'] = str(dic['end_date'])
                    result.append(dic)
                    dic = {}
                    is_empty = True
            if not is_empty:
                dic['end_date'] = end_date
                dic['rise'] =  bool(nav_df.loc[:dic['end_date']].iloc[-1][fund_id] > nav_df.loc[dic['begin_date'],fund_id])
                dic['begin_date'] = str(dic['begin_date'])
                dic['end_date'] = str(dic['end_date'])
                result.append(dic)
            nav_df.index.name = 'datetime'
            data = {
                '净值':nav_df.rename(columns=desc_name_dic),
                '持有期':result}
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_pos_date')

    def get_port_ret_resolve_date_range(self, trade_history):
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            begin_date, end_date = RawDataApi().get_date_range(time_para='ALL', begin_date=None, end_date=None)
            begin_date = list(order_list[0].keys())[0]
            data = {'begin_date':begin_date,'end_date':end_date}
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_ret_resolve_date_range')
    
    def get_port_ret_resolve(self, share_list , begin_date , end_date):
        try:
            basic = BasicDataApi()
            fund_list = list(set([i for dt, share_list in share_list.items() for i in list(share_list.keys())]))
            fund_info = self.get_all_fund_info(fund_list=fund_list)
            desc_name_dic = fund_info.set_index('fund_id').to_dict()['desc_name']
            all_ret_dict = []
            for i in range(len(list(share_list.keys()))):
                this_date = list(share_list.keys())[i]
                if i+1 < len(list(share_list.keys())) :
                    next_date = list(share_list.keys())[i+1]
                else :
                    next_date = datetime.date.today()

                if next_date <= begin_date: 
                    continue
                elif next_date <= end_date: 
                    cal_end = next_date
                elif next_date > end_date: 
                    cal_end = end_date

                if this_date >= end_date: 
                    break
                elif this_date <= begin_date: 
                    cal_start = begin_date
                elif this_date > begin_date: 
                    cal_start = this_date
                ret_dict = {}
                for fund_id in list(share_list[this_date].keys()):
                    fund_share = share_list[this_date][fund_id]
                    fund_nav = self.get_all_fund_nav(start_date=cal_start,end_date=cal_end,fund_list=[fund_id])
                    fund_nav = fund_nav.ffill()
                    fund_ret = round((fund_nav.iloc[-1].values[0] * fund_share - fund_nav.iloc[0].values[0] * fund_share)*100,2)
                    ret_dict[desc_name_dic[fund_id]] = fund_ret
                all_ret_dict.append(ret_dict)
            return all_ret_dict
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_ret_resolve')

    def get_port_fund_weight(self, fund_wgt, trade_history):
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            fund_info = self.get_all_fund_info(fund_wgt.columns.tolist())
            name_dic = fund_info.set_index('fund_id').to_dict()['desc_name']
            fund_wgt = fund_wgt.rename(columns=name_dic)
            result = {}
            for types, fund_list in fund_type.items():
                result[types] = [name_dic[_] for _ in fund_list]

            _result = []
            for type_i, fund_list in result.items():
                _df = fund_wgt[fund_list].sum(axis=1)
                _df.name = type_i
                _result.append(_df)
            fund_type_wgt = pd.concat(_result,axis=1)
            trade_list = [j for i in order_list for j in i.keys()]
            dts = fund_wgt.index.tolist()
            dts = [dt for idx, dt in enumerate(dts) if idx % 10 == 0]
            fund_wgt_part_1 = fund_wgt.loc[dts]
            index_list = trade_list + [fund_wgt.index[0]] + [fund_wgt.index[-1]]
            fund_wgt_part_2 = fund_wgt.loc[fund_wgt.index.intersection(index_list)]
            fund_wgt = pd.concat([fund_wgt_part_1,fund_wgt_part_2]).sort_index()
            data = {
                '基金':fund_wgt,
                '类型':fund_type_wgt,
                '类型对照':result,
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_weight')

    def get_port_fund_mdd_details(self, trade_history):
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            result = self.get_portfolio_nav(trade_history=trade_history)
            df = result['净值']
            fund_wgt = result['各基权重']
            fund_nav = result['各基净值']

            fund_type_dic = {}
            for type_i, fund_list in fund_type.items():
                for fund_id in fund_list:
                    fund_type_dic[fund_id] = type_i
            mdd_part1 = (df.loc[:, '组合'] / df.loc[:, '组合'].rolling(10000, min_periods=1).max())
            mdd = round(1 - mdd_part1.min(),4)
            mdd_date1 = df.loc[:mdd_part1.idxmin(),'组合'].idxmax()
            mdd_date2 = mdd_part1.idxmin()
            exchange_list = [j for i in order_list for j in list(i.keys()) ]
            exchange_list = np.array(exchange_list)
            exchange_dts = exchange_list[(exchange_list> mdd_date1) & (exchange_list < mdd_date2)]
            fund_list = list(set([z for i in order_list for j in i.values() for z in j.keys() ]))
            if len(exchange_dts) == 0:
                date_list = [[mdd_date1,mdd_date2]]
            else:
                l = [mdd_date1] + exchange_dts + [mdd_date2]
                date_list = [ [i,l[l.index(i)+1]] for i in l if i != l[-1]]
            fund_info = self.get_all_fund_info(fund_list=fund_list)
            desc_name_dic = fund_info.set_index('fund_id').to_dict()['desc_name']
            _mdd_list = []
            for date_group in date_list:
                b_d = date_group[0]
                e_d = date_group[1]
                fund_wgt_dt = fund_wgt.loc[b_d].dropna()
                mdd_i = ((fund_nav.loc[e_d] / fund_nav.loc[b_d] - 1) * fund_wgt_dt)
                _mdd_list.append(mdd_i)
            mdd_dict = ((pd.concat(_mdd_list,axis=1).fillna(0) + 1).prod(axis=1) - 1).to_dict()
            df_result = pd.DataFrame([desc_name_dic]).T
            df_result.columns = ['基金名']
            df_result.loc[:,'回撤贡献'] = df_result.index.map(mdd_dict)
            df_result.loc[:,'类型'] = df_result.index.map(fund_type_dic)
            df_result = df_result.dropna()
            df_result.index.name = '基金代码'
            df_result = df_result.reset_index()    
            fund_nav = fund_nav.loc[mdd_date1:mdd_date2].rename(columns=desc_name_dic)
            fund_nav = fund_nav.reindex(pd.date_range(start=fund_nav.index[0], end=fund_nav.index[-1]))
            data = {
                'mdd': df_result,
                'fund_nav': fund_nav,
            }
            return data

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_mdd_details')

    def get_port_rolling_beta_index_info(self):
        return [['hs300','沪深300'],['csi500','中证500']] 

    def get_port_fund_alpha_detail(self, trade_history, benchmark_id_info): 
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            result = PortfolioDataApi().get_portfolio_nav(trade_history=trade_history)
            fund_nav = result['各基净值']
            fund_wgt = result['各基权重']
            dts_list = [j for i in order_list for j in i.keys()] + [fund_nav.index[-1]]
            dts_list = [[i,dts_list[dts_list.index(i)+1]] for i in dts_list if i != dts_list[-1]]

            index_price = BasicDataApi().get_index_price_dt(index_list=list(benchmark_id_info.values()),
                                                            start_date=fund_nav.index[0],
                                                            end_date=fund_nav.index[-1],
                                                        )
            index_price = index_price.pivot_table(index='datetime',columns='index_id',values='close')
            fund_info = self.get_all_fund_info(fund_list=fund_nav.columns.tolist())
            fund_desc_dic = fund_info.set_index('fund_id')['desc_name'].to_dict()
            index_info = BasicDataApi().get_index_info(index_list=list(benchmark_id_info.values()))
            index_desc_dic = index_info.set_index('index_id')['desc_name'].to_dict()
            result = {}
            for fund_ti,_fund_list in fund_type.items():
                _result = []
                for dts in dts_list:
                    b_d = dts[0]
                    e_d = dts[1]
                    fund_wgt_i = fund_wgt.loc[b_d:e_d].iloc[:-1].dropna(axis=1)
                    type_fund_list = fund_wgt_i.columns.intersection(_fund_list) 
                    wgts = fund_wgt_i[type_fund_list].mean()
                    _fund_nav = fund_nav.loc[b_d:e_d].iloc[:-1][type_fund_list]
                    _fund_ret = (_fund_nav.iloc[-1] / _fund_nav.iloc[0] - 1)# * wgts
                    _fund_ret = _fund_ret.to_dict()
                    index_id = benchmark_id_info[fund_ti]
                    index_rets = index_price.loc[b_d:e_d,index_id]
                    index_rets_i = index_rets.iloc[-1] / index_rets.iloc[0] - 1  
                    dic={
                        'begin_date':str(b_d),
                        'end_date':str(e_d),
                        'index_ret': int(index_rets_i * 10000),
                        'index_name':index_desc_dic[index_id],
                        'fund_details':[],
                    }
                    for _fund_id in type_fund_list:
                        _dic = {
                                'fund':fund_desc_dic[_fund_id],
                                'ret':int((_fund_ret[_fund_id] - index_rets_i) * 10000*wgts[_fund_id]),
                        }
                        dic['fund_details'].append(_dic)
                    _result.append(dic)
                result[fund_ti] = _result
            return result

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_fund_alpha_detail')

    def get_port_recent_ret_details(self, trade_history, index_id, time_para, begin_date, end_date, benchmark_id_info):
        try:
            order_list, fund_type = self.trade_history_parse(trade_history)
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            result = PortfolioDataApi().get_portfolio_nav(trade_history=trade_history)
            fund_nav=result['净值']
            port_nav = PortfolioDataApi().get_portfolio_mv(fund_nav=fund_nav, index_id=index_id,begin_date=begin_date,end_date=end_date,time_para=time_para)
            fund_info = self.get_all_fund_info(fund_list = result['各基净值'].columns.tolist())
            fund_desc_dic = fund_info.set_index('fund_id')['desc_name'].to_dict()
            fund_type_dic = { vi: k for k, v in fund_type.items() for vi in v}
            cols = port_nav['data'].columns
            cols = [i for i in cols if '价格比' not in i]
            result_1 = port_nav['data'][cols]
            bps = str(int((port_nav['data']['组合'].values[-1] / port_nav['data']['组合'].values[0] - 1) * 10000)) +'BP'
            res_1 = port_nav['stats'][0]
            result_1_str = f'{res_1} 总收益 {bps}'

            _index_price = result['大类净值'].loc[begin_date:]
            benchmark_id_info_r = {v: k for k, v in benchmark_id_info.items()}
            index_price = BasicDataApi().get_index_price_dt(index_list=list(benchmark_id_info.values()),start_date=begin_date,end_date=end_date)
            index_price = index_price.pivot_table(columns='index_id',values='close',index='datetime')
            index_price = index_price.rename(columns=benchmark_id_info_r)
            index_price = index_price.reindex(_index_price.index)
            result_2 = _index_price / _index_price.iloc[0] / (index_price / index_price.iloc[0])
            price_ratio = result_2.copy()
            res_2_dic = (_index_price.iloc[-1] / _index_price.iloc[0] - 1) * 10000
            result_2_str = ' '.join([f'{k} {int(v)}BP' for k, v in res_2_dic.items()])

            recent_ret = result['各基净值'].loc[begin_date:].dropna(axis=1)
            recent_ret = (recent_ret.iloc[-1] / recent_ret.iloc[0] - 1).to_frame()
            recent_ret.columns = ['基金涨跌']
            # TODO 考虑换仓
            wgt_df = result['各基权重'].tail(1).T
            wgt_df.columns = ['权重']
            recent_ret = recent_ret.join(wgt_df)
            recent_ret = recent_ret.dropna()
            recent_ret.loc[:,'基金收益'] = recent_ret['基金涨跌'] * recent_ret['权重']
            recent_ret['基金涨跌'] = recent_ret['基金涨跌'].map(lambda x : str(round(x * 100,2))+'%')
            recent_ret['权重'] = recent_ret['权重'].map(lambda x: str(round(100*x,2))) +'%'
            recent_ret['基金收益'] = recent_ret['基金收益'].map(lambda x: str(int(10000*x))) +'BP'
            recent_ret.loc[:,'开始时间'] = price_ratio.index[0]
            recent_ret.loc[:,'结束时间'] = price_ratio.index[-1]
            recent_ret.loc[:,'基金名'] = recent_ret.index.map(fund_desc_dic)
            recent_ret.loc[:,'基金类型'] = recent_ret.index.map(fund_type_dic)
            recent_ret = recent_ret[['基金名','开始时间','结束时间','基金类型','基金涨跌','权重','基金收益']]
            result_3 = recent_ret
            result_2 = result_2.reindex(pd.date_range(start=result_2.index[0], end=result_2.index[-1]))
            result_2.index.name = 'datetime'
            data = {
                '组合收益':result_1,
                '组合收益描述':result_1_str,
                '资产价格比收益':result_2,
                '资产价格比收益描述':result_2_str,
                '个基近期收益':result_3,
            }
            return data
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from portfolio.get_port_recent_ret_details')
