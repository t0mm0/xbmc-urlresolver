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
import common
import plugnplay
from plugnplay.interfaces import UrlResolver

#load all available plugins
plugins = os.path.join(common.plugin_path, 'plugins')
plugnplay.set_plugin_dirs(plugins)
plugnplay.load_plugins()

def resolve(web_url, username=None, password=None):
    """Resolve a web page to a media stream."""
    for imp in UrlResolver.implementors():
        if imp.valid_url(web_url):
            print 'resolving using %s plugin' % imp.name
            if imp.login_required():
                imp.login(username, password)
            return imp.get_media_url(web_url)
    return False
