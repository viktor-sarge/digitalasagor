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
from tkMessageBox import showerror
import pygame.mixer
import thread
import time
from language import lang
import language as lng
from videoplayer import VideoPlayer
from datamodel import tpSlideshow, tpVideo

#Fix for pygame and py2exe
import pygame._view

_soundEvent = "<<evEndOfSound>>"
_playerFrameClickEvent = "<<PlayerFrameClicked>>"
_sleepTime = 5
_sleepIntervalTime = 0.05

class PlayerDimensions:
    """Dimensions for a player in preview mode and in play mode"""
    def __init__(self, previewWidth, previewHeight, playWidth, playHeight):
        self.previewWidth = previewWidth
        self.previewHeight = previewHeight
        self.playWidth = playWidth
        self.playHeight = playHeight

class PlayerFrame(tki.Frame):
    """A player capable of playing movie clips and slideshows"""
    def __init__(self, parent, size, clbEnd = None, eventparent = None):
        """Initiate the player
        
        Arguments
        parent -- the parent frame of this player
        size -- a tuple containing the size of this player
        clbEnd -- a callback that will be called when a media item has stopped playing
        eventparent -- Tkinter object used for binding and generating events

        """
        #Initiate widget
        tki.Frame.__init__(self, parent, width = size[0], height = size[1], bg="black")
        #self.grid(row = 0, column = 0)
        self.grid_propagate(0)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        
        self._clbEnd = clbEnd
        self._currentMediaType = ''
        self._clbClicked = None
        
        if(eventparent is not None):
            self._eventparent = eventparent
        else:
            self._eventparent = parent
            
        l = tki.Label(self, bd = 0, highlightthickness = 0)
        l.bind("<Button-1>", self._ehClick)
        self._il = l
        
        v = VideoPlayer(self, size[0], size[1])
        v.bind("<Button-1>", self._ehClick)
        self._video = v
        
        self._media = None
        
        self._initSound()
        
    def play(self, media):
        """Start playback
        
        Argument
        media -- the media item to play
        
        """
        self._currentMediaType = media.type
        
        if(media.type == tpSlideshow):
            self._video.grid_remove()
            self._il.grid()
            self._abortSlideshow = False
            self._currentSlideIx = 0
            self._media = media
            self._startBgSound()
            self._updateSlideshow()
        elif(media.type == tpVideo):
            self._il.grid_remove()
            self._video.grid()
            self._video.play(media.getVideo())

    def stop(self):
        """Stop playback"""
        if(self._currentMediaType == tpSlideshow):
            self._abortSlideshow = True
            self._channel.stop()
        elif(self._currentMediaType == tpVideo):
            self._video.stop()
            
            if(self._clbEnd is not None):
                self._clbEnd()

    def setClbEnd(self, clb):
        """Assign callback that will be called when playback ends"""
        self._clbEnd = clb
        
    def setClbClicked(self, clb):
        """Assign callback that will be called when the player has been clicked"""
        self._clbClicked = clb

    def _initSound(self):
        """Initiate sound"""
        pygame.mixer.init()
    
        if(pygame.mixer.get_init() == None):
            showerror(lang[lng.txtSoundErrorTitle], lang[lng.txtCantInitSound])
            raise Exception(lang[lng.txtSoundErrorTitle])

        if(pygame.mixer.get_num_channels() < 2):
            showerror(lang[lng.txtSoundErrorTitle], 
                      lang[lng.txtTooFewChannels].format(pygame.mixer.get_num_channels()))
            raise Exception(lang[lng.txtSoundErrorTitle])

        self._channel = pygame.mixer.Channel(0)
        self._bgchannel = pygame.mixer.Channel(1)
        self._eventparent.bind(_soundEvent, self._ehEndSound)

    #Media related functions
    def _setImage(self, dispimage):
        """Display an image
        
        Argument
        dispimage -- the image to display
        
        """
        #Show image
        self._il.config(image = dispimage)

    def _thrWaitForSoundToEnd(self, dummy, d2):
        """Wait until a sound stops and generate an event when that happens
        
        Arguments
        dummy -- dummy argument needed to match the thread function template
        d2 -- dummy argument needed to match the thread function template
        
        """
        while(self._channel.get_busy()):
            time.sleep(0.1)

        self._eventparent.event_generate(_soundEvent, when="tail")
        
    def _thrWaitWithoutSound(self, dummy, d2):
        """Wait until _sleepTime seconds has passed
        
        Arguments
        dummy -- dummy argument needed to match the thread function template
        d2 -- dummy argument needed to match the thread function template
        
        """
        intervals = int(_sleepTime / _sleepIntervalTime)
        
        for i in range(intervals):
            if(self._abortSlideshow):
                break

            time.sleep(_sleepIntervalTime)

        self._eventparent.event_generate(_soundEvent, when="tail")
        
    def _getSound(self, filename):
        """Create and return a Sound given a filename
        
        Argument:
        filename -- full name and path of the sound file
        
        """
        return pygame.mixer.Sound(file = filename.encode('utf-8'))

    def _startBgSound(self):
        """Start the background sound of the current media item"""
        filename = self._media.getBgSound()
        
        if(filename is not None):
            try:
                #sound = pygame.mixer.Sound(file = filename)
                sound = self._getSound(filename)
                self._bgchannel.play(sound, loops = -1)
            except Exception as e:
                print(e)

    def _stopBgSound(self):
        """Start the background sound"""
        if(self._bgchannel.get_busy()):
            self._bgchannel.stop()

    def _setSound(self, soundName):
        """Start a sound
        
        Argument
        soundName -- the sound to start
        
        """
        try:
            sound = self._getSound(soundName)
            self._channel.play(sound)
            thread.start_new(self._thrWaitForSoundToEnd, (self, None))
        except:
            thread.start_new(self._thrWaitWithoutSound, (self, None))

    def _updateSlideshow(self):
        """Set image and sound of the current slideshow"""
        try:
            self._setImage(self._media.frames[self._currentSlideIx].getPlaybackImage())
            self._setSound((self._media.frames[self._currentSlideIx].getSound()))
        except:
            self._stopBgSound()
            showerror(lang[lng.txtPlayFrameError], lang[lng.txtCouldPlayFrame].format(self._currentSlideIx + 1) + self._media.title)
            self._endPlayback()

    def _endPlayback(self):
        self._stopBgSound()
        if(self._clbEnd is not None):
            self._clbEnd()

    #Event handlers
    def _ehEndSound(self, dummy):
        """Handle the event when a sound has stopped"""
        #Check if  playback is complete
        self._currentSlideIx = self._currentSlideIx + 1
        
        if(self._abortSlideshow or (self._currentSlideIx >= len( self._media.frames))):
            self._endPlayback()
        else:
            self._updateSlideshow()

    def _ehClick(self, event):
        """Handle the event when the player has been clicked"""
        if(self._clbClicked is not None):
            self._clbClicked()
