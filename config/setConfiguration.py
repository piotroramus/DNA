import argparse
import os
import urllib2
import subprocess
import shutil
from config import blue, warning, ok, fail, downloadURLs, cwd, joiner, run_command
from tools import ngs_tools_dict

def main():
    """
    Main configuration method made to be called in order to prepare reference files.
    """
    print blue("Welcome to NGS configurator\n")
    parser = argparse.ArgumentParser(description=blue('NGS configurator'))
    parser.add_argument('-download', default=joiner('downloads'), help='path to download directory')
    parser.add_argument('-hg', default=joiner('hg19'), help='path to hg19 reference files directory')
    args = parser.parse_args()
    prepare_input_files(args)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prepare_input_files(args=None):

    mkdir(args.download)
    mkdir(args.hg)
    if not exists(os.path.join(args.download, 'chromFa.tar.gz')):  
        if not download_file(args.hg, downloadURLs['hg19'], args.download):  
            raise Exception('Something went wrong while downloading the reference file')
    if not extract_file(joiner(args.download, 'chromFa.tar.gz'), joiner(args.hg, 'chromFa')):
        raise Exception('Something went wrong while extracting the reference file.')
    if not download_file('dbsnp_138.hg19.vcf.gz', downloadURLs['dbsnp'], joiner(args.hg, 'chromFa')):  
            raise Exception('Something went wrong while downloading the reference file')

    with cwd(joiner(args.hg, 'chromFa')):
        command = 'cat chrM.fa chr1.fa chr2.fa chr3.fa chr4.fa chr5.fa chr6.fa chr7.fa chr8.fa chr9.fa\
            chr10.fa chr11.fa chr12.fa chr13.fa chr14.fa chr15.fa chr16.fa chr17.fa chr18.fa\
            chr19.fa chr20.fa chr21.fa chr22.fa chrX.fa chrY.fa > hg19.fa'
        run_command(command, Exception)
        # command = 'wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/2.8/hg19/dbsnp_138.hg19.vcf.gz 2>/dev/null'
        # run_command(command, Exception)

        command = 'gunzip -f dbsnp_138.hg19.vcf.gz'
        run_command(command, Exception)
        command = 'module add ' + ngs_tools_dict['bwa'] + ' && bwa index -a bwtsw -p hg19 hg19.fa'
        run_command(command, Exception)
        command = 'module add ' + ngs_tools_dict['SamTools'] + ' && samtools faidx hg19.fa'
        run_command(command, Exception)
        command = 'module add ' + ngs_tools_dict['Picard'] + ' && $PICARDRUN CreateSequenceDictionary REFERENCE=hg19.fa OUTPUT=hg19.dict'
        run_command(command, Exception)
    ok('  ok\n')
    return True


def extract_file(path, destination, flags=''):
    print ' Extracting file: ' + path + ' into: ' + destination
    mkdir(destination)
    command = 'tar xf ' + path + ' -C ' + destination + ' ' + flags
    run_command(command, Exception)
    ok('  ok\n')
    return True


def exists(path):
    print ' Checking for existence of: ' + path
    if os.path.isfile(path):
        ok('Already here: \n    ' + path)
        return True
    warning('Not here!')
    return False


def download_file(name, url, destination):
    file_name = url.split('/')[-1]
    blue('\tDownloading: ' + file_name)
    command = 'wget ' + url + ' -O ' + os.path.join(destination, file_name)
    run_command(command, Exception, hide_stderr=True)
    return True


if __name__ == '__main__':
    main()
