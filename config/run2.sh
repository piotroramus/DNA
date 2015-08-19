#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $HOME/dev/dna/config/setConfiguration.py -download $STORAGE/download -hg $SCRATCH/hg -apps $STORAGE/apps -bwa $STORAGE/apps/bwa/bwa prep_files
