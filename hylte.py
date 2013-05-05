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
from Tkinter import Tk
from playergui import PlayerGui
from admingui import AdminGui
from datamodel import DataModel
from os import getcwd
import os.path
from sys import argv
import ConfigParser
from ConfigParser import NoOptionError
import codecs
import StringIO
import sys
import tempfile
import shutil
import ini
from spmanager import spmanager

#Inifile constants
_ininame = u'hylte.ini'
_inisection = u'Default'
_searchpathfilename = u'paths.ini'

def getConfigParser(inifile):
    """Return a ConfigParser given a unicode config file. 
    
    Arguments
    inifile -- the name of the inifile
    
    """
    
    if(os.path.exists(inifile)):
        parser = ConfigParser.ConfigParser()
        
        file = (codecs.open(inifile, "r", "utf8"))
        contents = file.read()
        file.close()
        
        #Workaround to remove the BOM from the contents - 
        #if the file is saved in UTF-8 without BOM it will work anyway;
        #if it is saved in UTF-8 (as Windows Notepad does) it will fail 
        #without this workaround
        if(ord(contents[0]) == 0xFEFF):
            contents = contents[1:]
            
        file = StringIO.StringIO(contents)
        parser.readfp(file)
        file.close()
        
        return parser
    else:
        return None


def main():
    """Load the inifile and start the player or the editor"""
    runhylte = True
    #Debug?
    fontsize = 12
    
    #Workaround for unicode in exefiles
    if hasattr(sys,"setdefaultencoding"):
        sys.setdefaultencoding("utf-8")
        print("setdefaultencoding")

    inidir = os.path.dirname(sys.argv[0])
    inifile = os.path.join(inidir, _ininame)
    
    if(os.path.exists(inifile)):
        parser = getConfigParser(inifile)
        #ConfigParser.ConfigParser()
        #parser.read(inifile)
        
        try:
            datadir = parser.get(ini.general, ini.datadir)
            width = parser.getint(ini.moviescreen, ini.width)
            height = parser.getint(ini.moviescreen, ini.height)
            playsize = (width, height)
            width = parser.getint(ini.preview, ini.width)
            height = parser.getint(ini.preview, ini.height)
            prevsize = (width, height)

        except NoOptionError as exc:
            print('Could not read ini file:', exc)
            return
        else:
            if(not os.path.isabs(datadir)):
                datadir = os.path.normpath(os.path.join(inidir, datadir))
    else:
        print('Inifile does not exist')
        return
            
            
    if(len(argv) > 1):
        runhylte = (argv[1].upper() != 'ADMIN')

    datamodel = DataModel(datadir, prevsize, playsize, True)

    try:
        wdir = tempfile.mkdtemp()
        root = Tk()

        if(runhylte):
            gui = PlayerGui(root, datamodel, parser)
        else:
            spmanager.load(os.path.normpath(os.path.join(inidir, _searchpathfilename)))
            gui = AdminGui(root, datamodel, wdir, parser)

        root.mainloop()
    
    finally:
        shutil.rmtree(wdir)
    
if __name__ == "__main__":
    main()
