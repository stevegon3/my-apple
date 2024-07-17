import os
from datetime import timedelta
import pandas as pd
import plotly.graph_objects as go


def check_download_data(data_file='finance-charts-apple.csv'):
    """Check for the full stock data file locally, if not exists, then download
    Return the file contents in a DF"""
    path_to_data = os.path.join('data', data_file)
    if os.path.exists(path_to_data):
        print("File retrieved locally")
        return pd.read_csv(path_to_data, index_col=0)
    else:
        # In a real life production environment, we would probably put this URL in a config file
        #  or take in from the command line
        url = 'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
        df_data = pd.read_csv(url, index_col=0)
        df_data.to_csv(path_to_data)
        print("File retrieved from Github and written locally")
        return df

def correct_order(df_data: pd.DataFrame) -> pd.DataFrame:
    """Take in a stock price DF and discard all rows that are out of order (by date)
    Assumption: less than 1M rows. If higher would have to use a different approach"""
    if not df_data.empty and 'date' in df_data.columns and isinstance(df_data['date'].iloc[0], pd.Timestamp):
        ordered_list = []
        last_date = pd.Timestamp.min
        for row in df_data.itertuples(index=False):
            if row.date > last_date:
                ordered_list.append(row)
                last_date = row.date
        return pd.DataFrame(data=ordered_list, columns=df.columns)
    else:
        return df

def answer_1(df_data: pd.DataFrame) -> (float, float, float):
    """Take a stock price DF and return the min, max and avg/mean"""
    min_close = df_data['AAPL.Close'].min()
    max_close = df_data['AAPL.Close'].max()
    avg_close = df_data['AAPL.Close'].mean()
    return min_close, max_close, avg_close

def answer_2(df_data: pd.DataFrame) -> float:
    """Take a stock price DF and return the avg/mean volume"""
    return df_data['AAPL.Volume'].mean()

def answer_3(df_data: pd.DataFrame, close_mean) -> pd.DataFrame:
    """Take a stock price DF and return the subset of rows that are below the mean volume
    Add a day of week column to the DF"""
    df_low_volume = df_data[df_data['AAPL.Volume'] < close_mean].copy()
    df_low_volume['date_col'] = pd.to_datetime(df_low_volume.index)
    df_low_volume['day_of_week'] = df_low_volume['date_col'].dt.day_name()
    return df_low_volume

def answer_4(df_data: pd.DataFrame) -> pd.DataFrame:
    """Take a stock price DF and return a weekly aggregate of the numeric data"""
    return df_data.resample('W').agg({'AAPL.Open': 'mean', 'AAPL.High': 'mean',
                                      'AAPL.Low': 'mean', 'AAPL.Close': 'mean',
                                      'AAPL.Volume': 'mean', 'AAPL.Adjusted': 'mean',
                                      'dn': 'mean', 'mavg': 'mean', 'up': 'mean'})


if __name__ == "__main__":
    df = check_download_data()
    print("Head of source data:")
    df['date'] = pd.to_datetime(df.index)
    unique_df = df.reset_index().drop_duplicates(subset='date', keep='first').set_index('date')
    new_df = correct_order(unique_df).set_index('date')
    print(new_df.head(5))

    print('-' * 80)
    print('Question 1: min, max, mean of Closing prices')
    min_close, max_close, avg_close = answer_1(new_df)
    print(f"Min Price: {min_close}")
    print(f"Max Price: {max_close}")
    print(f"Avg Price: {avg_close}")

    print('-' * 80)
    print('Question 2: Calculate the average Close volume. Write out rows with volume < mean to a CSV file')
    path_to_low_volume = os.path.join('data', 'low-volume.csv')
    close_mean = answer_2(new_df)
    print(f'The average close volume is {close_mean}')
    df_low_volume = new_df[new_df['AAPL.Volume'] < close_mean]
    print("Writing out subset of rows to file 'low-volume.csv'")
    df_low_volume.to_csv(path_to_low_volume)
    df_check = pd.read_csv(path_to_low_volume, index_col=0)
    print(f'Checking file wrote properly: {df_low_volume.equals(df_check)}')

    print('-' * 80)
    print('Question 3: Add the day of week as a column to the data frame')
    df_low_volume = answer_3(new_df, close_mean)
    df_low_volume_date = df_low_volume.copy()
    print(f'New dataframe has {len(df_low_volume)} rows:')
    print(df_low_volume.head(5))

    print('-' * 80)
    # Assumption: 'week level' is driven by the data. Ie if there are data not in a particular week, no rows are shown.
    # Assumption: we are aggregating the unique, in order data set (not the subset of data below the average volume).
    path_to_weekly_agg = os.path.join('data', 'weekly-aggregation.csv')
    print('Question 4: Aggregate the data sets to the week level and save the new data set as a separate csv file')
    df_weekly_all = answer_4(new_df)
    print(df_weekly_all.head(5))
    print(df_weekly_all.tail(5))
    print("Writing out subset of rows to file 'weekly-aggregation.csv'")
    df_weekly_all.to_csv(path_to_weekly_agg)
    df_check = pd.read_csv(path_to_weekly_agg, header=0)
    df_check['date'] = pd.to_datetime(df_check['date'])
    df_check.set_index('date', inplace=True)
    wrote_correct = (pd.to_numeric(df_weekly_all['AAPL.Close'], errors='coerce')
                     .sub(pd.to_numeric(df_check['AAPL.Close'], errors='coerce'))
                     .abs() < 1e-6).all()
    print(f'Checking file wrote properly: {wrote_correct}')

    print('-' * 80)
    # Candlestick Chart
    # Assumption: 'low volume days' are the days below the average volume
    # Assumption: Only low volume days are shown, so there will be many "missing" days on the chart
    df_low_volume_date['date_col'] = pd.to_datetime(df_low_volume_date['date_col'])
    df_low_volume_date['date_col_str'] = df_low_volume_date['date_col'].dt.strftime('%Y-%m-%d')
    df_low_volume_date = df_low_volume_date.sort_values('date_col_str')
    all_days = set(df_low_volume_date.date_col[0] + timedelta(x) for x in range((df_low_volume_date.date_col[len(df_low_volume_date.date_col) - 1] - df_low_volume_date.date_col[0]).days))
    missing = sorted(set(all_days) - set(df_low_volume_date.date_col))
    print(df_low_volume_date.head(5))
    fig = go.Figure(data=[go.Candlestick(
        x=df_low_volume_date['date_col_str'],
        open=df_low_volume_date['AAPL.Open'],
        high=df_low_volume_date['AAPL.High'],
        low=df_low_volume_date['AAPL.Low'],
        close=df_low_volume_date['AAPL.Close']
    )])
    fig.update_xaxes(rangebreaks=[dict(values=missing)], tickangle=90, nticks=int(len(df_low_volume_date['date_col_str'])/5))
    fig.update_layout(
        title='AAPL Candlestick Chart of Low Volume days',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_tickformat='%Y-%m-%d',
        xaxis_rangeslider_visible=False
    )
    fig.show()
