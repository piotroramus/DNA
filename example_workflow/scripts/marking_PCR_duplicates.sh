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


#Marking PCR duplicates
echo "Starting Marking PCR duplicates"

$JAVA -Xmx4g -Djava.io.tmpdir=/tmp \
-jar $PICARD_MARKDUPLICATES_JAR \
INPUT=input.bam \
OUTPUT=input.marked.bam \
METRICS_FILE=metrics \
CREATE_INDEX=true \
VALIDATION_STRINGENCY=LENIENT

echo "Marking PCR duplicates completed"