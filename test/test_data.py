import pandas as pd
from apple.answers import check_download_data, correct_order

def test_check_download_data(data_file='finance-charts-apple.csv'):
    df = check_download_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 506

def test_out_of_order_rows():
    """'In the event a row is out of order or a duplicate exists please ignore the record and report them out after the processing'
        Assumption: 'Out of Order' means that the date is lower than all the previous dates; we ignore that one
        We resume if the next date is higher than all the previous dates
        We flag any additional dates if they are lower than all the previous dates except the previous ones out of order:
        [Example 1]
        1 2015-02-17
        2 2015-02-18
        3 2015-02-16
        #3 is out of order and will be ignored

        [Example 2]
        1 2015-02-17
        2 2015-02-19
        3 2015-02-16
        4 2015-02-20
        5 2015-02-18
        #3 and #5 is out of order and will be ignored
        Rows with 1313 at the Open should be discarded"""
    columns = ['date', 'AAPL.Open', 'AAPL.High', 'AAPL.Low', 'AAPL.Close', 'AAPL.Volume', 'AAPL.Adjusted', 'dn', 'mavg', 'up', 'direction']
    data = [['2015-02-17', 127.489998, 128.880005, 126.919998, 127.830002, 63152400, 122.905254, 106.741052, 117.927667, 129.114281, 'Increasing'],
            ['2015-02-17', 1313, 128.880005, 126.919998, 127.830002, 63152400, 122.905254, 106.741052, 117.927667, 129.114281, 'Increasing'],
            ['2015-02-18', 128.489998, 128.9, 126.9, 127.8, 63152800, 124, 106.741052, 117.927667, 129.114281, 'Increasing'],
            ['2015-02-16', 1313, 127.9, 125.9, 127.8, 63152100, 124, 106.741052, 117.927667, 129.114281, 'Increasing'],
            ['2015-02-15', 1313, 127.9, 125.9, 127.8, 63152100, 124, 106.741052, 117.927667, 129.114281, 'Increasing'],
            ['2015-02-17', 1313.489998, 128.880005, 126.919998, 127.830002, 63152400, 122.905254, 106.741052, 117.927667, 129.114281, 'Increasing']]
    df = pd.DataFrame(data, columns=columns)
    df['date'] = pd.to_datetime(df['date'])
    result_df = correct_order(df)
    result = result_df[result_df['AAPL.Open'] == 1313]
    assert result.empty
