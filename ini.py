#    Copyright 2013 Regionbibliotek Halland
#
#    This file is part of Digitala sagor.
#
#    Digitala sagor is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Digitala sagor is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Digitala sagor.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os.path

delimiter = '|'

general = 'General'
fontname = 'fontname'
fontsize = 'fontsize'
datadir = 'datadir'
bgimage = 'bgimage'
fullscreen='fullscreen'

year = 'Year'
start = 'start'
space = 'space'
image = 'image'

moviescreen = 'Moviescreen'
left = 'left'
top = 'top'
width = 'width'
height = 'height'

preview = 'Preview'
columns = 'columns'
bordercolor = 'bordercolor'

controls = 'Controls'
prev = 'prev'
start = 'start'
next = 'next'

def getPath(path):
    """Return the full path of a file
    
    Argument
    path -- the path of the file, relative to the working directory
    
    """
    if(not os.path.isabs(path)):
        inidir = os.path.dirname(sys.argv[0])
        path = os.path.normpath(os.path.join(inidir, path))

    return path
