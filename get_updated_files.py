#!/usr/bin/env python3

import argparse
import datetime
import sys
from urllib.parse import urljoin

__VERSION__ = "2.0.0"

arg_parser = argparse.ArgumentParser(description="Filters paths of a DWD Open Data content.log file "
                                                 "for entries that have been updated.")
arg_parser.add_argument("content_log_files",
                        nargs="*",
                        default=[sys.stdin], type=argparse.FileType("r"),
                        help="The decompressed content.log file (default: STDIN)",
                        metavar="CONTENT_LOG_FILE")
arg_parser.add_argument("--updated-since", "-u",
                        type=datetime.datetime.fromisoformat,
                        required=True,
                        help="last time files were checked for updates")
arg_parser.add_argument("--url-base", "-b",
                        help="resolve the paths taken from content.log relative to the given base URL; "
                             "put the URL of the content.log.bz2 here to end up with correct hyperlinks "
                             "to DWD's Open Data")
arg_parser.add_argument("--min-delta", "-d",
                        default=60, type=int,
                        help="minimum number of seconds a file needs to be younger than UPDATED_SINCE (default: 60)")
arg_parser.add_argument('--version', action='version', version=f'%(prog)s {__VERSION__}')


def main():
    args = arg_parser.parse_args()
    updated_since = args.updated_since.astimezone(datetime.timezone.utc)

    for content_log_file in args.content_log_files:
        for line in content_log_file:
            # each line is of the scheme "path|size|changed_at"
            path, size, changed_at = line.strip().split("|")
            changed_at = datetime.datetime.fromisoformat(f"{changed_at}+00:00")
            # print paths of files that have been updated since UPDATED_SINCE
            # but require an extra MIN_DELTA seconds
            # because behind the scenes there are two separate servers answering to opendata.dwd.de
            # which might not be exactly in sync with each other
            if (changed_at - updated_since).total_seconds() > args.min_delta:
                if args.url_base:
                    print(urljoin(args.url_base, path))
                else:
                    print(path)


if __name__ == "__main__":
    main()
