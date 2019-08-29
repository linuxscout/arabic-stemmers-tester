rem make[1]: Entering directory '\home\zerrouki\workspace\tests\stemming'
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\words.csv.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\words.csv.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\words.csv.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\words.csv.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\words.csv output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\words.csv
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\gold.csv.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\gold.csv.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\gold.csv.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\gold.csv.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\gold.csv output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\gold.csv
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\qc.unq.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\qc.unq.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\qc.unq.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\qc.unq.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\qc.unq output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\qc.unq
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\klm.csv.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\klm.csv.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\klm.csv.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\klm.csv.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\klm.csv output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\klm.csv
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\nafis.unq.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\nafis.unq.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\nafis.unq.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\nafis.unq.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\nafis.unq output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\nafis.unq
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\qwc.csv.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\qwc.csv.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\qwc.csv.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\qwc.csv.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\qwc.csv output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\qwc.csv
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\kabi.v2.csv.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\kabi.v2.csv.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\kabi.v2.csv.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\kabi.v2.csv.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\kabi.v2.csv output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\kabi.v2.csv
rem  get the second column as stemm result
rem  change the heaer to mention the stemmer
rem  first out put of our stemmers(tashaphyne)
rem  assem and isri
mkdir -p output\tmp
cut -f7-14 output\processed\qlbstem.unq.csv.assem  > output\tmp\test-out.assem.txt
rem  moataz
cut -f2,3 output\processed\qlbstem.unq.csv.moataz  > output\tmp\test-out.moataz.txt
rem  khoja
cut -f2,3 output\processed\qlbstem.unq.csv.khoja  > output\tmp\test-out.khoja.txt
rem  farasa
cut -f3,4 output\processed\qlbstem.unq.csv.farasa  > output\tmp\test-out.farasa.txt
rem  join
paste output\qlbstem.unq.csv output\tmp\test-out.assem.txt output\tmp\test-out.moataz.txt 	output\tmp\test-out.khoja.txt  output\tmp\test-out.farasa.txt > output\joined\qlbstem.unq.csv
rem make[1]: Leaving directory '\home\zerrouki\workspace\tests\stemming'
