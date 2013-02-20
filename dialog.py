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
from Tkinter import Toplevel
        
def getDlg(root, title):
    """Create a dialog
    
    Arguments
    root -- dialog parent
    title -- dialog title
    
    """
    dlg = Toplevel(root)
    dlg.title(title)
    dlg.root = root
    
    dlg.grab_set()
    dlg.transient(root)
    dlg.resizable(False, False)
    return dlg

def showDlg(dlg):
    """Show a dialog created with getDlg
    
    Arguments
    dlg -- the dialog to show
    
    """    
    #Set location  
    root = dlg.root
    root.update_idletasks()
    dlg.update_idletasks()
    w = dlg.winfo_width()
    h = dlg.winfo_height()
    pw = root.winfo_width()
    ph = root.winfo_height()
    
    insx = (pw - w) / 2
    insx += root.winfo_rootx()
    insx = max(insx, 0)
    insy = (ph - h) / 2 
    insy += root.winfo_rooty()
    insy = max(insy, 0)
    geom = "+{}+{}".format(insx, insy)
    dlg.geometry(geom)
    dlg.mainloop()
    #root.wait_window(dlg)
