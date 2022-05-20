import json
import os
from urllib import response
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import string
import re

import pprint as pp

finviz_url = "https://finviz.com/quote.ashx?t="

tickers = ["AMZN", "AAPL", "AMD", "BABA", "CSCO", "FB", "GOOGL", "INTC", "MSFT", "NFLX", "NVDA", "PYPL", "TSLA", "TWTR", "V", "VZ", "WMT", "XOM"]

news_headlines = {}


def get_news_tables(ticker):
    url = finviz_url + ticker
    req = Request(url, headers={'User-Agent': 'my-app/0.0.1'})
    resp = urlopen(req)
    html = BeautifulSoup(resp, "lxml")
    return html.find(id = "news-table")

def get_news_headlines(table):
    response = []
    html_headline = table.findAll("tr")
    for index, row in enumerate(html_headline):
        headline = []
        headline.append(re.sub(r'[^\w\s]', '', row.a.text))
        headline.append(row.a["href"])
        headline.append(row.td.text.replace("\xa0", u""))
        headline.append(row.span.text[1:])
        response.append(headline)
    return response

def fix_dates(data):
    latest_date = ""
    for headline in data:
        timestamp = headline[2].split(" ")
        if len(timestamp) == 2:
            latest_date = timestamp[0]
        else:
            headline[2] = latest_date + " " + timestamp[0]
    return data

def group_by_date(data):
    by_date = {}
    for headline in data:
        date = headline[2].split(" ")[0]
        headline[2] = headline[2].split(" ")[1]
        headline_formatted = {}
        headline_formatted["title"] = headline[0]
        headline_formatted["url"] = headline[1]
        headline_formatted["timestamp"] = headline[2]
        headline_formatted["source"] = headline[3]
        try:
            by_date[date].append(headline_formatted)
        except KeyError:
            by_date[date] = [headline_formatted]
    return by_date

def save_to_json(data, ticker):
    for date in data:
        package = {"ticker": ticker, "date": date, "headlines": data[date]}
        if not os.path.isdir("data/" + ticker):
            os.mkdir("data/" + ticker)
        else:
            with open("data/" + ticker + "/" + date + ".json", "w") as f:
                json.dump(package, f, indent = 4)


for ticker in tickers:
    data = get_news_headlines(get_news_tables(ticker))
    data = fix_dates(data)
    data = group_by_date(data)
    save_to_json(data, ticker)