#! /usr/bin/env python

import sys
import logging
import subprocess

from toml_parser import TOMLParser

parser = TOMLParser()
args = sys.argv
if len(args) == 1:
    raise Exception("Specify configuration file!")
elif len(args) >= 3:
    raise Exception("Too many configuration files is specified!")
parser.parse(sys.argv[1])
conf = parser.dict_root
loglevel = conf['global']['loglevel']

if loglevel == 'DEBUG':
    level_ = logging.DEBUG
elif loglevel == 'INFO':
    level_ = logging.INFO
elif loglevel == 'WARNING':
    level_ = logging.WARNING
elif loglevel == 'ERROR':
    level_ = logging.ERROR
elif loglevel == 'CRITCAL':
    level_ = logging.CRITCAL

logging.basicConfig(level = level_)
logger = logging.getLogger(__name__)

logger.debug(conf)
try:
    cmd = ['mpirun', '-n', str(conf['global']['num_procs']), 'python', conf['global']['exec_name'], sys.argv[1]]
    logger.debug(cmd)
    ret = subprocess.check_output(cmd)
    logger.debug(ret)
except subprocess.CalledProcessError as e:
    print("*** Error occured in processing command! ***")
    print("Return code: {0}".format(e.returncode))
    print("Command: {0}".format(e.cmd))
    print("Output: {0}".format(e.output))
    raise e


