from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re
import urllib2
from urlresolver import common

class DivxstageResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "divxstage"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, web_url):
        try:
            html = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error('Divxstage: got http error %d fetching %s' %
                                   (e.code, web_url))
            return False
                
        r = re.search('<param name="src" value="(.+?)" />', html)
        if r:
            stream_url = r.group(1)
        else:
            message ='Divxstage: 1st attempt at finding the stream_url failed'
            common.addon.log_debug(message)
            r = re.search("\'flashvars\',\'file=(.+)&type=video", html)
            if r:
                stream_url = r.group(1)
            else:
                message = 'Divxstage: Giving up on finding the stream_url'
                common.addon.log_error(message)
                return False
        return stream_url


    def valid_url(self, web_url):
        return re.match('http://(www.)?divxstage.eu/' +
                        'video/[0-9A-Za-z]+', web_url)

