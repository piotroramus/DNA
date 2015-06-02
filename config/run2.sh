#!/usr/bin/env bash

python $HOME/dev/dna/config/setConfiguration.py -download $STORAGE/download -hg $SCRATCH/hg -apps $STORAGE/apps -bwa $STORAGE/apps/bwa/bwa prep_files
