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
from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin

class NovamovResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "novamov"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, web_url):
        #find key
        html = self.net.http_GET(web_url).content
        filename, filekey = re.search('flashvars.file="(.+?)".+?' + 
                                      'flashvars.filekey="(.+?)"', 
                                      html, re.DOTALL).groups()
        #get stream url from api
        api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % \
              (filekey, filename)
        html = self.net.http_GET(api).content
        stream_url = re.search('url=(.+?)&title', html).group(1)
        return stream_url
        
    def valid_url(self, web_url):
        return re.match('http:\/\/(?:www.)?novamov.com\/video\/' + 
                        '(?:[0-9a-zA-Z]+)(?:\/.+)?', web_url)

