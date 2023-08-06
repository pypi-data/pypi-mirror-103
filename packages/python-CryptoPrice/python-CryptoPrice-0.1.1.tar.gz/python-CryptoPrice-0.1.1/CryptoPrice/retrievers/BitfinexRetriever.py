import datetime
from typing import List, Tuple, Optional
from collections import defaultdict

import asyncio
import requests
from bfxapi.client import Client

from CryptoPrice.common.trade import TradingPair
from CryptoPrice.exceptions import RateAPIException
from CryptoPrice.retrievers.KlineRetriever import KlineRetriever
from CryptoPrice.common.prices import Kline
from CryptoPrice.utils.time import TIMEFRAME


class BitfinexRetriever(KlineRetriever):
    """
    docs: https://github.com/bitfinexcom/bitfinex-api-py
    https://docs.bitfinex.com/
    """
    kline_translation = {
        TIMEFRAME.m1: '1m',
        TIMEFRAME.m5: '5m',
        TIMEFRAME.m15: '15m',
        TIMEFRAME.m30: '30m',
        TIMEFRAME.h1: '1h',
        TIMEFRAME.h6: '6h',
        TIMEFRAME.h12: '12h',
        TIMEFRAME.d1: '1D',
    }

    def __init__(self, kline_timeframe: TIMEFRAME = TIMEFRAME.m1, closest_window: int = 310):
        self.client = Client()
        super(BitfinexRetriever, self).__init__('bitfinex', kline_timeframe, closest_window)

        self.assets_to_pair = defaultdict(dict)
        for trading_pair in self.supported_pairs:
            self.assets_to_pair[trading_pair.asset][trading_pair.ref_asset] = trading_pair

    @staticmethod
    def assets_from_symbol(symbol: str) -> Tuple[Optional[str], Optional[str]]:
        """
        transform a Bitfinex symbol to a tuple with the base and the quote asset.
        If the operation fail, return None, None

        :param symbol: Bitfinex symbol
        :type symbol: str
        :return: asset, ref_asset
        :rtype: Tuple[Optional[str], Optional[str]]
        """
        assets = symbol.split(':')
        try:
            return assets[0], assets[1]
        except IndexError:
            pass
        ref_assets = ['USD', 'UST', 'BTC', 'EUR', 'ETH']
        for ref_asset in ref_assets:
            if symbol.endswith(ref_asset):
                return symbol[:-len(ref_asset)], ref_asset
            elif symbol.startswith(ref_asset):
                return ref_asset, symbol[len(ref_asset):]
        return None, None

    def get_supported_pairs(self) -> List[TradingPair]:
        """
        Return the list of trading pair supported by this retriever

        :return: list of trading pairs
        :rtype: List[TradingPair]
        """
        url = "https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange"
        response = requests.get(url)
        symbols = response.json()[0]
        trading_pairs = []
        for symbol in symbols:
            asset, ref_asset = BitfinexRetriever.assets_from_symbol(symbol)
            if asset is not None and ref_asset is not None:
                trading_pairs.append(TradingPair(symbol, asset, ref_asset, source=self.name))
        return trading_pairs


    def _get_klines_online(self, asset: str, ref_asset: str, timeframe: TIMEFRAME,
                           start_time: int, end_time: int) -> List[Kline]:
        """
        Fetch klines online by asking the Bitfinex API

        :param asset: asset of the trading pair
        :type asset: str
        :param ref_asset: reference asset of the trading pair
        :type ref_asset: str
        :param timeframe: timeframe for the kline
        :type timeframe: TIMEFRAME
        :param start_time: fetch only klines with an open time greater or equal than start_time
        :type start_time: Optional[int]
        :param end_time: fetch only klines with an open time lower than end_time
        :type end_time: Optional[int]
        :return: list of klines
        :rtype: List[Kline]
        """
        try:
            pair_name = self.assets_to_pair[asset][ref_asset].name
        except KeyError:  # unsupported pair
            return []
        interval_trad = self.kline_translation[timeframe]

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.client.rest.get_public_candles('t' + pair_name, 1000 * start_time,
                                                                               1000 * end_time, section='hist',
                                                                               tf=interval_trad, limit='10000',
                                                                               sort=1))
        loop.close()
        if isinstance(response, dict):
            try:
                if response["error"] == "ERR_RATE_LIMIT":
                    retry_after = 1 + 60 - datetime.datetime.now().timestamp() % 60  # time until next minute
                    raise RateAPIException(retry_after)
            except KeyError:
                pass
            raise Exception(response)

        klines = []
        for row in response:
            open_timestamp = int(row[0] / 1000)
            open = float(row[1])
            close = float(row[2])
            high = float(row[3])
            low = float(row[4])

            klines.append(Kline(open_timestamp, open, high, low, close,
                                asset, ref_asset, timeframe, source=self.name))

        return klines
