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

import cookielib
import re
import urllib, urllib2
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay import Plugin

class PutlockerResolver(Plugin, UrlResolver):
    implements = [UrlResolver]
    name = "putlocker"

    def get_media_url(self, web_url):
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
        #find session_hash
        response = opener.open(web_url)
        html = response.read()
        session_hash = re.search('value="([0-9a-f]+?)" name="hash"', 
                                 html).group(1)

        #post session_hash
        response = opener.open(web_url, 
                               urllib.urlencode({'hash': session_hash,
                                                 'confirm': 
                                                   'Continue as Free User'}))
        
        #find download link
        xml_url = web_url.replace('/file/', '/get_file.php?stream=')
        response = opener.open(xml_url)
        html = response.read()
        flv_url = re.search('url="(.+?)"', html).group(1)
        return flv_url
        
    def valid_url(self, web_url):
        return re.match('http:\/\/(?:www.)?putlocker.com\/file\/' + 
                        '(?:[0-9A-F]+)(?:\/.+)?', web_url)
    
    def login_required(self):
        return False

