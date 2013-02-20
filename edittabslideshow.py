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

from tooltip import ToolTip

from editarea import EditArea
from scrollbox import Scrollbox
from language import lang
import language as lng
from tkMessageBox import showerror
from playerdlg import showPlayerDialog
from soundbutton import SoundButton
import fileformat as ff

from datamodel import Frame as SFrame, tpSlideshow
import tkFileDialog
import os
import os.path
import shutil
import spmanager as spm
from edittab import EditTab

class EditTabSlideshow(EditTab):
    """A Frame for editing slideshows"""
    def __init__(self, parent, wdir, datamodel, psize):
        """Initiate
        
        Arguments
        parent -- parent tkinter item
        wdir -- working directory
        datamodel -- the database that is edited by the program
        psize -- tuple defining preview size of images
        
        """
        EditTab.__init__(self, parent, wdir, datamodel, psize)
        
        self._mediatype = tpSlideshow
        
        #Create variables for common data
        self._svBgSound = StringVar()

        #Make the first row expandable        
        self.rowconfigure(0, weight = 1)

        #Add frame from super class
        self._superFrame.grid(row = 0, column = 0, sticky = W + N)

        #Create the right column
        rightFrame = Frame(self)
        rightFrame.grid(row = 0, column = 1, pady = 10, sticky = N + S)
        rightFrame.rowconfigure(2, weight = 1)

        commonFrame = Frame(rightFrame)
        commonFrame.grid(padx = 5, pady = 5, sticky = W)
        commonFrame.columnconfigure(0, weight = 1)
        commonFrame.columnconfigure(1, weight = 1)
        commonFrame.columnconfigure(2, weight = 1)
        
        l = Label(commonFrame, text = lang[lng.txtBgSound])
        l.grid(row = 0, column = 0, padx = 10, sticky = W)
        e = Entry(commonFrame, w = 32, textvariable = self._svBgSound, state = "readonly")
        e.grid(row = 1, column = 0, padx = 10, sticky = W);
        tt = ToolTip(e, '', textvariable = self._svBgSound, wraplength = self._tooltipwidth)

        b = SoundButton(commonFrame, lang[lng.txtListen], lang[lng.txtStop], self._clbPlaying)
        self._btnListen = b
        b.grid(row = 1, column = 1, padx = 10, sticky = W + E)

        b = Button(commonFrame, text = lang[lng.txtSelect] + '...', command = self._ehGetBgSound)
        b.grid(row = 1, column = 2, padx = 10)
        self._btnSelect = b

        b = Button(commonFrame, text = lang[lng.txtDelete], state = DISABLED, command = self._ehRemoveSound)
        b.grid(row = 1, column = 3, padx = 10)
        self._btnRemove = b

        b = Button(rightFrame, text = lang[lng.txtNewFrame], command = self._ehNewFrame)
        b.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = W)

        sb = Scrollbox(self, rightFrame)
        self.scrollbox = sb
        sb.grid(row=2, column = 0, sticky = N + S + W, padx = 10, pady = 10)

    def open(self, slideshow, prepared = False):
        """Open a slideshow for editing
        
        Arguments
        slideshow -- the slideshow
        prepared -- if true, all media data is already copied to the working folder
                    (i.e. the slideshow has been created automatically)
        
        """
        EditTab.open(self, slideshow, prepared = prepared)
        
        if(not prepared):
            if(slideshow.bgsound != ''):
                shutil.copyfile(slideshow.getPath(slideshow.bgsound), os.path.join(self._wdir, slideshow.bgsound))

        self._svBgSound.set(slideshow.bgsound)

        if(slideshow.bgsound != ''):
            self._btnListen.setSound(os.path.join(self._wdir, slideshow.bgsound))
            self._btnRemove.config(state = NORMAL)
        
        for frame in slideshow.frames:
            ea = self.scrollbox.getWidget(EditArea, self._wdir, self._tooltipwidth, self._ehPlayThisFrame, self._ehPlayFromHere)
            ea.setFrame(frame, not prepared)
            
        self.setDirty(prepared)
        self.editing = True

    def expandWidgets(self):
        """Add a frame to the slideshow"""
        self._ehNewFrame()
        
    def clear(self):
        """Clear the edit tab"""
        EditTab.clear(self)
        self.scrollbox.clear()
        self._svBgSound.set('')

    def _getCurrentSlideshow(self, fromindex = None, oneindex = None):
        """Create and return a slideshow representing a subset of the currently
        edited slideshow. If no parameters are given, the entire slideshow
        will be returned. 
        
        Arguments
        fromindex -- if not None, the slideshow will contain all frames starting with fromindex
        oneindex -- if not None and fromindex is None, the slideshow will contain the frame at oneindex
        
        """
        slideshow = EditTab._getCurrentSlideshow(self)
        slideshow.bgsound = self._svBgSound.get()
        
        if(fromindex is not None):
            r = range(fromindex, len(self.scrollbox.widgets))
            
            for i in r:
                ea = self.scrollbox.widgets[i]
                frame = SFrame(slideshow, ea.getImage(), ea.getSound())
                slideshow.addFrame(frame)
        elif(oneindex is not None):
            ea = self.scrollbox.widgets[oneindex]
            frame = SFrame(slideshow, ea.getImage(), ea.getSound())
            slideshow.addFrame(frame)
        else:
            for ea in self.scrollbox.widgets:
                frame = SFrame(slideshow, ea.getImage(), ea.getSound())
                slideshow.addFrame(frame)
            
        return slideshow
    
    def _clbPlaying(self, isPlaying):
        """
        To be called when a sound is playing

        Argument
        isPlaying -- a sound is playing

        """
        
        if(isPlaying):
            newstate = DISABLED
        else:
            newstate = NORMAL

        self._btnSelect.config(state = newstate)
        self._btnRemove.config(state = newstate)

    def _setSound(self, filename = '', targetname = ''):
        """
        Set background sound
        If no sound is specified, the background sound will be removed

        Arguments
        filename -- filename
        targetsname -- filename including path to working directory        

        """
        self._svBgSound.set(filename)
        self.setDirty(True)
        self._btnListen.setSound(targetname)
        
        if(filename == ''):
            newstate = DISABLED
        else:
            newstate = NORMAL

        self._btnRemove.config(state = newstate)

    #Event handlers
    def _ehPlayThisFrame(self, ea):
        """Event handler intended to be used by a frame to play that frame
        
        Argument
        ea -- the EditArea where the event occurred
        
        """
        media = self._getCurrentSlideshow(oneindex = ea.index)
        showPlayerDialog(self._parent, self._psize, media)
    
    def _ehPlayFromHere(self, ea):
        """Event handler intended to be used by a frame to play all frames
        starting with that frame
        
        Argument
        ea -- the EditArea where the event occurred
        
        """
        media = self._getCurrentSlideshow(fromindex = ea.index)
        showPlayerDialog(self._parent, self._psize, media)

    def _ehNewFrame(self):
        """Event handler for new frame"""
        self.scrollbox.getWidget(EditArea, self._wdir, self._tooltipwidth, self._ehPlayThisFrame, self._ehPlayFromHere)
        self.setDirty(True)
        
    def _ehRemoveSound(self):
        """Remove background sound"""
        self._setSound()

    def _ehGetBgSound(self):
        """Event handler for assigning a background sound"""
        initdir = spm.spmanager.getFirstPath([spm.SoundFolder, 
                                              spm.ImageFolder, 
                                              spm.MostRecentFolder])
        
        sourcename = tkFileDialog.askopenfilename(initialdir = initdir, filetypes = ff.dlgSoundFormats)
        
        if(len(sourcename) > 0):
            filename = os.path.basename(sourcename)
            targetname = os.path.join(self._wdir, filename)

            try:
                shutil.copyfile(sourcename, targetname)
            except IOError:
                showerror(lang[lng.txtCopyError], lang[lng.txtCouldNotCopy] + os.path.basename(filename))
                return

            self._setSound(filename, targetname)
            spm.spmanager.setPath(spm.SoundFolder, os.path.dirname(sourcename))
