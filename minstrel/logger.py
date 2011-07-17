# Author: Don Bauer <lordgnu@me.com>
# URL: http://github.com/lordgnu/Minstrel
# Created: Jul 16, 2011
#
# This file is part of Minstrel
#
# Minstrel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Minstrel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Minstrel.  If not, see <http://www.gnu.org/licenses/>.

import os
import threading
import logging
from logging import handlers

import minstrel

MAX_SIZE = 1000000 # 1mb
MAX_FILES = 5


# Simple rotating log handler that uses RotatingFileHandler
class RotatingLogger(object):

    def __init__(self, filename, max_size, max_files):
    
        self.filename = filename
        self.max_size = max_size
        self.max_files = max_files
        
        
    def initLogger(self, quiet=False):
    
        l = logging.getLogger('minstrel')
        l.setLevel(logging.DEBUG)
        
        self.filename = os.path.join(minstrel.LOG_DIR, self.filename)
        
        filehandler = handlers.RotatingFileHandler(self.filename, maxBytes=self.max_size, backupCount=self.max_files)
        filehandler.setLevel(logging.DEBUG)
        
        fileformatter = logging.Formatter('%(asctime)s - %(levelname)-7s :: %(message)s', '%d-%b-%Y %H:%M:%S')
        
        filehandler.setFormatter(fileformatter)
        l.addHandler(filehandler)
        
        if not quiet:
        
            consolehandler = logging.StreamHandler()
            consolehandler.setLevel(logging.INFO)
            
            consoleformatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s', '%d-%b-%Y %H:%M:%S')
            
            consolehandler.setFormatter(consoleformatter)
            l.addHandler(consolehandler)    
            self.log("Minstrel Logger Started", "debug")
        
    def log(self, message, level):
    
        logger = logging.getLogger('minstrel')
        
        threadname = threading.currentThread().getName()
        message = threadname + ' : ' + message
        
        if level == 'debug':
            logger.debug(message)
        elif level == 'info':
            logger.info(message)
        elif level == 'warn':
            logger.warn(message)
        else:
            logger.error(message)


minstrel_log = RotatingLogger('minstrel.log', MAX_SIZE, MAX_FILES)

def debug(message):
    minstrel_log.log(message, level='debug')

def info(message):
    minstrel_log.log(message, level='info')
    
def warn(message):
    minstrel_log.log(message, level='warn')
    
def error(message):
    minstrel_log.log(message, level='error')
    
