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
"""NOT USED!!!!!"""

from Tkinter import Frame, Canvas, Scrollbar, HORIZONTAL, VERTICAL, W, N, E, S

class ScrollFrame(Frame):
    
    def __init__(self, parent):
        master = Frame(parent, bg = 'green')
        master.grid(sticky = W + N + E + S)
        master.rowconfigure(0, weight = 1)
        master.columnconfigure(0, weight = 1)
        
        canvas = Canvas(master)
        self._canvas = canvas
        canvas.grid(row = 0, column = 0, sticky = W + N + E + S)
        hScroll = Scrollbar(master, orient = HORIZONTAL, command = canvas.xview)
        hScroll.grid(row = 1, column = 0, sticky = W + E)
        vScroll = Scrollbar(master, orient = VERTICAL, command = canvas.yview)
        vScroll.grid(row = 0, column = 1, sticky = N + S)

        canvas.configure(xscrollcommand = hScroll.set, yscrollcommand = vScroll.set)
        Frame.__init__(self, canvas, bg = 'blue')
        canvas.create_window(0, 0, window = self, anchor = N + W)
        
    def setupScrollbars(self):
        return
        self.update_idletasks()
        self._canvas.configure(scrollregion = (0, 0, self.winfo_width(), self.winfo_height()))
        
