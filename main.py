import smtplib
from datetime import datetime, timedelta
import os

import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
MAX_ARTICLE = 2
MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')
api_key_number = os.environ.get('api_key_number')
apiKey_news = os.environ.get('apiKey_news')

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"



params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': api_key_number,
}

yesterday_date = str(datetime.now().date() - timedelta(days=1))
before_yesterday_date = str(datetime.now().date() - timedelta(days=2))


respond = requests.get(STOCK_ENDPOINT, params=params)
data = respond.json()

yesterday_data = data['Time Series (Daily)'][yesterday_date]["1. open"]

before_yesterday_data = data['Time Series (Daily)'][before_yesterday_date]["1. open"]

open_number_yesterday = float(yesterday_data)
open_number_before_yesterday = float(before_yesterday_data)
difference = abs(open_number_yesterday - open_number_before_yesterday)

difference_percentage = (1-abs(open_number_yesterday / open_number_before_yesterday)) * 100


params = {
    'status': 'ok',
    'q': STOCK_NAME,
    'apiKey': apiKey_news,
}
response_news = requests.get(NEWS_ENDPOINT, params=params)
data_response_news = response_news.json()


art_list = []
for a in range(0, MAX_ARTICLE):
    headline = data_response_news['articles'][a]['title']
    Brief = data_response_news['articles'][a]['description']
    r = (headline, Brief)
    art_list.append(r)

if art_list:
    for a in range(0, MAX_ARTICLE):
        headline = art_list[a][0]
        brief = art_list[a][1]

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=f"Subject:{COMPANY_NAME}\n\n"
                                                                       f"Headline: {headline}\n"
                                                                       f"Brief: {brief}")
else:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=f"Subject:{COMPANY_NAME}\n\nNo news")

