import random
import re
from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin

class SeeonResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "seeon.tv"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, web_url):
        html = self.net.http_GET(web_url).content
        swf_url, play = re.search('data="(.+?)".+?file=(.+?)\.flv', 
                                  html, re.DOTALL).groups()
        rtmp = 'rtmp://live%d.seeon.tv/edge' % (random.randint(1, 10)) 
        rtmp += '/%s swfUrl=%s pageUrl=%s tcUrl=%s' % (play, swf_url, 
                                                       web_url, rtmp)
        return rtmp
        
    def valid_url(self, web_url):
        return re.match('http:\/\/(?:www.)?seeon.tv\/view\/(?:\d+)(?:\/.+)?',
                        web_url)
    
