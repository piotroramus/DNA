import argparse
import os
import urllib2
import subprocess
import shutil
from config import blue, warning, ok, fail, downloadURLs, cwd, joiner, run_command
from tools import ngs_tools

def main():
    """
    Main configuration method made to be called if user starts this script on his own
    """
    print blue("Welcome to NGS configurator\n")
    parser = argparse.ArgumentParser(description=blue('NGS configurator'))
    parser.add_argument('purpose', type=str, help='choose: prep_files | install | all')
    parser.add_argument('-download', default=joiner('downloads'), help='path to download directory')
    parser.add_argument('-hg', default=joiner('hg19'), help='path to hg19 reference files directory')
    parser.add_argument('-apps', default=joiner('apps'), help='path to applications directory')
    parser.add_argument('-bwa', default='bwa', help='path to bwa executable')
    # parser.add_argument('', type=str, help='choose: prep_files | install | all')
    args = parser.parse_args()
    configure.get(args.purpose, no_such_arg)(args=args)

def uninstall_tools(args=None):
    for tool in ngs_tools:
        blue('Uninstalling '+tool.name)
        unload_module(tool.module_path)

def install_tools(args=None):
    for tool in ngs_tools:
        blue('Installing '+tool.name)
        load_module(tool.module_path) 

    print "Running bwa"
    run_command('bwa', Exception)

def load_module(module):
    command = 'module load '+module
    blue(command)
    run_command(command, Exception)

def unload_module(module):
    command = 'set -e;module unload '+module
    blue(command)
    run_command(command, Exception)

def no_such_arg(args=None):
    fail('No such arg as: ' + args.purpose + ' \ntry: prep_files | install | all\n')


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prepare_input_files(args=None):
    def clean_downloads():
        pass

    mkdir(args.download)
    mkdir(args.hg)
    if not exists(os.path.join(args.download, 'chromFa.tar.gz')):  # sth wrong, not sure yet
        if not download_file(args.hg, downloadURLs['hg19'], args.download):  # TODO destination should be configurable
            return False
    if not extract_file(joiner(args.download, 'chromFa.tar.gz'), joiner(args.hg, 'chromFa')):
        return False

    with cwd(joiner(args.hg, 'chromFa')):
        command = 'cat chr1.fa chr2.fa chr3.fa chr4.fa chr5.fa chr6.fa chr7.fa chr8.fa chr9.fa\
            chr10.fa chr11.fa chr12.fa chr13.fa chr14.fa chr15.fa chr16.fa chr17.fa chr18.fa\
            chr19.fa chr20.fa chr21.fa chr22.fa chrX.fa chrY.fa chrM.fa > hg19.fa'
        blue('\t' + command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            fail('ERROR: \n' + err + '\n')
        ok('  ok\n')
        command = args.bwa + ' index -a bwtsw -p hg19 hg19.fa'
        blue('\t' + command)
        p = subprocess.Popen(command, shell=True)
        out, err = p.communicate()
        # print out
        # if err:
        #     warning('stderr: \n' + err + '\n')
    ok('  ok\n')
    return True


def extract_file(path, destination, flags=''):
    print ' Extracting file: ' + path + ' into: ' + destination
    mkdir(destination)
    command = 'tar xf ' + path + ' -C ' + destination + ' ' + flags
    blue('\t' + command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        fail('ERROR: \n' + err + '\n')
        return False
    ok('  ok\n')
    return True


def exists(path):
    print ' Checking for existence of: ' + path
    if os.path.isfile(path):
        ok('Already here: \n    ' + path)
        return True
    warning('Not here!')
    return False
    # return True


def full_configuration(args=None):
    if not install_tools(args):
        fail('nah')
    if not prepare_input_files(args):
        fail('nah')
    print ok('ok')

def install_lib1(path, install=True):
    print '  Configuring: ' + path
    command = './configure'
    blue('    ' + command)
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if (p.returncode == 0) and err:
        warning('WARNING: \n' + err + '\n')
    elif p.returncode == 1:
        fail('ERROR: \n' + err + '\n')
        return False
    print '\n  Configure went OK, time for make.\n'
    command = 'make'
    if install:
        command += ' && make install'
    blue('    ' + command)
    p = subprocess.Popen(command, shell=True)
    out, err = p.communicate()
    return True


def download_file(name, url, destination):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(os.path.join(destination, file_name), 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "  Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,
    f.close()
    print '\n'
    return True

configure = {
    'prep_files': prepare_input_files,
    'install': install_tools,
    'uninstall': uninstall_tools,
    'all': full_configuration
}

if __name__ == '__main__':
    main()
