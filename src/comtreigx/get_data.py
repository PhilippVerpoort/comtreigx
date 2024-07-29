from itertools import islice
from pathlib import Path
from typing import Optional
from warnings import warn
from datetime import datetime

import pandas as pd
from comtradeapicall import getTarifflineData

from comtreigx.hs_codes import hs_codes_map


def api_call(commodity: str, period_codes: list[str], hs_codes: list[str],
             subscription_key: str, quiet: bool, freq: str) -> pd.DataFrame:
    # batch_size = 20
    # loop over period and hs codes
    ret_list = []
    periods = ','.join(
        [f"{period}{month+1:02d}" for period in period_codes for month in range(12)]
        if freq == 'M' else
        period_codes
    )
    for hs_code in hs_codes:
        if not quiet:
            print(f"Getting HS Code {hs_code} for periods {periods} ... ", end='')
        flow_codes = 'M,FM,MIP,RM,MOP'
        df = getTarifflineData(
            subscription_key, typeCode='C', freqCode=freq, clCode='HS', period=periods, reporterCode='',
            cmdCode=hs_code, flowCode=flow_codes, partnerCode='', partner2Code=None, customsCode=None,
            motCode=None, maxRecords=250000, format_output='JSON', countOnly=None, includeDesc=True,
        )
        if df is None:
            raise Exception('Something went wrong. Exiting.')
        if len(df) >= 250000:
            warn(f"Data may be incomplete, maximum number of records has been reached. HS Code: {hs_code}")
        df.insert(0, 'commodity', commodity)
        ret_list.append(df)
        if not quiet:
            print('Done!' + (' (empty)' if df.empty else ''))

    return pd.concat(ret_list)


def clean_arguments(period_codes: Optional[int | float | str | list[int | float | str] | tuple[int | float | str]],
                    commodities: Optional[str | list[str] | tuple[str]],
                    ) -> (list[str], list[str]):
    # convert ints and floats to strs and convert singular values to lists
    period_codes = (
        [str(period) for period in range(1980, datetime.now().year, 1)] if period_codes is None else
        [str(int(period)) for period in period_codes] if isinstance(period_codes, list | tuple) else
        [str(int(period_codes))]
    )

    # convert
    commodities = (
        hs_codes_map.index.to_list() if commodities is None else
        commodities if isinstance(commodities, list | tuple) else
        [commodities]
    )

    # return
    return period_codes, commodities


def cache_data(cache_dir: Path,
               period_codes: int | float | str | list[int | float | str] | tuple[int | float | str],
               commodities: Optional[str | list[str] | tuple[str]] = None,
               subscription_key: Optional[str] = None,
               freq: str = 'A',
               quiet: bool = False,
               ) -> None:
    # check that the output directory exists and is a directory
    if not (cache_dir.exists() and cache_dir.is_dir()):
        raise Exception('Cache directory does not exist.')

    # raise warning if no subscription key provided
    if not subscription_key:
        warn('API calls should be done with a valid subscription key, but none provided. The request will likely fail.')

    # clean arguments
    period_codes, commodities = clean_arguments(period_codes, commodities)

    # loop over commodities
    for commodity, hs_codes in hs_codes_map.loc[commodities].items():
        # get data
        loaded_data = api_call(
            commodity=commodity,
            period_codes=period_codes,
            hs_codes=hs_codes,
            subscription_key=subscription_key,
            quiet=quiet,
            freq=freq,
        )

        # loop over grouped data
        if not quiet:
            print('Saving to files ...', end='')
        for period, rows in loaded_data.groupby('period'):
            cache_file = cache_dir / f"{commodity}_{period}{freq}.csv"
            rows.to_csv(cache_file, index=False, sep=',', quotechar='"', encoding='utf-8')
        if not quiet:
            print('Done!')


def load_data(period_codes: int | float | str | list[int | float | str] | tuple[int | float | str],
              commodities: Optional[str | list[str] | tuple[str]] = None,
              cache_dir: Optional[str | Path] = None,
              subscription_key: Optional[str] = None,
              freq: str = 'A',
              ) -> pd.DataFrame:
    # check that either cache directory or subscription key are provided
    if not cache_dir and not subscription_key:
        raise Exception('Must provide either a cache directory or subscription key.')

    # check that the output directory exists and is a directory
    if isinstance(cache_dir, str):
        cache_dir = Path(cache_dir)
    if cache_dir and not (cache_dir.exists() and cache_dir.is_dir()):
        raise Exception(f"Cache directory does not exist: {cache_dir.absolute()}")

    # clean arguments
    period_codes, commodities = clean_arguments(period_codes, commodities)

    # loop over period and hs codes
    ret_list = []
    for period in period_codes:
        for commodity in commodities:
            if cache_dir is not None:
                cache_file = cache_dir / f"{commodity}_{period}{freq}.csv"
                if cache_file.exists() and cache_file.is_file():
                    cached_data = pd.read_csv(cache_file, sep=',', quotechar='"', encoding='utf-8')
                    ret_list.append(cached_data)
            if subscription_key and not (cache_dir and cache_file.exists() and cache_file.is_file()):
                hs_codes = hs_codes_map.at[commodity]
                loaded_data = api_call(
                    commodity=commodity,
                    period_codes=[period],
                    hs_codes=hs_codes,
                    subscription_key=subscription_key,
                    quiet=True,
                    freq=freq,
                )
                ret_list.append(loaded_data)

    # return
    return pd.concat(ret_list) if ret_list else pd.DataFrame()
