import argparse
from colorama import init
import os
import urllib2
import subprocess
from config import blue, warning, ok, fail, downloadURLs


def no_such_arg(args=None):
    print fail('No such arg as: ' + args.purpose + ' \ntry: prep_files | install | all\n')


def main():
    """
    Main configuration method made to be called if user starts this script on his own
    """
    init()
    print blue("Welcome to NGS configurator\n")
    parser = argparse.ArgumentParser(description=blue('NGS configurator'))
    parser.add_argument('purpose', type=str, help='choose: prep_files | install | all')
    # parser.add_argument('', type=str, help='choose: prep_files | install | all')
    args = parser.parse_args()
    configure.get(args.purpose, no_such_arg)(args=args)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prepare_input_files(args=None):
    def clean_downloads():
        pass

    def cd_2_up():
        print blue('cd ../..')
        os.chdir('../..')
        print '\tcwd: ' + os.getcwd()

    mkdir('downloads/')
    mkdir('hg19/')
    if not exists('downloads/chromFa.tar.gz'):  # sth wrong, not sure yet
        if not download_file('hg19', downloadURLs['hg19'], 'downloads/'):  # TODO destination should be configurable
            return False
    if not extract_file(os.path.join('downloads', 'chromFa.tar.gz'), 'hg19/chromFa'):
        return False
    print blue('cd hg19/chromFa')
    os.chdir('hg19/chromFa')
    print '\tcwd: ' + os.getcwd()
    command = 'cat chr1.fa chr2.fa chr3.fa chr4.fa chr5.fa chr6.fa chr7.fa chr8.fa chr9.fa\
        chr10.fa chr11.fa chr12.fa chr13.fa chr14.fa chr15.fa chr16.fa chr17.fa chr18.fa\
        chr19.fa chr20.fa chr21.fa chr22.fa chrX.fa chrY.fa chrM.fa > hg19.fa'
    print blue('\t' + command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print fail('ERROR: \n' + err + '\n')
        cd_2_up()
        return False
    print ok('  ok\n')
    command = 'bwa index -a bwtsw -p hg19 hg19.fa'
    print blue('\t' + command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print fail('ERROR: \n' + err + '\n')
        cd_2_up()
        return False
    cd_2_up()
    print ok('  ok\n')
    return True


def extract_file(path, destination):
    print ' Extracting file: ' + path + ' into: ' + destination
    mkdir(destination)
    command = 'tar xf ' + path + ' -C ' + destination
    print blue('\t' + command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print fail('ERROR: \n' + err + '\n')
        return False
    print ok('  ok\n')
    return True


def exists(path):
    print ' Checking for existence of: ' + path
    if os.path.isfile(path):
        print ok('Already here: \n    ' + path)
        return True
    print warning('Not here!')
    return False
    # return True


def full_configuration(args=None):
    if not install_tools(args):
        print fail('nah')
    if not prepare_input_files(args):
        print fail('nah')
    print ok('ok')


def install_tools(args=None):
    print warning('Not implemented yet!\n')
    pass


configure = {
    'prep_files': prepare_input_files,
    'install': install_tools,
    'all': full_configuration,
}


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


if __name__ == '__main__':
    main()