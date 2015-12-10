if [ $# -eq 1 ]; then
  DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
  OUTPUT_FILE=$1

  python $HOME/dev/dna/runWorkflow.py -download $STORAGE/download -hg $SCRATCH/hg -1 > $OUTPUT_FILE
else
	echo "Incorrect number of arguments passed $# expected 1"
fi
