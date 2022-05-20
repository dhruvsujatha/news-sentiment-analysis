from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import os

with open("tickers.txt") as tickers:
    tickers = tickers.read().splitlines()

JSON_PATH = "json/"
CSV_PATH = "csv/"

def framify_json(json):
    framified = pd.DataFrame()
    framified["ticker"] = json["ticker"]
    framified["date"] = json["date"]
    framified["title"] = json["headlines"].apply(lambda x: x["title"])
    framified["url"] = json["headlines"].apply(lambda x: x["url"])
    framified["timestamp"] = json["headlines"].apply(lambda x: x["timestamp"])
    framified["source"] = json["headlines"].apply(lambda x: x["source"])
    return framified

for ticker in tickers:
    spill_dir = os.listdir(JSON_PATH + ticker)
    for file in spill_dir:
        json_file = pd.read_json(JSON_PATH + ticker + "/" + file)
        framified = framify_json(json_file)
        if not os.path.isdir(CSV_PATH + ticker):
            os.mkdir(CSV_PATH + ticker)
        framified.to_csv(CSV_PATH + ticker + "/" + file.replace(".json", ".csv"), index = False)
