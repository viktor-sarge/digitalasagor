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
from Tkinter import NW
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import ini

class TransparentButton:
    """A button with a transparent image that draws itself on a canvas"""
    def __init__(self, canvas, font, iniline, scalefactor):
        """Initiate the transparent button
        
        Arguments
        canvas -- the canvas on which to draw the button
        iniline -- a line of text describing a transparent button
        font -- the font to use for the text
        scalefactor -- tuple containing (horizontal scaling, vertical scaling)
        
        """
        self._canvas = canvas
        self._font = font
        self._getSettings(iniline, scalefactor[0], scalefactor[1])
        self._enabled = True
        self._text = None
        self._event = None
        self._image = canvas.create_image(self._insleft, self._instop, 
                                          image = self._imageobj, anchor = NW)

    def setText(self, text):
        """Set the text of the transparent button
        
        Argument
        text -- the text to set; no check is performed to make sure it fits
        
        """
        if(self._text is not None):
            self._canvas.delete(self._text)
            
        if(self._enabled):
            color = self._activecolor
        else:
            color = self._inactivecolor
            
        self._text = self._canvas.create_text(self._insleft + self._textleft, 
                                     self._instop + self._texttop, font = self._font, 
                                     text = text, fill = color)

        if(self._event is not None):
            self._canvas.tag_bind(self._text, '<Button-1>', lambda event, arg = self : self._event(event, arg))
            
    def setCommand(self, handler):
        """Set the event handler of the transparent button
        
        Argument
        handler -- the event handler
        
        """
        if(self._enabled):
            self._unbindEvents()
            
        self._event = handler
        
        if(self._enabled):
            self._bindEvents()

    def setEnabled(self, enabled):
        """Set the state of the transparent button
        
        Argument
        enabled -- If true the event will fire and the text will have its active appearance
        
        """
        if(self._enabled == enabled):
            return
        
        self._enabled = enabled
        
        if(self._enabled):
            self._bindEvents()
            if(self._text is not None):
                self._canvas.itemconfig(self._text, fill = self._activecolor)
        else:
            self._unbindEvents()
            if(self._text is not None):
                self._canvas.itemconfig(self._text, fill = self._inactivecolor)

    def _getSettings(self, iniline, xfactor, yfactor):
        """Load the image and read the settings
        
        Argument
        iniline -- a line of text describing a transparent button
        xfactor -- horizontal scaling
        yfactor -- vertical scaling
        
        """
        inilist = iniline.split(ini.delimiter)
        image = Image.open(ini.getPath(inilist[0]))
        self._insleft = int(inilist[1])
        self._instop = int(inilist[2])
        self._textleft = int(inilist[3])
        self._texttop = int(inilist[4])
        self._activecolor = inilist[5]
        self._inactivecolor = inilist[6]
        
        #Scale image and values if any scaling shall be performed
        if(xfactor != 1 or yfactor != 1):
            (w, h) = image.size
            w = int(w * xfactor + 0.5)
            h = int(h * yfactor + 0.5)
            image = image.resize((w, h), Image.ANTIALIAS )

            self._insleft = int(self._insleft * xfactor + 0.5)
            self._instop = int(self._instop * yfactor + 0.5)
            self._textleft = int(self._textleft * xfactor + 0.5)
            self._texttop = int(self._texttop * yfactor + 0.5)

        self._imageobj = ImageTk.PhotoImage(image)

    def _bindEvents(self):
        """Activate the event handler if it is specified"""
        if(self._event is not None):
                self._canvas.tag_bind(self._image, '<Button-1>', lambda event, arg = self : self._event(event, arg))
            
                if(self._text is not None):
                    self._canvas.tag_bind(self._text, '<Button-1>', lambda event, arg = self : self._event(event, arg))

    def _unbindEvents(self):
        """Deactivate the event handler if it is specified"""
        if(self._event is not None):
            self._canvas.tag_unbind(self._image, '<Button-1>')
            
            if(self._text is not None):
                self._canvas.tag_unbind(self._text, '<Button-1>')
