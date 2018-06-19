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
calc_pattern = conf['global']['calc_pattern']
exec_cond = conf[calc_pattern]['exec_cond']
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
logger.info(calc_pattern)

logger.debug(conf)
logger.debug(exec_cond.values)
cmd = ['mpirun', '-n', str(conf['global']['num_procs']), 'python', conf['global']['exec_name'], sys.argv[1]]
logger.debug(cmd)
subprocess.check_output(cmd)
