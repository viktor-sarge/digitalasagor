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

from language import lang
import language as lng
import dialog
import thread

class _ProgressDialog(tki.Frame):
    """A Frame intended to be placed in a Toplevel object. 
    
    This class will load the images of a datamodel, visualize the progress and 
    then close the Toplevel window. It will not be possible to abort the 
    load operation by closing the Toplevel. 
    
    """
    def __init__(self, toplevel, datamodel):
        """Initiate and make a pending call to _load()
        
        Arguments
        toplevel -- Toplevel object in which this Frame will be placed
        datamodel -- datamodel in which to load the images

        """
        tki.Frame.__init__(self, toplevel)

        self._parent = toplevel
        self._datamodel = datamodel
        self._progresstext = tki.StringVar()
        
        self.grid()
        self.rowconfigure(1, weight = 1)

        l = tki.Label(self, textvariable = self._progresstext)
        l.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tki.W)
        pbar = ttk.Progressbar(self, orient = tki.HORIZONTAL, length = 400, mode = 'determinate', maximum = 1.0)
        self._pbar = pbar
        pbar.grid(row = 1, column = 0, columnspan = 2,  padx = 5, pady = 5, sticky = tki.W + tki.E)
        toplevel.after_idle(self._load)
        toplevel.protocol("WM_DELETE_WINDOW", self._dontquit)

    def _updateBar(self, progress):
        """Callback function to Datamodel.loadImageData
        
        Argument
        progress -- current load progress; 0.0 <= progress <= 1.0
        
        """
        self._pbar.config(value = progress)
        self._progresstext.set(lang[lng.txtLoadImageProgress].format(progress))
        
    def _load(self):
        """Start the load operation by launching a thread"""
        thread.start_new(self._thrLoadImages, (self, None))
        
    def _thrLoadImages(self, dummy, d2):
        """Perform the load operation and make a pending call to _quit
        
        Arguments
        dummy -- unused
        d2 -- unused
        
        """
        self._datamodel.loadImageData(self._updateBar)
        self._pbar.config(value = 1)
        self._parent.after_idle(self._quit)

    def _dontquit(self):
        """Event handler for WM_DELETE_WINDOW that does nothing"""
        pass

    def _quit(self):
        """Close the Toplevel object"""
        self._parent.destroy()

class DataModelLoader:
    """Display a progress bar while loading a datamodel"""
    
    def __init__(self, root, datamodel):
        """Initiate
        
        Arguments
        root -- Tk object
        datamodel -- datamodel in which to load the images
        previewsize -- tuple containing dimensions for preview images
        playersize -- tuple containing dimensions for playback images
        
        """
        self._root = root
        self._datamodel = datamodel

    def load(self):
        """Load the images in the datamodel while displaying a progress dialog"""
        
        if(self._datamodel.isEmpty()):
            return

        dlg = dialog.getDlg(self._root, lang[lng.dlgLoadImages])
        pd = _ProgressDialog(dlg, self._datamodel)
        dialog.showDlg(dlg)
