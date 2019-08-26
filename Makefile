#/usr/bin/sh
#
DATA_DIR :=samples/
OUTPUT :=tests/output
SCRIPT :=scripts
VERSION=0.4
DOC="."
DATE=`echo date`
NORMOPT=
#directory to store data genered by extrernal stemmers
EXTRN_DATA_DIR=output/processed
#DataSets
DATA_GOLD=gold.csv
DATA_QC=qc.unq
#~ DATA_QI=quran_word_v0.5.2.csv
DATA_QI=klm.csv
DATA_NAFIS=nafis.unq
DATA_WORDS=words.csv
DATA_QWC=qwc.csv
#~ DATA_KB=kabi.csv
DATA_KB=kabi.v2.csv
DATA_QLB=qlbstem.unq.csv
# default data sets
DATA=${DATA_QI}
#External stemmers directories
KHOJA_DIR=other_stemmers/khoja-stemmer-command-line
MOATAZ_DIR=other_stemmers/moataz-arabic-light-stemmer/
FARASA_DIR=other_stemmers/FarasaSegmenter/FarasaSrc
# options for test_stemmers (all or only cited)
OPTIONS=--all
default: all
# Clean build files
all:

# Publish to github
publish:
	git push origin master 
	
# prepare corpus to be compatible with this script:
prepare_all: prepare_gold
prepare_gold:
	echo -e "word\troot\tlemma" >samples/gold.csv
	paste samples/golden_corpus/core/words.txt samples/golden_corpus/core/roots.txt samples/golden_corpus/core/stems.txt >> samples/gold.csv
farasa_all:farasa_words   farasa_gold  farasa_qc farasa_qi farasa_nafis farasa_qwc farasa_kb
farasa_quranic_corpus farasa_qc: DATA=${DATA_QC}
farasa_gold: DATA=${DATA_GOLD}
farasa_nafis: DATA=${DATA_NAFIS}
farasa_quran_index farasa_qi:DATA=${DATA_QI}
farasa_words:DATA=${DATA_WORDS}
farasa_qwc:DATA=${DATA_QWC}
farasa_kb:DATA=${DATA_KB}
farasa_qlb:DATA=${DATA_QLB}

farasa farasa_words farasa_quran_index farasa_qi farasa_gold farasa_quranic_corpus farasa_qc farasa_nafis farasa_qwc farasa_kb farasa_qlb: 
	#Generate stemmed data by Farasa stemmer
	# extract only words columns
	cut -f1 samples/${DATA}  > /tmp/test-in.txt
	# run stemmer

	cd ${FARASA_DIR};export FarasaDataDir=${PWD}/other_stemmers/FarasaSegmenter/FarasaData/;java -jar dist/Farasa.jar -i /tmp/test-in.txt -o /tmp/test-out.txt
	# strip spaces from test-out
	sed -i 's/ //g' /tmp/test-out.txt
	# rename result to take stemmer name
	sed 's/;ورد;/farasa/1' -i /tmp/test-out.txt
	# need a preprocess
	# the /tmp/test-out.2.txt contains two fields 'farasa' and 'farasa_stem'
	python scripts/process_farasa_stemmer.py -f /tmp/test-out.txt -o  /tmp/test-out.2.txt
	# join two files #copy file into samples
	paste /tmp/test-in.txt  /tmp/test-out.2.txt > ${EXTRN_DATA_DIR}/${DATA}.farasa

khoja_all: khoja_words   khoja_gold  khoja_qc khoja_qi khoja_nafis khoja_qwc khoja_kb
khoja_quranic_corpus khoja_qc: DATA=${DATA_QC}
khoja_gold: DATA=${DATA_GOLD}
khoja_nafis: DATA=${DATA_NAFIS}
khoja_quran_index khoja_qi:DATA=${DATA_QI}
khoja_words:DATA=${DATA_WORDS}
khoja_qwc:DATA=${DATA_QWC}
khoja_kb:DATA=${DATA_KB}
khoja_qlb:DATA=${DATA_QLB}

