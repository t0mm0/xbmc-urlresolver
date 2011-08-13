=================
Coding the Plugin
=================

Now it is time to start actually writing some code.

:mod:`urlresolver.plugnplay.interfaces` defines what methods your resolver class
needs to implement in order to work as a plugin. Head on over there to read the 
full reference documentation for those interfaces.

The first thing to do is get a clone of the urlresolver git repository. If you 
are planning on submitting code it is probably better to fork it first, then you
will be able to send pull requests with your changes. This is beyond the scope 
of this tutorial so for full details please see the 
`github help pages <http://help.github.com/>`_.

I work under linux, and use symbolic links to let XBMC see my development 
versions of addons (not sure of the best way of doing this on other operating
systems). For example, assuming the git repo was checked out in the home 
directory::

    $ ln -s ~/xbmc-urlresolver/script.module.urlresolver ~/.xbmc/addons/
    $ ln -s ~/xbmc-urlresolver/script.module.t0mm0.common ~/.xbmc/addons/
    $ ln -s ~/xbmc-urlresolver/plugin.video.t0mm0.test ~/.xbmc/addons/

After restarting XBMC your addons will be found by XBMC.

Skeleton
========

Lets start off by making a 'skeleton' plugin.

Make a new file in ``script.module.urlresolver/lib/plugins`` called 
``videobb.py`` and put the following code in it:
    
.. code-block:: python
    :linenos:
    
    from t0mm0.common.net import Net
    from urlresolver.plugnplay.interfaces import UrlResolver
    from urlresolver.plugnplay.interfaces import PluginSettings
    from urlresolver.plugnplay import Plugin

    class MyVideobbResolver(Plugin, UrlResolver, PluginSettings):
        implements = [UrlResolver, PluginSettings]
        name = "myvideobb"

        def __init__(self):
            p = self.get_setting('priority') or 100
            self.priority = int(p)
            self.net = Net()

        def get_media_url(self, web_url):
            return 'media url'
            
        def valid_url(self, web_url):
            return False
            
Here's a quick explanation.

* *Line 1* - import the :class:`~t0mm0.common.net.Net` routines from :mod:`t0mm0.common.net`. 
  This lets us easy handle HTTP calls (including handling cookies and proxies)
  with the minimum of code.
