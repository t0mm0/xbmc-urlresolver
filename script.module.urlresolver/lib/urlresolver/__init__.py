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
from plugnplay.interfaces import PluginSettings
from plugnplay.interfaces import SiteAuth

#load all available plugins
plugnplay.set_plugin_dirs(common.plugins_path)
plugnplay.load_plugins()

def resolve(web_url):
    """Resolve a web page to a media stream."""
    imp = find_resolver(web_url)
    if imp:
        print 'resolving using %s plugin' % imp.name
        if SiteAuth in imp.implements:
            print 'logging in'
            imp.login()
        return imp.get_media_url(web_url)
    return False
    
def filter_urls(urls):
    ret = []
    for url in urls:
        imp = find_resolver(url)
        if imp:
            ret.append(url)
    return ret
        
def find_resolver(web_url):
    for imp in UrlResolver.implementors():
        if imp.valid_url(web_url):
            return imp
    return False
    
        
def display_settings():
    update_settings_xml()
    common.addon.openSettings()
        
def update_settings_xml():
    try:
        try:
            os.makedirs(os.path.dirname(common.settings_file))
        except OSError:
            pass

        f = open(common.settings_file, 'w')
        try:
            f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write('<settings>\n')    
            for imp in PluginSettings.implementors():
                f.write(imp.get_settings_xml())
            f.write('</settings>')
        finally:
            f.close
    except IOError:
        print 'error writing ' + common.settings_file

update_settings_xml()
