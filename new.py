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
import datetime

from editarea import EditArea
from scrollbox import Scrollbox
from language import lang
import language as lng
import datamodel as dm
import tkFileDialog
import os
import os.path
import shutil
import fileformat as ff
import spmanager as spm

class NewTab(Frame):
    """A Frame for creating new slideshows"""
    def __init__(self, parent, edittabslideshow, edittabvideo, nb):
        Frame.__init__(self, parent)
        
        self._edittabslideshow = edittabslideshow
        self._edittabvideo = edittabvideo
        self._notebook = nb
        
        gb = ttk.Labelframe(self, text = ' ' + lang[lng.txtNew] + ' ')
        gb.grid(padx = 50, pady = 50)
        
        b = Button(gb, text = lang[lng.txtNewEmpty], command = self._ehNewFromScratch)
        b.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = W + E)
        b = Button(gb, text = lang[lng.txtNewVideo], command = self._ehNewVideo)
        b.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = W + E)
        b = Button(gb, text = lang[lng.txtNewFromFolder] + '...', command = self._ehNewFromFolder)
        b.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = W + E)
        
    def _openNew(self, slideshow, tab, prep):
        """Open a new slideshow
        
        Arguments
        slideshow -- the newly created slideshow
        tab -- the tab to open (i.e. slideshow or video)
        prep -- if the files of the slideshow are already prepared
        
        """
        tab.open(slideshow, prepared = prep)
        self._notebook.tab(tab, state = 'normal')
        self._notebook.select(tab)

    def _ehNewFromScratch(self):
        """Create a new slideshow unless the user aborts the operation"""
        if(not self._edittabslideshow.isOkToOpen()):
            return

        slideshow = dm.Slideshow(self._edittabslideshow.editdatamodel, category = str(datetime.datetime.now().year))
        self._openNew(slideshow, self._edittabslideshow, False)

    def _ehNewVideo(self):
        """Create a new video slideshow unless the user aborts the operation"""
        if(not self._edittabvideo.isOkToOpen()):
            return

        slideshow = dm.Slideshow(self._edittabvideo.editdatamodel, category = str(datetime.datetime.now().year))
        self._openNew(slideshow, self._edittabvideo, False)

    def _ehNewFromFolder(self):
        """Create a new slideshow from a folder unless the user aborts the operation"""
        if(not self._edittabslideshow.isOkToOpen()):
            return
        
        initdir = spm.spmanager.getFirstPath([spm.SlideshowFolder, 
                                              spm.ImageFolder, 
                                              spm.SoundFolder, 
                                              spm.MostRecentFolder])

        dirpath = tkFileDialog.askdirectory()#(initialdir = r'C:\Projekt\Digital delaktighet\media')
        
        if(dirpath != ''):
            spm.spmanager.setPath(spm.SlideshowFolder, os.path.dirname(dirpath))
            files = os.listdir(dirpath)
            
            images = []
            sounds = []
            bgsound = ''
            
            for f in files:
                (name, ext) = os.path.splitext(f)
                if(name.upper() == ff.bgsoundname.upper()):
                    bgsound = f
                elif(ext.upper() in ff.validImageFormats):
                    images.append(f)
                elif(ext.upper() in ff.validSoundFormats):
                    sounds.append(f)
                    
            images.sort(key = unicode.upper)
            sounds.sort(key = unicode.upper)
            
            slideshow = dm.Slideshow(self._edittabslideshow.editdatamodel, category = str(datetime.datetime.now().year))
            slideshow.bgsound = bgsound
            
            slideshowpath = slideshow.getPath('')
            
            if(os.path.exists(slideshowpath)):
               shutil.rmtree(slideshowpath)
               
            os.makedirs(slideshowpath)
                    
            if(bgsound != ''):
                shutil.copyfile(os.path.join(dirpath, bgsound), slideshow.getPath(bgsound))
    
            media = zip(images, sounds)
            
            for (i, s) in media:
                frame = dm.Frame(slideshow, i, s)
                slideshow.addFrame(frame)
                shutil.copyfile(os.path.join(dirpath, i), os.path.join(slideshowpath, i))
                shutil.copyfile(os.path.join(dirpath, s), os.path.join(slideshowpath, s))
    
            self._openNew(slideshow, self._edittabslideshow, True)
