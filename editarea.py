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
from Tkinter import StringVar, Button, Label, Frame, W, N, E, S, NORMAL, DISABLED, LEFT
import ttk
import tkFileDialog
import shutil
import os
import os.path
from tkMessageBox import showerror

import pygame.mixer

import PIL.Image as Image
import PIL.ImageTk as ImageTk
import PIL.PngImagePlugin
import PIL.GifImagePlugin
import PIL.JpegImagePlugin
import PIL.BmpImagePlugin
Image._initialized=2

from tooltip import ToolTip

from scrollbox import IndexedFrame
from language import lang
import language as lng
from soundbutton import SoundButton
import spmanager as spm
import fileformat as ff
import language as lng
from language import lang

_previewWidth = 125
_previewHeight = 100
_displayedFilenameLength = 16

class EditArea(IndexedFrame):
    """A panel that is used for defining frames in slideshows"""
    def __init__(self, parent, wdir, tooltipwidth, ehThis, ehFromHere):
        """Initiate
        
        Arguments
        parent -- parent tkinter item
        wdir -- working directory
        tooltipwidth -- maximum width of the tooltip
        ehThis -- callback for playing one frame
        ehFromHere -- callback for playing the rest of the frames from a given position

        """
        IndexedFrame.__init__(self, parent)

        self._wdir = wdir
        self._il = None
        self._parent = parent

        self._lblFrame = StringVar()
        self._lblImagename = StringVar()
        self._lblImagenamefull = StringVar()
        self._lblSoundname = StringVar()
        self._lblSoundnamefull = StringVar()
        
        self._fullSoundName = ''
        
        content = self._content
        content.columnconfigure(0, weight = 1)
        content.columnconfigure(1, weight = 1)
        content.rowconfigure(0, weight = 1)
        content.rowconfigure(1, weight = 1)
        content.rowconfigure(2, weight = 1)

        #Left group box
        lf = ttk.LabelFrame(content)
        self._lfSlide = lf
        lf.grid(row = 0, column = 0, sticky = W + N + E + S, padx = 5)

        button = Button(lf, text = lang[lng.txtPlayThisFrame] + '...', command = lambda arg=self: ehThis(arg))
        button.grid(row = 1, column = 0, sticky = W + E, padx = 5, pady = 5)
        
        button = Button(lf, text = lang[lng.txtPlayFromHere] + '...', command = lambda arg=self: ehFromHere(arg))
        button.grid(row = 2, column = 0, sticky = W + E, padx = 5, pady = 5)
        
        #Image group box
        lf = ttk.LabelFrame(content, text = ' ' + lang[lng.txtImage] + ' ')
        lf.grid(row = 0, column = 1, padx = 5, sticky = W + N + E + S)
        label = Label(lf, textvariable = self._lblImagename, justify = LEFT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = W)
        
        tt = ToolTip(label, '', textvariable = self._lblImagenamefull, wraplength = tooltipwidth)
        
        button = Button(lf, text = lang[lng.txtSelect] + '...', command = self._ehGetImage)
        button.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 5)
        button.ref = self

        imFrame = Frame(lf)
        self._imageFrame = imFrame
        imFrame['width'] = _previewWidth
        imFrame['height'] = _previewHeight
        imFrame.grid(row = 1, column = 1, padx = 5, pady = 5)
        imFrame.grid_propagate(0)
        
        lf = ttk.Labelframe(content, text = ' ' + lang[lng.txtSound] + ' ')
        lf.grid(row = 0, column = 2, padx = 5, sticky = W + N + E + S)
        
        #Sound group box
        label = Label(lf, textvariable = self._lblSoundname)
        label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W, columnspan = 10)
        
        tt = ToolTip(label, '', textvariable = self._lblSoundnamefull, wraplength = tooltipwidth)
        
        button = SoundButton(lf, lang[lng.txtListen], lang[lng.txtStop], self._clbPlaying)
        self._btnSound = button
        button.grid(row = 1, column = 0, sticky = W + E, padx = 5, pady = 5)
        
        button = Button(lf, text = lang[lng.txtSelect] + '...', command = self._ehGetSound)
        button.grid(row = 2, column = 0, sticky = W + E, padx = 5, pady = 5)
        self._btnSelect = button
        
        button = Button(lf, text = lang[lng.txtDelete], state = DISABLED, command = self._ehRemoveSound)
        button.grid(row = 3, column = 0, sticky = W + E, padx = 5, pady = 5)
        self._btnRemove = button

        fr = Frame(lf, width = 160)
        fr.grid(row = 4, column = 0, columnspan = 10)

    def setFrame(self, frame, copy = True):
        """Set the contents of a frame
        
        Arguments
        frame -- the frame to set
        copy -- if not false, the contents of frame will be copied to the working directory
        
        """
        self._addImage(frame.getImage(), copy)
        self._addSound(frame.getSound(), copy)

    def update(self):
        """Update the frame index displayed on the panel"""
        self._lfSlide['text'] = ' ' + lang[lng.txtSlide] + ' ' + str(self.index + 1) + ' '
        
    def getImage(self):
        """Return the name and path to the image in this frame"""
        return self._lblImagenamefull.get()
    
    def getSound(self):
        """Return the name and path to the sound in this frame"""
        return self._lblSoundnamefull.get()
    
    def _getIndex(self):
        """Return the index of this frame"""
        return self.index
        
    def _setLabel(self, stringvar, text):
        """Set the text of a StringVar and prefix it with an ellipsis if it is too long
        
        stringvar -- the StringVar
        text -- the text
        
        """
        dispName = text

        if(len(dispName) > _displayedFilenameLength):
            dispName = '...' + dispName[-_displayedFilenameLength:]
        
        stringvar.set(dispName)

    def _setImage(self, imageName):
        """Display the image of this frame
        
        Argument
        imageName -- the name of the image
        
        """
        imageNameFull = os.path.join(self._wdir, imageName)
        
        try:
            image = Image.open(imageNameFull)
        except IOError:
            return

        image.thumbnail((_previewWidth, _previewHeight), Image.ANTIALIAS)
        imageTk = ImageTk.PhotoImage(image)

        self._lblImagenamefull.set(imageName)
        self._setLabel(self._lblImagename, imageName)
        
        
        if(self._il != None):
            self._il.destroy()

        #Show image
        imagelabel = Label(self._imageFrame, image = imageTk)
        imagelabel.place(relx=.5, rely=.5, anchor="c")   
        self._il = imagelabel 
        self._imageRef = imageTk
        
    def _setSound(self, soundName):
        """Display the sound of this frame
        
        Argument
        soundName -- the name of the sound
        
        """
        self._lblSoundnamefull.set(soundName)
        self._setLabel(self._lblSoundname, soundName)
        
    def _addImage(self, imageNameExtPath, copy = True):
        """Add an image to this frame
        
        Arguments
        imageNameExtPath -- the full name of the image
        copy -- if not false, the image will be copied to the working directory
        
        """
        if(copy):
            self._copyFile(imageNameExtPath)

        self._setImage(os.path.basename(imageNameExtPath))

    def _addSound(self, soundNameExtPath, copy = True):
        """Add a sound to this frame
        
        Arguments
        soundNameExtPath -- the full name of the sound
        copy -- if not false, the image will be copied to the working directory
        
        """
        if(soundNameExtPath != ''):
            newstate = NORMAL

            if(copy):
                self._copyFile(soundNameExtPath)
        else:
            newstate = DISABLED

        self._setSound(os.path.basename(soundNameExtPath))
        self._btnSound.setSound(self._getLocalFilename(soundNameExtPath))
        self._btnRemove.config(state = newstate)

    def _getLocalFilename(self, filenamepath):
        """Return the full name and path that a specified file would get in this frame
        
        Argument
        filenamepath -- the full name and path of the file

        """
        if(filenamepath != ''):
            filename = os.path.basename(filenamepath)
            return os.path.join(self._wdir, filename)
        else:
            return ''

    def _copyFile(self, filenamepath):
        """Copy a file to this frame
        
        Argument
        filenamepath -- the full name and path of the file
        
        """
        if(filenamepath != ''):
            shutil.copyfile(filenamepath, self._getLocalFilename(filenamepath))
            
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

    def _ehGetImage(self):
        """Event handler for the add image button"""
        initdir = spm.spmanager.getFirstPath([spm.ImageFolder, 
                                              spm.SoundFolder, 
                                              spm.MostRecentFolder])
        filename = tkFileDialog.askopenfilename(initialdir = initdir, filetypes = ff.dlgImageFormats)

        if(len(filename) > 0):
            try:
                self._addImage(filename)
            except IOError:
                showerror(lang[lng.txtCopyError], lang[lng.txtCouldNotCopy] + os.path.basename(filename))
                return

            self._parent.setDirty()
            spm.spmanager.setPath(spm.ImageFolder, os.path.dirname(filename))

    def _ehRemoveSound(self):
        """Event handler for removing sound"""
        self._setSound('')
        self._btnSound.setSound('')
        self._btnRemove.config(state = DISABLED)
        self._parent.setDirty()

    def _ehGetSound(self):
        """Event handler for the add sound button"""
        initdir = spm.spmanager.getFirstPath([spm.SoundFolder, 
                                              spm.ImageFolder, 
                                              spm.MostRecentFolder])
        
        filename = tkFileDialog.askopenfilename(initialdir = initdir, filetypes = ff.dlgSoundFormats)
        
        if(len(filename) > 0):
            try:
                self._addSound(filename)
            except IOError:
                showerror(lang[lng.txtCopyError], lang[lng.txtCouldNotCopy] + os.path.basename(filename))
                return

            self._parent.setDirty()
            spm.spmanager.setPath(spm.SoundFolder, os.path.dirname(filename))
