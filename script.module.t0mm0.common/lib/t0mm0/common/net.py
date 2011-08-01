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

import cookielib
import gzip
import re
import StringIO
import urllib
import urllib2

class HeadRequest(urllib2.Request):
    def get_method(self):
        return 'HEAD'

class Net:
    _cj = cookielib.LWPCookieJar()
    _proxy = None
    _user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 ' + \
                  '(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
    _http_debug = False
    
    def __init__(self, cookie_file='', proxy='', user_agent='', 
                 http_debug=False):
        if cookie_file:
            self.set_cookies(cookie_file)
        if proxy:
            self.set_proxy(proxy)
        if user_agent:
            self.set_user_agent(user_agent)
        self._http_debug = http_debug
        self._update_opener()
        
    def set_cookies(self, cookie_file):
        try:
            self._cj.load(cookie_file, ignore_discard=True)
            self._update_opener()
            return True
        except:
            return False
        
    def get_cookies(self):
        return self._cj._cookies

    def save_cookies(self, cookie_file):
        self._cj.save(cookie_file, ignore_discard=True)        
        
    def set_proxy(self, proxy):
        self._proxy = proxy
        self._update_opener()
        
    def get_proxy(self):
        return self._proxy
        
    def set_user_agent(self, user_agent):
        try:
            self._user_agent = user_agent
            return True
        except:
            return False
        
    def get_user_agent(self):
        return self._user_agent
        
    def _update_opener(self):
        if self._http_debug:
            http = urllib2.HTTPHandler(debuglevel=1)
        else:
            http = urllib2.HTTPHandler()
            
        if self._proxy:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj),
                                          urllib2.ProxyHandler({'http': 
                                                                self._proxy}), 
                                          urllib2.HTTPBasicAuthHandler(),
                                          http)
        
        else:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj),
                                          urllib2.HTTPBasicAuthHandler(),
                                          http)
        urllib2.install_opener(opener)
        
    def http_GET(self, url, compression=True):
        return self._fetch(url, compression=compression)
        
    def http_POST(self, url, data, compression=True):
        return self._fetch(url, data, compression=compression)
    
    def http_HEAD(self, url):
        req = HeadRequest(url)
        req.add_header('User-Agent', self._user_agent)
        try:
            response = urllib2.urlopen(req)
        except:
            response = False
        return response

    def _fetch(self, url, data={}, compression=True):
        encoding = ''
        req = urllib2.Request(url)
        if data:
            data = urllib.urlencode(data)
            req = urllib2.Request(url, data)
        req.add_header('User-Agent', self._user_agent)
        if compression:
            req.add_header('Accept-Encoding', 'gzip')
        response = urllib2.urlopen(req)
        html = response.read()
        try:
            if response.headers['content-encoding'].lower() == 'gzip':
                html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
        except:
            pass
        
        try:
            content_type = response.headers['content-type']
            if 'charset=' in content_type:
                encoding = content_type.split('charset=')[-1]
        except:
            pass

        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' +
                      '\s+charset=(.+?)"', html, re.IGNORECASE)
        if r:
            encoding = r.group(1) 
                   
        try:
            html = unicode(html, encoding)
        except:
            pass
            
        return html

