# coding=utf-8
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

"""This unit contains translations for different languages. 

"""
txtPrev = "Previous"
txtNext = "Next"
txtPlay = "Play"
txtStop = "Stop"
txtMoviesFromYear = "MoviesFromYear"
txtTitle = "Title"
txtBy = "By"
txtUp = 'Up'
txtDown = 'Down'
txtDelete = 'Delete'
txtTop = 'To Top'
txtBottom = 'To Bottom'
txtImage = 'Image'
txtSound = 'Sound'
txtSlide = 'Slide'
txtListen = 'Listen'
txtSelect = 'Select'
txtPlayFromHere = 'Play from Here'
txtPlayThisFrame = 'Play This Frame'
txtTitle = 'Title'
txtAuthor = 'Author'
txtDesc = 'Description'
txtCommon = 'Common'
txtBgSound = 'Background Sound'
txtNewFrame = 'New Frame'
txtSave = 'Save'
txtExport = 'Export'
txtCategory = 'Category'
txtSelectedSlideshow = 'Selected Slideshow'
txtEdit = 'Edit'
txtDb = 'Database'
txtSCount = 'Number of Slideshows'
txtImport = 'Import'
txtSelCount = u"Number of Selected Slideshows"
txtSelection = u"Selected Slideshows"
txtCancel = u"Cancel"
txtNew = u"New Project"
txtNewEmpty = u"New Empty Project"
txtNewFromFolder = u"New Project from Folder"
txtExpFileFormat = u"Digitala Sagor Archive"
txtPage = 'Page'
txtVideo = 'Video'
txtWatch = 'Watch'
txtNewVideo = 'New Video'
txtPlayer = 'Player'
txtNew = 'New'
txtManage = 'Manage'
txtEditVideo = 'Edit Video'
txtEditSlideshow = 'Edit Slideshow'
txtNewSession = 'New session'
txtPlaybackFinished = 'Playback finished'
txtPlaybackStarted = 'Playback started'
txtUserStoppedPlayback = 'User stopped playback'
txtGroup = "Group"
txtFilter = "Filter"
txtClear = "Clear"
txtClearAll = "Clear All"
txtField = "Field"
txtValue = "Value"
txtActiveFilters = "Active Filters"
txtLoadImageProgress = 'Loading images...'
txtAdminTitle = 'Administration'
txtExportError = 'Export Error'
txtCouldNotExport = 'Could not export '
txtCorruptImportTitle = 'Import Error'
txtCorruptImport = 'Import file is corrupt'
txtCopyError = 'Copy Error'
txtCouldNotCopy = 'Could not copy '
txtOpenError = 'Error'
txtCouldNotOpen = 'Could not open '
txtPlayFrameError = 'Error'
txtCouldPlayFrame = 'Could not play frame {} in '
txtCouldNotImportSlideshow = 'Could not import '
txtSaveError = 'Error'
txtCouldNotSave = 'Could not save '
txtSoundErrorTitle = 'Sound Error'
txtCantInitSound = 'Cannot initialize sound'
txtTooFewChannels = 'Too few sound channels available; need 2 but found {}'
txtNoMoviesTitle = 'No Movies'
txtNoMovies = 'There are no movies to show. Please select another database in the inifile.'

dlgUnsavedTitle = "Unsaved Changes Title"
dlgUnsaved = "Unsaved Changes"
dlgDelFrameTitle = "Remove Frame Title"
dlgDelFrame = "Remove Frame"
dlgDelSShowTitle = "Remove Slideshow Title"
dlgDelSShow = "Remove Slideshow"
dlgLoadImages = 'Loading Images'

