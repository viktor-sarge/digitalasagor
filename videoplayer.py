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
from ctypes import windll
from win32com.client import Dispatch, DispatchWithEvents

#clip = r'C:\Users\PC\Desktop\hylte-public-viktorkommentar5nov2011.mp4'

clickHandler = None
        
class WMPEvents:
    """Event handler class for Windows Media Player"""
    def OnClick(self, nButton, nShiftState, fX, ):
        """Handle the OnClick event of the Windows Media Player
        
        Arguments
        nButton -- unused
        nShiftState -- unused
        fX -- unused
        fY -- unused
        
        """
        clickHandler()

class VideoPlayer(tki.Frame):
    """A Tkinter Frame containing Windows Media Player"""
    
    def __init__(self, parent, width, height):
        """Initiate the video player
        
        Arguments
        parent -- the parent frame of this video player
        width -- the width of this video player
        height -- the height of this video player
        
        """
        tki.Frame.__init__(self, parent, width = width, height = height)
        #self.grid(sticky = tki.W + tki.N + tki.E + tki.S)
        self.grid_propagate(0)
        
        hwnd = self.winfo_id()
        windll.atl.AtlAxWinInit()
        fwnd = windll.user32.CreateWindowExA(0, 'AtlAxWin', 0, 0x50000000, 0, 0, width, height, hwnd, 0, 0, 0)
        
        if(fwnd == 0):
            error = windll.kernel32.GetLastError()
        
        #wmp = DispatchWithEvents('WMPlayer.OCX', WMPEvents)
        wmp = Dispatch('WMPlayer.OCX')
        self._wmp = wmp
        wmp_addr = int(repr(wmp._oleobj_).split()[-1][2:-1], 16)
        windll.atl.AtlAxAttachControl(wmp_addr, fwnd, 0)

        wmp.uiMode = 'mini'
        wmp.enableContextMenu = False
        
        global clickHandler
        clickHandler = self._togglePlayer

    def _togglePlayer(self):
        """Toggle play/pause"""
        if(self._playing):
            self._wmp.controls.pause()
            self._playing = False
        else:
            self._wmp.controls.play()
            self._playing = True
        
    def play(self, media):
        """Start playing a video
        
        Argument
        media -- the video to start
        
        """
        self._playing = True
        self._wmp.URL = media
        
    def stop(self):
        """Stop playing a video"""
        self._wmp.close()
