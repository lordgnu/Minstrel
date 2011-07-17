#!/usr/bin/env python
# Author: Don Bauer <lordgnu@me.com>
# URL: http://github.com/lordgnu/Minstrel
# Created: Jul 15, 2011
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

import sys, os

# Needed for compiling an executable (From Sick-Beard)
if sys.hexversion >= 0x020600F0:
    from multiprocessing import freeze_support

from lib.configobj import ConfigObj

import threading

import minstrel
from minstrel import webStart, logger

try:
    import argparse
except ImportError:
    import lib.argparse as argparse 

def main():
    """
    Main start function
    """
    
    # Fixed Path
    if hasattr(sys, 'frozen'):
        minstrel.MINSTREL_FULLNAME = os.path.normpath(os.path.abspath(sys.executable))
    else: 
        minstrel.MINSTREL_FULLNAME = os.path.normpath(os.path.abspath(__file__))
    
    # File name
    minstrel.MINSTREL_NAME = os.path.basename(minstrel.MINSTREL_FULLNAME)
    
    # Root Directory
    minstrel.ROOT = os.path.dirname(minstrel.MINSTREL_FULLNAME)
    
    # Data Directory
    minstrel.DATA_DIR = os.path.join(minstrel.ROOT, 'data');
    
    # Log directory
    minstrel.LOG_DIR = os.path.join(minstrel.ROOT, 'logs');
    
    # Template Dir
    minstrel.TEMPLATES = os.path.join(minstrel.ROOT, 'www/interfaces/default')
    
    # Arguments
    minstrel.ARGS = sys.argv[1:]
    
    # Argument Parser
    parser = argparse.ArgumentParser(description='Music library management and SABnzbd+ helper')
    
    parser.add_argument('-q', '--quiet', action='store_true', help='Turn off console logging')
    parser.add_argument('-d', '--daemon', action='store_true', help='Run Minstrel as a daemon')
    parser.add_argument('-p', '--port', type=int, help='Force minstrel to run on a specific port')
    parser.add_argument('--config', help='Specify a config file to use')
    parser.add_argument('--nolaunch', action='store_true', help='Prevent the browser from launching when Minstrel starts')
    
    args = parser.parse_args()
    minstrel.ARGS_COMPILED = args
    
    if args.quiet:
        minstrel.QUIET = True
    
    if args.daemon:
        minstrel.QUIET = True
        minstrel.DAEMON = True
    
    if args.config:
        minstrel.CONFIG_FILE = args.config
    else:
        minstrel.CONFIG_FILE = os.path.join(minstrel.ROOT, 'config.ini')
    
    # Attempt to create the data directory
    if not os.path.exists(minstrel.DATA_DIR):
        try:
            os.makedirs(minstrel.DATA_DIR)
        except OSError:
            raise SystemExit('Data directory does not exist and could not be created: ' + minstrel.DATA_DIR)
    
    # Log Directory
    if not os.path.exists(minstrel.LOG_DIR):
        try:
            os.makedirs(minstrel.LOG_DIR)
        except OSError:
            raise SystemExit('Log directory does not exist and could not be created: ' + minstrel.LOG_DIR)
    
    # Make sure we can write to the data directory
    if not os.access(minstrel.DATA_DIR, os.W_OK):
        raise SystemExit('Data directory is not writable: ' + minstrel.DATA_DIR)
    
    # Database
    minstrel.DATABASE_FILE = os.path.join(minstrel.DATA_DIR, 'minstrel.db')
    
    # Config Object
    minstrel.CONFIG = ConfigObj(minstrel.CONFIG_FILE)
    
    # Name our thread
    threading.currentThread().name = "MAIN"
    
    # Actually start doing stuff now
    minstrel.init()
    
    # Are we running a daemon
    if minstrel.DAEMON:
        minstrel.daemonize();
    
    # Lets start the webserver
    if args.port:
        http_port = args.port
        logger.info("Starting Minstrel with forced port: %i" % http_port)
    else:
        http_port = minstrel.HTTP_PORT
    
    webStart.initialize({
         'http_port':   http_port,
         'http_host':   minstrel.HTTP_HOST,
         'http_root':   minstrel.HTTP_ROOT,
         'http_user':   minstrel.HTTP_USER,
         'http_pass':   minstrel.HTTP_PASS
         })
    
        

if __name__ == "__main__":
    if sys.hexversion >= 0x020600F0:
        # Sick-Beard does this for Windows EXE so we will too
        freeze_support()
    main()