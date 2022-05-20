from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

data = pd.read_json("AMZN_May-19-22.json")
headlines = pd.DataFrame()
headlines["ticker"] = data["ticker"]
headlines["date"] = data["date"]
headlines["title"] = data["headlines"].apply(lambda x: x["title"])
headlines["url"] = data["headlines"].apply(lambda x: x["url"])
headlines["timestamp"] = data["headlines"].apply(lambda x: x["timestamp"])
headlines["source"] = data["headlines"].apply(lambda x: x["source"])
print(headlines.head())
