from contextlib import contextmanager
import os

downloadURLs = {
    'bwa': 'http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.12.tar.bz2',
    'pickard': 'https://github.com/broadinstitute/picard/tarball/master/picard.tar.gz',
    'hg19': 'http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz'
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


class Ver(object):
    verbose = 4


def set_verbosity(args):
    if args.VERBOSE:
        try:
            v_level = int(args.VERBOSE)
        except:
            v_level = 4
        finally:
            Ver.verbose = v_level


def verbosity_decorator(f):
    
    def wrapper(st):
        res = f(st, Ver.verbose)
        return res
        
    return wrapper


@verbosity_decorator
def blue(st, a=2):
    if a>3:
        print bcolors.OKBLUE + st + bcolors.ENDC


@verbosity_decorator
def warning(st, a=2):
    if a>1:
        print bcolors.WARNING + st + bcolors.ENDC


@verbosity_decorator
def ok(st, a=2):
    if a>2:
        print bcolors.OKGREEN + st + bcolors.ENDC


@verbosity_decorator
def fail(st, a=2):
    if a>0:
        print bcolors.FAIL + st + bcolors.ENDC


@contextmanager
def cwd(newdir):
    olddir = os.path.abspath(os.curdir)
    try:
        os.chdir(newdir)
        print blue('cwd: ' + newdir)
        yield
    finally:
        os.chdir(olddir)
        print blue('cwd: ' + olddir)


def joiner(path, *paths):
    return os.path.abspath(os.path.join(path, *paths))
