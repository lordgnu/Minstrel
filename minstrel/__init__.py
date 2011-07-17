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

import os, sys, subprocess
import cherrypy
import threading
import webbrowser

from lib import simplejson
from lib.configobj import ConfigObj

from minstrel import logger

# Version
CURRENT_VERSION = "0.1"

# Variables we will need
MINSTREL_FULLNAME = None
MINSTREL_NAME = None

# Root directory
ROOT = None

# Data Directory
DATA_DIR = None

# Config Stuff
CONFIG_FILE = None
CONFIG = None

# Templating stuff
TEMPLATES = None

# Database
DATABASE_FILE = None

# Log Directory
LOG_DIR = None

# Arguments
ARGS = None
ARGS_COMPILED = None

# Options
QUIET = False
DAEMON = False

# Web-server options
HTTP_PORT = None
HTTP_HOST = None
HTTP_USER = None
HTTP_PASS = None
HTTP_ROOT = None

LAUNCH_BROWSER = False

INIT_LOCK = threading.Lock()
__INITIALIZED__ = False


def init():
    with INIT_LOCK:
    
        global __INITIALIZED__, ROOT, DATA_DIR, CONFIG_FILE, CONFIG, DATABASE_FILE, ARGS, ARGS_COMPILED, \
            QUIET, DAEMON, MINSTREL_NAME, HTTP_PORT, HTTP_HOST, HTTP_USER, HTTP_PASS, HTTP_ROOT, \
            LAUNCH_BROWSER, LOG_DIR, TEMPLATES
    
        if __INITIALIZED__:
            return False
        
        # Start the logger
        logger.minstrel_log.initLogger(quiet=QUIET)
        
        # Check configurations
        logger.info("Checking config...")
        check_config_section('General')
        
        try:
            HTTP_PORT = config_int('General', 'http_port', 8085)
        except:
            HTTP_PORT = 8085
        
        if HTTP_PORT < 21 or HTTP_PORT > 65535:
            logger.warn("Invalid HTTP Port setting")
            HTTP_PORT = 8085
        
        # Check all the other HTTP parts
        HTTP_HOST = config_str('General', 'http_host', '0.0.0.0')
        HTTP_USER = config_str('General', 'http_user', '')
        HTTP_PASS = config_str('General', 'http_pass', '')
        HTTP_ROOT = config_str('General', 'http_root', '/')
        
        LAUNCH_BROWSER = bool(config_int('General','launch_browser', 1))
        
        # Check the database
        logger.info("Checking database tables...")
        check_database()
        
        # @todo: Put Some Versioning Check Stuff Here
        # @todo: Git Integration Goes here too
        
        __INITIALIZED__ = True
        return True


def check_database():
    pass

def check_config():
    pass
   


def config_val(type, section, item, default):
    try:
        if type == 'int':
            val = int(CONFIG[section][item])
        else:
            val = CONFIG[section][item]
    except:
        val = default
        try:
            CONFIG[section][item] = val
        except:
            CONFIG[section] = {}
            CONFIG[section][item] = val
    
    logger.info('[{0}][{1}] -> {2}'.format(section, item, val))
    return val

def config_str(section, item, default):
    return config_val('string', section, item, default)
    

def config_int(section, item, default):
    return config_val('int', section, item, default)
    

def check_config_section(section):
    """
    Check the INI for a config section - Create it if it doesn't exist
    """
    try:
        CONFIG[section]
        return True
    except:
        CONFIG[section] = {}
        return False

def config_write():
    new_config = ConfigObj()
    new_config.filename = CONFIG_FILE

    new_config['General'] = {}
    new_config['General']['http_port'] = HTTP_PORT
    new_config['General']['http_host'] = HTTP_HOST
    new_config['General']['http_username'] = HTTP_USER
    new_config['General']['http_password'] = HTTP_PASS
    new_config['General']['http_root'] = HTTP_ROOT
    new_config['General']['launch_browser'] = int(LAUNCH_BROWSER)
    
    new_config.write()

def daemonize():
    pass

def launch_browser(host, port, root):
    if host == '0.0.0.0':
        host = 'localhost'
    
    try:
        webbrowser.open('http://%s:%i%s' % (host, port, root))
    except Exception, e:
        logger.error("Could not launch browser: %s" % e)

def shutdown(restart=False, update=False):
    cherrypy.engine.exit();
    
    config_write();
    
    if update:
        pass
    
    if restart:
        popen_list = [sys.executable, MINSTREL_FULLNAME]
        popen_list += ARGS
        if '--nolaunch' not in popen_list:
            popen_list += ['--nolaunch']
        logger.info("Restarting Minstrel with " + str(popen_list))
        subprocess.Popen(popen_list, cwd=os.getcwd())
    
    os._exit(0)
            