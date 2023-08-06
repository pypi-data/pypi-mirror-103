from prophets import Isaiah, TwitterParser, Elijiah
import sys
from pprint import pprint

if __name__ == "__main__":
    print(f"Abraham Version: {open('version').read().strip()}")

    args = [sys.argv[1:]] if sys.argv[1:] else ["tesla"]  # default args

    # """
    darthvader = Isaiah(
        news_source="newsapi",
        newsapi_key="3530e04f04034a85a0ebf4d925c83c69",
        bearer_token=open("keys/twitter-bearer-token").read().strip(),
    )  # splitting means that it recursively splits a large text into sentences and analyzes each individually

    # """
    scores = darthvader.news_summary(*args)  # latest date to get news from
    print("News\n--")
    pprint(scores)
    scores = darthvader.twitter_summary(*args, size=200)  # latest date to get news from
    print("\nTwitter\n--")
    pprint(scores)
