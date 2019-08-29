rem make[1]: Entering directory '\home\zerrouki\workspace\tests\stemming'
echo " generate latex and charts "
cd output\visuale\; tar cvfz  archives\arx-2019-08-29.23:33.tar.gz  pivots  images visualize.* global.stats.csv
python scripts\visualize_tests_stats.py -f output\stats\qc.unq.stats -o output\visuale\
rem make[1]: Leaving directory '\home\zerrouki\workspace\tests\stemming'