def getSwedish():
    """Return a dictionary containing the constants above translated to Swedish."""
    result = dict()
    result[txtPrev] = u"Förra"
    result[txtNext] = u"Nästa"
    result[txtPlay] = u"Spela"
    result[txtStop] = u"Stoppa"
    result[txtMoviesFromYear] = u"Filmer från år "
    result[txtBy] = u"av"
    result[txtUp] = u"Upp"
    result[txtDown] = u"Ner"
    result[txtDelete] = u"Ta bort"
    result[txtTop] = u"Först"
    result[txtBottom] = u"Sist"
    result[txtImage] = u"Bild"
    result[txtSound] = u"Ljud"
    result[txtSlide] = u"Scen"
    result[txtListen] = u"Lyssna"
    result[txtSelect] = u"Välj"
    result[txtPlayFromHere] = u"Spela härifrån"
    result[txtPlayThisFrame] = u"Spela denna"
    result[txtTitle] = u"Titel"
    result[txtAuthor] = u"Författare"
    result[txtDesc] = u"Beskrivning"
    result[txtCommon] = u"Allmänt"
    result[txtBgSound] = u"Bakgrundsljud"
    result[txtNewFrame] = u"Ny scen"
    result[txtSave] = u"Spara"
    result[txtExport] = u"Exportera"
    result[txtCategory] = u"År"
    result[txtSelectedSlideshow] = u"Valt bildspel"
    result[txtEdit] = u"Redigera"
    result[txtDb] = u"Databas"
    result[txtSCount] = u"Antal bildspel"
    result[txtImport] = u"Importera"
    result[txtSelCount] = u"Antal valda bildspel"
    result[txtSelection] = u"Valda bildspel"
    result[txtCancel] = u"Avbryt"
    result[txtNew] = u"Nytt bildspel"
    result[txtNewEmpty] = u"Nytt tomt bildspel"
    result[txtNewFromFolder] = u"Nytt bildspel från katalog"
    result[txtExpFileFormat] = u"Digitala sagor-arkiv"
    result[txtPage] = u"Sida"
    result[txtVideo] = u"Film"
    result[txtWatch] = u"Spela upp"
    result[txtNewVideo] = u"Ny film"
    result[txtPlayer] = u"Spelare"
    result[txtNew] = u"Nytt"
    result[txtManage] = u"Hantera"
    result[txtEditVideo] = u"Redigera film"
    result[txtEditSlideshow] = u"Redigera bildspel"
    result[txtNewSession] = u"Ny session"
    result[txtPlaybackFinished] = u"Uppspelning klar"
    result[txtPlaybackStarted] = u"Uppspelning påbörjad"
    result[txtUserStoppedPlayback] = u"Användaren avbröt uppspelningen"
    result[txtGroup] = u"Klass och skola"
    result[txtFilter] = u"Sök"
    result[txtClear] = u"Rensa"
    result[txtClearAll] = u"Rensa alla"
    result[txtField] = u"Fält"
    result[txtValue] = u"Värde"
    result[txtActiveFilters] = u"Aktiva sökfilter"
    result[txtLoadImageProgress] = u"Laddar bilder... {: >7.2%} klart"
    result[txtAdminTitle] = u"Digitala sagor"
    result[txtExportError] = u"Exportfel"
    result[txtCouldNotExport] = u"Kunde inte exportera "
    result[txtCorruptImportTitle] = u"Importfel"
    result[txtCorruptImport] = u"Importfilen är korrupt"
    result[txtCopyError] = u"Fel"
    result[txtCouldNotCopy] = u"Kunde inte lägga till "
    result[txtOpenError] = u"Fel"
    result[txtCouldNotOpen] = u"Kunde inte öppna "
    result[txtPlayFrameError] = u"Fel"
    result[txtCouldPlayFrame] = u"Kunde inte spela scen {} i "
    result[txtCouldNotImportSlideshow] = u"Kunde inte importera "
    result[txtSaveError] = u"Error"
    result[txtCouldNotSave] = u"Kunde inte spara "
    result[txtSoundErrorTitle] = u"Ljudfel"
    result[txtCantInitSound] = u"Kan inte initiera ljud"
    result[txtTooFewChannels] = u"För få ljudkanaler tillgängliga; behöver 2 men hittade bara {}"
    result[txtNoMoviesTitle] = u"Inga filmer"
    result[txtNoMovies] = u"Det finns inga filmer att visa. Vänligen välj en annan databas i inifilen."

    result[dlgUnsavedTitle] = u"Osparade ändringar"
    result[dlgUnsaved] = u"Ett bildspel är redan öppet för redigering. Vill du spara ändringarna?"
    result[dlgDelFrameTitle] = u"Bekräfta ta bort scen"
    result[dlgDelFrame] = u"Vill du verkligen ta bort scenen?"
    result[dlgDelSShowTitle] = u"Bekräfta borttagning"
    result[dlgDelSShow] = u"Vill du verkligen ta bort bildspelen?"
    result[dlgLoadImages] = u"Laddar bilder"

    return result

