from contextlib import contextmanager
import os
import subprocess

downloadURLs = {
    'hg19': 'http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz',
    'dbsnp': 'ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/2.8/hg19/dbsnp_138.hg19.vcf.gz'
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
        blue('cwd: ' + newdir)
        yield
    finally:
        os.chdir(olddir)
        blue('cwd: ' + olddir)


def joiner(path, *paths):
    return os.path.abspath(os.path.join(path, *paths))


def run_command(command, error_type, ship_output=False, print_cmd=True, hide_stderr=False):
    if print_cmd:
        blue(command)
    if ship_output:
        p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if (p.returncode == 0) and err and not hide_stderr:
        warning('WARNING: \n' + err + '\n')
    elif p.returncode > 0:
        warning('WARNING: \n' + err + '\n')
        raise error_type('Something went wrong while: ' + command + '\n' + err)
    if ship_output:
        return out.strip()


def run_commands(list_of_commands, error_type, ship_output=False, print_cmd=True):
    for cmd in list_of_commands:
        if ship_output:
            return run_command(cmd, error_type, ship_output=ship_output, print_cmd=print_cmd)
        else:
            run_command(cmd, error_type, ship_output=ship_output, print_cmd=print_cmd)
