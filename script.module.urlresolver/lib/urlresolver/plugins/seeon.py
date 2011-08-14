import random
import re
from t0mm0.common.net import Net
import urllib2
from urlresolver import common
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
        try:
            html = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error('seeon.tv: got http error %d fetching %s' %
                                    (e.code, web_url))
            return False
        r = re.search('data="(.+?)".+?file=(.+?)\.flv', html, re.DOTALL)
        if r:
            swf_url, play = r.groups()
        else:
            common.addon.log_error('seeon.tv: rtmp stream not found')
            return False
        
        rtmp = 'rtmp://live%d.seeon.tv/edge' % (random.randint(1, 10)) 
        rtmp += '/%s swfUrl=%s pageUrl=%s tcUrl=%s' % (play, swf_url, 
                                                       web_url, rtmp)
        return rtmp
        
    def valid_url(self, web_url):
        return re.match('http://(www.)?seeon.tv/view/(?:\d+)', web_url)
    
