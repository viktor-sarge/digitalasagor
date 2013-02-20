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

from language import lang
import language as lng
from playerdlg import showPlayerDialog
from datamodel import tpVideo
import tkFileDialog
import os
import os.path
import shutil
import spmanager as spm
from edittab import EditTab

_videoFileFormats = [('mp4', '*.mp4'), ('avi', '*.avi'), ('wmv', '*.wmv'), ('mpeg', '*.mpeg'), ('mov', '*.mov')]

class EditTabVideo(EditTab):
    """A Frame for editing video based stories"""
    def __init__(self, parent, wdir, datamodel, psize):
        """Initiate
        
        Arguments
        parent -- parent tkinter item
        wdir -- working directory
        datamodel -- the database that is edited by the program
        psize -- tuple defining preview size of videos
                
        """
        EditTab.__init__(self, parent, wdir, datamodel, psize)

        self._mediatype = tpVideo

        #Create variables for common data
        self._svVideo = StringVar()

        #Make the first row expandable        
        self.rowconfigure(0, weight = 1)

        #Add frame from super class
        self._superFrame.grid(row = 0, column = 0, sticky = W + N)

        #Create the right column
        rightLf = ttk.LabelFrame(self, text = ' ' + lang[lng.txtVideo] + ' ')
        rightLf.grid(row = 0, column = 1, pady = 10, sticky = W + N)
        rightFrame = Frame(rightLf)
        rightFrame.grid()

        e = Entry(rightFrame, w = 32, textvariable = self._svVideo, state = "readonly")
        e.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = W);

        tt = ToolTip(e, '', textvariable = self._svVideo, wraplength = parent.winfo_screenwidth() * 4 / 5)

        b = Button(rightFrame, text = lang[lng.txtSelect] + '...', command = self._ehGetVideo)
        b.grid(row = 0, column = 1, padx = 10, pady = 5)

        b = Button(rightFrame, text = lang[lng.txtWatch], command = self._ehWatch)
        b.grid(row = 0, column = 2, padx = 10, pady = 5)

    def open(self, slideshow, prepared = False):
        """Open a slideshow for editing
        
        Arguments
        slideshow -- the slideshow
        prepared -- if true, all media data is already copied to the working folder
                    (i.e. the slideshow has been created automatically)
        
        """
        EditTab.open(self, slideshow, prepared = False)

        if(not prepared):
            if(slideshow.video != ''):
                shutil.copyfile(slideshow.getPath(slideshow.video), os.path.join(self._wdir, slideshow.video))

        self._svVideo.set(slideshow.video)

    def clear(self):
        """Clear the edit tab"""
        EditTab.clear(self)
        self._svVideo.set('')

    def _getCurrentSlideshow(self):
        """Create and return a slideshow representing the currently edited slideshow."""
        slideshow = EditTab._getCurrentSlideshow(self)
        slideshow.video = self._svVideo.get()

        return slideshow        
        
    #Event handlers
    def _ehGetVideo(self):
        """Event handler for assigning a video"""
        initdir = spm.spmanager.getFirstPath([spm.VideoFolder, 
                                              spm.MostRecentFolder])
        
        filenamepath = tkFileDialog.askopenfilename(initialdir = initdir, filetypes = _videoFileFormats)
        
        if(len(filenamepath) > 0):
            filename = os.path.basename(filenamepath)

            try:
                shutil.copyfile(filenamepath, os.path.join(self._wdir, filename))
            except IOError:
                showerror(lang[lng.txtCopyError], lang[lng.txtCouldNotCopy] + os.path.basename(filename))
                return

            self._svVideo.set(filename)
            self.setDirty(True)
            spm.spmanager.setPath(spm.VideoFolder, os.path.dirname(filenamepath))

    def _ehWatch(self):
        """Event handler for preview of the video"""
        media = self._getCurrentSlideshow()
        showPlayerDialog(self._parent, self._psize, media)
