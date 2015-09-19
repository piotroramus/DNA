import argparse

from config.config import blue, joiner, run_command, ok, cwd


def actual_alignment(args):
    blue('Going for STAGE_1 - actual_alignment')
    with cwd(joiner(args.hg, 'chromFa')):
        cmd = args.bwa + ' aln -t 4 -f input.sai hg19 input.fastq'
        blue(cmd)
        run_command(cmd, Exception)
        cmd = args.bwa + ' samse -f out.sam -r "@RG\tID:bwa\tLB:Exome1Lib\tSM:Exome1Sampl\tPL:ILLUMINA" hg19 input.sai input.fastq'
        blue(cmd)
        run_command(cmd, Exception)
        # cmd = args.bwa + ' sampe -f out.sam -r "@RQ\tID:<ID>\tLB:<LIBRARY_NAME>\tSM:<SAMPLE_NAME>\tPL:ILLUMINA" hg19 input1.sai input2.sai input1.fq input2.fq'
    ok('done')


def SAM_to_BAM_conversion(args):
    blue('Going for STAGE_2 - SAM_to_BAM_conversion')
    with cwd(joiner(args.hg, 'chromFa')):
        cmd = args.java + ' -Xmx4g -Djava.io.tmpdir=/tmp -jar ' + args.PICARD + ' SortSam SO=coordinate INPUT=out.sam OUTPUT=output.bam VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=true'
        blue(cmd)
        run_command(cmd, Exception)
    ok('done')


def marking_PCR_duplicates(args):
    blue('Going for STAGE_3 - marking_PCR_duplicates')
    with cwd(joiner(args.hg, 'chromFa')):
        cmd = args.java + ' -Xmx4g -Djava.io.tmpdir=/tmp -jar ' + args.PICARD + ' MarkDuplicates INPUT=output.bam OUTPUT=output.marked.bam METRICS_FILE=metrics CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT'
        blue(cmd)
        run_command(cmd, Exception)
    ok('done')


def main():
    """
    Main configuration method made to be called if user starts this script on his own
    """
    blue("Welcome to NGS configurator\n")
    parser = argparse.ArgumentParser(description=blue('NGS configurator'))
    parser.add_argument('-download', default=joiner('downloads'), help='path to download directory')
    parser.add_argument('-hg', default=joiner('hg19'), help='path to hg19 reference files directory')
    parser.add_argument('-apps', default=joiner('apps'), help='path to applications directory')
    parser.add_argument('-bwa', default='bwa', help='path to bwa executable')
    parser.add_argument('-java', default='java', help='path to java executable')
    parser.add_argument('--java-home', dest='JAVA_HOME', default='/usr/lib', help='path to JAVA_HOME')
    parser.add_argument('-picard', dest='PICARD', default='picard', help='path to picard jar')
    parser.add_argument('-1', dest='STAGE_1', action='store_true', help='set true if you want to run stage 1 - \"actual alignment\"')
    parser.add_argument('-2', dest='STAGE_2', action='store_true', help='set true if you want to run stage 2 - \"SAM to BAM conversion\"')
    parser.add_argument('-3', dest='STAGE_3', action='store_true', help='set true if you want to run stage 3 - \"marking_PCR_duplicates\"')
    parser.add_argument('-all', dest='ALL_STAGES', action='store_true', help='set true if you want to run all stages one by one.')
    args = parser.parse_args()

    if args.ALL_STAGES:
        blue('All stages to be processed.')
    if args.STAGE_1 or args.ALL_STAGES:
        actual_alignment(args)
    if args.STAGE_2 or args.ALL_STAGES:
        SAM_to_BAM_conversion(args)
    if args.STAGE_3 or args.ALL_STAGES:
        marking_PCR_duplicates(args)

if __name__ == '__main__':
    main()
