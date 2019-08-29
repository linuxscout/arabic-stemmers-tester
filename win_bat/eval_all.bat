rem make[1]: Entering directory '\home\zerrouki\workspace\tests\stemming'
rem  test stemmers with quran index dataset
rem  run stemmer
python scripts\eval_stemming_result.py -f output\joined\qc.unq  -o output\stats\qc.unq.stats --all
rem  test stemmers with quran index dataset
rem  run stemmer
python scripts\eval_stemming_result.py -f output\joined\gold.csv --normalize -o output\stats\gold.csv.stats --all
rem  test stemmers with quran index dataset
rem  run stemmer
python scripts\eval_stemming_result.py -f output\joined\klm.csv  -o output\stats\klm.csv.stats --all
rem  test stemmers with quran index dataset
rem  run stemmer
python scripts\eval_stemming_result.py -f output\joined\nafis.unq  -o output\stats\nafis.unq.stats --all
rem  test stemmers with quran index dataset
rem  run stemmer
python scripts\eval_stemming_result.py -f output\joined\qwc.csv  -o output\stats\qwc.csv.stats --all
rem  test stemmers with quran index dataset
rem  run stemmer
python scripts\eval_stemming_result.py -f output\joined\kabi.v2.csv  -o output\stats\kabi.v2.csv.stats --all
rem  test stemmers with quran index dataset
rem  run stemmer
python scripts\eval_stemming_result.py -f output\joined\qlbstem.unq.csv  -o output\stats\qlbstem.unq.csv.stats --all
rem make[1]: Leaving directory '\home\zerrouki\workspace\tests\stemming'
