Overview
========

``script.module.urlresolver`` is a XBMC addon which provides a URL resolving 
service to other addons. It exposes a simple interface (:mod:`urlresolver`)
whcih allows other addons to send it a URL to webpage associated with a piece
of media content, which :mod:`urlresolver` then transforms into a direct URL to 
the actual media file. These addons do not need to know anything about the file 
hosts or even which host is being used.

This makes it very easy to make addons which point to files(or streams) hosted 
on a wide variety of filehosting services. It also allows plugins to be written 
to extend functionality by supporting new file hosts or streaming sites. Once
a resolver plugin is written and installed, it is then available to any addon
which uses :mod:`urlresolver`.

This tutorial will show you how to make a new plugin to support a file host.
We will be building a fully functional plugin to allow the resolving of URLs
hosted at http://videobb.com (which is included in 
``script.module.urlresolver``) from analysing the site to writing and testing
the code.

This module will be much more useful if many developers provide resolver 
plugins (I do not have time to write plugins for every site!), so I have tried 
to make resolver plugins as simple as possible to write. However if you can 
think of any improvements don't hesitate to get in touch with me via the 
project site at https://github.com/t0mm0/xbmc-urlresolver.

Tools
-----

So the first thing to do is to make sure you have the required tools. Luckily 
this is normally pretty straightforward! For most sites you will be able to
work out what is going on from looking at the HTML source and monitoring what
files are downloaded by the page. For both of these, I use 
`Google Chrome <http://www.google.co.uk/chrome>`_ and so this is what I will
describe, but the same things can be accomplished using 
`Firefox <http://getfirefox.com>`_ with the `Firebug <http://getfirebug.com>`_
plugin. 

Sometimes (although not required for this site) if the site uses the 
rtmp protocol `rtmpdump, rtmpsrv and rtmpsuck <http://rtmpdump.mplayerhq.hu/>`_
are very useful tools.


