import os
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

from QuotesDownloader import SoftfxDownloader, QuotesType, QuotesPeriodicity

qd = SoftfxDownloader.Downloader()
now = datetime.date.today()

d = qd.get_quotes("EURUSD", now - relativedelta(days=30), now, QuotesPeriodicity.M1, QuotesType.Bids)
print(d.head(10))



