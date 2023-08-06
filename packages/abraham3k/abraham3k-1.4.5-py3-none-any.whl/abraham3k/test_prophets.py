from prophets import Isaiah, TwitterParser, Elijiah
import sys
from pprint import pprint
from datetime import datetime, timedelta

if __name__ == "__main__":
    print(f"Abraham Version: {open('version').read().strip()}")

    args = [sys.argv[1:]] if sys.argv[1:] else ["tesla"]  # default args

    # """
    darthvader = Isaiah(
        news_source="newsapi",
        newsapi_key=open("keys/newsapi-public").read().strip(),
        bearer_token=open("keys/twitter-bearer-token").read().strip(),
    )  # splitting means that it recursively splits a large text into sentences and analyzes each individually

    newest = datetime.now()
    oldest = newest - timedelta(days=7)  # datetime one week ago = the finish line

    scores = darthvader.twitter_summary_interval(
        *args, oldest, newest, period=timedelta(hours=1)
    )  # latest date to get news from
    scores["tesla"].to_csv("datasets/427sent.csv")

    print("Total\n--")
    print(scores)

    """
    scores = darthvader.news_summary(*args)  # latest date to get news from
    print("News\n--")
    pprint(scores)

    scores = darthvader.twitter_summary(*args, size=100)  # latest date to get news from
    print("\nTwitter\n--")
    pprint(scores)
    """