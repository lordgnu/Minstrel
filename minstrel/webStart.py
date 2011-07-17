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
import sys

import cherrypy

import minstrel

from minstrel import logger
from webInterface import MinstrelInterface

def initialize(options={}):
    
    cherrypy.config.update({
                'log.screen':            False,
                'server.thread_pool':     10,
                'server.socket_port':     options['http_port'],
                'server.socket_host':     options['http_host'],
                'engine.autoreload_on':    False,
        })

    conf = {
        '/': {
            'tools.staticdir.root': os.path.join(minstrel.ROOT, 'www')
        },
        '/images':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "images"
        },
        '/css':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "css"
        },
        '/js':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "js"
        },
        '/favicon.ico':{
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "images/favicon.ico"
        }
    }
    
    if options['http_pass'] != "":
        
        conf['/'].update({
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'Minstrel',
            'tools.auth_basic.checkpassword':  cherrypy.lib.auth_basic.checkpassword_dict(
                    {options['http_user']:options['http_pass']})
        })
        

    # Prevent time-outs
    cherrypy.engine.timeout_monitor.unsubscribe()
    
    logger.info("HTTP ROOT: " + options['http_root'])
    
    cherrypy.tree.mount(MinstrelInterface(), options['http_root'], config = conf)
    
    try:
        cherrypy.process.servers.check_port(options['http_host'], options['http_port'])
        cherrypy.server.start()
    except IOError:
        logger.error("Could not bind to port {0} - Is Minstrel already running?".format(options['http_port']))
        sys.exit(0)
    
    cherrypy.server.wait()