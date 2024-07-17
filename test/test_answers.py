import pandas as pd
from apple.answers import answer_1, answer_2, answer_3, answer_4

url = 'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
test_df = pd.read_csv(url, index_col=0)
test_df['date'] = pd.to_datetime(test_df.index)
test_df = test_df.set_index('date')
test_df['Date'] = pd.to_datetime(test_df.index)

def test_answer_1():
    min_close, max_close, avg_close = answer_1(test_df)
    assert min_close == 90.339996
    assert max_close == 135.509995
    assert avg_close == 112.95833971146244

def test_answer_2():
    close_mean = answer_2(test_df)
    assert close_mean == 43178420.9486166

def test_answer_3():
    close_mean = answer_2(test_df)
    print(test_df.head(5))
    new_df = answer_3(test_df, close_mean)
    assert len(new_df) == 304

def test_answer_4():
    new_df = answer_4(test_df)
    assert abs(new_df['AAPL.Open'].values[0] - 128.054996) < 1e-6
    assert abs(new_df['AAPL.Close'].values[0] - 128.625000) < 1e-6
    assert abs(new_df['AAPL.Open'].values[-1] - 134.435001) < 1e-6
    assert abs(new_df['AAPL.Close'].values[-1] - 134.792500) < 1e-6
