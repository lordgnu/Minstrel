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

import os, sys

import cherrypy

import time
import datetime
import threading

import minstrel

from minstrel import logger

import Cheetah
from Cheetah.Template import Template

class PageTemplate(Template):
    def __init__(self, *args, **KWs):
        KWs['file'] = os.path.join(minstrel.TEMPLATES, KWs['file'])
        super(PageTemplate, self).__init__(*args, **KWs)

def _sanitize(string):
    return unicode(string).encode('utf-8', 'xmlcharrefreplace')

class MinstrelInterface(object):
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("home")
    
    @cherrypy.expose
    def home(self):
        page = PageTemplate(file="dashboard.tmpl")
        logger.info("Web hit /home")
        
        return _sanitize(page)
    
    @cherrypy.expose
    def shutdown(self):
        logger.info("Minstrel is shutting down (Browser request)")
        threading.Timer(2, minstrel.shutdown).start()
        return "Stopping minstrel"
    
    @cherrypy.expose
    def restart(self):
        logger.info("Minstrel is restarting (Browser request)")
        threading.Timer(2, minstrel.shutdown, [True]).start()
        return "Restarting minstrel"
        