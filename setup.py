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
from distutils.core import setup
import py2exe, sys, os

#Fix for pygame
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("libogg-0.dll", "sdl_ttf.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

setup(console = ['hylte.py'], options={"py2exe":{"dll_excludes":[ "mswsock.dll", "powrprof.dll" ]}})
