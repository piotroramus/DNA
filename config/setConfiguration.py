import argparse
from colorama import init
import os
import urllib2
from config import blue, warning, ok, fail, downloadURLs


def no_such_arg(args=None):
    print fail('No such arg as: ' + args.purpose + ' \ntry: prep_files | install | all\n')


def main():
    '''
    Main configuration method made to be called if user starts this script on his own
    '''
    init()
    print blue("Welcome to NGS configurator\n")
    parser=argparse.ArgumentParser(description=blue('NGS configurator'))
    parser.add_argument('purpose', type=str, help='choose: prep_files | install | all')
    args = parser.parse_args()
    configure.get(args.purpose, no_such_arg)(args=args)


def prepare_input_files(args=None):
    def mkdir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def clean_downloads():
        pass

    mkdir('downloads/')
    download_file('hg19', downloadURLs['hg19'], 'downloads/')  # TODO destination should be configurable
    pass


def full_configuration(args=None):
    print warning('Not implemented yet!\n')
    pass


def install_tools(args=None):
    print warning('Not implemented yet!\n')
    pass


configure = {
    'prep_files' : prepare_input_files,
    'install' : install_tools,
    'all' : full_configuration,
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
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()
    print '\n'
    return True


if __name__ == '__main__':
    main()