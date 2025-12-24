import pandas as pd
import yfinance as yf
from datetime import timedelta

def get_next_close(ticker, filing_date):
    # first available close price after filing date+1
    start_date = filing_date + timedelta(days=1)
    end_date = start_date + timedelta(days=10)
    try:
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False
        )

        if data.empty:
            return None

        close = data["Close"]

        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        return float(close.iloc[0])

    except Exception as e:
        print(f"Error fetching data for {ticker} on {filing_date}: {e}")
        return None
    
# def add_financial_market_data(df):
#     df['filing_date'] = pd.to_datetime(df['filing_date'])
#     # first available close price after filing date+1


# #     def get_next_close(ticker, filing_date):
# #         start_date = filing_date + timedelta(days=1)
# #         end_date = start_date + timedelta(days=10)
# #         try:
# #             data = web.DataReader(ticker, 'yahoo', start_date, end_date)
# #             if not data.empty:
# #                 return data['Close'].iloc[0]
# #             return None
# #         except Exception:
# #             return None
        
#     # def get_next_close(ticker, filing_date):
#     #     start_date = filing_date + timedelta(days=1)
#     #     end_date = start_date + timedelta(days=10)
#     #     try:
#     #         data = yf.download(ticker, start=start_date, end=end_date)
#     #         if not data.empty:
#     #             first_close = data['Close'].iloc[0]
#     #             return first_close
#     #         else:
#     #             return None
#     #     except Exception as e:
#     #         print(f"Error fetching data for {ticker} on {filing_date}: {e}")
#     #         return None

#     df['next_close'] = df.apply(lambda row: get_next_close(row['ticker'], row['filing_date']), axis=1)
#     return df

def add_financial_market_data(df):
    df['filing_date'] = pd.to_datetime(df['filing_date'])

    df['next_close'] = df.apply(
        lambda row: get_next_close(row['ticker'], row['filing_date']),
        axis=1
    )

    return df