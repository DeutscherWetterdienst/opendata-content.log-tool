#!/usr/bin/env python3

import argparse
import datetime
import fnmatch

__VERSION__ = "1.0.0"

arg_parser = argparse.ArgumentParser(description="Filters paths of a DWD Open Data content.log file "
                                                 "for entries that have been updated.")
arg_parser.add_argument("updated_since", metavar="UPDATED_SINCE",
                        type=datetime.datetime.fromisoformat,
                        help="Last time files were checked for updates")
arg_parser.add_argument("--content-log", "-f", metavar="CONTENT_LOG_FILE", default="content.log",
                        type=argparse.FileType("r"),
                        help="The decompressed content.log file (default: content.log)")
arg_parser.add_argument("--wildcards", "-w", metavar="WILDCARDS_FILE",
                        type=argparse.FileType("r"),
                        help="Filter results by a set of wildcards")
arg_parser.add_argument("--min-delta", "-d", default=60,
                        type=int,
                        help="Minimum number of seconds a file needs to be younger than UPDATED_SINCE "
                             "(default: 60)")
arg_parser.add_argument('--version', action='version', version=f'%(prog)s {__VERSION__}')


def main():
    args = arg_parser.parse_args()
    wildcards = "".join(args.wildcards.readlines()).split() if args.wildcards is not None else ["*"]

    for line in args.content_log:
        # skip all lines that do not match any specified wildcard
        if not any(fnmatch.fnmatch(line, wildcard) for wildcard in wildcards):
            continue
        # each line is of the scheme "path|size|changed_at"
        path, size, changed_at = line.strip().split("|")
        changed_at = datetime.datetime.fromisoformat(changed_at)
        # print paths of files that have been updated since UPDATED_SINCE
        # but require an extra MIN_DELTA seconds
        # because behind the scenes there are two separate servers answering to opendata.dwd.de
        # which might not be exactly in sync with each other
        if (changed_at - args.updated_since).total_seconds() > args.min_delta:
            print(path)


if __name__ == "__main__":
    main()
