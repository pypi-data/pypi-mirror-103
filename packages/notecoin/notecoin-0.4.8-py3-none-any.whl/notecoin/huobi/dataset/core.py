import os

from notedata.tables import SqliteTable


class TradeDetail(SqliteTable):
    def __init__(self, table_name='trade_detail', db_path=None, *args, **kwargs):
        if db_path is None:
            db_path = os.path.abspath(
                os.path.dirname(__file__)) + '/data/coin.db'

        super(TradeDetail, self).__init__(db_path=db_path, table_name=table_name, *args, **kwargs)
        self.columns = ['trade_id', 'ts', 'direction', 'price', 'amount']

    def create(self):
        self.execute("""
            create table if not exists {} (
               trade_id       BIGINT         
              ,amount         FLOAT 
              ,price          FLOAT
              ,ts             BIGINT
              ,direction      VARCHAR(5)
              ,primary key (trade_id)           
              )
            """.format(self.table_name))


class SymbolInfo(SqliteTable):
    def __init__(self, table_name='symbol_info', db_path=None, *args, **kwargs):
        if db_path is None:
            db_path = os.path.abspath(
                os.path.dirname(__file__)) + '/data/coin.db'

        super(SymbolInfo, self).__init__(db_path=db_path,
                                         table_name=table_name, *args, **kwargs)
        self.columns = ['symbol', 'base_currency', 'quote_currency', 'price_precision', 'amount_precision',
                        'symbol_partition',
                        'state', 'value_precision',
                        'min_order_amt', 'max_order_amt',
                        'limit_order_min_order_amt', 'limit_order_max_order_amt',
                        'sell_market_min_order_amt', 'sell_market_max_order_amt',
                        'buy_market_max_order_value',
                        'min_order_value', 'max_order_value',
                        'leverage_ratio', 'underlying', 'mgmt_fee_rate', 'charge_time',
                        'rebal_time', 'rebal_threshold',
                        'init_nav', 'api_trading'
                        ]

    def create(self):
        self.execute("""
                create table if not exists {} (
                symbol		                    VARCHAR	-- 交易对
                ,base_currency                  VARCHAR -- 交易对中的基础币种
                ,quote_currency		            VARCHAR	-- 交易对中的报价币种
                ,price_precision		        integer	-- 交易对报价的精度（小数点后位数）
                ,amount_precision		        integer	-- 交易对基础币种计数精度（小数点后位数）
                ,symbol_partition		        VARCHAR	-- 交易区，可能值: [main，innovation]
                ,`state`		                VARCHAR	-- 交易对状态；可能值: [online，offline,suspend] online _ 已上线；offline _ 交易对已下线，不可交易；suspend -- 交易暂停；pre_online _ 即将上线
                ,value_precision		        integer	-- 交易对交易金额的精度（小数点后位数）
                ,min_order_amt		            float	-- 交易对限价单最小下单量 ，以基础币种为单位（即将废弃）
                ,max_order_amt		            float	-- 交易对限价单最大下单量 ，以基础币种为单位（即将废弃）
                ,limit_order_min_order_amt		float	-- 交易对限价单最小下单量 ，以基础币种为单位（NEW）
                ,limit_order_max_order_amt		float	-- 交易对限价单最大下单量 ，以基础币种为单位（NEW）
                ,sell_market_min_order_amt		float	-- 交易对市价卖单最小下单量，以基础币种为单位（NEW）
                ,sell_market_max_order_amt		float	-- 交易对市价卖单最大下单量，以基础币种为单位（NEW）
                ,buy_market_max_order_value		float	-- 交易对市价买单最大下单金额，以计价币种为单位（NEW）
                ,min_order_value		        float	-- 交易对限价单和市价买单最小下单金额 ，以计价币种为单位
                ,max_order_value		        float	-- 交易对限价单和市价买单最大下单金额 ，以折算后的USDT为单位（NEW）
                ,leverage_ratio		            float	-- 交易对杠杆最大倍数(仅对逐仓杠杆交易对、全仓杠杆交易对、杠杆ETP交易对有效）
                ,underlying		                VARCHAR	-- 标的交易代码 (仅对杠杆ETP交易对有效)
                ,mgmt_fee_rate		            float	-- 持仓管理费费率 (仅对杠杆ETP交易对有效)
                ,charge_time		            VARCHAR	-- 持仓管理费收取时间 (24小时制，GMT+8，格式：HH:MM:SS，仅对杠杆ETP交易对有效)
                ,rebal_time		                VARCHAR	-- 每日调仓时间 (24小时制，GMT+8，格式：HH:MM:SS，仅对杠杆ETP交易对有效)
                ,rebal_threshold		        float	-- 临时调仓阈值 (以实际杠杆率计，仅对杠杆ETP交易对有效)
                ,init_nav		                float	-- 初始净值（仅对杠杆ETP交易对有效）
                ,api_trading		            VARCHAR	-- API交易使能标记（有效值：enabled, disabled）
                ,PRIMARY KEY (symbol)
                )
                """.format(self.table_name))