* *Line 2-4* - Import the interfaces we need to implement.
* *Line 6-7* - Define our plugin's class. The classes in brackets on line 6
  are classes that your plugin will inherit from. ``Plugin`` must be included
  here to take care of some stuff behind the scenes, but nothing else needs to
  be done regarding ``Plugin``. 
  
  ``implements`` must be a list of classes you 
  want to commit to implmenting. In this case we will implement 
  :class:`~urlresolver.plugnplay.interfaces.UrlResolver` (which means we can 
  resolve URLs - every plugin does this!) and 
  :class:`~urlresolver.plugnplay.interfaces.PluginSettings` (which means our 
  plugin can have settings. I suggest that all plugins implement 
  ``PluginSettings`` unless there is a good reason not to as you get the 
  priority setting (which doesn't do much yet but I hope to make more use of in
  the future) free. As it happens, our plugin will need custom settings to 
  decide which quality stream to play by default.
* *Line 8* - Define a human readable name for our plugin. It is used as the
  name for the settings page among other things.
* *Line 10-13* Our plugin's ``__init__`` method, It gets called when the plugin 
  is initialised. 11-12 set up the priority value from the settings, and 13 
  makes an instance of the ``Net`` class. The reason I do this here is that if 
  you need cookies then all calls to ``self.net`` will automatically keep the 
  same ``cookiejar`` (the jar won't be automatically saved, but it will last the
  lifetime of the plugin which is often all that is required. If you need 
  cookies saved between plugin runs, look at 
  :meth:`~t0mm0.common.net.Net.save_cookies`). 
  
  For many plugins this ``__init__`` method can be left as is.
* *Line 15-16* A stub for our main method. This is where the code to turn the
  ``web_url`` into a media URL will go.
* *Line 18-19* A stub for the method that determines whether this plugin is 
  capable of handling any given ``web_url``.  
 
Now turn on debugging in XBMC and navigate to the 't0mm0 test addon' in 
'video addons'. Check the XBMC log (I normally leave a terminal open in linux
with ``tail -n 100 -f ~/.xbmc/temp/xbmc.log`` which shows you the log in real 
time - other operating systems may vary). Scroll back a bit and you should see 
something similar to the following two lines::

    18:35:03 T:122399600 M:374116352   DEBUG: urlresolver: registering plugin: myvideobb (MyVideobbResolver), as: UrlResolver (P=100)
    18:35:03 T:122399600 M:374116352   DEBUG: urlresolver: registering plugin: myvideobb (MyVideobbResolver), as: PluginSettings (P=100)

This shows that your new plugin is installed and initialised correctly.

Can We Handle It?
=================

Lets fill in the ``valid_url()`` method. This is where your plugin advertises
what URLs it is capable of resolving. This method needs to return ``True`` if we 
think we can resolve it and ``False`` if not.

We have already found a couple of URLs we know we need to handle:

#. ``http://videobb.com/video/{VIDEO_ID}``
#. ``http://videobb.com/watch_video.php?v={VIDEO_ID}``
   
   I also noticed an embeddable URL in my travels around the net which we might 
   as well support:
#. ``http://videobb.com/e/{VIDEO_ID}``

I also noticed that all of these URLs work if they start ``www.`` as well.

We have also already established that the regex representation of ``{video_ID}`` 
is ``[0-9A-Za-z]+`` (1 or more or any digit, or upper or lower case letter).

So we can start to make a regular expression that will match any of these URLs.
Lets start by making one that will match URL 1::

    'http://(www.)?videobb.com/video/[0-9A-Za-z]+'
    
Looks simple enough. The brackets around the 'www.' followed by a question mark 
makes that part optional. Lets try it out using python's interactive 
interpreter::

    >>> print re.match('http://(www.)?videobb.com/video/[0-9A-Za-z]+', 'http://videobb.com/video/8FvAG6AQpHi8')
    <_sre.SRE_Match object at 0xb77fcaa0>
    >>> print re.match('http://(www.)?videobb.com/video/[0-9A-Za-z]+', 'http://videobb.com/watch_video.php?v=8FvAG6AQpHi8')
    None
    >>> print re.match('http://(www.)?videobb.com/video/[0-9A-Za-z]+', 'http://videobb.com/e/8FvAG6AQpHi8')
    None

As you can see, so far only the URL 1 is covered (The ``SRE_MATCH`` object will
evaluate as True and ``None`` will evaluate as ``False``)

No we'll add support for the second URL::

    'http://(www.)?videobb.com/(video/|watch_video.php\?v=)[0-9A-Za-z]+'

The pipe character (``|``) means it will match either the left part of the 
brackets **OR** the right part.

Lets see how we do now::

    >>> print re.match('http://(www.)?videobb.com/(video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://videobb.com/video/8FvAG6AQpHi8')
    <_sre.SRE_Match object at 0xb7805e78>
    >>> print re.match('http://(www.)?videobb.com/(video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://videobb.com/watch_video.php?v=8FvAG6AQpHi8')
    <_sre.SRE_Match object at 0xb7805a40>
    >>> print re.match('http://(www.)?videobb.com/(video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://videobb.com/e/8FvAG6AQpHi8')
    None

So now we add support for URL 3::

    'http://(www.)?videobb.com/(e/|video/|watch_video.php\?v=)[0-9A-Za-z]+'
    
You can see I've just added one more OR in there. Now all 3 URLs I know about 
will be detected by this regular expression whether it includes a www. or not::

    >>> print re.match('http://(www.)?videobb.com/(e/|video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://videobb.com/video/8FvAG6AQpHi8')
    <_sre.SRE_Match object at 0xb7805ec0>
    >>> print re.match('http://(www.)?videobb.com/(e/|video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://videobb.com/watch_video.php?v=8FvAG6AQpHi8')
    <_sre.SRE_Match object at 0xb7805a40>
    >>> print re.match('http://(www.)?videobb.com/(e/|video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://videobb.com/e/8FvAG6AQpHi8')
    <_sre.SRE_Match object at 0xb7805e78>
    >>> print re.match('http://(www.)?videobb.com/(e/|video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://www.videobb.com/video/8FvAG6AQpHi8')
    <_sre.SRE_Match object at 0xb7805e78>
    >>> print re.match('http://(www.)?videobb.com/(e/|video/|watch_video.php\?v=)[0-9A-Za-z]+', 'http://different-hoster.com/video/8FvAG6AQpHi8')
    None

So lets use that to fill in our ``valid_url()`` method. Replace the existing 
stub with::

    def valid_url(self, web_url):
        return re.match('http://(www.)?videobb.com/' + 
                        '(e/|video/|watch_video.php\?v=)' +
                        '[0-9A-Za-z]+')
                        
and add::

    import re
    
to the top of the file.

In case you are wondering why I split the regular expression on multiple lines,
it is to make it more readable. I always try and keep line lengths less than 80
characters, as suggested in :pep:`8`.

.. seealso::

    If you'd like more info on regular expressions, check out the module docs
    for the :mod:`re` module, or read one of the many fine tutorials on the
    web such as http://www.regular-expressions.info/.

Testing ``valid_url()``
=======================

Lets add some test urls into the test addon. Under::

    elif mode == 'test':

add::

    addon.add_video_item('http://videobb.com/video/8FvAG6AQpHi8', 
                         {'title': 'videobb test 1'})
    addon.add_video_item('http://videobb.com/watch_video.php?v=8FvAG6AQpHi8', 
                         {'title': 'videobb test 2'})
    addon.add_video_item('http://videobb.com/e/8FvAG6AQpHi8', 
                         {'title': 'videobb test 3'})

Now we can test to see if our plugin tries to resolve these links by trying to
play them in XBMC. 

Go to 't0mm0 test addon' in 'video addons'. Select 'resolver settings' and 
change the priority for our plugin to something lower than the existing videobb
plugin. This will ensure that when we try and play a videobb link, our 
'myvideobb' plugin will be tried first (plugins are tried in priority order from
low numbers to high).

Now select '\*test links\*' and you should see the links we just added. Give one 
a try. It won't play anything because we haven't written the code yet, but you
should see the following in the log which proves the URL is being sent to our 
new plugin::

    20:38:11 T:3040648048 M:556085248  NOTICE: urlresolver: resolving using myvideobb plugin
    20:38:11 T:3040648048 M:555970560   DEBUG: t0mm0 test addon: resolved to: media url

If it still says ``resolving using videobb plugin`` you have done something 
wrong. Go back and check your regular expressions and check the priority 
settings.

The Main Event
==============

Now lets replace the ``get_media_url()`` method with something useful:

.. code-block:: python
    :linenos:

    def get_media_url(self, web_url):
        #find video_id
        r = re.search('(?:/e/|/video/|v=)([0-9a-zA-Z]+)', web_url)
        if r:
            video_id = r.group(1)
        else:
            common.addon.log_error('myvideobb: video_id not found')
            return False

        #grab json info for this video
        json_url = 'http://videobb.com/player_control/settings.php?v=%s' % \
                                                                    video_id
        try:
            json = self.net.http_GET(json_url).content
        except urllib2.URLError, e:
            common.addon.log_error('myvideobb: got http error %d fetching %s' %
                                    (e.code, api_url))
            return False
            
        #find highest quality URL
        r = re.finditer('"l".*?:.*?"(.+?)".+?"u".*?:.*?"(.+?)"', json)
        chosen_res = 0
        stream_url = False
        if r:
            for match in r:
                res, url = match.groups()
                res = int(res.strip('p'))
                if res > chosen_res:
                    stream_url = url.decode('base-64')
                    chosen_res = res
        else:
            common.addon.log_error('myvideobb: stream url not found')
            return False

        return stream_url

You'll also need to add::

    import urllib2
    from urlresolver import common

to the top of the file. 

Although we use :class:`~t0mm0.common.net.Net` to handle the network 
communications, we still need to import :mod:`urllib2` in order to catch the
exceptions if something goes wrong.

``urlrsolver.common`` is imported so that we can use the logging functions.

This code is split into three main sections:

#. :ref:`find-video-id` (lines 3-8)
#. :ref:`grab-json` (lines 11-18)
#. :ref:`grab-url` (lines 21-33)

.. _find-video-id:

Find video_id
-------------

This section finds the video ID from the URL that has been passed to the 
plugin.

* *Line 2* - More regular expressions. This one grabs the video ID from the URL
  passed to the plugin. We already know it matches the pattern used for 
  ``valid_url()`` so we can make some assumptions. The left hand capture group
  (enclosed by brackets) is not actually captured because it begins ``?:`` but
  is just used to make sure the right hand capture group starts at the right 
  place. 
* *Line 4-8* - If a match was found, ``video_id`` will be the contents of the 
  first (and only) capture group returned. Otherwise log the problem and give
  up, returning ``False`` to tell the addon that we couldn't resolve this URL.

.. _grab-json:

Grab JSON info for this video
-----------------------------

This section of code handles grabbing the URL of the JSON information and 
getting its contents.

* *Line 11-12* - Construct the URL to fetch using the ``video_id`` we found 
  earlier.
* *Line 13-18* - Use :class:`~t0mm0.common.net.Net` to grab the URL's content,
  catching the exception if we get an error (such as 404 not found). Again if 
  there is an error we log it and return ``False``.

.. _grab-url:

Find highest quality URL
------------------------

This section looks through the JSON and finds the best quality URL available.

Remember this from earlier:

.. code-block:: javascript
  
            "res": [{
                "d": false,
                "l": "240p",
                "u": "aHR0cDovL3MxMC52aWRlb2JiLmNvbTo4MC9zP3Y9OEZ2QUc2QVFwSGk4JnQ9MTMxMzIzOTczMCZ1PSZjPUIzOUQyOThBNzY0QkNGRTdDRThFNTExRkYyRjQ3MTFEOTY0MkRBMUJGOUNBNEQ2ODA5NDkwRkNGRTAyM0UwN0Mmcj0x"
            }, {
                "d": true,
                "l": "480p",
                "u": "aHR0cDovL3MxMC52aWRlb2JiLmNvbTo4MC9zP3Y9OEZ2QUc2QVFwSGk4JnQ9MTMxMzIzOTczMCZ1PSZjPUIzOUQyOThBNzY0QkNGRTdDRThFNTExRkYyRjQ3MTFEOTY0MkRBMUJGOUNBNEQ2ODA5NDkwRkNGRTAyM0UwN0Mmcj0y"
            }]
        }
    }
  
