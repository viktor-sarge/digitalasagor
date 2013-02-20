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
from Tkinter import NW, NORMAL, HIDDEN, StringVar, Canvas
from tkMessageBox import showerror

import PIL.Image as Image
import PIL.ImageTk as ImageTk
from test.test_iterlen import len
Image._initialized=2

from language import lang
import language as lng
import ini
from playerframe import PlayerFrame
from previewframe import PreviewFrame
from datacollector import DataCollector
from transpbtn import TransparentButton
from common import updateProgress, HylteSettings
from progressdlg import DataModelLoader

_preview = 'preview'
_play = 'play'

class PlayerGui:
    """The main GUI of the Digitala sagor player"""
    def __init__(self, root, datamodel, config):
        """Initiate the program
        
        Arguments
        root -- the Tk instance of the application
        datamodel -- the data model instance to show
        config -- ConfigParser containing application settings
        
        """
        self._datamodel = datamodel

        #Create string variables        
        self._lblTitle = StringVar()
        self._lblAuthor = StringVar()
        self._activeInPreview = []
        self._activeInPlay = []
        self._datacollector = DataCollector()
        self._userstop = False
        
        #Initiate GUI and data
        self._setupDisplay(root, config)
        self._initData(config)
        
        #Create transparent buttons
        self._setupCategories(config)
        self._setupControls(root, config)

        #Create player
        self._playerFrame = PlayerFrame(root, self._settings.playersize, self._playbackStopped)
        self._playerFrame.setClbClicked(self._clbClicked)
        self._playerwnd = self._canvas.create_window(self._settings.playerpos[0], 
                                                     self._settings.playerpos[1], 
                                                     window = self._playerFrame, 
                                                     anchor = NW)

        #Create preview
        self._previewFrame = PreviewFrame(root, self._datacollector, self._canvas, self._settings)
        self._previewFrame.setClbActivate(self._clbClicked)
        self._previewFrame.previewsubset(self._currentMovies)

        self._updateBrowseButtons()
        
        self._setPreviewMode()

        self._dml = DataModelLoader(root, self._datamodel)
        #after_idle does not work here; 100 ms is an arbitrarily chosen delay time
        root.after(100, self._dml.load)

    def _setupDisplay(self, root, config):
        """Set screen size and add background image
        
        root -- the Tk instance of the application
        config -- ConfigParser containing application settings

        """
        fullscreen = config.getboolean(ini.general, ini.fullscreen)
        bgimage = ini.getPath(config.get(ini.general, ini.bgimage))
        
        image = Image.open(bgimage)
        backgroundIm = ImageTk.PhotoImage(image)        
        
        if(fullscreen):
            screenwidth = root.winfo_screenwidth()
            screenheight = root.winfo_screenheight()
            (w, h) = image.size
            self._scalefactor = (screenwidth / float(w), screenheight / float(h))
            image = image.resize((screenwidth, screenheight))
        else:
            (screenwidth, screenheight) = image.size
            self._scalefactor = (1, 1)
            
        geom = "{}x{}+{}+{}".format(screenwidth, screenheight, 0, 0)
        root.geometry(geom)
        root.overrideredirect(1)
        
        background = Canvas(root, width = screenwidth, height = screenheight)
        self._canvas = background
        background.pack()
        backgroundIm = ImageTk.PhotoImage(image)
        self._backgroundIm = backgroundIm
        background.create_image(0,0, image = backgroundIm, anchor = NW)
        
    def _setupCategories(self, config):
        """Add buttons to browse between categories
        
        config -- ConfigParser containing application settings
        
        """
        #Get all button data
        lines = []
        ctr = 1
        option = ini.image + str(ctr)
        
        while(config.has_option(ini.year, option)):
            line = config.get(ini.year, option)
            lines.append(line)
            ctr += 1
            option = ini.image + str(ctr)
            
        #Create as many buttons as needed
        buttondata = zip(lines, self._years)
        
        if(len(buttondata) < len(self._years)):
            print('Warning! There are more categories than category buttons - some categories will not be shown')
            
        ctr = 0
        
        for (line, year) in buttondata:
            tb = TransparentButton(self._canvas, self._settings.generalfont, line, self._scalefactor)
            tb.setText(year)
            tb.setCommand(self._ehYear)
            tb.index = ctr
            ctr += 1
            self._activeInPreview.append(tb)

    def _setupControls(self, root, config):
        """Initiate control buttons        
        
        root -- the Tk instance of the application
        config -- ConfigParser containing application settings

        """
        iniline = config.get(ini.controls, ini.prev)
        tb = TransparentButton(self._canvas, self._settings.generalfont, iniline, self._scalefactor)
        tb.setCommand(self._ehPrev)
        self._btnPrev = tb
        self._activeInPreview.append(tb)
        
        iniline = config.get(ini.controls, ini.next)
        tb = TransparentButton(self._canvas, self._settings.generalfont, iniline, self._scalefactor)
        tb.setCommand(self._ehNext)
        self._btnNext = tb
        self._activeInPreview.append(tb)

        iniline = config.get(ini.controls, ini.start)
        tb = TransparentButton(self._canvas, self._settings.generalfont, iniline, self._scalefactor)
        self._btnPlay = tb

    def _initData(self, config):
        """Initiate internal variables        
        
        config -- ConfigParser containing application settings

        """
        #Check that there are movies
        if(self._datamodel.isEmpty()):
            showerror(lang[lng.txtNoMoviesTitle], lang[lng.txtNoMovies])
            raise Exception(lang[lng.txtNoMoviesTitle])

        #Initiate variables
        self._settings = HylteSettings(config, self._scalefactor)
        self._subsetSize = self._settings.previewcolumns * 2

        self._currentYearIx = 0
        self._years = sorted(self._datamodel.allMovies.iterkeys())
        self._updateYearState()

    def _updateBrowseButtons(self):
        """Set the text of the browse buttons to indicate current subsets"""
        prev = self._currentSubsetIndex
        next = self._currentSubsetIndex + 2
        
        if(prev == 0):
            prev = self._currentSubsetCount
            
        if(next > self._currentSubsetCount):
            next = 1
               
        text = lang[lng.txtPage] + " {}/{}".format(prev, self._currentSubsetCount)
        self._btnPrev.setText(text)
        
        text = lang[lng.txtPage] + " {}/{}".format(next, self._currentSubsetCount)
        self._btnNext.setText(text)

    def _updateYearState(self):
        """Update internal variables that depend on the selected category"""
        self._currentMovies = self._datamodel.allMovies.get(self._years[self._currentYearIx])
        self._currentMovieCount = len(self._currentMovies)
        self._currentSubsetIndex = 0
        self._currentSubsetCount = (len(self._currentMovies) + self._subsetSize - 1) / self._subsetSize

    def _setPlayMode(self):
        """Enable player, disable preview"""
        for button in self._activeInPreview:
            button.setEnabled(False)

        self._btnPlay.setText(lang[lng.txtStop])
        self._btnPlay.setCommand(self._ehStop)

        self._canvas.itemconfigure(self._playerwnd, state = NORMAL)
        self._previewFrame.setVisible(False)
        self._mode = _play

    def _setPreviewMode(self):
        """Enable preview, disable player"""
        for button in self._activeInPreview:
            button.setEnabled(True)

        self._btnPlay.setText(lang[lng.txtPlay])
        self._btnPlay.setCommand(self._ehPlay)
        
        self._canvas.itemconfigure(self._playerwnd, state = HIDDEN)
        self._previewFrame.setVisible(True)
        self._mode = _preview

    def _setSubset(self):
        """Display a subset of the available media items"""
        self._updateBrowseButtons()
        start = self._subsetSize * self._currentSubsetIndex
        stop = min(start + self._subsetSize + 1, self._currentMovieCount)
        self._previewFrame.previewsubset(self._currentMovies[start:stop])
        
    def _play(self):
        """Start playback"""
        self._setPlayMode()
        self._datacollector.addStatisticLine(lng.txtPlaybackStarted)
        
        try:
            self._playerFrame.play(self._previewFrame.selecteditem)
        except:
            self._playbackStopped()

    def _stop(self):
        """Stop playback"""
        #Update time to ensure that the session doesn't end because of the movie length
        self._datacollector.reset()
        self._datacollector.addStatisticLine(lng.txtUserStoppedPlayback)
        self._userstop = True
        self._playerFrame.stop()

    #Callbacks
    def _playbackStopped(self):
        """Handle user data collection and set preview mode"""
        if(not self._userstop):
            self._datacollector.reset()
            self._datacollector.addStatisticLine(lng.txtPlaybackFinished)
            self._userstop = False

        self._setPreviewMode()

    def _clbClicked(self):
        """Switch between playback and preview depending on mode"""
        if(self._mode == _preview):
            self._play()
        elif(self._mode == _play):
            self._stop()

    #Event handlers
    def _ehPlay(self, event, tb):
        """Handle play event
        
        Arguments
        event -- event object
        tb -- transparent button instance
        
        """
        self._play()
        
    def _ehStop(self, event, tb):
        """Handle stop event
        
        Arguments
        event -- event object
        tb -- transparent button instance
        
        """
        self._stop()

    def _ehYear(self, event, tb):
        """Handle an event from one of the category buttons
        
        Arguments
        event -- event object
        tb -- transparent button instance
        
        """
        self._datacollector.detect()
        
        self._currentYearIx = tb.index
        self._updateYearState()
        self._updateBrowseButtons()
        self._previewFrame.previewsubset(self._currentMovies[:self._subsetSize])

    def _ehPrev(self, event, tb):
        """Handle an event from the browse backward button
        
        Arguments
        event -- event object
        tb -- transparent button instance
        
        """
        self._datacollector.detect()
        if(self._currentSubsetIndex > 0):
            self._currentSubsetIndex -= 1
        else:
            self._currentSubsetIndex = self._currentSubsetCount - 1
            
        self._setSubset()
                    
    def _ehNext(self, event, tb):
        """Handle an event from the browse forward button
        
        Arguments
        event -- event object
        tb -- transparent button instance
        
        """
        
        self._datacollector.detect()
        if(self._currentSubsetIndex < (self._currentSubsetCount - 1)):
            self._currentSubsetIndex += 1
        else:
            self._currentSubsetIndex = 0
            
        self._setSubset()
