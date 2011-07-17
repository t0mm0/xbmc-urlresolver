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
try:
    import xbmc, xbmcaddon, xbmcgui, xbmcplugin
    is_xbmc = True
except:
    is_xbmc = False
    print 'not running on xbmc'
    
if is_xbmc:
    addon = xbmcaddon.Addon(id='script.module.urlresolver')
    plugin_path = addon.getAddonInfo('path')
    profile_path = addon.getAddonInfo('profile')
else:
    plugin_path = os.path.dirname(__file__)
    profile_path = plugin_path
