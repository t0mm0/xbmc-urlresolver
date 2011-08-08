'''
    common XBMC Module
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
'''

import cgi
import re
import unicodedata
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

class Addon:

    def __init__(self, addon_id, argv=None):
        self.addon = xbmcaddon.Addon(id=addon_id)
        if argv:
            self.url = argv[0]
            self.handle = int(argv[1])
            self.queries = self.parse_query(argv[2][1:])
        

    def get_author(self):    
        return self.addon.getAddonInfo('author')
            

    def get_changelog(self):    
        return self.addon.getAddonInfo('changelog')
            

    def get_description(self):    
        return self.addon.getAddonInfo('description')
            

    def get_disclaimer(self):    
        return self.addon.getAddonInfo('disclaimer')
            

    def get_fanart(self):    
        return self.addon.getAddonInfo('fanart')
            

    def get_icon(self):    
        return self.addon.getAddonInfo('icon')
            

    def get_id(self):    
        return self.addon.getAddonInfo('id')
            

    def get_name(self):    
        return self.addon.getAddonInfo('name')
            

    def get_path(self):    
        return self.addon.getAddonInfo('path')
            

    def get_profile(self):    
        return self.addon.getAddonInfo('profile')
            

    def get_stars(self):    
        return self.addon.getAddonInfo('stars')
            

    def get_summary(self):    
        return self.addon.getAddonInfo('summary')
            

    def get_type(self):    
        return self.addon.getAddonInfo('type')
            

    def get_version(self):    
        return self.addon.getAddonInfo('version')
            
    def get_setting(self, setting):
        return self.addon.getSetting(setting)
        
    def get_string(self, string_id):
        return self.addon.getLocalizedString(string_id)   

    def parse_query(self, query, defaults={'mode': 'main'}):
        queries = cgi.parse_qs(query)
        q = defaults
        for key, value in queries.items():
            if len(value) == 1:
                q[key] = value[0]
            else:
                q[key] = value
        return q


    def build_plugin_url(self, queries):
        return self.url + '?' + urllib.urlencode(queries)


    def log(self, msg, level=xbmc.LOGNOTICE):
        msg = unicodedata.normalize('NFKD', unicode(msg)).encode('ascii',
                                                                 'ignore')
        xbmc.log('%s: %s' % (self.get_name(), msg), level)
        
    def log_error(self, msg):
        self.log(msg, xbmc.LOGERROR)    
        
    def log_debug(self, msg):
        self.log(msg, xbmc.LOGDEBUG)    

    def log_notice(self, msg):
        self.log(msg, xbmc.LOGNOTICE)    

    def resolve_url(self, stream_url):
        if stream_url:
            self.log_debug('resolved to: %s' % stream_url)
            xbmcplugin.setResolvedUrl(self.handle, True, 
                                      xbmcgui.ListItem(path=stream_url))
        else:
            self.log_error('failed to resolve stream')
            #show_error([get_string(30002)])
            xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())

    
    def add_item(self, url, infolabels, img='', fanart='', resolved=False, 
                 total_items=0, playlist=False, item_type='video'):
        infolabels = self.unescape_dict(infolabels)
        if not resolved:
            url = self.build_plugin_url({'play': url})
        listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, 
                                    thumbnailImage=img)
        listitem.setInfo(item_type, infolabels)
        listitem.setProperty('IsPlayable', 'true')
        listitem.setProperty('fanart_image', fanart)
        if playlist is not False:
            self.log_debug('adding item: %s - %s to playlist' % (infolabels['title'], url))
            playlist.add(url, listitem)
        else:
            self.log_debug('adding item: %s - %s' % (infolabels['title'], url))
            xbmcplugin.addDirectoryItem(self.handle, url, listitem, 
                                        isFolder=False, totalItems=total_items)


    def add_video_item(self, url, infolabels, img='', fanart='', resolved=False, 
                       total_items=0, playlist=False):
        self.add_item(url, infolabels, img, fanart, resolved, total_items, 
                      playlist, item_type='video')


    def add_music_item(self, url, infolabels, img='', fanart='', resolved=False, 
                       total_items=0, playlist=False):
        self.add_item(url, infolabels, img, fanart, resolved, total_items, 
                      playlist, item_type='music')


    def add_directory(self, url_queries, title, img='', fanart='', 
                      total_items=0, is_folder=True):
        title = self.unescape(title)
        url = self.build_plugin_url(url_queries)
        self.log_debug(u'adding dir: %s - %s' % (title, url))
        listitem = xbmcgui.ListItem(title, iconImage=img, 
                                    thumbnailImage=img)
        if not fanart:
            fanart = self.get_fanart()
        listitem.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(self.handle, url, listitem, 
                                    isFolder=is_folder, totalItems=total_items)


    def end_of_directory(self):
        xbmcplugin.endOfDirectory(self.handle)
        

    #http://stackoverflow.com/questions/1208916/decoding-html-entities-with-python/1208931#1208931
    def _decode_callback(self, matches):
        id = matches.group(1)
        try:
            return unichr(int(id))
        except:
            return id


    def decode(self, data):
        return re.sub("&#(\d+)(;|(?=\s))", self._decode_callback, data).strip()


    def unescape(self, text):
        text = self.decode(text)
        rep = {'&lt;': '<',
               '&gt;': '>',
               '&quot': '"',
               '&rsquo;': '\'',
               '&acute;': '\'',
               }
        for s, r in rep.items():
            text = text.replace(s, r)
        # this has to be last:
        text = text.replace("&amp;", "&")
        return text
        
    def unescape_dict(self, d):
        out = {}
        for key, value in d.items():
            out[key] = self.unescape(value)
        return out
        
        

