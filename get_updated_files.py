#!/usr/bin/env python3

import argparse
import datetime
import fnmatch
from urllib.parse import urljoin

__VERSION__ = "1.1.0"

arg_parser = argparse.ArgumentParser(description="Filters paths of a DWD Open Data content.log file "
                                                 "for entries that have been updated.")
arg_parser.add_argument("updated_since", metavar="UPDATED_SINCE",
                        type=datetime.datetime.fromisoformat,
                        help="Last time files were checked for updates")
arg_parser.add_argument("--content-log", "-f", metavar="CONTENT_LOG_FILE", default="content.log",
                        type=argparse.FileType("r"),
                        help="The decompressed content.log file (default: content.log)")
arg_parser.add_argument("--url-base", "-b",
                        help="Resolve the paths taken from content.log relative to the given base URL; "
                             "put the URL of the content.log.bz2 here to end up with correct hyperlinks "
                             "to DWD's Open Data")
arg_parser.add_argument("--min-delta", "-d", default=60,
                        type=int,
                        help="Minimum number of seconds a file needs to be younger than UPDATED_SINCE "
                             "(default: 60)")
arg_parser.add_argument("--wildcards", "-w", metavar="WILDCARDS_FILE",
                        type=argparse.FileType("r"),
                        help=argparse.SUPPRESS)
arg_parser.add_argument('--version', action='version', version=f'%(prog)s {__VERSION__}')


def main():
    args = arg_parser.parse_args()
    wildcards = "".join(args.wildcards.readlines()).split() if args.wildcards is not None else []

    for line in args.content_log:
        # skip all lines that do not match any specified wildcard
        # wildcard = [] is falsy will skip the conditional block
        # this is a DEPRECATED feature and the option is hidden in --help
        # as a replacement, use grep in beforehand to reduce content.log to the relevant lines
        if wildcards and not any(fnmatch.fnmatch(line, wildcard) for wildcard in wildcards):
            continue
        # each line is of the scheme "path|size|changed_at"
        path, size, changed_at = line.strip().split("|")
        changed_at = datetime.datetime.fromisoformat(changed_at)
        # print paths of files that have been updated since UPDATED_SINCE
        # but require an extra MIN_DELTA seconds
        # because behind the scenes there are two separate servers answering to opendata.dwd.de
        # which might not be exactly in sync with each other
        if (changed_at - args.updated_since).total_seconds() > args.min_delta:
            if args.url_base:
                print(urljoin(args.url_base, path))
            else:
                print(path)


if __name__ == "__main__":
    main()