class KlineDetail(SqliteTable):
    def __init__(self, table_name='kline', db_path=None, *args, **kwargs):
        if db_path is None:
            db_path = os.path.abspath(
                os.path.dirname(__file__)) + '/data/coin.db'

        super(KlineDetail, self).__init__(db_path=db_path, table_name=table_name, *args, **kwargs)
        self.columns = ['id', 'amount', 'count', 'open', 'close', 'low', 'high', 'vol']

    def create(self):
        self.execute("""
            create table if not exists {} (
               id	    bigint	-- 调整为新加坡时间的时间戳，单位秒，并以此作为此K线柱的id
              ,amount	float	-- 以基础币种计量的交易量
              ,`count`	integer	-- 交易次数
              ,`open`   float	-- 本阶段开盘价
              ,`close`	float	-- 本阶段收盘价
              ,low	    float	-- 本阶段最低价
              ,high	    float	-- 本阶段最高价
              ,vol	    float	-- 以报价币种计量的交易量
              ,primary key (id)           
              )
            """.format(self.table_name))


class Kline1MinDetail(KlineDetail):
    def __init__(self, table_name='kline_1min', db_path=None, *args, **kwargs):
        super(Kline1MinDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline5MinDetail(KlineDetail):
    def __init__(self, table_name='kline_5min', db_path=None, *args, **kwargs):
        super(Kline5MinDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline15MinDetail(KlineDetail):
    def __init__(self, table_name='kline_15min', db_path=None, *args, **kwargs):
        super(Kline15MinDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline30MinDetail(KlineDetail):
    def __init__(self, table_name='kline_30min', db_path=None, *args, **kwargs):
        super(Kline30MinDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline60MinDetail(KlineDetail):
    def __init__(self, table_name='kline_60min', db_path=None, *args, **kwargs):
        super(Kline60MinDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline4HourDetail(KlineDetail):
    def __init__(self, table_name='kline_4hour', db_path=None, *args, **kwargs):
        super(Kline4HourDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline1DayDetail(KlineDetail):
    def __init__(self, table_name='kline_1day', db_path=None, *args, **kwargs):
        super(Kline1DayDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline1MonDetail(KlineDetail):
    def __init__(self, table_name='kline_1mon', db_path=None, *args, **kwargs):
        super(Kline1MonDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline1WeekDetail(KlineDetail):
    def __init__(self, table_name='kline_1week', db_path=None, *args, **kwargs):
        super(Kline1WeekDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)


class Kline1YearDetail(KlineDetail):
    def __init__(self, table_name='kline_1year', db_path=None, *args, **kwargs):
        super(Kline1YearDetail, self).__init__(table_name=table_name, db_path=db_path, *args, **kwargs)
