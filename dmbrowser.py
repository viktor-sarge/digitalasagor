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
from Tkinter import W, N, E, S, EXTENDED, END, WORD, DISABLED, NORMAL, INSERT, ANCHOR, VERTICAL
import ttk

from language import lang
import language as lng
from common import validateText

_maxInputLen = 24
_filterOps = [lang[lng.txtTitle], lang[lng.txtAuthor], lang[lng.txtGroup], lang[lng.txtCategory], lang[lng.txtDesc]]

class _Filter:
    """Contains filter parameters"""
    def __init__(self, op, text):
        """Initiate
        
        Arguments
        op -- property to filter
        text -- text to filter
        
        """
        self.op = op
        self.text = text
        
    def __str__(self):
        return (self.op + '=' + self.text).encode('utf8')

class DataModelBrowser(tki.Frame):
    """Visualize the contents of a Digitala Sagor database"""
    
    def __init__(self, parent, datamodel):
        """Initiate
        
        Arguments
        parent -- the parent to this instance
        datamodel -- the datamodel to visualize

        """
        tki.Frame.__init__(self, parent)

        self._title = tki.StringVar()
        self._author = tki.StringVar()
        self._group = tki.StringVar()
        self._category = tki.StringVar()
        self._scount = tki.StringVar()
        self._selcount = tki.StringVar()
        self._filterText = tki.StringVar()

        #self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 2)
        
        self._parent = parent
        self._datamodel = datamodel
        
        #Left column
        dataframe = tki.Frame(self)
        dataframe.grid(row = 0, column = 0, rowspan = 2, sticky = W + N + S + E)
        dataframe.rowconfigure(1, weight = 1)
        dataframe.columnconfigure(0, weight = 1)
        
        #Filtering
        self._filter = dict()
        gb = ttk.LabelFrame(dataframe, text = ' ' + lang[lng.txtFilter] + ' ')
        gb.grid(row = 0, column = 0, sticky = W + N + S + E, padx = 10, pady = 10)
        
        l = tki.Label(gb, text = lang[lng.txtField])
        l.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W)
        
        l = tki.Label(gb, text = lang[lng.txtValue])
        l.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = W)
        
        cb = ttk.Combobox(gb, values = _filterOps, state = "readonly")
        self._cbops = cb
        cb.set(_filterOps[0])
        cb.grid(row = 1, column = 0, padx = 5, pady = 0)
        tcmd = (parent.register(validateText), '%d', '%s', '%S', _maxInputLen)
        e = tki.Entry(gb, w = 32, validate = "key", validatecommand = tcmd, textvariable = self._filterText)
        e.grid(row = 1, column = 1, padx = 5, pady = 0)
        
        b = tki.Button(gb, text = lang[lng.txtFilter], command = self._ehAddFilter)
        b.grid(row = 1, column = 2, padx = 5, pady = 0)
        
        lbf = tki.Frame(gb)
        lbf.grid(row = 2, column = 0, rowspan = 2, padx = 5, pady = 5)
                 
        l = tki.Label(lbf, text = lang[lng.txtActiveFilters])
        l.grid(row = 0, column = 0, padx = 0, pady = 5, sticky = W)
        sb = tki.Scrollbar(lbf, orient = VERTICAL)
        lb = tki.Listbox(lbf, activestyle = 'dotbox', height = 8, yscrollcommand = sb.set)
        lb.grid(row = 1, column = 0, sticky = W + N + S + E)
        self._filterlistbox = lb
        sb.config(command = lb.yview)
        sb.grid(row = 1, column = 1, sticky = N + S)
        #lb.grid(row = 0, column = 0, rowspan = 2, padx = 10, pady = 10, sticky = W + N + S + E)
        
        b = tki.Button(gb, text = lang[lng.txtClear], command = self._ehRemoveFilter)
        b.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = W + S)

        b = tki.Button(gb, text = lang[lng.txtClearAll], command = self._ehRemoveAllFilters)
        b.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = S)

        #Main listbox
        #lb = Listbox(self, activestyle = 'dotbox')
        lb = tki.Listbox(dataframe, activestyle = 'dotbox', selectmode = EXTENDED)
        self._listbox = lb
        #lb.grid(row = 0, column = 0, rowspan = 2, padx = 10, pady = 10, sticky = W + N + S + E)
        lb.grid(row = 1, column = 0, rowspan = 2, padx = 10, pady = 10, sticky = W + N + S + E)
        lb.bind('<<ListboxSelect>>', self._ehselect)

        #Right column
        infoframe = tki.Frame(self)
        infoframe.grid(row = 0, column = 1, sticky = W + N + E + S)
        
        #Selected slideshow
        selgb = ttk.LabelFrame(infoframe, text = ' ' + lang[lng.txtSelectedSlideshow] + ' ')
        self._gbselected = selgb
        selgb.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = W + N + E + S)
        
        l = tki.Label(selgb, text = lang[lng.txtTitle])
        l.grid(row = 0, column = 0, padx = 10, pady = 0, sticky = W)
        e = tki.Entry(selgb, textvariable = self._title, state = "readonly")
        e.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = W + E);
        
        l = tki.Label(selgb, text = lang[lng.txtAuthor])
        l.grid(row = 2, column = 0, padx = 10, pady = 0, sticky = W)
        e = tki.Entry(selgb, textvariable = self._author, state = "readonly")
        e.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = W + E);
        
        l = tki.Label(selgb, text = lang[lng.txtGroup])
        l.grid(row = 4, column = 0, padx = 10, pady = 0, sticky = W)
        e = tki.Entry(selgb, textvariable = self._group, state = "readonly")
        e.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = W + E);
        
        l = tki.Label(selgb, text = lang[lng.txtCategory])
        l.grid(row = 6, column = 0, padx = 10, pady = 0, sticky = W)
        e = tki.Entry(selgb, textvariable = self._category, state = "readonly")
        e.grid(row = 7, column = 0, padx = 10, pady = 5, sticky = W + E);
        
        l = tki.Label(selgb, text = lang[lng.txtDesc])
        l.grid(row = 8, column = 0, padx = 10, pady = 0, sticky = W)
        t = tki.Text(selgb, width = 32, height = 8, wrap = WORD, state = DISABLED)
        t.grid(row = 9, column = 0, padx = 10, pady = 5, sticky = W + E + S)
        self._tdesc = t

        #Multiple selection
        selgb = ttk.LabelFrame(infoframe, text = ' ' + lang[lng.txtSelection] + ' ')
        self._gbselection = selgb
        selgb.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = W + N + E + S)
        
        l = tki.Label(selgb, text = lang[lng.txtSelCount])
        l.grid(row = 2, column = 0, padx = 10, pady = 0, sticky = W)
        e = tki.Entry(selgb, textvariable = self._selcount, state = "readonly")
        e.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = W + E);

        #Database
        dbgb = ttk.LabelFrame(infoframe, text = ' ' + lang[lng.txtDb] + ' ')
        self._gbdb = dbgb
        dbgb.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = W + N + E + S)
        
        l = tki.Label(dbgb, text = lang[lng.txtSCount])
        l.grid(row = 0, column = 0, padx = 10, pady = 0, sticky = W)
        e = tki.Entry(dbgb, textvariable = self._scount, state = "readonly")
        e.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = W + E);
        
    def _populateListbox(self, contents = None):
        """Add media items to the listbox
        
        Argument
        contents -- a list of media items to show in the listbox
        
        """
        self._contents = dict()
        self._listbox.delete(0, END)
        index = 0
        
        if(contents is None):
            contents = self._datamodel.getAll()
            
        contents.sort(key = lambda movie:movie.title)

        for m in contents:
            self._listbox.insert(END, m)
            self._contents[str(index)] = m
            index += 1
                
        self._scount.set(str(index))
        self._selcount.set(0)
        self._displayInfo()
                
    def _displayInfo(self, item = None):
        """Display information about one media item
        
        Argument
        item -- the item to display information about
        
        """
        if(item is not None):
            self._title.set(item.title)
            self._author.set(item.author)
            self._group.set(item.group)
            self._category.set(item.category)
            self._tdesc.config(state = NORMAL)
            self._tdesc.delete(1.0, END)
            self._tdesc.insert(INSERT, item.description)
            self._tdesc.config(state = DISABLED)
        else:
            self._title.set('')
            self._author.set('')
            self._group.set('')
            self._category.set('')
            self._tdesc.config(state = NORMAL)
            self._tdesc.delete(1.0, END)
            self._tdesc.config(state = DISABLED)

    def _getSelectedItem(self, updateGui = False):
        """Return the first selected item and optionally update the GUI
        
        Argument
        updateGui -- if true, the GUI will be updated with information 
                     about the current selection
        
        """
        s = self._listbox.curselection()
        
        if(updateGui):
            count = len(s)
            self._selcount.set(count)

        if(s == ()):
            return None
        else:
            return self._contents[s[0]]

    def _filtermatch(self, subtext, text):
        """Check if a subtext exists inside a text
        
        Arguments
        subtext -- the subtext
        text -- the text
        
        """
        return (subtext.lower() in text.lower())

    def _applyFilter(self, filterid, list):
        """Apply a passfilter to a list of items and return the resulting list
        
        Arguments
        filterid -- id of the filter to apply
        list -- list of items to filter
        
        """
        passed = []
        filter = self._filter[filterid]
        filterop = filter.op
        filtertext = filter.text

        if(filterop == lang[lng.txtAuthor]):
            for i in list:
                if(self._filtermatch(filtertext, i.author)):
                    passed.append(i)
        elif(filterop == lang[lng.txtTitle]):
            for i in list:
                if(self._filtermatch(filtertext, i.title)):
                    passed.append(i)
        elif(filterop == lang[lng.txtGroup]):
            for i in list:
                if(self._filtermatch(filtertext, i.group)):
                    passed.append(i)
        elif(filterop == lang[lng.txtCategory]):
            for i in list:
                if(self._filtermatch(filtertext, i.category)):
                    passed.append(i)
        elif(filterop == lang[lng.txtDesc]):
            for i in list:
                if(self._filtermatch(filtertext, i.description)):
                    passed.append(i)

        return passed

    def _applyAllFilters(self):
        """Apply all filters to all items in the current datamodel"""
        passed = self._datamodel.getAll()
        
        for f in self._filter:
            passed = self._applyFilter(f, passed)

        self._populateListbox(passed)

    #Event handlers
    def _ehselect(self, event):
        """Event handler for listbox selection
        
        Argument
        event -- the event object
        
        """
        item = self._getSelectedItem(True)
        self._displayInfo(item)

    def _ehRemoveAllFilters(self):
        """Remove all filters from the listbox"""
        
        self._filterlistbox.delete(0, END)
        self._filter.clear()
        self._populateListbox()

    def _ehRemoveFilter(self):
        """Remove the currently selected filter from the listbox"""
        sel = self._filterlistbox.curselection()
        
        if(sel <> ()):
            s = self._filterlistbox.get(sel)
            print('Remove ' + s)
            self._filterlistbox.delete(sel)
            del self._filter[s]
            self._applyAllFilters()

    def _ehAddFilter(self):
        """Add a filter"""
        filterop = self._cbops.get()
        filtertext = self._filterText.get()
        self._filterText.set('')
        filter = _Filter(filterop, filtertext)
        
        if(not filter.__str__() in self._filter):
            self._filter[filter.__str__()] = filter
            self._filterlistbox.insert(END, filter)
            self._applyAllFilters()
