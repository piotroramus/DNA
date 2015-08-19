import argparse

from config.config import blue, joiner, run_command, ok, cwd


def actual_alignment(args):
    blue('Going for STAGE_1 - actual_alignment')
    with cwd(joiner(args.hg, 'chromFa')):
        cmd = args.bwa + ' aln -t 4 -f input.sai hg19 input.fastq'
        blue(cmd)
        run_command(cmd, Exception)
        cmd = args.bwa + ' samse -f out.sam -r "@RG\tID:<ID>\tLB:<LIBRARY_NAME>\tSM:<SAMPLE_NAME>\tPL:ILLUMINA" hg19 input.sai input.fq'
        blue(cmd)
        run_command(cmd, Exception)
        cmd = args.bwa + ' sampe -f out.sam -r "@RQ\tID:<ID>\tLB:<LIBRARY_NAME>\tSM:<SAMPLE_NAME>\tPL:ILLUMINA" hg19 input1.sai input2.sai input1.fq input2.fq'
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
    parser.add_argument('-1', dest='STAGE_1', action='store_true', help='set true if you want to run stage 1 - \"actual alignment\"')
    parser.add_argument('-all', dest='ALL_STAGES', action='store_true', help='set true if you want to run all stages one by one.')
    args = parser.parse_args()

    if args.ALL_STAGES:
        blue('All stages to be processed.')
    if args.STAGE_1 or args.ALL_STAGES:
        actual_alignment(args)

if __name__ == '__main__':
    main()