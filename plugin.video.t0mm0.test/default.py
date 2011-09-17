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

import os
import re
import string
import sys
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import urlresolver

addon = Addon('plugin.video.t0mm0.test', sys.argv)
net = Net()

logo = os.path.join(addon.get_path(), 'art','logo.jpg')

base_url = 'http://tubeplus.me'

mode = addon.queries['mode']
play = addon.queries.get('play', None)

if play:
    url = addon.queries.get('url', '')
    host = addon.queries.get('host', '')
    media_id = addon.queries.get('media_id', '')
    #stream_url = urlresolver.resolve(play)
    stream_url = urlresolver.HostedMediaFile(url=url, host=host, media_id=media_id).resolve()
    addon.resolve_url(stream_url)

elif mode == 'resolver_settings':
    urlresolver.display_settings()

elif mode == 'test':
    addon.add_video_item({'url': 'http://www.2gb-hosting.com/v/94fb733db6e9f984b07da3cb238eb277/2074fe10f41c7e1.flv.html'}, 
                         {'title': '2gbhosting url'})
    addon.add_video_item({'host': '2gb-hosting.com', 'media_id': 'e1593e96e19f7ecced3778668e809c77/efc5d03968fbca6.avi.html'}, 
                         {'title': '2gbhosting media id'})
    addon.add_video_item({'url': 'http://www.megaupload.com/?d=9T8NHCK4'}, 
                         {'title': 'megaupload url'})
    addon.add_video_item({'host': 'megaupload.com', 'media_id': '9T8NHCK4'}, 
                         {'title': 'megaupload media id'})
    addon.add_video_item({'url': 'http://www.putlocker.com/file/DFE7599AE064911A'}, 
                         {'title': 'putlocker url'})
    addon.add_video_item({'host': 'putlocker.com', 'media_id': 'DFE7599AE064911A'}, 
                         {'title': 'putlocker media id'})
    '''
    addon.add_video_item('http://www.2gb-hosting.com/v/e1593e96e19f7ecced3778668e809c77/efc5d03968fbca6.avi.html', 
                         {'title': '2gb-hosting'})
    addon.add_video_item('http://www.divxstage.eu/video/eb20c352c3ccc', 
                         {'title': 'divxstage'})
    addon.add_video_item('http://www.megaupload.com/?d=TQPQJM5H', 
                         {'title': 'megaupload'})
    addon.add_video_item('http://www.megavideo.com/?v=LYWNYM1J', 
                         {'title': 'megavideo'})
    addon.add_video_item('http://www.movshare.net/video/rnqmuilri1b71', 
                         {'title': 'movshare'})
    addon.add_video_item('http://www.nolimitvideo.com/video/bdb6e2c62fe027a7b20a/friends-with-benefits-ts', 
                         {'title': 'nolimitvideo'})
    addon.add_video_item('http://www.novamov.com/video/kdshwq2cj6vxv', 
                         {'title': 'novamov'})
    addon.add_video_item('http://www.putlocker.com/file/DFE7599AE064911A', 
                         {'title': 'putlocker'})
    addon.add_video_item('http://seeon.tv/view/14451', 
                         {'title': 'seeon.tv'})
    addon.add_video_item('http://www.sockshare.com/embed/541433EA7B32FB39', 
                         {'title': 'sockshare'})
    addon.add_video_item('http://www.tubeplus.me/player/1962655/Entourage/season_8/episode_2/Out_With_a_Bang_/', 
                         {'title': 'tubeplus'})
    addon.add_video_item('http://videobb.com/video/8FvAG6AQpHi8', 
                         {'title': 'videobb'})
    addon.add_video_item('http://www.videoweed.es/file/crirmdz3tj116', 
                         {'title': 'videoweed'})
    addon.add_video_item('http://www.vidxden.com/0up93nsov4w9/Hells.Kitchen.US.S07E07.WS.PDTV.XviD-LOL.avi.html', 
                         {'title': 'vidxden avi'})
    addon.add_video_item('http://www.vidxden.com/embed-ce9eahujm85p.html', 
                         {'title': 'vidxden flv'})
    addon.add_video_item('http://www.youtube.com/watch?v=Q3VJOl_XeGs', 
                         {'title': 'youtube'})
    '''
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
    addon.show_small_popup('t0mm0 test addon', 'Is now loaded enjoy', 6000,
                           logo)
    addon.add_directory({'mode': 'test'}, '*test links*')
    addon.add_directory({'mode': 'tv'}, 'tubeplus.me tv')
    addon.add_directory({'mode': 'resolver_settings'}, 'resolver settings', 
                        is_folder=False)


if not play:
    addon.end_of_directory()


