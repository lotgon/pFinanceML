import sys
from QuotesDownloader.SoftfxDownloader import *
import datetime
from dateutil.relativedelta import relativedelta


def main():
    print("Python version:", sys.version)
    test2()

def test1():
    dl = Downloader()
    now = datetime.date.today()
    test = dl.get_quotes("EURUSD", now - relativedelta(months=4), now, QuotesPeriodicity.H1, QuotesType.Bids)
    print(test)
def test2():
    dl = Downloader()
    now = datetime.date.today()
    test = dl.get_quotes("EURUSD", now - relativedelta(months=9), now, QuotesPeriodicity.H1, QuotesType.BidsAsks)
    print(test)

if __name__ == "__main__":
    main()

#%%
