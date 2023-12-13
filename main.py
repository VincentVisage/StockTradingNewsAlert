import html
import requests
import os
import smtplib
from datetime import date, timedelta

MY_EMAIL = 'your mail'
PASSWORD = 'your pass'

API_KEY = os.environ.get('API_STOCK')
NEWS_API = '6574ed7c42814be79d52bc9e08fb1ec5'
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={API_KEY}'
r = requests.get(url)
data = r.json()

keys = list(data['Time Series (Daily)'].keys())
yesterday = data['Time Series (Daily)'][keys[1]]
before_yesterday = data['Time Series (Daily)'][keys[2]]

yesterday_close = float(yesterday['4. close'])
before_yesterday_close = float(before_yesterday['4. close'])
print(yesterday_close)
print(before_yesterday_close)
procent = round(abs((yesterday_close/before_yesterday_close) * 100 - 100), 2)
print(procent)
stock_change =  f'🔺{procent}%' if before_yesterday_close < yesterday_close else f'🔻{procent}%'

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
today = date.today()
yesterday_date = today - timedelta(days=1)

url = f'https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={yesterday_date}&sortBy=popularity&apiKey={NEWS_API}'

r = requests.get(url)
data = r.json()
news = [a for a in data['articles'] if data['articles'].index(a) < 3]
print(news)

with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    for a in news:
        title = html.unescape(a['title'])
        description = a['description']
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:{title} {stock_change}\n\n{description}".encode('utf-8')
        )


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

