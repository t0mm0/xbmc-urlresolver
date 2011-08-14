'''
    t0mm0 test XBMC Addon
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
import urlresolver

addon = Addon('plugin.video.t0mm0.test', sys.argv)
net = Net()

base_url = 'http://tubeplus.me'

mode = addon.queries['mode']
play = addon.queries.get('play', None)

if play:
    stream_url = urlresolver.resolve(play)
    addon.resolve_url(stream_url)

elif mode == 'resolver_settings':
    urlresolver.display_settings()

elif mode == 'test':
    addon.add_video_item('http://www.putlocker.com/file/DFE7599AE064911A', 
                         {'title': 'putlocker'})
    addon.add_video_item('http://www.novamov.com/video/kdshwq2cj6vxv', 
                         {'title': 'novamov'})
    addon.add_video_item('http://seeon.tv/view/14451', 
                         {'title': 'seeon.tv'})
    addon.add_video_item('http://www.megaupload.com/?d=TQPQJM5H', 
                         {'title': 'megaupload'})
    addon.add_video_item('http://www.sockshare.com/file/541433EA7B32FB39', 
                         {'title': 'sockshare'})
    addon.add_video_item('http://www.videoweed.es/file/crirmdz3tj116', 
                         {'title': 'videoweed'})
    addon.add_video_item('http://videobb.com/video/8FvAG6AQpHi8', 
                         {'title': 'videobb'})
    addon.add_video_item('http://www.tubeplus.me/player/1962655/Entourage/season_8/episode_2/Out_With_a_Bang_/', 
                         {'title': 'tubeplus'})

elif mode == 'tv':
    browse = addon.queries.get('browse', False)
    if browse == 'alpha':
        letter = addon.queries.get('letter', False)
        if letter:
            url = 'http://tubeplus.me/browse/tv-shows/All_Genres/%s/' % letter
            html = net.http_GET(url).content
            r = '<div class="list_item.+?src="(.+?)".+?<a class="plot".+?' + \
                'href="(.+?)".+?<b>(.+?)<\/b>.+?<\/b>(.+?)<'
            regex = re.finditer(r, html, re.DOTALL)
            for s in regex:
                thumb, url, title, plot = s.groups()
                addon.add_directory({'mode': 'series', 
                                     'url': base_url + url}, 
                                     title, 
                                     img=base_url+thumb)

        else:
            addon.add_directory({'mode': 'tv', 
                                 'browse': 'alpha',
                                 'letter': '-'}, '#')
            for l in string.uppercase:
                addon.add_directory({'mode': 'tv', 
                                     'browse': 'alpha',
                                     'letter': l}, l)
        
    else:
        addon.add_directory({'mode': 'tv', 'browse': 'alpha'}, 'A-Z')

elif mode == 'series':
    url = addon.queries['url']
    html = net.http_GET(url).content
    r = 'javascript:show_season\("(\d+?)","(.+?)"\)'
    regex = re.finditer(r, html, re.DOTALL)
    for s in regex:
        season, data = s.groups()
        episodes = data.split('||')
        for episode in episodes:
            params = episode.split('_')
            if len(params) == 5:
                ep_url = '%s/player/%s/' % (base_url, 
                                                                      params[2])
                title = 'S%sE%s - %s (%s)' % (params[0], params[1], 
                                              params[3], params[4])
                addon.add_video_item(ep_url, {'title': title})
    

elif mode == 'main':
    addon.add_directory({'mode': 'test'}, '*test links*')
    addon.add_directory({'mode': 'tv'}, 'tubeplus.me tv')
    addon.add_directory({'mode': 'resolver_settings'}, 'resolver settings', 
                        is_folder=False)


if not play:
    addon.end_of_directory()


