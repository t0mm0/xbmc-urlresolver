Analyse the Target Site
=======================

The first step in writing a resolver plugin (after choosing the site of 
course!) is to analyse the target site to see how it works. Remember, your
plugin will be passed a URL to a web page on your target site and your code
must be able to turn that into the direct URL to the media file or stream.

First Look
----------

Our target site is http://videobb.com so let's start by looking at a video on
that site.

The front page contains links to some videos so that is probably a good place
to start. Notice they are in the form ``http://videobb.com/video/{VIDEO_ID}`` so
this is definitely going to be a pattern we want to advertise our plugin as
capable of handling. The video id seems to comprise of numbers and both lower
and upper case letters (or in regex terms ``[0-9A-Za-z]``).

Clicking on one of these links (I chose http://videobb.com/video/8FvAG6AQpHi8) 
notice that you get diverted to 
``http://videobb.com/watch_video.php?v={VIDEO_ID}`` (in my case 
http://videobb.com/watch_video.php?v=8FvAG6AQpHi8). Another pattern we'll
want to be able to handle.

Are We Human?
-------------

Notice there appears to be no 'Are you human?' verification that there is with 
many sites. This could be because we have clicked through from their front page
which may have set a cookie or the referrer header to the right value.

Lets test that out. Start by opening an incognito window of Chrome. This is a 
handy trick to ensure that no cookies are left over from previous visits without
having to keep clear them out.

Now paste the URL to the video page 
(http://videobb.com/watch_video.php?v=8FvAG6AQpHi8) into the URL bar and hit 
enter. Looks like it works so I guess they don't do any checking at all - nice!

If you find your host does require that you prove you are human, often this is 
just a case of sending some cookies, or posting some form values.

Finding the Media URL
---------------------

Now the fun part!

Open the developer tools of Chrome (Shift + Ctrl + I), open the 'Network' tab 
and reload the page. You should see a list of all the files that page loads. 

Click on the play button of the flash video and you'll see some extra activity 
in the network tab.

.. figure::  /images/rp1.png
    :align:  center

    Spot the useful file....
    
Ah, one of those has a mime type of ``video/x-flv`` - that has to be our video!
Clicking on that entry shows that the request URL is 
``http://s153.videobb.com/s?v=8FvAG6AQpHi8&r=2&t=1313232595&u=&c=11885AACE290D85BA5F8CB5B6430028F9642DA1BF9CA4D6809490FCFE023E07C&start=0``.

It looks like ``t`` is a Unix timestamp, and ``c`` looks like an access token, 
so this will probably be different for you. Indeed you can try reloading the 
page and pressing play again and you'll see the URL is different.

Where is it Hidden?
-------------------

A quick search of the page source shows that this URL isn't just included in the
HTML. I guess they didn't want to make it *too* easy.

Looking through the HTML of the page (use the 'Resources' tab) you can see 
where the code is to embed the flash player, so lets take a look at that:

.. code-block:: html

  <div class="flashframe">
    <div class="video_player" id="videoPlayer">
      <script type="text/javascript">
      swfobject.registerObject("base", "9.0.0", "/player/expressInstall.swf");
      </script>
      <object width="982" height="462" id="base" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" style="visibility: visible;">
        <param value="/player/player.swf?pv=1_1_78" name="movie">
        <param value="setting=aHR0cDovL3ZpZGVvYmIuY29tL3BsYXllcl9jb250cm9sL3NldHRpbmdzLnBocD92PThGdkFHNkFRcEhpOA==" name="FlashVars">
        <param value="true" name="allowfullscreen">
        <param value="always" name="allowscriptaccess">
        <param value="transparent" name="wmode">
        <embed src="/player/player.swf?pv=1_1_78" flashvars="setting=aHR0cDovL3ZpZGVvYmIuY29tL3BsYXllcl9jb250cm9sL3NldHRpbmdzLnBocD92PThGdkFHNkFRcEhpOA==" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="982" height="462" wmode="transparent" name="ESAHDMP"></embed>
      </object>
    </div>
  </div>

Notice the ``value="setting=aHR0cDovL3ZpZGVvYmIu....`` part? This looks 
suspiciously like a `base64 <http://en.wikipedia.org/wiki/Base64>`_ encoded URL
(the ``=`` used as padding at the end are a giveaway, although not always 
present in a base64 encoded string, and strings staring with 'http://' will 
always encode to a value starting 'aHR0cD...').

We can check this out using an online decoder such as 
http://base64decode.org/, or even using the python interactive interpretor::

    >>> 'aHR0cDovL3ZpZGVvYmIuY29tL3BsYXllcl9jb250cm9sL3NldHRpbmdzLnBocD92PThGdkFHNkFRcEhpOA=='.decode('base-64')
    'http://videobb.com/player_control/settings.php?v=8FvAG6AQpHi8'

Looks like we will be able to generate that URL without having to load the video 
page. Lets see what it contains. If you load that URL in the browser you'll see
it is `JSON <http://en.wikipedia.org/wiki/JSON>`_ encoded. To make it easier to 
read, use 'view source' and copy and paste the entire source code into 
`jsbeautifier.org <http://jsbeautifier.org>`_.

There is all sorts of interesting and not-so-interesting stuff in there, but
lets look right at the very bottom where you find:

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
    
More base64 encoded URLs? Perhaps one for each different quality? Lets try::

    >>> 'aHR0cDovL3MxMC52aWRlb2JiLmNvbTo4MC9zP3Y9OEZ2QUc2QVFwSGk4JnQ9MTMxMzIzOTczMCZ1PSZjPUIzOUQyOThBNzY0QkNGRTdDRThFNTExRkYyRjQ3MTFEOTY0MkRBMUJGOUNBNEQ2ODA5NDkwRkNGRTAyM0UwN0Mmcj0x'.decode('base-64')
    'http://s10.videobb.com:80/s?v=8FvAG6AQpHi8&t=1313239730&u=&c=B39D298A764BCFE7CE8E511FF2F4711D9642DA1BF9CA4D6809490FCFE023E07C&r=1'
    >>> 'aHR0cDovL3MxMC52aWRlb2JiLmNvbTo4MC9zP3Y9OEZ2QUc2QVFwSGk4JnQ9MTMxMzIzOTczMCZ1PSZjPUIzOUQyOThBNzY0QkNGRTdDRThFNTExRkYyRjQ3MTFEOTY0MkRBMUJGOUNBNEQ2ODA5NDkwRkNGRTAyM0UwN0Mmcj0y'.decode('base-64')
    'http://s10.videobb.com:80/s?v=8FvAG6AQpHi8&t=1313239730&u=&c=B39D298A764BCFE7CE8E511FF2F4711D9642DA1BF9CA4D6809490FCFE023E07C&r=2'


Paste these URLs (well, the ones you get as these ones will have expired!) into 
your favourite media player and you should see video!

What Do We Know?
----------------

At this stage, we now have enough info to write our plugin.

We know some URL patterns that we can resolve, we know what URL we need to 
retrieve in order to find the media URLs 
(``http://videobb.com/player_control/settings.php?v={VIDEO_ID}``), 
and we know how the media URLs are encoded (base64).

Time to move on and write some code!
