import pandas as pd
from apple.answers import check_download_data

def test_check_download_data(data_file='finance-charts-apple.csv'):
    df = check_download_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 506