## Test Stemmers

#Dataset :
nafis
gold
qi quranic_corpus
qc quran_index
### Run Test on data set
for individual data set
```
make gold
```
* change to qi, qc or nafis
* results are stored in output/${dataset}.csv
* statistics are stored in output/${dataset}.csv.stats


for all datasets

```
make test_all
```
### Collect tests statstics  after tests
 Whithout runing again the tests, you can collect stats
*** Individuals***
```
make eval_gold
```
change to eval_qi, eval_qc or eval_nafis

*** for all ***
```
make eval_all
```

## Visualize statitics into Latex and Excel

We can visualize and convert results into Excels and Latex
```
make visualize
```
Global Stats are stored in output/global.stats.csv


### Run Statistics on Datasets

Show datasets statitics
```
make show_gold
```
Change to qi, qc or nafis.
To show all stats
```
make show_all
```
