#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $HOME/dev/dna/runWorkflow.py -download $STORAGE/download -hg $SCRATCH/hg -all

