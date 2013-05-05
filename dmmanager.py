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
from Tkinter import Button, Frame, W, N, NORMAL, DISABLED
from tkMessageBox import showerror

from language import lang
import language as lng
import packfile
import tkMessageBox

from dmbrowser import DataModelBrowser
from importdlg import showImportDlg
from datamodel import tpVideo
from playerdlg import showPlayerDialog

class DataModelManager(DataModelBrowser):
    """Manage a Digitala Sagor database"""
    def __init__(self, parent, datamodel, edittabslideshow, edittabvideo, notebook, wdir, psize):
        """Initiate
        
        Arguments
        parent -- parent tkinter item
        datamodel -- the database to manage
        edittabslideshow -- edit tab for slideshows
        edittabvideo -- edit tab for videos
        notebook -- the Notebook where the tabs are located
        wdir -- the working directory
        psize -- size of previewed images and videos
        
        """
        DataModelBrowser.__init__(self, parent, datamodel)
        
        self._edittabslideshow = edittabslideshow
        self._edittabvideo = edittabvideo
        self._notebook = notebook
        self._wdir = wdir
        self._psize = psize
        
        controlframe = Frame(self._gbselected)
        controlframe.grid()#(row = 1, column = 1, sticky = W + N)
        b = Button(controlframe, text = lang[lng.txtEdit], command = self._ehEdit)
        self._btnEdit = b
        b.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W + N)
        b = Button(controlframe, text = lang[lng.txtPlay] + '...', command = self._ehPlay)
        self._btnPlay = b
        b.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = W + N)
        
        controlframe = Frame(self._gbselection)
        controlframe.grid()#(row = 1, column = 1, sticky = W + N)
        b = Button(controlframe, text = lang[lng.txtDelete], command = self._ehDelete)
        self._btnDelete = b
        b.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W + N)
        b = Button(controlframe, text = lang[lng.txtExport] + '...', command = self._ehExport, state = DISABLED)
        self._btnExport = b
        b.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = W + N)

        controlframe = Frame(self._gbdb)
        controlframe.grid()#(row = 1, column = 1, sticky = W + N)
        b = Button(controlframe, text = lang[lng.txtImport] + '...', command = self._ehImport)
        self._btnImport = b
        b.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W + N)
        
        #Add callback to make sure the list box is updated when an item is saved
        edittabslideshow.clbSave = self._populateListbox
        self._populateListbox()
              
    def _getSelectedItem(self, updateGui = False):
        """Return the first selected item and optionally update the GUI
        
        Argument
        updateGui -- if true, the GUI will be updated with information 
                     about the current selection
        
        """
        result = DataModelBrowser._getSelectedItem(self, updateGui)
        self._updateGuiState(result is not None)
        return result

    def _updateGuiState(self, selectionExists):
        """Update the state of the GUI
        
        Argument
        selectionExists -- at least one item is selected in the listbox
        
        """
        if(selectionExists):
            selstate = NORMAL
        else:
            selstate = DISABLED
        
        self._btnExport.config(state = selstate)
        self._btnEdit.config(state = selstate)
        self._btnDelete.config(state = selstate)
        self._btnPlay.config(state = selstate)

    #Event handlers
    def _ehEdit(self):
        """Edit an item"""
        item = self._getSelectedItem()
                
        if(item is not None):
            if(item.type == tpVideo):
                edittab = self._edittabvideo
            else:
                edittab = self._edittabslideshow

            if(edittab.isOkToOpen()):
                try:
                    edittab.open(item)
                except:
                    showerror(lang[lng.txtOpenError], lang[lng.txtCouldNotOpen] + item.title)
                    edittab.clear()
                    return

                self._notebook.tab(edittab, state = 'normal')
                self._notebook.select(edittab)

    def _ehPlay(self):
        """Preview an item"""
        item = self._getSelectedItem()
        
        if(item is not None):
            showPlayerDialog(self._parent, self._psize, item)

    def _ehDelete(self):
        """Delete an item"""
        response = tkMessageBox.askyesno(lang[lng.dlgDelSShowTitle], lang[lng.dlgDelSShow], parent = self._parent)
        
        if(not response):
            return
        
        selection = self._listbox.curselection()
        
        if(selection == ()):
            return
        
        for s in selection:
            self._datamodel.deleteSlideshow(self._contents[s])

        self._datamodel.saveToFile()
        self._populateListbox()
        self._displayInfo()
        
    def _ehImport(self):
        """Import a database"""
        dm = packfile.getImportDm(self._wdir)
        
        if(dm is None):
            return
        
        dm.setPrevsize(self._datamodel.getPrevsize())
        dm.setPlaysize(self._datamodel.getPlaysize())

        items = showImportDlg(self._parent, dm, self._psize)

        if(len(items) <= 0):
            return
        
        for i in items:
            if(not self._datamodel.addSlideshow(i)):
                showerror(lang[lng.txtCorruptImportTitle], lang[lng.txtCouldNotImportSlideshow] + i.title)

        self._datamodel.saveToFile()
        self._populateListbox()

    def _ehExport(self):
        """Export the currently selected items"""
        #Get items to export
        selection = self._listbox.curselection()
        
        if(selection == ()):
            return
        
        items = []
        
        for s in selection:
            items.append(self._contents[s])
        
        packfile.export(items, self._wdir)
