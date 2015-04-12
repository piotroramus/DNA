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


#Produce raw SNP calls
echo "Starting Producing raw SNP calls"

$JAVA -Xmx4g -jar $GENOME_ANALYSIS_TK_JAR \
-glm BOTH \
-R hg19.fa \
-T UnifiedGenotyper \
-I input.marked.realigned.fixed.recal.bam \
-D dbsnp132.txt \
-o snps.vcf \
-metrics snps.metrics \
-stand_call_conf 50.0 \
-stand_emit_conf 10.0 \
-dcov 1000 \
-A DepthOfCoverage \
-A AlleleBalance \
-L target_intervals.bed

echo "Producing raw SNP calls completed"