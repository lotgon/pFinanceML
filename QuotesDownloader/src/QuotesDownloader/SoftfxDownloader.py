import os
import pkgutil
import subprocess
import pandas
import platformdirs
import zipfile
import io
import enum
import time


class QuotesType(str, enum.Enum):
    Bids = 'bids'
    Asks = 'asks'
    Ticks = 'ticks'
    BidsAsks = 'bidsasks'


class QuotesPeriodicity(str, enum.Enum):
    M1 = 'M1'
    M15 = 'M15'
    H1 = 'H1'
    D1 = 'D1'


class Downloader:
    def __init__(self, path2tool=""):
        if path2tool == "":
            path2tool = os.path.join(platformdirs.user_cache_dir(), "pythonQuotesDownloader")
        self._dir2exe = path2tool
        self._path2exe = os.path.join(path2tool, "QuotesDownloader.exe")
        os.makedirs(os.path.dirname(self._dir2exe), exist_ok=True)
        pkgdata = pkgutil.get_data(__name__, 'tool/QuotesDownloader.zip')
        with zipfile.ZipFile(io.BytesIO(pkgdata)) as zip_ref:
            zip_ref.extractall(self._dir2exe)
        self._path2cache = os.path.join(self._dir2exe, "cache")
        os.makedirs(os.path.dirname(self._path2cache), exist_ok=True)
        self._login = "100"
        self._password = "TTqfdeppmhDR"
        self._server = "ttlive.fxopen.com"

    def get_quotes(self, symbol, startDate, endDate, periodicity: QuotesPeriodicity, typeQuotes: QuotesType) -> pandas.DataFrame:
        if typeQuotes == QuotesType.BidsAsks:
            bids = self.get_quotes(symbol, startDate, endDate, periodicity, QuotesType.Bids)
            asks = self.get_quotes(symbol, startDate, endDate, periodicity, QuotesType.Asks)
            return bids.merge(asks, how='outer', on="date_time", suffixes=(".bids", ".asks"))
        qt = "Bid"
        if typeQuotes == QuotesType.Asks:
            qt = "Ask"
        elif qt == QuotesType.Ticks:
            qt = "Ticks"
        file_name = f"{symbol} {qt} {periodicity}  {startDate.strftime('%Y%m%d')}  {endDate.strftime('%Y%m%d')}.csv"
        file_name = os.path.join(self._path2cache, file_name)

        if not os.path.exists(file_name):
            self.__download_data(file_name, symbol, startDate, endDate, periodicity, typeQuotes)

        data = pandas.read_csv(file_name, sep=';')
        return data

    def __download_data(self, file_name, symbol, startDate, endDate, periodicity: QuotesPeriodicity, typeQuotes: QuotesType):
        parameters = f" -a={self._server} -p=5042 -u={self._login} -w={self._password} -s={symbol} -f={startDate} -t={endDate} -o=csv -v=false -d={periodicity} -l=\"{self._path2cache}\" -r={typeQuotes}"

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= (subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW)
        startupinfo.wShowWindow = subprocess.SW_HIDE
        subprocess.Popen(self._path2exe + parameters, startupinfo=startupinfo)
        total_time = 5
        while total_time > 0 and not (os.path.exists(file_name) and os.path.getsize(file_name) > 0):
            time.sleep(.1)
            total_time -= .1

