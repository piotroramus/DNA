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


#Local realignment around indels
echo "Starting Local realignment around indels"

$JAVA -Xmx4g -jar $GENOME_ANALYSIS_TK_JAR \
-T RealignerTargetCreator \
-R hg19.fa \
-o input.bam.list \
-I input.marked.bam

$JAVA -Xmx4g -Djava.io.tmpdir=/tmp \
-jar $GENOME_ANALYSIS_TK_JAR \
-I input.marked.bam \
-R hg19.fa \
-T IndelRealigner \
-targetIntervals input.bam.list \
-o input.marked.realigned.bam

$JAVA -Djava.io.tmpdir=/tmp/flx-auswerter \
-jar $PICARD_FIXMATEINFORMATION_JAR \
INPUT=input.marked.realigned.bam \
OUTPUT=input_bam.marked.realigned.fixed.bam \
SO=coordinate \
VALIDATION_STRINGENCY=LENIENT \
CREATE_INDEX=true

echo "Local realignment around indels completed"