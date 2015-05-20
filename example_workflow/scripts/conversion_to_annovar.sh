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


#Conversion to annovar file format
echo "Starting Conversion to annovar file format"

$CONVERT_2_ANNOVAR --format vcf4 --includeinfo snp.recalibrated.filtered.vcf > snp.annovar
$SUMMARIZE_ANNOVAR --buildver hg19 snp.annovar ./humandb -outfile snps

echo "Conversion to annovar file format completed"