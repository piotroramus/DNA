#!/usr/bin/env bash

#Load config
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
properties=$CURRENT_DIR/../config.properties
if [ -f $properties ]; then

   . $properties

else
   echo "ERROR: $properties not found"
   echo "Exit -1"
   exit -1
fi


#Actual Alignment
echo "Starting Actual Alignment"

#$BWA aln -t 4 -f input.sai -I hg19 input.fastq
#without -I flag
$BWA aln -t 4 -f input.sai hg19 input.fastq
$BWA samse -f out.sam -r "@RG\tID:<ID>\tLB:<LIBRARY_NAME>\tSM:<SAMPLE_NAME>\tPL:ILLUMINA" hg19 input.sai input.fq
$BWA sampe -f out.sam -r "@RQ\tID:<ID>\tLB:<LIBRARY_NAME>\tSM:<SAMPLE_NAME>\tPL:ILLUMINA" hg19 input1.sai input2.sai input1.fq input2.fq

echo "Actual Alignment Completed"