import argparse
import os
import urllib2
import subprocess
from config import blue, warning, ok, fail, downloadURLs, cwd, joiner, run_command


def no_such_arg(args=None):
    fail('No such arg as: ' + args.purpose + ' \ntry: prep_files | install | all\n')


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
            # cd_2_up()
            # return False
        ok('  ok\n')
        command = args.bwa + ' index -a bwtsw -p hg19 hg19.fa'
        blue('\t' + command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            fail('ERROR: \n' + err + '\n')
            # cd_2_up()
            # return False
        # cd_2_up()
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


def install_tools(args=None):
    mkdir(args.download)
    mkdir(args.apps)
    blue('Installing bwa')
    if not exists(os.path.join(args.download, 'bwa-0.7.12.tar.bz2')):
        if not download_file('bwa', downloadURLs['bwa'], args.download):
            return False
    if not extract_file(os.path.join(args.download, 'bwa-0.7.12.tar.bz2'), os.path.join(args.apps, 'bwa'), flags=' --strip-components=1'):
        return False
    with cwd(joiner(args.apps, 'bwa')):
        install_lib1(os.path.abspath(os.curdir), install=False)

    blue('Installing ant')
    if not exists(os.path.join(args.download, 'apache-ant-1.9.6-bin.tar.gz')):
        if not download_file('ant', downloadURLs['ant'], args.download):
            return False
    if not extract_file(os.path.join(args.download, 'apache-ant-1.9.6-bin.tar.gz'), os.path.join(args.apps, 'ant'), flags=' --strip-components=1'):
        return False
    # no need to install ant; its a binary distro.

    blue('Installing Picard')
    
    if not exists(os.path.join(args.download, 'master')):
        if not download_file('picard', downloadURLs['picard'], args.download):
            return False
    if not extract_file(os.path.join(args.download, 'master'), os.path.join(args.apps, 'picard'), flags=' --strip-components=1'):
        return False
    with cwd(os.path.join(args.apps, 'picard')):
        command = 'export JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk-1.6.0.35.x86_64/jre/bin && ' + os.path.join(args.apps, 'ant', 'bin', 'ant') + ' -lib lib/ant package-commands'
        run_command(command, Exception)


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