khoja khoja_words khoja_quran_index  khoja_gold khoja_quranic_corpus khoja_qc khoja_qi khoja_nafis khoja_qwc khoja_kb khoja_qlb:
	#Generate stemmed data by khoja stemmer
	# extract only words columns
	cut -f1 samples/${DATA}  > /tmp/test-in.txt
	# run stemmer
	cd ${KHOJA_DIR};java -jar khoja-stemmer-command-line.jar /tmp/test-in.txt /tmp/test-out.txt
	# strip spaces from test-out
	sed -i 's/ //g' /tmp/test-out.txt
	# rename result to take stemmer name
	sed 's/word/khoja_stem/1'  /tmp/test-out.txt > /tmp/test-out.2.txt
	sed 's/word/khoja/1' -i /tmp/test-out.txt
	# join two files #copy file into samples
	paste /tmp/test-in.txt /tmp/test-out.txt /tmp/test-out.2.txt > ${EXTRN_DATA_DIR}/${DATA}.khoja
	
moataz_all: moataz_words moataz_gold  moataz_qc moataz_qi moataz_nafis moataz_qwc moataz_kb
moataz_quranic_corpus moataz_qc: DATA=${DATA_QC}
moataz_gold: DATA=${DATA_GOLD}
moataz_nafis: DATA=${DATA_NAFIS}
moataz_quran_index moataz_qi:DATA=${DATA_QI}
moataz_words:DATA=${DATA_WORDS}
moataz_qwc:DATA=${DATA_QWC}
moataz_kb:DATA=${DATA_KB}
moataz_qlb:DATA=${DATA_QLB}

moataz moataz_words moataz_quran_index  moataz_gold moataz_quranic_corpus moataz_qc moataz_qi moataz_nafis moataz_qwc moataz_kb moataz_qlb:
	#Generate stemmed data by moataz stemmer
	# extract only words columns
	cut -f1 samples/${DATA}  > /tmp/test-in.txt
	# run stemmer
	cd ${MOATAZ_DIR};java -jar arabic-light-stemmer.jar /tmp/test-in.txt /tmp/test-out.txt
	# strip spaces from test-out
	sed -i 's/ //g' /tmp/test-out.txt
	# rename result to take stemmer name
	sed 's/word/moataz_stem/1'  /tmp/test-out.txt > /tmp/test-out.2.txt
	sed 's/word/moataz/1' -i /tmp/test-out.txt
	# join two files #copy file into samples
	paste /tmp/test-in.txt /tmp/test-out.txt /tmp/test-out.2.txt> ${EXTRN_DATA_DIR}/${DATA}.moataz
	
	


## Test Assem and Isri on all data 
assem_all: assem_words assem_gold  assem_qc assem_qi assem_nafis assem_qwc assem_kb
assem_quranic_corpus assem_qc: DATA=${DATA_QC}
assem_gold: DATA=${DATA_GOLD}
assem_nafis: DATA=${DATA_NAFIS}
assem_quran_index assem_qi:DATA=${DATA_QI}
assem_words:DATA=${DATA_WORDS}
assem_qwc:DATA=${DATA_QWC}
assem_kb:DATA=${DATA_KB}
assem_qlb:DATA=${DATA_QLB}

assem assem_words assem_quran_index  assem_gold assem_quranic_corpus assem_qc assem_qi assem_nafis assem_qwc assem_kb assem_qlb:
	python scripts/test_assem_isri_stemmer.py -f samples/${DATA} -o ${EXTRN_DATA_DIR}/${DATA}.assem 


# Datasets
dev:OPTIONS=
dev:qi

quranic_corpus qc: DATA=${DATA_QC}
gold: DATA=${DATA_GOLD}
nafis: DATA=${DATA_NAFIS}
quran_index qi:DATA=${DATA_QI}
words:DATA=${DATA_WORDS}
qwc:DATA=${DATA_QWC}
kb:DATA=${DATA_KB}
qlb:DATA=${DATA_QLB}
# test all datasets with all stemmers
#~ test_all_data: OPTIONS=--all
test_all_data:OPTIONS=
test_all_data:test_all
test_all:OPTIONS=--all
test_all: words gold qc qi nafis qwc kb qlb

