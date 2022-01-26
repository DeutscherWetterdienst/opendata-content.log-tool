# content.log Tool

A reference implementation for processing the content.log files found at opendata.dwd.de/weather.

Example usage:

```
wget https://opendata.dwd.de/weather/nwp/content.log.bz2
bunzip2 content.log.bz2
echo "./icon-d2/grib/*/t_2m/*" > wildcards.txt
./get_updated_files.py -w wildcards.txt 2022-01-26T03:00 > updated_files.txt
```

The produced file `updated_files.txt` will hold all pathnames as given by content.log that are updated since
`2022-01-26 03:00:00 UTC` according to the file's modification date. Remember that those paths are relative to the
directory the `content.log.bz2` was in, in this case https://opendata.dwd.de/weather/nwp/.

Also mind that there are multiple servers behind https://opendata.dwd.de which might not be exactly in sync with each
other regarding file modification timestamps. Look into the code of `get_updated_files.py` for a suggestion on how to
deal with that.

While this program relies on the file modification timestamp dumped into `content.log.bz2`, it might be more feasible
to process the data reference time that is contained in the filenames instead.

```
$ ./get_updated_files.py --help
usage: get_updated_files.py [-h] [--content-log CONTENT_LOG_FILE] [--wildcards WILDCARDS_FILE] [--min-delta MIN_DELTA] [--version] UPDATED_SINCE

Filters paths of a DWD Open Data content.log file for entries that have been updated.

positional arguments:
  UPDATED_SINCE         Last time files were checked for updates

optional arguments:
  -h, --help            show this help message and exit
  --content-log CONTENT_LOG_FILE, -f CONTENT_LOG_FILE
                        The decompressed content.log file (default: content.log)
  --wildcards WILDCARDS_FILE, -w WILDCARDS_FILE
                        Filter results by a set of wildcards
  --min-delta MIN_DELTA, -d MIN_DELTA
                        Minimum number of seconds a file needs to be younger than UPDATED_SINCE (default: 60)
  --version             show program's version number and exit
```