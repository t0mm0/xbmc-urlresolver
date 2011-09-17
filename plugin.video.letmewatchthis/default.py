'''
    letmewatchthis XBMC Addon
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

import re
import string
import sys
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import urllib2
import urlresolver

addon = Addon('plugin.video.letmewatchthis', sys.argv)
net = Net()

base_url = 'http://www.1channel.ch'
genres = ['All', 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 
          'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 
          'History', 'Horror', 'Japanese', 'Korean', 'Music', 'Musical', 
          'Mystery', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 
          'Talk-Show', 'Thriller', 'War', 'Western', 'Zombies']
          
mode = addon.queries['mode']
play = addon.queries.get('play', None)

if play:
    url = addon.queries.get('url', None)
    try:
        addon.log_debug('fetching %s' % url)
        html = net.http_GET(url).content
    except urllib2.URLError, e:
        html = ''
        addon.log_error('got http error %d fetching %s' %
                        (e.code, url))
    
    #find all sources and their info
    sources = []
    for s in re.finditer('class="movie_version.+?quality_(.+?)>.+?url=(.+?)' + 
                         '&domain=(.+?)&.+?"version_veiws">(.+?)</', 
                         html, re.DOTALL):
        q, url, host, views = s.groups()
        verified = s.group(0).find('star.gif') > -1
        title = host.decode('base-64')
        if verified:
            title += ' [verified]'
        title += ' (%s)' % views.strip()
        url = url.decode('base-64')
        hosted_media = urlresolver.HostedMediaFile(url=url, title=title)
        sources.append(hosted_media)

    stream_url = urlresolver.choose_source(sources).resolve()
    addon.resolve_url(stream_url)

elif mode == 'browse':
    browse = addon.queries.get('browse', False)
    genre = addon.queries.get('genre', False)
    letter = addon.queries.get('letter', False)
    section = addon.queries.get('section', '')
    if letter:        
        html = '> >> <'
        if genre == 'All':
            genre = ''
        if letter == 'All':
            letter = ''
        page = 0
        while html.find('> >> <') > -1:
            page += 1
            url = '%s/?letter=%s&sort=alphabet&page=%s&genre=%s&%s' % (
                                         base_url, letter, page, genre, section)
            try:
                addon.log_debug('fetching %s' % url)
                html = net.http_GET(url).content
            except urllib2.URLError, e:
                html = ''
                addon.log_error('got http error %d fetching %s' %
                                (e.code, web_url))

            r = re.search('number_movies_result">([0-9,]+)', html)
            if r:
                total = int(r.group(1).replace(',', ''))
            else:
                total = 0
                
            r = 'class="index_item.+?href="(.+?)".+?src="(.+?)".+?' + \
                'alt="Watch (.+?)"'
            regex = re.finditer(r, html, re.DOTALL)
            urls = []
            for s in regex:
                url, thumb, title = s.groups()
                if url not in urls:
                    urls.append(url)
                    if section == 'tv':
                        addon.add_directory({'mode': 'series', 
                                             'url': base_url + url}, 
                                             title, 
                                             img=thumb,
                                             total_items=total)
                    else:
                        addon.add_video_item({'url': base_url + url}, 
                                             {'title': title}, 
                                              img=thumb, total_items=total)

    elif genre:
        if genre != 'All':
            addon.add_directory({'mode': 'browse', 
                                 'section': section,
                                 'genre': genre,
                                 'letter': 'All'}, 'All')
        addon.add_directory({'mode': 'browse', 
                             'section': section,
                             'genre': genre,
                             'letter': '123'}, '#')
        for l in string.uppercase:
            addon.add_directory({'mode': 'browse', 
                                 'section': section,
                                 'genre': genre,
                                 'letter': l}, l)
    
    else:
        for genre in genres:
            addon.add_directory({'mode': 'browse', 
                                 'section': section,
                                 'genre': genre}, genre)
            
        
elif mode == 'series':
    url = addon.queries['url']
    try:    
        addon.log_debug('fetching %s' % url)
        html = net.http_GET(url).content
    except urllib2.URLError, e:
        html = ''
        addon.log_error('got http error %d fetching %s' %
                        (e.code, web_url))
                        
    regex = re.search('movie_thumb"><img src="(.+?)"', html)
    if regex:
        img = regex.group(1)
    else:
        addon.log_error('couldn\'t find image')
        img = ''
    
    regex = re.search('<p style="width:460px; display:block;">(.+?)</p', html,
                      re.DOTALL)
    if regex:
        plot = regex.group(1).strip()
    else:
        addon.log_error('couldn\'t find plot')
        plot = ''
    
    seasons = re.search('tv_container(.+?)<div class="clearer', html, re.DOTALL)    
    if not seasons:
        addon.log_error('couldn\'t find seasons')
    else:
        for season in seasons.group(1).split('<h2>'):
            r = re.search('<a.+?>(.+?)</a>', season)
            if r:
                season_name = r.group(1)
            else:
                season_name = 'Unknown Season'
                addon.log_error('couldn\'t find season title')

            r = '"tv_episode_item".+?href="(.+?)">(.*?)</a>'
            episodes = re.finditer(r, season, re.DOTALL)
            for ep in episodes:
                url, title = ep.groups()
                title = re.sub('<[^<]+?>', '', title.strip())
                title = re.sub('\s\s+' , ' ', title)
                addon.add_video_item({'url': base_url + url}, 
                                     {'title': '%s %s' % (season_name, title),
                                      'plot': plot}, img=img)


elif mode == 'main':
    addon.add_directory({'mode': 'browse', 'section': 'tv'}, 'TV')
    addon.add_directory({'mode': 'browse', 'section': ''}, 'Movies')
    addon.add_directory({'mode': 'resolver_settings'}, 'Resolver Settings', 
                        is_folder=False)

elif mode == 'resolver_settings':
    urlresolver.display_settings()


if not play:
    addon.end_of_directory()


