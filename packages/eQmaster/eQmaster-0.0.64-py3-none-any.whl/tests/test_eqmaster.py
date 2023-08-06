import os
import unittest
import eQmaster
import pandas

BUCKET = 'ephod-tech.trading-advisor.auto-trade.tw.data'

class TesteQmaster(unittest.TestCase):
    def setUp(self):
        self.eq = eQmaster.eQueries(
            {
                'config_path': 'tests/data/market.json',
                'key': '70b5197c-44bd-4ff4-abd3-c5f3db92e03f',
                'credential': '62ab148d-deb6-4549-acb9-8d4693e96396',
                'stock_data_src': 'tests/data/{symbol}/{filename}',
                'index_data_src': 'tests/data/{symbol}/{filename}'
            }
        )
        print(self.eq)

    def tearDown(self):
        os.remove('70b5197c-44bd-4ff4-abd3-c5f3db92e03f')
        os.remove('62ab148d-deb6-4549-acb9-8d4693e96396')

    def testSetup(self):
        assert self.eq.username == 'ava'
        assert self.eq.password == 'ava'
        assert self.eq.config_path == 'tests/data/market.json'
        assert self.eq.stock_data_src == 'tests/data/{symbol}/{filename}'
        assert self.eq.index_data_src == 'tests/data/{symbol}/{filename}'

    def testGet_Stock_Columns_Match(self):
        df = self.eq.get(attr='stock', search_list=['0050.tw'], columns=['Stock_Symbol', 'Date', 'Margin_Purchase_Buy_Lot', 'High', 'Low', 'Volume'])
        clist = [x for x in df.columns if x not in ['Stock_Symbol', 'Date', 'Margin_Purchase_Buy_Lot', 'High', 'Low', 'Volume']]
        assert len(clist) == 0

    def testGet_Stock_Columns_Mismatch(self):
        df = self.eq.get(attr='stock', search_list=['0050.tw'], columns=['Stock_Symbol', 'Date', 'Margin_Purchase_Buy_Lot', 'High', 'Low', 'Volume', 'MissingCol'])
        clist = [x for x in df.columns if x not in ['Stock_Symbol', 'Date', 'Margin_Purchase_Buy_Lot', 'High', 'Low', 'Volume']]
        assert len(clist) == 0

    def testGet_Stock_Count_Match(self):
        df = self.eq.get(attr='stock', search_list=['0050.tw'], columns=['Stock_Symbol', 'Date', 'High', 'Low', 'Volume'])
        assert df['Stock_Symbol'].count() == len(df['Date'].unique())

    def testGet_Stock_Warrant_Count_Match(self):
        df = self.eq.get(attr='stock', search_list=['0050.tw'], columns=['Stock_Symbol', 'Date', 'High', 'Low', 'Volume', 'Warrant_Symbol', 'Warrant_Type', 'Name'])
        assert len(df['Date'].unique()) <= len(df['Warrant_Symbol'].unique())

    def testGet_Index_Warrant_Columns_Match(self):
        df = self.eq.get(attr='index', search_list=['IX0001'], columns=['Index_Symbol','Date','Volume','Warrant_Symbol','Warrant_Name'])
        clist = [x for x in df.columns if x not in ['Index_Symbol','Date','Volume','Warrant_Symbol','Warrant_Name']]
        assert len(clist) == 0

    def testIndexColumns(self):
        _list = self.eq.columns('index')
        clist = [x for x in _list if x not in ['Index_Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Index_Volume', 'Index_Stock_Share', 'PE_Ratio', 'PB_Ratio', 'CDIV_Ratio', 'Warrant_Symbol', 'Name', 'Close', 'Price_Flux', 'Idx_Close', 'Idx_Down', 'Type', 'Execution', 'List_Date', 'Execution_Start_Date', 'Last_Trade_Date', 'Execution_End_Date', 'Execution_Ratio', 'Execution_Price', 'Max_Execution_Price', 'Min_Execution_Price', 'Date']]
        assert len(clist) == 0

    def testStockColumns(self):
        _list = self.eq.columns('stock')
        clist = [x for x in _list if x not in ['Stock_Symbol', 'Date', 'Margin_Purchase_Buy_Lot', 'Margin_Purchase_Sold_Lot', 'Short_Sale_Buy_Lot', 'Short_Sale_Sold_Lot', 'Margin_Purchase_Difference_Lot', 'Margin_Purchase_Difference_1000', 'Short_Sale_Difference_Lot', 'Short_Sale_Difference_1000', 'Margin_Purchase_Utilization_Rate', 'Short_Sale_Utilization_Rate', 'MP_SS_Ratio', 'LMR', 'SMR', 'TMR', 'Open', 'High', 'Low', 'Close', 'Volume', 'Stock_No', 'PE_Ratio', 'PB_Ratio', 'CDIV_Ratio', 'Open_Adj', 'High_Adj', 'Low_Adj', 'Close_Adj', 'Warrant_Symbol', 'Warrant_Name', 'Warrant_Close', 'Price_Flux', 'Idx_Close', 'Idx_Down', 'Type', 'Execution', 'List_Date', 'Execution_Start_Date', 'Last_Trade_Date', 'Execution_End_Date', 'Execution_Ratio', 'Execution_Price', 'Max_Execution_Price', 'Min_Execution_Price', 'Annd_s', 'D0001', 'D0002', 'D0003', 'D0005', 'D0006', 'D0007', 'Foreign_STrade', 'Trust_STrade', 'Retail_STrade', 'Total_STrade', 'Foreign_Buy_Lot', 'Foreigh_Sell_Lot', 'Trust_Buy_Lot', 'True_Sell_Lot', 'Retail_Buy_Lot', 'Retail_Sell_Let', 'Foreign_Stock', 'Trust_Stock', 'Retail_Stock', 'Foreign_Stock_PCT', 'Trust_Stock_PCT', 'Retail_Stock_PCT']]
        assert len(clist) == 0

    def testConvertStockSymbol(self):
        stock_symbol_list = self.eq.convert_symbol(['0050.tw'])
        assert stock_symbol_list[0] == '0050'

    def testInfo(self):
        listed_stock_companies = eQmaster.get_listed_companies()        
        cnt = listed_stock_companies.count()
        
        assert len(cnt) > 0 and cnt[0] > 0
    
    def testBolingerBand(self):
        df = pandas.read_parquet('tests/data/0050/stock_price.parquet.gzip')
        ret = eQmaster.bolinger_band(df, label='close_adj')

        assert 'UpperBand' in ret.columns
        assert 'LowerBand' in ret.columns

    def testNegBolingerBand(self):
        df = pandas.read_parquet('tests/data/0050/stock_price.parquet.gzip')
        ret = eQmaster.bolinger_band(df, label='Close')

        assert ret is None

if __name__ == '__main__':
    unittest.main()