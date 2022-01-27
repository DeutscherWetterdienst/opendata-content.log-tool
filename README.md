# content.log Tool

A reference implementation for processing the content.log files found at opendata.dwd.de/weather.

Example usage:

```
CONTENT_LOG_URL="https://opendata.dwd.de/weather/nwp/content.log.bz2"
PATTERN="/icon-d2/grib/03/t_2m/.*_icosahedral_"
LAST_RUN_AT=$(date -ud 00:00 -Ihours)

wget $CONTENT_LOG_URL -O content.log.bz2
bzgrep $PATTERN content.log.bz2 > my_content.log
./get_updated_files.py -b $CONTENT_LOG_URL -u $LAST_RUN_AT my_content.log > updated_files.txt
wget -i updated_files.txt
```

Running the program above will download all updated files into the current working directory. The produced file
`updated_files.txt` will hold hyperlinks to files that are updated since the given date-time according
to the file's modification date found in content.log.

Also mind that there are multiple servers behind https://opendata.dwd.de which might not be exactly in sync with each
other regarding file modification timestamps. Look into the code of `get_updated_files.py` for a suggestion on how to
deal with that.

While this program relies on the file modification timestamp dumped into `content.log.bz2`, it might be more feasible
to process the data reference time that is contained in the filenames instead.

```
$ ./get_updated_files.py --help
usage: get_updated_files.py [-h] --updated-since UPDATED_SINCE [--url-base URL_BASE]
                            [--min-delta MIN_DELTA] [--version]
                            [CONTENT_LOG_FILE [CONTENT_LOG_FILE ...]]

Filters paths of a DWD Open Data content.log file for entries that have been updated.

positional arguments:
  CONTENT_LOG_FILE      The decompressed content.log file (default: STDIN)

optional arguments:
  -h, --help            show this help message and exit
  --updated-since UPDATED_SINCE, -u UPDATED_SINCE
                        last time files were checked for updates
  --url-base URL_BASE, -b URL_BASE
                        resolve the paths taken from content.log relative to the given
                        base URL; put the URL of the content.log.bz2 here to end up with
                        correct hyperlinks to DWD's Open Data
  --min-delta MIN_DELTA, -d MIN_DELTA
                        minimum number of seconds a file needs to be younger than
                        UPDATED_SINCE (default: 60)
  --version             show program's version number and exit
```