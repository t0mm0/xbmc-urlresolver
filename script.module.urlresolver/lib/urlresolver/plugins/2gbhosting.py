from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re
import urllib2
from urlresolver import common
import os

class TowgbhostingResolver(Plugin, UrlResolver, PluginSettings):
	implements = [UrlResolver, PluginSettings]
	name = "2gbhosting"
	profile_path = common.profile_path
	cookie_file = os.path.join(profile_path, '%s.cookies' % name)

	def __init__(self):
		p = self.get_setting('priority') or 100
		self.priority = int(p)
		try:
                        os.makedirs(os.path.dirname(self.cookie_file))
                except OSError:
                        pass
		self.net = Net()

	


	def get_media_url(self, web_url):
                # Lets get hold of the submit parameters
                data = {}
                try:
                        check = self.net.set_cookies(self.cookie_file)
                        if not check:
                                common.addon.log_error('2gbhosting: Could not set cookie_file')
                                
                        html = self.net.http_GET(web_url).content
                except urllib2.URLError, e:
                        common.addon.log_error('2gb-hosting: got http error %d fetching %s' %
                                               (e.code, web_url))
                        return False

                r = re.search('<input type="hidden" name="sid" value="(.+?)" />', html)
                sid = ""
                if r:
                        sid = r.group(1)
                        common.addon.log_error('eg-hosting: found sid' + sid)
                else:
                        common.addon.log_error('2gb-hosting: Could not find sid')
                        return False
                
                        

                #Do a post to get the stream_url
                try:
                        data = { 'sid' : sid,'submit' : 'Click Here To Continue', }
                        html = self.net.http_POST(web_url, data).content
                except urllib2.URLError, e:
                        common.addon.log_error('2gbhosting: got http error %d fetching %s' %
                                               (e.code, web_url))
                        return False
                
                r = re.search('swf\|(.+?)\|mpl\|\d+\|(.+?)\|stretching\|autostart\|jpg\|' +
                              'exactfit\|provider\|write\|lighttpd\|.+?\|' +
                              'thumbs\|mediaspace\|(.+)\|(.+)\|(.+?)\|image\|files', html)
                stream_url = ""
                if r:
                        stream_host = r.group(1)
                        url_part4 = r.group(2)
                        url_part2 = r.group(3)
                        url_part1 = r.group(4)
                        url_extension = r.group(5)

                        stream_url = 'http://' + stream_host + '.' + '2gb-hosting.com/files/' + url_part1 + '/' + url_part2 + '/2gb/' + url_part4 + '.' + url_extension
                        common.addon.log_error('2gbhosting: streaming url' + stream_url)
                else:
                        common.addon.log_error('2gbhosting: stream_url not found')
                        return False
                
                
		return stream_url

	

	def valid_url(self, web_url):
		return re.match('http://(www.)?2gb-hosting.com/v/' +
                                '[0-9A-Za-z]+/[0-9a-zA-Z]+.*', web_url)

