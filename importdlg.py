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
from Tkinter import *
import ttk

from language import lang
import language as lng
import dialog
from playerdlg import showPlayerDialog
from dmbrowser import DataModelBrowser

class DataModelImportDialog(DataModelBrowser):
    """A data model browser that displays a Digitala Sagor database in read-only mode"""
    def __init__(self, parent, impDatamodel, selection, psize):
        """Initiate
        
        Arguments
        parent -- the parent tkinter item
        impDatamodel -- the database to display
        selection -- list to which selected items will be added
        psize -- size of previewed images and videos
        
        """
        DataModelBrowser.__init__(self, parent, impDatamodel)
        
        self._impdm = impDatamodel
        self._selection = selection
        self._psize = psize

        self.grid(row = 0, column = 0)
        controlframe = Frame(self._gbselected)
        controlframe.grid()#(row = 1, column = 1, sticky = W + N)
        b = Button(controlframe, text = lang[lng.txtPlay] + '...', command = self._ehPlay)
        self._btnPlay = b
        b.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W + N)

        control = Frame(self)
        control.grid(row = 1, column = 1, sticky = E)
        b = Button(control, text = lang[lng.txtCancel], command = self._ehCancel)
        b.grid(row = 0, column = 0, padx = 10, pady = 10)
        b = Button(control, text = lang[lng.txtImport], command = self._ehImport)
        self._btnImport = b
        b.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        self._populateListbox()
        
    def _updateGuiState(self, selectionExists):
        """Update the state of the GUI
        
        Argument
        selectionExists -- at least one item is selected in the listbox
        
        """
        if(selectionExists):
            selstate = NORMAL
            self._clearSelection()
            selection = self._listbox.curselection()
            
            for s in selection:
                self._selection.append(self._contents[s])

        else:
            selstate = DISABLED
        
        self._btnPlay.config(state = selstate)
        self._btnImport.config(state = selstate)

    def _clearSelection(self):
        """Remove items from the return list"""
        while(len(self._selection) > 0):
            self._selection.pop()

    #Event handlers
    def _ehImport(self):
        """The import button has been pressed"""
        self._parent.destroy()
        
    def _ehCancel(self):
        """The cancel button has been pressed"""
        self._clearSelection()
        self._ehImport()
        
    def _ehPlay(self):
        """The play button has been pressed"""
        showPlayerDialog(self._parent, self._psize, self._getSelectedItem())

def showImportDlg(root, impDatamodel, psize):
    """Show an import dialog and return the selected items"""
    result = []
    
    dlg = dialog.getDlg(root, lang[lng.txtImport])
    dmid = DataModelImportDialog(dlg, impDatamodel, result, psize)
    dialog.showDlg(dlg)
    
    return result
