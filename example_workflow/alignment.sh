#!/bin/bash

#Load config
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
properties=$CURRENT_DIR/config.properties
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



#filter SNPs
echo "Starting filtering SNPs"

$JAVA -Xmx4g -jar $GENOME_ANALYSIS_TK_JAR \
-R hg19.fa \
-T VariantFiltration \
-B:variant,VCF snp.vcf.recalibrated \
-o snp.recalibrated.filtered.vcf \
--clusterWindowSize 10 \
--filterExpression "MQ0 >= 4 && ((MQ0 / (1.0 * DP)) > 0.1)" \
--filterName "HARD_TO_VALIDATE" \
--filterExpression "DP < 5 " \
--filterName "LowCoverage" \
--filterExpression "QUAL < 30.0 " \
--filterName "VeryLowQual" \
--filterExpression "QUAL > 30.0 && QUAL < 50.0 " \
--filterName "LowQual" \
--filterExpression "QD < 1.5 " \
--filterName "LowQD" \
--filterExpression "SB > -10.0 " \
--filterName "StrandBias"

echo "Filtering SNPs completed"



#Conversion to annovar file format
echo "Starting Conversion to annovar file format"

$CONVERT_2_ANNOVAR --format vcf4 --includeinfo snp.recalibrated.filtered.vcf > snp.annovar
$SUMMARIZE_ANNOVAR --buildver hg19 snp.annovar ./humandb -outfile snps

echo "Conversion to annovar file format completed"