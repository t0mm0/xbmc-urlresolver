from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re
import urllib2
from urlresolver import common

class nolimitvideoResolver(Plugin, UrlResolver, PluginSettings):
	implements = [UrlResolver, PluginSettings]
	name = "nolimitvideo"

	def __init__(self):
		p = self.get_setting('priority') or 100
		self.priority = int(p)
		self.net = Net()

	


	def get_media_url(self, web_url):
                try:
                        html = self.net.http_GET(web_url).content
                except urllib2.URLError, e:
                        common.addon.log_error('nolimitvideo: got http error %d fetching %s' %
                                               (e.code, web_url))
                        return False
                
                r = re.search('\'file\': \'(.+?)\',', html)
                stream_url = ""
                if r:
                        stream_url = r.group(1)
                else:
                        common.addon.log_error('nolimitvideo: stream_url not found')
                        return False
                
		return stream_url

	

	def valid_url(self, web_url):
		return re.match('http://(www)?.nolimitvideo.com/' +
                                'video/[0-9A-Za-z]+/', web_url)


