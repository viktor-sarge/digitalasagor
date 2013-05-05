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
from language import lang
import language as lng
import dialog
from playerframe import PlayerFrame

class PlayerDialog(tki.Frame):
    """A frame that plays a media item"""
    def __init__(self, parent, size, media):
        """Initiate
        
        Arguments
        parent -- parent tkinter item
        size -- a tuple defining the size of the player
        media -- the media item to play
        
        """
        tki.Frame.__init__(self, parent)
        self.grid(row = 0, column = 0)
        
        self._parent = parent
        self._media = media
        self._cancelpending = False
        self._playing = False
        
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        player = PlayerFrame(self, size, self._end, self)
        self._player = player
        player.grid(row = 0, column = 0, padx = 5, pady = 5)
        
        bf = tki.Frame(self)
        bf.grid(row = 1, column = 0, pady = 5)
        b = tki.Button(bf, text = lang[lng.txtPlay], command = self._ehPlay)
        self._btnplay = b
        b.grid(row = 0, column = 0, padx = 10)
        b = tki.Button(bf, text = lang[lng.txtStop], command = self._ehStop)
        self._btnstop = b
        b.grid(row = 0, column = 1, padx = 10)
        b = tki.Button(bf, text = lang[lng.txtCancel], command = self._ehCancel)
        b.grid(row = 0, column = 2, padx = 10)
        
        parent.protocol("WM_DELETE_WINDOW", self._ehCancel)
        self._updateGuiState(False)
        
    def _updateGuiState(self, playing):
        """Update the state of the dialog
        
        Argument
        playing -- determine whether the player is playing or not
        
        """
        if(playing):
            stopstate = tki.NORMAL
            playstate = tki.DISABLED
        else:
            stopstate = tki.DISABLED
            playstate = tki.NORMAL
        
        self._btnplay.config(state = playstate)
        self._btnstop.config(state = stopstate)
        self._playing = playing

    def _end(self):
        """Callback intended to be called when the player stops playing"""
        self._updateGuiState(False)
        
        if(self._cancelpending):
            self._parent.destroy()

    def _ehPlay(self):
        """Event handler for the play button"""
        try:
            self._player.play(self._media)
        except:
            self._updateGuiState(False)
            print('Unable to play media!')
        else:
            self._updateGuiState(True)

    def _ehStop(self):
        """Event handler for the stop button"""
        self._player.stop()
        self._updateGuiState(False)

    def _ehCancel(self):
        """Event handler for the cancel button"""
        if(self._playing):
            self._cancelpending = True
            self._player.stop()
        else:
            self._parent.destroy()

def showPlayerDialog(root, size, media):
    """Display a modal player dialog
    
    Arguments
    size -- tuple defining the size of the player
    media -- the media item to play
    
    """
    dlg = dialog.getDlg(root, lang[lng.txtPlayer])
    pd = PlayerDialog(dlg, size, media)
    dlg.focus_set()
    dialog.showDlg(dlg)
