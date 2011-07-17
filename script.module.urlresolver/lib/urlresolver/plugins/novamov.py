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

import re
import urllib2
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay import Plugin

class NovamovResolver(Plugin, UrlResolver):
    implements = [UrlResolver]
    name = "novamov"

    def get_media_url(self, web_url):
        response = urllib2.urlopen(web_url)
        html = response.read()
        flv_url = re.search('flashvars.file="(.+?)"', html).group(1)
        return flv_url
        
    def valid_url(self, web_url):
        return re.match('http:\/\/(?:www.)?novamov.com\/video\/' + 
                        '(?:[0-9a-zA-Z]+)(?:\/.+)?', web_url)
    
    def login_required(self):
        return False

