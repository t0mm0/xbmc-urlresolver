from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re
import urllib2
from urlresolver import common
import os

class TwogbhostingResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "2gbhosting"


    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()


    def get_media_url(self, web_url):
        data = {}
        try:
            html = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error('2gb-hosting: http error %d fetching %s' %
                                    (e.code, web_url))
            return False

        r = re.search('<input type="hidden" name="sid" value="(.+?)" />', html)
        if r:
            sid = r.group(1)
            common.addon.log_debug('eg-hosting: found sid' + sid)
        else:
            common.addon.log_error('2gb-hosting: Could not find sid')
            return False
        try:
            data = { 'sid' : sid,'submit' : 'Click Here To Continue', }
            html = self.net.http_POST(web_url, data).content
        except urllib2.URLError, e:
            common.addon.log_error('2gbhosting: got http error %d fetching %s' %
                                    (e.code, web_url))
            return False

        r = re.search('swf\|(.+?)\|mpl\|\d+\|(.+?)\|stretching\|autostart\|' +
                      'jpg\|exactfit\|provider\|write\|lighttpd\|.+?\|' +
                      'thumbs\|mediaspace\|(.+)\|(.+)\|(.+?)\|image\|files', 
                      html)
        if r:
            stream_host, url_part4, url_part2, url_part1, ext = r.groups()
            stream_url = 'http://%s.2gb-hosting.com/files/%s/%s/2gb/%s.%s' % (
                             stream_host, url_part1, url_part2, url_part4, ext)
            common.addon.log_debug('2gbhosting: streaming url ' + stream_url)
        else:
            common.addon.log_error('2gbhosting: stream_url not found')
            return False

        return stream_url



    def valid_url(self, web_url):
        return re.match('http://(www.)?2gb-hosting.com/v/' +
                        '[0-9A-Za-z]+/[0-9a-zA-Z]+.*', web_url)

