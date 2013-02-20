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
import math
import ini
from language import lang
import language as lng
from datamodel import tpSlideshow, tpVideo

_infocolor = 'gray95'
_panelcolor = 'white'
_staticitemtag = 'STATICPREVIEWITEMS'
_linewidth = 5

class PreviewFrame(tki.Frame):
    """A preview frame which displays slideshows in preview mode. The
    currently selected slideshow is provided in variable selecteditem. 
    
    """
    def __init__(self, parent, datacollector, canvas, settings):
        """Creates the preview frame. 

        Arguments
        parent -- the root Tk object
        datacollector -- a DataCollector that stores usage statistics
        canvas -- the canvas object on which to lay out the preview frame
        settings -- config settings
        
        """
        self._bordercolor = settings.bordercolor

        tki.Frame.__init__(self, parent, width = settings.playersize[0], height = settings.playersize[1], bg = _panelcolor)
        #canvas.create_window(pos[0], pos[1], window = self, anchor = tki.NW)
       # self.grid(row = 0, column = 0)
        #self.grid()
        self.grid_propagate(0)
        
        self._parent = parent
        self._canvas = canvas
        self._prevcols = settings.previewcolumns
        self._datacollector = datacollector
        self._clbActivate = None
        
        self._lblTitle = tki.StringVar()
        self._lblAuthor = tki.StringVar()
        self._lblDesc = tki.StringVar()
        
        self._panels = []
        self._triangle = None
        self._border = None
        self._visible = False
        self._prevsize = settings.previewsize
        self.selecteditem = None
        
        #Calculate dimensions
        sparewidth = settings.playersize[0] - (self._prevcols * settings.previewsize[0])
        spareheight = settings.playersize[1] - (3 * settings.previewsize[1] / 1)
        xspace = sparewidth / (2 * self._prevcols)
        yspace = spareheight / 4
        xcoord = xspace
        ycoord = yspace
        triy = settings.playerpos[1] + ycoord + settings.previewsize[1] + (_linewidth + 1) / 2

        #Create preview panels        
        for i in range(2):
            for j in range(self._prevcols):
                index = (i * self._prevcols) + j
                bf = tki.Frame(parent, width = settings.previewsize[0], height = settings.previewsize[1])
                bf.grid_propagate(0)
                bf.rowconfigure(0, weight = 1)
                bf.columnconfigure(0, weight = 1)
                wnd = canvas.create_window(settings.playerpos[0] + xcoord, settings.playerpos[1] + ycoord, window = bf, anchor = tki.NW)
                label = tki.Label(bf, bg = _panelcolor)
                label.grid(sticky = tki.W + tki.N + tki.E + tki.S)
                label.itemindex = index
                label.bottomedge = (settings.playerpos[0] + xcoord + settings.previewsize[0] / 2, triy)
                label.topleft = (settings.playerpos[0] + xcoord, settings.playerpos[1] + ycoord)
                label.bind("<Button-1>", self._ehSelect)
                label.wnd = wnd
                self._panels.append(label)
                xcoord += (xspace * 2) + settings.previewsize[0]

            xcoord = xspace
            ycoord += 2 * (yspace + settings.previewsize[1])
            triy = settings.playerpos[1] + ycoord - 1 - _linewidth / 2
            
        #Create info panel
        frame = tki.Frame(parent, width = settings.playersize[0] - (2 * xspace), height = settings.previewsize[1], bg = _infocolor)
        frame.grid_propagate(0)
        frame.columnconfigure(1, weight = 1)
        
        wnd = canvas.create_window(settings.playerpos[0] + xspace, settings.playerpos[1] + settings.previewsize[1] + 2 * yspace, window = frame, anchor = tki.NW)
        canvas.itemconfig(wnd, tags = _staticitemtag)
        label = tki.Label(frame, textvariable = self._lblTitle, bg = _infocolor)
        label.grid(row=0, column=0, padx = 5, pady = 5, sticky = tki.W)
        label = tki.Label(frame, textvariable = self._lblAuthor, bg = _infocolor)
        label.grid(row=1, column=0, padx = 5, sticky = tki.W)
        
        self._uppertriy = settings.playerpos[1] + settings.previewsize[1] + 2 * yspace - 1
        self._lowertriy = self._uppertriy + settings.previewsize[1] + 1

        xpad = 10
        wlen = settings.playersize[0] - (2 * xspace) - xpad

        label = tki.Label(frame, textvariable = self._lblDesc, bg = _infocolor, justify = tki.LEFT, anchor = tki.W,
                           wraplength = wlen)
        label.grid(row=2, column=0, columnspan = 2, padx = xpad, pady = 5, sticky = tki.W + tki.E)

    def setClbActivate(self, clb):
        """Set function to call when a media item is activated
        
        Argument
        clb -- the callback to call; no arguments are passed
        
        """
        self._clbActivate = clb

    def previewsubset(self, subset):
        """Displays a set of slideshows in preview mode 

        Arguments
        subset -- the set of slideshows to display
        
        """        
        assert(len(subset) > 0), 'Fatal error: tried to preview empty list'
        
        if(len(subset) > self._prevcols * 2):
            subset = subset[:self._prevcols * 2]
        
        self._subset = subset
        ix = 0
        
        for frame in subset:
            if(frame.type == tpSlideshow):
                self._panels[ix].config(text = '', image = frame.frames[0].getPreviewImage())
            elif(frame.type == tpVideo):
                 self._panels[ix].config(text = lang[lng.txtVideo], image = '')
                
            self._panels[ix].active = True
            ix += 1
        
        while(ix < self._prevcols * 2):
            self._panels[ix].active = False
            ix += 1
            
        self._applyVisibility()
        self._selectframe(0)
        
    def setVisible(self, visible):
        """Set the visibility of the PreviewFrame
        
        Argument
        visible -- determines whether to show or hide the PreviewFrame
        
        """
        self._visible = visible
        self._applyVisibility()

    def _applyVisibility(self):
        """Set the visibility of the previewed media items"""
        if(self._visible):
            newstate = tki.NORMAL
        else:
            newstate = tki.HIDDEN
            
        for p in self._panels:
            if(p.active):
                self._canvas.itemconfig(p.wnd, state = newstate)
            else:
                self._canvas.itemconfig(p.wnd, state = tki.HIDDEN)
                
        self._canvas.itemconfig(_staticitemtag, state = newstate)
        
    def _drawtriangle(self, coord1, isUpper):
        """Draw the triangular pointer from the text box to the currently selected media item
        
        Arguments
        coord1 -- a tuple containing the coordinates of the triangle tip
        isUpper -- True if the selected media item is located in the upper row
        
        """
        if(self._triangle is not None):
            self._canvas.delete(self._triangle)

        x0 = coord1[0]
        y0 = coord1[1]

        if(isUpper):
            y1 = self._uppertriy
            dist = y1 - y0
        else:
            y1 = self._lowertriy
            dist = y0 - y1
            
        y2 = y1

        halfbase = int(dist / math.sin(math.radians(60))) / 2
        x1 = x0 - halfbase
        x2 = x0 + halfbase
        
        self._triangle = self._canvas.create_polygon(x0, y0, x1, y1, x2, y2, outline = _infocolor, fill = _infocolor)
        self._canvas.itemconfig(self._triangle, tags = _staticitemtag)
        self._canvas.tag_raise(self._triangle)
        
    def _drawborder(self, topleft):
        """Draw the border of the currently selected media item
        
        Argument
        topleft -- a tuple containing the top left coordinate of the 
                   currently selected media item
        
        """
        if(self._border is not None):
            self._canvas.delete(self._border)
            
        self._border = self._canvas.create_rectangle(topleft[0] , topleft[1], 
                                                topleft[0] + self._prevsize[0], topleft[1] + self._prevsize[1], 
                                                outline = self._bordercolor, width = _linewidth)

        self._canvas.itemconfig(self._border, tags = _staticitemtag)
        self._canvas.tag_raise(self._border)

    def _selectframe(self, index, clicked = False):
        """Mark a media item as selected or start it if clicked or already selected
        
        Arguments
        index -- the index of the media item to select
        clicked -- indicates if the media item was clicked
        
        """
        olditem = self.selecteditem
        self.selecteditem = self._subset[index]
        
        #If an item was already selected and it was clicked, it is considered activated
        if(olditem == self.selecteditem and clicked):
            if(self._clbActivate is not None):
                self._clbActivate()
        else:
            self._lblTitle.set(self.selecteditem.title)
            self._lblDesc.set(self.selecteditem.description)
            self._drawtriangle(self._panels[index].bottomedge, index < self._prevcols)
            self._drawborder(self._panels[index].topleft)
            
            text = lang[lng.txtBy] + ' ' + self.selecteditem.author
            
            if(self.selecteditem.group <> ''):
                text = text + ', ' + self.selecteditem.group
            
            self._lblAuthor.set(text)

    def _ehSelect(self, event):
        """Event handler for clicks on the media item previews

        Argument
        event -- the event object

        """
        self._datacollector.detect()
        if(event.widget.itemindex < len(self._subset)):
            self._selectframe(event.widget.itemindex, True)
