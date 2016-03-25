
This script suites include 2 parts, fio scripts, pylog2xls scripts. 

First part, fio scripts is as follows. 

  fio_perf.py           - for performance test.
  fio_perf_latency.py   - for performance and latency test with 512, 
                          4k, 1m block sizes.
  fio_stress.py         - for stress test with verify options.

Second part, the following scripts can convert fio log from above 
scripts to Excel file.

  instMod.sh            - this script will install xlwt-0.7.2.tar.gz
                          package. pylog2xls will use this package.
  pylog2xls.py          - it will convert iops and bw from fio log.
  pylog2xls_latency.py  - this script will convert iops, bw, slat, 
                          clat, lat from fio log