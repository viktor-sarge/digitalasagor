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
from Tkinter import Button, NORMAL, DISABLED
from tkMessageBox import showerror
import pygame.mixer
import thread
import time
from language import lang
import language as lng

_soundEndEvent = '<<SoundPlayerEnd>>'

class _SoundPlayer:
    """Play a sound and optionally call a callback when it stops"""
    def __init__(self, parent, clb = None):
        """Initiate
        
        Arguments
        parent -- tkinter parent (used for event generation)
        clb -- function to be called when a sound stops playing
        
        """
        self._parent = parent
        pygame.mixer.init()

        if(pygame.mixer.get_init() == None):
            showerror(lang[lng.txtSoundErrorTitle], lang[lng.txtCantInitSound])
            raise Exception(lang[lng.txtSoundErrorTitle])

        if(pygame.mixer.get_num_channels() < 1):
            showerror(lang[lng.txtSoundErrorTitle], 
                      lang[lng.txtTooFewChannels].format(pygame.mixer.get_num_channels()))
            raise Exception(lang[lng.txtSoundErrorTitle])

        self._channel = pygame.mixer.Channel(0)
        parent.bind(_soundEndEvent, clb)

    def playSound(self, filename):
        """Play a sound
        
        Argument
        filename -- the name of the sound file
        
        """
        sound = pygame.mixer.Sound(file = filename)
        self.stopSound()
        self._channel.play(sound)
        thread.start_new(self._thrWaitForSoundToEnd, (self, None))
        
    def stopSound(self):
        """Stop playing a sound"""
        if(self._channel.get_busy()):
            self._channel.stop()

    def _thrWaitForSoundToEnd(self, dummy, d2):
        """Thread function that will generate an event when a sound stops playing
        
        Arguments
        dummy -- dummy argument
        d2 -- dummy argument
        
        """
        while(self._channel.get_busy()):
            time.sleep(0.1)

        self._parent.event_generate(_soundEndEvent, when="tail")

class SoundButton(Button):
    """A toggleable button that plays an associated sound"""
    def __init__(self, parent, passivetext, activetext, clbPlaying = None):
        """Initiate
        
        Arguments
        parent -- the parent tkinter item
        passivetext -- text to display when the sound is not playing
        activetext -- text to display when the sound is playing
        clbPlaying -- callback to call whenever the state changes
        
        """
        #Set the width of the button explicitly to avoid a resize when the test is changed
        bwidth = max(len(passivetext), len(activetext))
        Button.__init__(self, parent, text = passivetext, width = bwidth, state = DISABLED, 
                        command = self._ehPressed)
        self._texts = dict()
        self._texts[True] = activetext
        self._texts[False] = passivetext
        self._sound = ''
        self._playing = False
        self._soundplayer = _SoundPlayer(self, self._clbEnd)
        self._clbPlaying = clbPlaying

    def setSound(self, filename):
        """Set the sound associated with this button
        
        Argument
        filename -- the name of the soundfile
        
        """
        self._sound = filename

        if(filename != ''):
            newstate = NORMAL
        else:
            newstate = DISABLED

        self.config(state = newstate)

    def _setPlaying(self, playing):
        """Set the state of the button
        
        Argument
        playing -- true iff playing
        
        """
        self.config(text = self._texts[playing])
        self._playing = playing
        
        if(self._clbPlaying is not None):
            self._clbPlaying(playing)

    def _clbEnd(self, event):
        """Callback to be called when the sound stops playing"""
        self._setPlaying(False)

    def _ehPressed(self):
        """Event handler for the button"""
        if(self._playing):
            self._soundplayer.stopSound()
        else:
            try:
                self._setPlaying(True)
                self._soundplayer.playSound(self._sound)
            except:
                self._setPlaying(False)
