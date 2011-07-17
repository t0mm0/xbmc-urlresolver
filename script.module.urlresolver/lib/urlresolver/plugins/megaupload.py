"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import random
import re
import urllib2

from lib import _megaupload
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay import Plugin
from urlresolver import common

class MegaUploadResolver(Plugin, UrlResolver):
    implements = [UrlResolver]
    name = "megaupload"
    profile_path = common.profile_path    
    cookie_file = os.path.join(profile_path, '%s.cookies' % name)
    
    def get_media_url(self, web_url):
        media_url = _megaupload.resolveURL(web_url, self.cookie_file)
        #TODO: do some waiting depending on self.login_type
        print 'login type: %s' % self.login_type
        return media_url[0]
        
    def valid_url(self, web_url):
        return re.match('http:\/\/(?:www.)?megaupload.com\/\?d=' + 
                        '(?:[0-9A-Z]+)(?:\/.+)?', web_url)
    
    def login_required(self):
        return 'optional'
        
    def login(self, username=None, password=None):
        self.username = username
        self.password = password
        self.login_type = _megaupload.doLogin('regular', self.cookie_file, username, password)

