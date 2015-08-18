#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $DIR/setConfiguration.py -download $STORAGE/download -hg $SCRATCH/hg -apps $STORAGE/apps install