(this is the beautified version, the real thing is all on a single line)

* *Line 21* - We could have used 
  `simplejson <http://simplejson.github.com/simplejson/>`_ here but (despite its 
  name!) it would be more work than regular expressions. 
  
  We capture two values ``l`` which is the resolution, and ``u`` which is the 
  base64 encoded URL. We use :func:`re.finditer` because there may be more than
  one result which we want to loop through.
  
* *Line 22-23* - Set up some variables. ``chosen_res`` will keep track of the
  currently chosen resolution, and ``stream_url`` is set to ``False`` so that if
  the next few lines go wrong this method will return ``False`` and the addon 
  will know something went wrong.
  
* *Line 25* - Loop through all the matches we made.

* *Line 26* - Grab the two values from the capture groups for this match.

* *Line 27* - Remove any 'p' from the end of the resolution. This is just a 
  guess, because this JSON is not documented we can not tell what all the 
  possible resolutions are, but the only ones I have seen are '240p' and '480p'
  so i think it's safe to assume if there are any others they will probably end 
  in 'p'.
  
* *Line 28-30* If the resolution for this match is higher than our current 
  selection, set ``stream_url`` to be this URL (remember it is base64 encoded
  so we need to :func:`decode`) and update the value in ``chosen_res`` so we
  know what our currently chosen resolution is for the next time round the loop.
  
* *Line 32-33* - As usual, log the error and return ``False`` if the regular
  expression didn't match.
  
  
There you have it - a working plugin! Try it out with one of your test links in 
XBMC and you should see (as well as some video playing!) something like this in 
the log::

    23:43:30 T:2916084592 M:407699456  NOTICE: urlresolver: resolving using myvideobb plugin
    23:43:30 T:2916084592 M:405127168   DEBUG: t0mm0 test addon: resolved to: http://s200.videobb.com:80/s?v=8FvAG6AQpHi8&t=1313275412&u=&c=C08FDA7D2B03F3E262C00750C5984C809642DA1BF9CA4D6809490FCFE023E07C&r=2

Read the next section to see how to add a quality setting.