# test some stemmers
# only mentioned stemmers 
test_some:OPTIONS=
test_some:test_all
words_some:OPTIONS=
words_some:words


test words test_some gold quranic_corpus qc quran_index qi nafis qwc kb qlb:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts/test_stemmers_rooters.py -f samples/${DATA} -o output/${DATA} 

# evaluation when processing is done, and we wan't to process again

eval_quranic_corpus eval_qc: DATA=${DATA_QC}
eval_gold: DATA=${DATA_GOLD}
eval_gold: NORMOPT=--normalize
eval_nafis: DATA=${DATA_NAFIS}
eval_quran_index eval_qi:DATA=${DATA_QI}
eval_qwc:DATA=${DATA_QWC}
eval_kb:DATA=${DATA_KB}
eval_qlb:DATA=${DATA_QLB}

# eval all stemmers
#~ eval_all:OPTIONS=--all
eval_some:OPTIONS=
eval_some:eval_all
eval_all:eval_qc eval_gold  eval_qi eval_nafis eval_qwc eval_kb eval_qlb
eval eval_quranic_corpus eval_qc eval_gold eval_quran_index eval_qi eval_nafis eval_qwc eval_kb eval_qlb:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts/eval_stemming_result.py -f output/joined/${DATA} ${NORMOPT} -o output/stats/${DATA}.stats ${OPTIONS}

# Show datasets stats
show_data: show_qc show_qi show_nafis show_gold show_kb show_qwc show_qlb
show_qc: DATA=${DATA_QC}
show_gold: DATA=${DATA_GOLD}
show_nafis: DATA=${DATA_NAFIS}
show_qi:DATA=${DATA_QI}
show_qwc:DATA=${DATA_QWC}
show_kb:DATA=${DATA_KB}
show_qlb:DATA=${DATA_QLB}
show_qc show_gold show_qi show_nafis show_qwc show_kb show_qlb:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts/show_datasets_stats.py -f samples/${DATA} -o output/datasets_stats/${DATA}.sets >> output/datasets_stats/global.sets

