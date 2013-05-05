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
from tkMessageBox import askyesnocancel, showerror

from datamodel import DataModel, Slideshow
import os
import os.path
import shutil
import packfile
from common import validateText

_maxTitleLen = 24

class EditTab(Frame):
    """Abstract class for editing slideshows; sub classes should add 
    their own GUI elements together with _superFrame"""
    def __init__(self, parent, wdir, datamodel, psize):
        """Initiate
        
        Arguments
        parent -- parent tkinter item
        wdir -- working directory
        datamodel -- the database that is edited by the program
        psize -- tuple defining preview size of images
        
        """
        Frame.__init__(self, parent)
        
        self._parent = parent
        self._wdirbase = wdir
        self._wdir = ''
        self._masterdm = datamodel
        self._psize = psize
        self.editdatamodel = DataModel(wdir, datamodel.getPrevsize(), datamodel.getPlaysize())
        self._activeuid = None
        self._category = ''
        self.clbSave = None
        
        self._tooltipwidth = parent.winfo_screenwidth() * 4 / 5
        
        #Create variables for common data
        self._svTitle = StringVar()
        self._svAuthor = StringVar()
        self._svGroup = StringVar()
        self._svSaveBtn = StringVar()

        #Create fields for common properties and buttons for save/export
        superFrame = Frame(self)
        self._superFrame = superFrame
        leftLF = ttk.LabelFrame(superFrame, text = ' ' + lang[lng.txtCommon] + ' ')
        commonFrame = Frame(leftLF)
        commonFrame.grid(padx = 5, pady = 5, sticky = W + E)
        commonFrame.columnconfigure(0, weight = 1)

        l = Label(commonFrame, text = lang[lng.txtTitle])
        l.grid(row = 2, column = 0, padx = 10, sticky = W)
        tcmd = (parent.register(self._ehOnValidateTitle), '%d', '%s', '%S')
        e = Entry(commonFrame, w = 32, validate = "key", validatecommand = tcmd, textvariable = self._svTitle)
        e.grid(row = 3, column = 0, padx = 10, sticky = W)

        l = Label(commonFrame, text = lang[lng.txtAuthor])
        l.grid(row = 4, column = 0, padx = 10, sticky = W)

        e = Entry(commonFrame, w = 32, validate = "key", validatecommand = tcmd, textvariable = self._svAuthor)
        e.grid(row = 5, column = 0, padx = 10, sticky = W);
        
        l = Label(commonFrame, text = lang[lng.txtGroup])
        l.grid(row = 6, column = 0, padx = 10, sticky = W)

        e = Entry(commonFrame, w = 32, validate = "key", validatecommand = tcmd, textvariable = self._svGroup)
        e.grid(row = 7, column = 0, padx = 10, sticky = W);
        
        l = Label(commonFrame, text = lang[lng.txtDesc])
        l.grid(row = 8, column = 0, padx = 10, sticky = W)

        t = Text(commonFrame, width = 32, height = 8, wrap = WORD)
        self._tDesc = t
        t.grid(row = 9, column = 0, columnspan = 3, padx = 10, sticky = W + E)
        t.bind('<Key>', self._ehKey)
                
        leftLF.grid(row = 0, column = 0, columnspan = 2, sticky = N + W + E, padx = 10, pady = 10)
        
        bframe = Frame(superFrame) 
        bframe.grid(row = 1, column = 0, sticky = W)
        
        b = Button(bframe, textvariable = self._svSaveBtn, command = self._ehSave)
        b.grid(row = 0, column = 0, padx = 10, sticky = W)
        
        b = Button(bframe, text = lang[lng.txtExport] + '...', command = self._ehExport)
        b.grid(row = 0, column = 1, sticky = W)

        self.setDirty(False)
        self.editing = False

    def open(self, slideshow, prepared = False):
        """Open a slideshow for editing
        
        Arguments
        slideshow -- the slideshow
        prepared -- if true, all media data is already copied to the working folder
                    (i.e. the slideshow has been created automatically)
        
        """
        self._wdir = os.path.join(self._wdirbase, slideshow.uid)
        self._activeuid = slideshow.uid
        self._category = slideshow.category

        if(not prepared):
            if(os.path.exists(self._wdir)):
               shutil.rmtree(self._wdir)

            os.makedirs(self._wdir)

        self._svTitle.set(slideshow.title)
        self._svAuthor.set(slideshow.author)
        self._svGroup.set(slideshow.group)
        self._tDesc.insert(INSERT, slideshow.description)

        self.setDirty(prepared)
        self.editing = True

    def isOkToOpen(self):
        """Return if it is ok to open another slideshow. If there are unsaved
        changes a yes/no/cancel dialog will be shown."""
        if(self._dirty):
            response = askyesnocancel(lang[lng.dlgUnsavedTitle], lang[lng.dlgUnsaved], parent = self)
          
            if(response is None):
                return False
            elif(response):
                self._save()
            
            self.clear()            
        elif(self.editing):
            self.clear()

        return True

    def setDirty(self, dirty):
        """Update the state of unsaved changes
        
        Argument
        dirty -- the state of unsaved changes
        
        """
        self._dirty = dirty
        text = lang[lng.txtSave]

        if(dirty):
            text = text + '*'

        self._svSaveBtn.set(text)

    def clear(self):
        """Clear the edit tab"""
        self._svTitle.set('')
        self._svAuthor.set('')
        self._svGroup.set('')
        self._tDesc.delete(1.0, END)
        if(os.path.exists(self._wdir) and not os.listdir(self._wdir)):
            shutil.rmtree(self._wdir)
        self.setDirty(False)
        self.editing = False

    def _save(self):
        """Save the currently opened slideshow"""
        slideshow = self._getCurrentSlideshow()

        if(self._masterdm.addSlideshow(slideshow)):
            self._masterdm.saveToFile()
        else:
            showerror(lang[lng.txtSaveError], lang[lng.txtCouldNotSave] + slideshow.title)
            return

        self.setDirty(False)

    def _getCurrentSlideshow(self):
        """Create and return the currently edited slideshow."""
        slideshow = Slideshow(self.editdatamodel, uid = self._activeuid, type = self._mediatype)
        slideshow.title = self._svTitle.get()
        slideshow.author = self._svAuthor.get()
        slideshow.group = self._svGroup.get()
        slideshow.category = self._category
        slideshow.description = self._tDesc.get(0.0, END)
            
        return slideshow

    #Event handlers
    def _ehKey(self, event):
        """Event handler for key events
        
        Argument
        event -- dummy event object
        
        """
        self.setDirty(True)

    def _ehSave(self):
        """Event handler for saving the slideshow"""
        self._save()
        if(self.clbSave is not None):
            self.clbSave()

    def _ehExport(self):
        """Event handler for exporting the slideshow"""
        item = [self._getCurrentSlideshow()]        
        packfile.export(item, self._wdirbase)

    def _ehOnValidateTitle(self, d, s, S):
        """Event handler for validating a text input to an entry
        
        Arguments
        d -- type of action
        s -- value of entry prior to editing
        S -- the text string being inserted or deleted, if any

        """
        result = validateText(d, s, S, _maxTitleLen)

        if(result):
            self.setDirty(True)

        return result
