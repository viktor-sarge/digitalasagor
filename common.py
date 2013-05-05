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
import ini

_defaultMaxLength = 24

def updateProgress(prog):
    """Simple progress indicator; will output progress to standard output
    
    Argument
    prog -- the current progress
    
    """
    print(str(prog) + ' %')
    
def scale(value, factor):
    """Scale a value and round the result

    Arguments
    value -- the value to scale
    factor -- scale factor

    """
    return int(value * factor + 0.5)

def scaleTuple(values, factors):
    """Scale a two dimensional tuple and round the result

    Arguments
    values -- the value to scale
    factors -- scale factors

    """
    x = int(values[0] * factors[0] + 0.5)
    y = int(values[1] * factors[1] + 0.5)

    return (x, y)

def validateText(d, s, S, maxlength):
    """Validate a text

    Arguments
    d -- type of action
    s -- value of entry prior to editing
    S -- the text string being inserted or deleted, if any
    maxlength -- maximum allowed textlength

    """
    try:
        maxlength = int(maxlength)
    except ValueError:
        maxlength = _defaultMaxLength

    if(d == '0'):
        result = True
    elif((S is not None)):
        result = (len(S + s) <= maxlength)
    else:
        result = False

    return result

class HylteSettings:
    """Store ini settings for Digitala sagor"""
    def __init__(self, config, scalefactor):
        """Read the settings
        
        Arguments
        config -- a ConfigParser containing the settings
        scalefactor -- a tuple containing an x,y scale factor for the graphics
        
        """
        playerpos = (config.getint(ini.moviescreen, ini.left), config.getint(ini.moviescreen, ini.top))
        self.playerpos = scaleTuple(playerpos, scalefactor)

        playersize = (config.getint(ini.moviescreen, ini.width), config.getint(ini.moviescreen, ini.height))
        self.playersize = scaleTuple(playersize, scalefactor)

        previewsize = (config.getint(ini.preview, ini.width), config.getint(ini.preview, ini.height))
        self.previewsize = scaleTuple(previewsize, scalefactor)
        
        self.previewcolumns = config.getint(ini.preview, ini.columns)
        self.bordercolor = config.get(ini.preview, ini.bordercolor)

        fontname = config.get(ini.general, ini.fontname)
        fontsize = config.getint(ini.general, ini.fontsize)
        fontsize = scale(fontsize, scalefactor[1])
        self.generalfont = (fontname, fontsize)