join_data:
	cat output/datasets_stats/*.stats |sort > output/datasets_stats/global.sets
	# remove brackets
	sed -i -r "s/(\[|\])//g"  output/datasets_stats/global.sets
	
visualize:
	echo " generate latex and charts "
	cd output/visuale/; tar cvfz  archives/arx-${shell date +'%Y-%m-%d.%H:%M'}.tar.gz \
	pivots  images visualize.* global.stats.csv
	python scripts/visualize_tests_stats.py -f output/stats/qc.unq.stats -o output/visuale/



# debug rooter
debug_qwc:
	python scripts/test_rooters_debug.py -f samples/qwc.csv -o output/qwc.debug.csv > output/qwc.debug
debug_klm:
#~ 	python scripts/test_rooters_debug.py -f samples/klm.1000.csv -o output/klm.debug.csv > output/klm.debug
	python scripts/test_rooters_debug.py -f samples/klm.csv -o output/klm.debug.csv > output/klm.debug
debug_nafis:
	python scripts/test_rooters_debug.py -f samples/nafis.unq -o output/nafis.debug.csv > output/nafis.debug
debug_gold:
	python scripts/test_rooters_debug.py -f samples/gold.csv -o output/gold.debug.csv > output/gold.debug
debug_abdo:
	python scripts/test_rooters_debug.py -f samples/abdnormal.csv -o output/abdo.debug.csv > output/abdo.debug
debug:
	python scripts/test_rooters_debug.py -f samples/words_debug.csv -o output/word_debug.csv > output/words.debug
show_result:
	python scripts/test_show_result.py -f output/words.csv -o output/word.reduced.csv

matrix:
	python scripts/test_root_matrix.py -f samples/words_debug.csv -o output/word_debug.csv > output/words.matrix 
matrix_qwc:
	python scripts/test_root_matrix.py -f samples/qwc.csv -o output/qwc_debug.csv > output/qwc.matrix 
qalsadi:
	python scripts/test_analex.py > output/text.txt


test_some_win:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts\test_stemmers_rooters.py -f samples\gold.csv -o output\gold.csv --dir samples
	python scripts\test_stemmers_rooters.py -f samples\qc.unq -o output\qc.unq --dir samples
	python scripts\test_stemmers_rooters.py -f samples\qi.csv -o output\qi.csv --dir samples
	python scripts\test_stemmers_rooters.py -f samples\nafis.unq -o output\nafis.unq --dir samples
	python scripts\test_stemmers_rooters.py -f samples\words.csv -o output\words.csv --dir samples
	python scripts\test_stemmers_rooters.py -f samples\qwc.csv -o output\qwc.csv --dir samples
	python scripts\test_stemmers_rooters.py -f samples\kabi.csv -o output\kabi.csv --dir samples

eval_some_win:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts\eval_stemming_result.py -f output\gold.csv -o output\gold.csv.stats 
	python scripts\eval_stemming_result.py -f output\qc.unq -o output\qc.unq.stats
	python scripts\eval_stemming_result.py -f output\qi.csv -o output\qi.csv.stats
	python scripts\eval_stemming_result.py -f output\nafis.unq -o output\nafis.unq.stats
	python scripts\eval_stemming_result.py -f output\words.csv -o output\words.csv.stats
	python scripts\eval_stemming_result.py -f output\qwc.csv -o output\qwc.csv.stats
	python scripts\eval_stemming_result.py -f output\kabi.csv -o output\kabi.csv.stats

zip:
	tar cvfz releases/rooter.${shell date +'%Y-%m-%d'}.tar.gz  rooter/   scripts/ samples/ output/joined output/processed output/stats output/test_stats output/visuale/images/ output/visuale/pivots/ README.md  Makefile test_win.bat


join_all: join_words join_gold  join_qc join_qi join_nafis join_qwc join_kb join_qlb
join_qc: DATA=${DATA_QC}
join_gold: DATA=${DATA_GOLD}
join_nafis: DATA=${DATA_NAFIS}
join_qi:DATA=${DATA_QI}
join_words:DATA=${DATA_WORDS}
join_qwc:DATA=${DATA_QWC}
join_kb:DATA=${DATA_KB}
join_qlb:DATA=${DATA_QLB}

join join_words   join_gold  join_qc join_qi join_nafis join_qwc join_kb join_qlb:
	# get the second column as stemm result
	# change the heaer to mention the stemmer
	# first out put of our stemmers(tashaphyne)
	# assem and isri
	cut -f7-14 ${EXTRN_DATA_DIR}/${DATA}.assem  > /tmp/test-out.assem.txt
	# moataz
	cut -f2,3 ${EXTRN_DATA_DIR}/${DATA}.moataz  > /tmp/test-out.moataz.txt
	# khoja
	cut -f2,3 ${EXTRN_DATA_DIR}/${DATA}.khoja  > /tmp/test-out.khoja.txt
	# farasa
	cut -f3,4 ${EXTRN_DATA_DIR}/${DATA}.farasa  > /tmp/test-out.farasa.txt
	# join
	paste output/${DATA} /tmp/test-out.assem.txt /tmp/test-out.moataz.txt 	/tmp/test-out.khoja.txt  /tmp/test-out.farasa.txt > output/joined/${DATA}
help:
	# To process external stemmers do
	# step 1
	# make khaja_all
	# make farasa_all
	# make moataz_all
	# make assem_all ( for assem and isri
	## Step 2
	# run out stemmers Tashaphyne
	# make test_all
	## Step 3
	# make join_all
	## step 4
	# make eval_all
	##step 5
	# make visualize
	echo "help"
	
basic:
	python scripts/basicrooter.py -f samples/klm.csv -o output/klm.basic.csv > output/klm.basic.out.csv 
