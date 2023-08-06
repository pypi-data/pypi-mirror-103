from prophets import Isaiah, TwitterParser, Elijiah
import sys
from pprint import pprint

if __name__ == "__main__":
    print(f"Abraham Version: {open('version').read().strip()}")
    tp = TwitterParser(
        "AAAAAAAAAAAAAAAAAAAAADlsOwEAAAAAbU2spi7uom94cd9T5bGtwQs1ruU%3DpbX9zabbqoAEa4NkeSjuJk7GEft1mck9Y3FDhNKjFkIWQfqFb6"
    )

    args = [sys.argv[1:]] if sys.argv[1:] else ["tesla"]  # default args

    # """
    darthvader = Isaiah(
        news_source="newsapi",
        newsapi_key="3530e04f04034a85a0ebf4d925c83c69",
        bearer_token=open("keys/twitter-bearer-token").read().strip(),
        splitting=True,
        weights={"desc": 0.4, "text": 0.2, "title": 0.4},
    )  # splitting means that it recursively splits a large text into sentences and analyzes each individually

    scores = darthvader.twitter_sentiment(
        *args,
    )  # latest date to get news from
    pprint(scores)

    scores = darthvader.news_sentiment_summary(
        *args,
        window=2,  # how many days back from up_to to get news from
        up_to="2021-4-22T00:00:00Z",
    )  # latest date to get news from
    pprint(scores)
# """
