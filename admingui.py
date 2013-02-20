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
import Tkinter as tki
import ttk
from editarea import EditArea
from scrollbox import Scrollbox, IndexedFrame
from edittabslideshow import EditTabSlideshow
from edittabvideo import EditTabVideo
from dmmanager import DataModelManager
from new import NewTab
from language import lang
import language as lng
from common import HylteSettings
from spmanager import spmanager
from progressdlg import DataModelLoader

#Test
import Tkinter, tkFileDialog
import os
import os.path
import shutil

_windowoffset = 30
_taskbaroffset = 100
_programname = 'Administration'

class AdminGui:
    def __init__(self, root, datamodel, wdir, config):
        self._root = root
        root.protocol("WM_DELETE_WINDOW", self._ehQuit)
        root.title(lang[lng.txtAdminTitle])
        
        settings = HylteSettings(config, (1, 1))

        #Initiate main window        
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight() - _taskbaroffset
        
        psize = settings.playersize
        psize = (min(psize[0], screenwidth), min(psize[1], screenheight))
        
        geom = "{}x{}+{}+{}".format(screenwidth, screenheight, 0, 0)
        root.geometry(geom)
        
        root.rowconfigure(0, weight = 1)
        root.columnconfigure(0, weight = 1)

        canvas = tki.Canvas(root)
        canvas.grid(row = 0, column = 0, sticky = 'nswe')
        
        hScroll = tki.Scrollbar(root, orient = tki.HORIZONTAL, command = canvas.xview)
        hScroll.grid(row=1, column=0, sticky='we')
        vScroll = tki.Scrollbar(root, orient = tki.VERTICAL, command = canvas.yview)
        vScroll.grid(row=0, column=1, sticky='ns')
        canvas.configure(xscrollcommand = hScroll.set, yscrollcommand = vScroll.set)
        frame = tki.Frame(canvas, bg = 'green')
        #frame.grid(row = 0, column = 0, sticky = 'wnes')
#
#        frame.rowconfigure(0, weight = 1)
#        frame.columnconfigure(0, weight = 1)
        
        #nb = ttk.Notebook(root, width = screenwidth, height = screenheight)

        canvas.create_window(0, 0, window = frame, anchor = 'nw')
        #nb = ttk.Notebook(frame, width = maxx, height = maxy)
        nb = ttk.Notebook(frame)
        #nb = ttk.Notebook(root)
        nb.grid(row = 0, column = 0, sticky = 'wnes')

#        frame.update_idletasks()
#        canvas.configure(scrollregion = (0, 0, frame.winfo_width(), frame.winfo_height()))
        
        #nb.pack(fill = tki.BOTH, expand = 1)
        
        print(wdir)
        
        ets = EditTabSlideshow(nb, wdir, datamodel, psize)
        etv = EditTabVideo(root, wdir, datamodel, psize)
        
        nt = NewTab(nb, ets, etv, nb)

        mb = DataModelManager(nb, datamodel, ets, etv, nb, wdir, psize)

        nb.add(nt, text = lang[lng.txtNew])
        nb.add(mb, text = lang[lng.txtManage])
        nb.add(ets, text = lang[lng.txtEditSlideshow])
        nb.add(etv, text = lang[lng.txtEditVideo])
        nb.tab(etv, state = 'disabled')
        
        #Add a dummy slideshow so the Notebook can calculate its width
        nb.tab(ets, state = 'normal')
        nb.select(2)
        ets.expandWidgets()
        nb.update_idletasks()

        maxheight = max(screenheight - int(hScroll['width']) - _windowoffset, nb.winfo_height())

        canvas.configure(scrollregion = (0, 0, nb.winfo_width(), maxheight))
        root.maxsize(nb.winfo_width() + int(hScroll['width']) + _windowoffset, maxheight + int(hScroll['width']) + _windowoffset)
        nb.configure(height = maxheight)
        ets.clear()
        nb.select(0)
        nb.tab(ets, state = 'disabled')
        self._dml = DataModelLoader(root, datamodel)
        root.after_idle(self._dml.load)

    def _ehQuit(self):
        """Terminate the application."""
        spmanager.save()
        self._root.destroy()
