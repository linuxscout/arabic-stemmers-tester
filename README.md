## Test Stemmers

#Dataset :
nafis
gold
qi quranic_corpus
qc quran_index
qcw quran corpus words
kb kabi

## Config file
a config file in scripts directory to help to choose stemmers to tests.
### Run Test on data set
for individual data set
```
make gold
```
* change to qi, qc or nafis
* results are stored in output/${dataset}.csv
* statistics are stored in output/${dataset}.csv.stats

Run a stemmer on dataset
```
make khoja_nafis
```

Run a stemmer on all dataset
```
make khoja_all
make moataz_all
make assem_all
make farasa_all
```
results are stored on output/processed


for Tashaphyne stemmers on all datasets

```
make test_all
```
### Merge all files

To merge all result files into joined files 
```
make join_all
```
The merged files are stored on output/joined

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
Statistics are stored on output/stats

## Visualize statitics into Latex and Excel

We can visualize and convert results into Excels and Latex
```
make visualize
```
Global Stats are stored in output/visuale directory:
it contains:
* a tex file
* charts images
* pivots tables of evaluation

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
