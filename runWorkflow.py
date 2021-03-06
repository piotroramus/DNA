import argparse

from config.config import blue, joiner, run_command, ok, cwd, run_commands
from config.tools import ngs_tools_dict
from config.setConfiguration import download_file


def actual_alignment(args):
    blue('Going for STAGE_1 - actual_alignment')
    with cwd(joiner(args.hg, 'chromFa')):
        cmds = [
            'module add ' + ngs_tools_dict['bwa'] + ' && bwa aln -t 4 -f input.sai hg19 input.fastq',
            'module add ' + ngs_tools_dict['bwa'] + ' && bwa samse -f out.sam -r "@RG\tID:bwa\tLB:Exome1Lib\tSM:Exome1Sampl\tPL:ILLUMINA" hg19 input.sai input.fastq',
        ]
        run_commands(cmds, Exception)
    ok('done')


def SAM_to_BAM_conversion(args):
    blue('Going for STAGE_2 - SAM_to_BAM_conversion')
    with cwd(joiner(args.hg, 'chromFa')):
        cmd = 'module add ' + ngs_tools_dict['Picard'] + ' && $PICARDRUN SortSam SO=coordinate INPUT=out.sam OUTPUT=output.bam VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=true'
        run_command(cmd, Exception)
    ok('done')


def marking_PCR_duplicates(args):
    blue('Going for STAGE_3 - marking_PCR_duplicates')
    with cwd(joiner(args.hg, 'chromFa')):
        cmd = 'module add ' + ngs_tools_dict['Picard'] + ' && $PICARDRUN MarkDuplicates INPUT=output.bam OUTPUT=output.marked.bam METRICS_FILE=metrics CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT'
        run_command(cmd, Exception)
    ok('done')


def local_realignment(args):
    blue('Going for STAGE_4 - local_realignment')
    with cwd(joiner(args.hg, 'chromFa')):
        cmds = [
            'module add ' + ngs_tools_dict['GATK'] + ' && $GATK_RUN -T RealignerTargetCreator -R hg19.fa -o input.bam.list -I output.marked.bam',
            'module add ' + ngs_tools_dict['GATK'] + ' && $GATK_RUN -I output.marked.bam -R hg19.fa -T IndelRealigner -targetIntervals input.bam.list -o input.marked.realigned.bam',
            'module add ' + ngs_tools_dict['Picard'] + ' && $PICARDRUN FixMateInformation INPUT=input.marked.realigned.bam OUTPUT=input_bam.marked.realigned.fixed.bam SO=coordinate VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=true',
        ]
        run_commands(cmds, Exception)
    ok('Done!')


def quality_score_recalibration(args):
    blue('Going for STAGE_5 - quality_score_recalibration')
    with cwd(joiner(args.hg, 'chromFa')):
        cmds = [
            'module add ' + ngs_tools_dict['GATK'] + ' && $GATK_RUN -T BaseRecalibrator -R hg19.fa -I input_bam.marked.realigned.fixed.bam -L chr20 -knownSites dbsnp_138.hg19.vcf -o recal_data.table',
            'module add ' + ngs_tools_dict['GATK'] + ' && $GATK_RUN -T PrintReads -R hg19.fa -I input_bam.marked.realigned.fixed.bam -L chr20 -BQSR recal_data.table -o recal_reads.bam',
        ]
        run_commands(cmds, Exception)
    ok('Done!')


def run_haplotype_caller(args):
    blue('Going for STAGE_6 - run_haplotype_caller')
    with cwd(joiner(args.hg, 'chromFa')):
        cmd = 'module add ' + ngs_tools_dict['GATK'] + ' && $GATK_RUN -T HaplotypeCaller -R hg19.fa -I recal_reads.bam -L chr20 --genotyping_mode DISCOVERY -stand_call_conf 30 -stand_emit_conf 10 -o raw_variants.vcf'
        run_command(cmd, Exception)
    ok('Done!')


def main():
    """
    Main configuration method made to be called if user starts this script on his own
    """
    blue("Welcome to NGS configurator\n")
    parser = argparse.ArgumentParser(description=blue('NGS configurator'))
    parser.add_argument('-download', default=joiner('downloads'), help='path to download directory')
    parser.add_argument('-hg', default=joiner('hg19'), help='path to hg19 reference files directory')
    parser.add_argument('-1', dest='STAGE_1', action='store_true', help='set true if you want to run stage 1 - \"actual alignment\"')
    parser.add_argument('-2', dest='STAGE_2', action='store_true', help='set true if you want to run stage 2 - \"SAM to BAM conversion\"')
    parser.add_argument('-3', dest='STAGE_3', action='store_true', help='set true if you want to run stage 3 - \"marking_PCR_duplicates\"')
    parser.add_argument('-4', dest='STAGE_4', action='store_true', help='set true if you want to run stage 4 - \"local_realignment\"')
    parser.add_argument('-5', dest='STAGE_5', action='store_true', help='set true if you want to run stage 5 - \"quality score recalibration\"')
    parser.add_argument('-6', dest='STAGE_6', action='store_true', help='set true if you want to run stage 6 - \"produce raw SNP calls\"')
    parser.add_argument('-all', dest='ALL_STAGES', action='store_true', help='set true if you want to run all stages one by one.')
    parser.add_argument('--seq-read-url', dest='SEQ_READ_URL', help='url to your input file')
    args = parser.parse_args()

    if args.SEQ_READ_URL:
        if not download_file('input file', args.SEQ_READ_URL, joiner(args.hg, 'chromFa')):
            raise Exception('Something went wrong while downloading the input file')
        with cwd(joiner(args.hg, 'chromFa')):
            run_command('gunzip -f ' + args.SEQ_READ_URL.strip().split('/')[-1], Exception)
            run_command('mv ' + args.SEQ_READ_URL.strip().split('/')[-1].strip().split('.gz')[0] + ' input.fastq', Exception)

    if args.ALL_STAGES:
        blue('All stages to be processed.')
    if args.STAGE_1 or args.ALL_STAGES:
        actual_alignment(args)
    if args.STAGE_2 or args.ALL_STAGES:
        SAM_to_BAM_conversion(args)
    if args.STAGE_3 or args.ALL_STAGES:
        marking_PCR_duplicates(args)
    if args.STAGE_4 or args.ALL_STAGES:
        local_realignment(args)
    if args.STAGE_5 or args.ALL_STAGES:
        quality_score_recalibration(args)
    if args.STAGE_6 or args.ALL_STAGES:
        run_haplotype_caller(args)
    


if __name__ == '__main__':
    main()
