if [ $# -eq 2 ]; then
  DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
  OUTPUT_FILE=$1
  SEQ_URL=$2

  python $HOME/DNA/runWorkflow.py -download $STORAGE/download -hg $SCRATCH/hg --seq-read-url $SEQ_URL -all > $OUTPUT_FILE
else
	echo "Incorrect number of arguments passed $# expected 2"
fi
