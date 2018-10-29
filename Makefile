#/usr/bin/sh
#
DATA_DIR :=samples/
OUTPUT :=tests/output
SCRIPT :=scripts
VERSION=0.4
DOC="."
#directory to store data genered by extrernal stemmers
EXTRN_DATA_DIR=samples
#DataSets
DATA_GOLD=gold.csv
DATA_QC=qc.unq
DATA_QI=quran_word_v0.5.2.csv
DATA_NAFIS=nafis.unq
DATA_WORDS=words.csv
DATA_QWC=qwc.csv
DATA_KB=kabi.csv
# default data sets
DATA=${DATA_QI}
#External stemmers directories
KHOJA_DIR=other_stemmers/khoja-stemmer-command-line
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
farasa_all:farasa_quran_index  farasa_gold farasa_quranic_corpus
farasa_quranic_corpus farasa_qc: DATA=${DATA_QC}
farasa_gold: DATA=${DATA_GOLD}
farasa_nafis: DATA=${DATA_NAFIS}
farasa_quran_index farasa_qi:DATA=${DATA_QI}
farasa_words:DATA=${DATA_WORDS}
farasa_qwc:DATA=${DATA_QWC}
farasa_kb:DATA=${DATA_KB}

farasa farasa_words farasa_quran_index farasa_qi farasa_gold farasa_quranic_corpus farasa_qc farasa_nafis farasa_qwc farasa_kb: 
	#Generate stemmed data by Farasa stemmer
	# extract only words columns
	cut -f1 samples/${DATA}  > /tmp/test-in.txt
	# run stemmer

	cd ${FARASA_DIR};export FarasaDataDir=${PWD}/other_stemmers/FarasaSegmenter/FarasaData/;java -jar dist/Farasa.jar -i /tmp/test-in.txt -o /tmp/test-out.txt
	# strip spaces from test-out
	sed -i 's/ //g' /tmp/test-out.txt
	# join two files #copy file into samples
	paste /tmp/test-in.txt /tmp/test-out.txt > ${EXTRN_DATA_DIR}/${DATA}.farasa

khoja_all: khoja_quran_index  khoja_gold khoja_quranic_corpus
khoja_quranic_corpus khoja_qc: DATA=${DATA_QC}
khoja_gold: DATA=${DATA_GOLD}
khoja_nafis: DATA=${DATA_NAFIS}
khoja_quran_index khoja_qi:DATA=${DATA_QI}
khoja_words:DATA=${DATA_WORDS}
khoja_qwc:DATA=${DATA_QWC}
khoja_kb:DATA=${DATA_KB}

khoja khoja_words khoja_quran_index  khoja_gold khoja_quranic_corpus khoja_qc khoja_qi khoja_nafis khoja_qwc khoja_kb:
	#Generate stemmed data by khoja stemmer
	# extract only words columns
	cut -f1 samples/${DATA}  > /tmp/test-in.txt
	# run stemmer
	cd ${KHOJA_DIR};java -jar khoja-stemmer-command-line.jar /tmp/test-in.txt /tmp/test-out.txt
	# strip spaces from test-out
	sed -i 's/ //g' /tmp/test-out.txt
	# join two files #copy file into samples
	paste /tmp/test-in.txt /tmp/test-out.txt > ${EXTRN_DATA_DIR}/${DATA}.khoja
	

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
# test all datasets with all stemmers
#~ test_all_data: OPTIONS=--all
test_all_data:test_all
test_all: test words test_some gold quranic_corpus qc quran_index qi nafis qwc kb

# test some stemmers
test_some:OPTIONS=


test words test_some gold quranic_corpus qc quran_index qi nafis qwc kb:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts/test_stemmers_rooters.py -f samples/${DATA} -o output/${DATA} --dir ${EXTRN_DATA_DIR} ${OPTIONS}

# evaluation when processing is done, and we wan't to process again
eval_quranic_corpus eval_qc: DATA=${DATA_QC}
eval_gold: DATA=${DATA_GOLD}
eval_nafis: DATA=${DATA_NAFIS}
eval_quran_index eval_qi:DATA=${DATA_QI}
eval_qwc:DATA=${DATA_QWC}
eval_kb:DATA=${DATA_KB}

# eval all stemmers
eval_all:OPTIONS=--all
eval_all:eval_qc eval_gold  eval_qi eval_nafis eval_qwc eval_kb
eval eval_quranic_corpus eval_qc eval_gold eval_quran_index eval_qi eval_nafis eval_qwc eval_kb:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts/eval_stemming_result.py -f output/${DATA} -o output/${DATA}.stats ${OPTIONS}

# Show datasets stats
show_data: show_qc show_qi show_nafis show_gold
show_qc: DATA=${DATA_QC}
show_gold: DATA=${DATA_GOLD}
show_nafis: DATA=${DATA_NAFIS}
show_qi:DATA=${DATA_QI}
show_qwc:DATA=${DATA_QWC}
show_kb:DATA=${DATA_KB}
show_qc show_gold show_qi show_nafis show_qwc show_kb:
	# test stemmers with quran index dataset
	# run stemmer
	python scripts/show_datasets_stats.py -f samples/${DATA} -o output/${DATA}.sets


visualize:
	echo " generate latex and charts "
	python scripts/visualize_tests_stats.py -f output/qc.unq.stats -o output/visualize.tex

# debug rooter
debug_qwc:
	python scripts/test_rooters_debug.py -f samples/qwc.csv -o output/qwc.debug.csv > output/qwc.debug
debug:
	python scripts/test_rooters_debug.py -f samples/words_debug.csv -o output/word_debug.csv > output/words.debug
debug_qwc_win:
	python scripts\test_rooters_debug.py -f samples\qwc.csv -o output\qwc.debug.csv > output\qwc.debug
debug_win:
	python scripts\test_rooters_debug.py -f samples\words_debug.csv -o output\word_debug.csv > output\words.debug
