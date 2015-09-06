#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $HOME/dev/dna/runWorkflow.py -download $STORAGE/download -hg $SCRATCH/hg -apps $STORAGE/apps -bwa $STORAGE/apps/bwa/bwa -java $STORAGE/apps/java/bin/java -picard $STORAGE/apps/picard/dist/picard.jar -all

