

downloadURLs = {
	'bwa': 'http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.12.tar.bz2',
	'pickard': 'https://github.com/broadinstitute/picard/tarball/master/picard.tar.gz',
    'hg19' : 'http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz'
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def blue(st):
    return bcolors.OKBLUE + st + bcolors.ENDC

def warning(st):
    return bcolors.WARNING + st + bcolors.ENDC

def ok(st):
    return bcolors.OKGREEN + st + bcolors.ENDC

def fail(st):
    return bcolors.FAIL + st + bcolors.ENDC