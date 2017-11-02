#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------

PROJECT=wav2time

#------------------------------------------------------------------------------
# tools
#------------------------------------------------------------------------------

PYTHON=/bin/python35/python

#------------------------------------------------------------------------------
# private targets
#------------------------------------------------------------------------------

.PHONY: .FORCE

.FORCE:

#------------------------------------------------------------------------------
# public targets
#------------------------------------------------------------------------------

default: clean initialize wav2time edit time2csv finalize

initialize:

wav2time:
	python wav2time.py data/efekty-11_24_1033.wav
	python wav2time.py data/efekty-10_30_1438.wav

edit:
	pax -rws'/in/out/' data/etykiety-in-11_24_1033.txt .

time2csv:
	python time2csv.py data/etykiety-out-11_24_1033.txt

finalize:

clean:
	# -rm -f data/etykiety-*.txt 2> /dev/null
	# -rm -f data/etykiety-*.csv 2> /dev/null
	-rm -f data/*norm.wav 2> /dev/null
