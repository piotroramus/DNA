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


#SAM to BAM conversion
echo "Starting SAM to BAM conversion"

$JAVA -Xmx4g -Djava.io.tmpdir=/tmp \
-jar $PICARD_SORTSAM_JAR \
SO=coordinate \
INPUT=input.sam \
OUTPUT=output.bam \
VALIDATION_STRINGENCY=LENIENT \
CREATE_INDEX=true

echo "SAM to BAM conversion Completed"