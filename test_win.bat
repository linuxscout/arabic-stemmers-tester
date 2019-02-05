
::~ rem test_some_win:
::~ python scripts\test_stemmers_rooters.py -f samples\gold.csv -o output\processed\gold.csv --dir samples
::~ python scripts\test_stemmers_rooters.py -f samples\qc.unq -o output\processed\qc.unq --dir samples
::~ python scripts\test_stemmers_rooters.py -f samples\qi.csv -o output\processed\qi.csv --dir samples
::~ python scripts\test_stemmers_rooters.py -f samples\nafis.unq -o output\processed\nafis.unq --dir samples
::~ python scripts\test_stemmers_rooters.py -f samples\words.csv -o output\processed\words.csv --dir samples
::~ python scripts\test_stemmers_rooters.py -f samples\qwc.csv -o output\processed\qwc.csv --dir samples
::~ python scripts\test_stemmers_rooters.py -f samples\kabi.csv -o output\processed\kabi.csv --dir samples

::~ # test_assem
::~ python scripts\test_assem_isri_stemmer.py -f samples\gold.csv -o output\processed\gold.csv --dir samples
::~ python scripts\test_assem_isri_stemmer.py -f samples\qc.unq -o output\processed\qc.unq --dir samples
::~ python scripts\test_assem_isri_stemmer.py -f samples\qi.csv -o output\processed\qi.csv --dir samples
::~ python scripts\test_assem_isri_stemmer.py -f samples\nafis.unq -o output\processed\nafis.unq --dir samples
::~ python scripts\test_assem_isri_stemmer.py -f samples\words.csv -o output\processed\words.csv --dir samples
::~ python scripts\test_assem_isri_stemmer.py -f samples\qwc.csv -o output\processed\qwc.csv --dir samples
::~ python scripts\test_assem_isri_stemmer.py -f samples\kabi.csv -o output\processed\kabi.csv --dir samples


rem eval_some_win:
python scripts\eval_stemming_result.py -f output\joined\gold.csv -o output\stats\gold.csv.stats 
python scripts\eval_stemming_result.py -f output\\joined\qc.unq -o output\stats\qc.unq.stats
python scripts\eval_stemming_result.py -f output\joined\qi.csv -o output\stats\qi.csv.stats
python scripts\eval_stemming_result.py -f output\joined\nafis.unq -o output\stats\nafis.unq.stats
python scripts\eval_stemming_result.py -f output\joined\words.csv -o output\stats\words.csv.stats
python scripts\eval_stemming_result.py -f output\joined\qwc.csv -o output\stats\qwc.csv.stats
python scripts\eval_stemming_result.py -f output\joined\kabi.csv -o output\stats\kabi.csv.stats

make visualize 
