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
import urllib
import urllib2
from urlresolver import common
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin

class TedTalksResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "tedtalks"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)

    def get_media_url(self, host, media_id):
        plugin = 'plugin://plugin.video.ted.talks/?mode=playVideo&name=ted&icon=ted&url=' +\
                 urllib.quote_plus(media_id)
        return plugin


    def get_url(self, host, media_id):
        return media_id


    def get_host_and_id(self, url):
        return ('ted.com', url)


    def valid_url(self, url, host):
        return re.match('http://(www.)?ted.com/.+', url)

    def get_settings_xml(self):
        xml = PluginSettings.get_settings_xml(self)
        xml += '<setting label="This plugin calls the tedtalks addon - '
        xml += 'change settings there." type="lsep" />\n'
        return xml
