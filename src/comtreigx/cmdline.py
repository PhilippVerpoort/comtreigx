#!/usr/bin/env python
import argparse
from pathlib import Path

from comtreigx.get_data import cache_data


# main execution function
def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog='comtreigex',
        description='UN Comtrade Energy-intensive Goods Extraction (COMTREIGEX)',
        epilog='For further details, please consult the source code.',
    )
    subparsers = parser.add_subparsers(title='commands', dest='command', help='sub-command help')

    # create the parser for the "conv" command
    parser_conv = subparsers.add_parser('cache')
    parser_conv.add_argument('-q', '--quiet', action="store_true", default=False, help='Silence output when caching data.')
    parser_conv.add_argument('-p', '--periods', type=lambda s: s.split(','), default=None, help='List of periods to obtain.')
    parser_conv.add_argument('-c', '--commodities', default=None, help='List of commodities to obtain.')
    parser_conv.add_argument('-f', '--freq', default='A', help='Temporal frequency of data (A for annual or M for monthly).')
    parser_conv.add_argument('subscrkey', type=str, help='Subscription key for Comtrade API.')
    parser_conv.add_argument('cachedir', type=Path, help='Directory where files will be cached.')

    # parse arguments
    args = parser.parse_args()
    cmd = args.command

    # switch between different commands
    match cmd:
        case None:
            print('Please provide a commmand, e.g. "cache".')
        case 'cache':
            cache_data(
                cache_dir=args.cachedir,
                period_codes=args.periods,
                commodities=args.commodities,
                subscription_key=args.subscrkey,
                quiet=args.quiet,
                freq=args.freq,
            )
        case _:
            print(f"Unknown command: {cmd}")

    return


# __main__ routine
if __name__ == '__main__':
    main()