def getEnglish():
    """Return a dictionary containing the constants above translated to English."""
    result = dict()
    result[txtPrev] = u"Previous"
    result[txtNext] = u"Next"
    result[txtPlay] = u"Play"
    result[txtStop] = u"Stop"
    result[txtMoviesFromYear] = u"Movies from Year "
    result[txtBy] = u"by"
    result[txtUp] = u"Up"
    result[txtDown] = u"Down"
    result[txtDelete] = u"Delete"
    result[txtTop] = u"First"
    result[txtBottom] = u"Last"
    result[txtImage] = u"Image"
    result[txtSound] = u"Sound"
    result[txtSlide] = u"Frame"
    result[txtListen] = u"Listen"
    result[txtSelect] = u"Select"
    result[txtPlayFromHere] = u"Play from Here"
    result[txtPlayThisFrame] = u"Play This"
    result[txtTitle] = u"Title"
    result[txtAuthor] = u"Author"
    result[txtDesc] = u"Description"
    result[txtCommon] = u"Common"
    result[txtBgSound] = u"Background sound"
    result[txtNewFrame] = u"New Frame"
    result[txtSave] = u"Save"
    result[txtExport] = u"Export"
    result[txtCategory] = u"Year"
    result[txtSelectedSlideshow] = u"Selected Slideshow"
    result[txtEdit] = u"Edit"
    result[txtDb] = u"Database"
    result[txtSCount] = u"Number of Slideshows"
    result[txtImport] = u"Import"
    result[txtSelCount] = u"Number of selected Slideshows"
    result[txtSelection] = u"Selected Slideshows"
    result[txtCancel] = u"Cancel"
    result[txtNew] = u"New Slideshow"
    result[txtNewEmpty] = u"New Empty Slideshow"
    result[txtNewFromFolder] = u"New Slideshow from Folder"
    result[txtExpFileFormat] = u"Digitala Sagor Archive"
    result[txtPage] = u"Page"
    result[txtVideo] = u"Video"
    result[txtWatch] = u"Play"
    result[txtNewVideo] = u"New Video"
    result[txtPlayer] = u"Player"
    result[txtNew] = u"New"
    result[txtManage] = u"Manage"
    result[txtEditVideo] = u"Edit Video"
    result[txtEditSlideshow] = u"Edit Slideshow"
    result[txtNewSession] = u"New session"
    result[txtPlaybackFinished] = u"Playback Complete"
    result[txtPlaybackStarted] = u"Playback Started"
    result[txtUserStoppedPlayback] = u"User Stopped Playback"
    result[txtGroup] = u"Class and School"
    result[txtFilter] = u"Search"
    result[txtClear] = u"Clear"
    result[txtClearAll] = u"Clear All"
    result[txtField] = u"Field"
    result[txtValue] = u"Value"
    result[txtActiveFilters] = u"Active Search Filters"
    result[txtLoadImageProgress] = u"Loading images... {: >7.2%} complete"
    result[txtAdminTitle] = u"Digitala Sagor"
    result[txtExportError] = u"Export Error"
    result[txtCouldNotExport] = u"Could not export "
    result[txtCorruptImportTitle] = u"Import Error"
    result[txtCorruptImport] = u"The import file is corrupt"
    result[txtCopyError] = u"Error"
    result[txtCouldNotCopy] = u"Could not add "
    result[txtOpenError] = u"Error"
    result[txtCouldNotOpen] = u"Could not open "
    result[txtPlayFrameError] = u"Error"
    result[txtCouldPlayFrame] = u"Could not play frame {} in "
    result[txtCouldNotImportSlideshow] = u"Could not import "
    result[txtSaveError] = u"Error"
    result[txtCouldNotSave] = u"Could not save "
    result[txtSoundErrorTitle] = u"Sound Error"
    result[txtCantInitSound] = u"Cannot initialize sound"
    result[txtTooFewChannels] = u"Too few sound channels available; need 2 but found {}"
    result[txtNoMoviesTitle] = u"No Movies"
    result[txtNoMovies] = u"There are no movies to show. Please select another database in the inifile."

    result[dlgUnsavedTitle] = u"Unsaved Changes"
    result[dlgUnsaved] = u"A slideshow is opened for editing. Do you want to save the changes?"
    result[dlgDelFrameTitle] = u"Confirm Delete Frame"
    result[dlgDelFrame] = u"Are you sure you want to delete the frame?"
    result[dlgDelSShowTitle] = u"Confirm Delete Slideshows"
    result[dlgDelSShow] = u"Are you sure you want to delete the slideshows?"
    result[dlgLoadImages] = u"Loading Images"

    return result

"""Variable lang contains the dictionary that is used in the application."""
lang = getSwedish()
#lang = getEnglish()
