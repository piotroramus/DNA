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


#Quality score recalibration
echo "Starting Quality score recalibration"

$JAVA -Xmx4g -jar $GENOME_ANALYSIS_TK_JAR \
-l INFO \
-R hg19.fa \
--DBSNP dbsnp132.txt \
-I input.marked.realigned.fixed.bam \
-T CountCovariates \
-cov ReadGroupCovariate \
-cov QualityScoreCovariate \
-cov CycleCovariate \
-cov DinucCovariate \
-recalFile input.recal_data.csv

$JAVA -Xmx4g -jar $GENOME_ANALYSIS_TK_JAR \
-l INFO \
-R hg19.fa \
-I input.marked.realigned.fixed.bam \
-T TableRecalibration \
--out input.marked.realigned.fixed.recal.bam \
-recalFile input.recal_data.csv

echo "Quality score recalibration completed"
