#!/usr/bin/env python
"""
    urlresolver XBMC Addon
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
"""

import sys
import urlresolver

username = sys.argv[1]
password = sys.argv[2]

print urlresolver.resolve('http://www.novamov.com/video/kdshwq2cj6vxv')
print urlresolver.resolve('http://www.putlocker.com/file/DFE7599AE064911A')
print urlresolver.resolve('http://seeon.tv/view/14451')
print urlresolver.resolve('http://www.megaupload.com/?d=TQPQJM5H')
print urlresolver.resolve('http://www.megaupload.com/?d=3V1W8ATM', username, password)

