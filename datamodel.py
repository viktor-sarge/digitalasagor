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
from xml.dom.minidom import parse, Document
import os.path
import shutil
import uuid

import PIL.Image
import PIL.ImageTk

_xmlname = 'data.xml'

el_repository = "MovieRepository"
el_dir = "Directory"
el_slideshow = "Slideshow"
el_frame = "Frame"
el_desc = "Description"
attr_year = "Year"
attr_title = "Title"
attr_author = "Author"
attr_subdir = "SubDirectory"
attr_image = "Image"
attr_sound = "Sound"
attr_bgsound = "BgSound"
attr_category = "Category"
attr_type = "Type"
attr_video = "Video"
attr_group = "Group"

tpSlideshow = "Slideshow"
tpVideo = "Video"

class Frame:
    """One part of a slideshow"""
    def __init__(self, parent, image, sound):
        """Initiate the Frame
        
        Arguments
        parent -- the parent Slideshow
        image -- the image of this Frame
        sound -- the sound of this Frame
        
        """
        self._parent = parent
        self.image = image
        self.sound = sound
        self._previmage = None
        self._playbackimage = None
        
    def getImage(self):
        """Return the path of the image"""
        if(self.image <> ''):
            return self._parent.getPath(self.image)
        else:
            return ''

    def getSound(self):
        """Return the path of the sound """
        if(self.sound <> ''):
            return self._parent.getPath(self.sound)
        else:
            return ''

    def getPreviewImage(self):
        """Load the preview image if necessary and return it"""
        if(self._previmage is None):
            self._previmage = self._loadImageData(self._parent.getPrevsize())

        return self._previmage
    
    def getPlaybackImage(self):
        """Load the preview image if necessary and return it"""
        if(self._playbackimage is None):
            self._playbackimage = self._loadImageData(self._parent.getPlaysize())
            
        return self._playbackimage

    def _loadImageData(self, dimensions):
        """Return a scaled version of the image in this instance
        
        Arguments
        dimensions -- tuple containing desired width and height of the scaled image
        
        """
        image = PIL.Image.open(self.getImage())
        image = self._resizeImage(image, dimensions[0], dimensions[1])
        return PIL.ImageTk.PhotoImage(image)

    def loadImageData(self):
        """Load the image in preview and play size. If an image is already 
        loaded it will not be loaded again. 
        
        """
        
        if(self._previmage is None):
            self._previmage = self._loadImageData(self._parent.getPrevsize())

        if(self._playbackimage is None):
            self._playbackimage = self._loadImageData(self._parent.getPlaysize())

    def _resizeImage(self, image, maxwidth, maxheight):
        """Return a resized, keeping the aspect ratio of the original image
        
        Arguments
        image -- the input image
        maxwidth -- maximum width of the resized image
        maxheight -- maximum height of the resized image
        
        """
        width = float(image.size[0])
        height = float(image.size[1])
        ratio = width / height
        displayratio = float(maxwidth) / float(maxheight)
        
        if(ratio > displayratio):
            newwidth = maxwidth
            newheight = int(maxwidth / ratio)
        else:
            newwidth = int(maxheight * ratio)
            newheight = maxheight

        return image.resize((newwidth, newheight), PIL.Image.ANTIALIAS)

class Slideshow:
    """A slideshow"""
    def __init__(self, parent, xmlnode = None, uid = None, category = '', type = tpSlideshow):
        """Initiate the slideshow
        
        Arguments
        parent -- the parent DataModel
        xmlnode -- XML representation of the slideshow; will be used for initialization if specified
        uid --- the unique identifier of the slideshow
        category -- the category this slideshow belongs to
        type -- the type of this slideshow - shall be either tpSlideshow or tpVideo
        
        """
        self.frames = []
        self.parent = parent
        
        if(xmlnode is not None):
            self.uid = xmlnode.attributes[attr_subdir].value
            self.title = xmlnode.attributes[attr_title].value
            self.author = xmlnode.attributes[attr_author].value
            
            
            try:
                self.group = xmlnode.attributes[attr_group].value
            except KeyError:
                self.group = ''
            
            try:
                self.type = xmlnode.attributes[attr_type].value
            except KeyError:
                self.type = tpSlideshow

            self.category = xmlnode.attributes[attr_category].value
            
            if(self.type == tpSlideshow):
                self.bgsound = xmlnode.attributes[attr_bgsound].value
                self.video = ''
            elif(self.type == tpVideo):
                self.bgsound = ''
                self.video = xmlnode.attributes[attr_video].value

            for i in xmlnode.childNodes:
                if(i.nodeType == i.ELEMENT_NODE):
                    if(i.nodeName == el_frame):
                        image = i.attributes[attr_image].value
                        sound = i.attributes[attr_sound].value
                        self.frames.append(Frame(self, image, sound))
                    elif(i.nodeName == el_desc):
                        for j in i.childNodes:
                            if(j.nodeType == j.TEXT_NODE):
                                self.description = j.nodeValue.strip()

        else:
            self.title = ''
            self.author = ''
            self.bgsound = ''
            self.video = ''
            self.description = ''
            self.group = ''  
            self.category = category
            self.type = type
            
            if(uid is not None):
                self.uid = uid
            else:
                self.uid = str(uuid.uuid1())

    def __str__(self):
        return self.title

    def __repr__(self):
        return 'Slideshow: ' + self.title

    def addFrame(self, frame):
        """Add a frame to the slideshow
        
        Argument
        frame -- the frame to add
        
        """
        self.frames.append(frame)
            
    def getPrevsize(self):
        """Return a tuple containing size of preview images"""
        return self.parent.getPrevsize()
    
    def getPlaysize(self):
        """Return a tuple containing size of playback images"""
        return self.parent.getPlaysize()
    

    def getPath(self, filename):
        """Return the path to a file in the slideshow
        
        Argument
        filename -- the name of the file
        
        """
        return self.parent.getPath(os.path.join(self.uid, filename))
    
    def getXml(self, doc):
        """Return an XML representation of the slideshow
        
        Argument
        doc -- the XML document that will contain the new XML element
        
        """
        element = doc.createElement(el_slideshow)
        element.setAttribute(attr_bgsound, self.bgsound)
        element.setAttribute(attr_video, self.video)
        element.setAttribute(attr_title, self.title)
        element.setAttribute(attr_author, self.author)
        element.setAttribute(attr_subdir, self.uid)
        element.setAttribute(attr_category, self.category)
        element.setAttribute(attr_type, self.type)
        element.setAttribute(attr_group, self.group)
        descelement = doc.createElement(el_desc)
        descelement.appendChild(doc.createTextNode(self.description))
        element.appendChild(descelement)
        
        for frame in self.frames:
            subelement = doc.createElement(el_frame)
            subelement.setAttribute(attr_image, os.path.basename(frame.getImage()))
            subelement.setAttribute(attr_sound, os.path.basename(frame.getSound()))
            element.appendChild(subelement)
        
        return element
    
    def getBgSound(self):
        """Return the background sound of the slideshow, if any"""
        result = None
        
        if(self.bgsound != ''):
            result = self.getPath(self.bgsound)
            
        return result
    
    def loadImageData(self):
        """Load the image of all Frames in two sizes; preview and full size. If None is
        specified instead of image sizes, no load will occur. 
        
        """
        for frame in self.frames:
            frame.loadImageData()

    def getVideo(self):
        """Return the path to the video of this slideshow"""
        return self.getPath(self.video)

class DataModel:
    """The media repository of Digitala Sagor. Items are of class Slideshow and
    they are grouped by category. 

    """
    def __init__(self, topdir, prevsize = None, playsize = None, loadfromfile = False):
        """Initiate the data model
        
        Arguments
        topdir -- the directory of the media repository
        prevsize -- tuple containing size of preview images
        playsize -- tuple containing size of playback images
        loadfromfile -- if True, the repository will be loaded from XML if
        there is an XML file at the specified location; otherwise a new
        repository will be created

        """
        self._topdir = topdir
        self._doc = None
        self._prevsize = prevsize
        self._playsize = playsize
        self.allMovies = dict()
        
        if(loadfromfile):
            loadfromfile = os.path.exists(os.path.join(topdir, _xmlname))

        if(loadfromfile):
            #Traverse the movie repository
            xmldoc = parse(os.path.normpath(os.path.join(topdir, _xmlname)))
            self._doc = xmldoc
            
            for movieNode in xmldoc.documentElement.childNodes:
                if(movieNode.nodeType == movieNode.ELEMENT_NODE):
                    if(movieNode.nodeName == el_slideshow):
                        slideshow = Slideshow(self, movieNode)
                        category = slideshow.category
                        
                        if(category not in self.allMovies.keys()):
                            movieList = []
                            self.allMovies[category] = movieList
                        else:
                            movieList = self.allMovies[category]

                        #Store slideshow in the list
                        movieList.append(slideshow)
                                    
            self._cull()
        else:
            self._doc = Document()
            root = self._doc.createElement(el_repository)
            self._doc.appendChild(root)
            
    def getAll(self):
        """Return all Slideshows in the repository"""
        result = []
        
        for key in self.allMovies.keys():
            ml = self.allMovies[key]
            
            for m in ml:
                result.append(m)
                
        return result

    def addSlideshow(self, slideshow, dontmove = False):
        """Add a Slideshow to the media repository
        
        Argument
        slideshow -- the Slideshow to add
        dontmove -- if true, the slideshow remains in its original DataModel
        
        """
        category = slideshow.category
        
        if(category not in self.allMovies.keys()):
            exists = False
            movieList = []
            self.allMovies[category] = movieList
        else:
            movieList = self.allMovies[category]
            matches = filter(lambda s: s.uid == slideshow.uid, movieList)
            if(len(matches) == 0):
                exists = False
            elif(len(matches) == 1):
                exists = True
            else:
                exists = True
                print(len(matches), 'instances of slideshow', slideshow.uid)

        sdir = self.getPath(slideshow.uid)

        #Rename current slideshow directory            
        if(exists):
            bkpdir = self.getPath('__bkp__' + slideshow.uid)
            os.rename(sdir, bkpdir)
        
        #Create new directory and add all data
        os.mkdir(sdir)
        
        try:
            self._copyFiles(sdir, slideshow)
        except:
            if(exists):
                self._undoNewFiles(sdir, bkpdir)

            return False

        #Everything related to the datamodel where the slideshow came from has been copied, set this datamodel as parent
        if(not dontmove):
            slideshow.parent = self

        #Remove backup, old data structure and xml data
        oldNode = None
        
        if(exists):
            for node in self._doc.documentElement.childNodes:
                if(node.nodeType == node.ELEMENT_NODE):
                    if(node.nodeName == el_slideshow):
                        if(node.attributes[attr_subdir].value == slideshow.uid):
                            oldNode = node
                            break

            try:
                self._doc.documentElement.replaceChild(slideshow.getXml(self._doc), oldNode)
            except:
                self._undoNewFiles(sdir, bkpdir)
                return False
                            
            self.allMovies[category] = map(lambda s: slideshow if(s.uid == slideshow.uid) else s, movieList)

            try:
                shutil.rmtree(bkpdir, True)
            except:
                print('Could not remove temporary backup folder')            
        else:
            try:
                self._doc.documentElement.appendChild(slideshow.getXml(self._doc))
            except:
                try:
                    shutil.rmtree(sdir, True)
                except:
                    print('Could not remove new folder')            

                return False

            movieList.append(slideshow)

        return True

    def deleteSlideshow(self, slideshow):
        """Remove a Slideshow from the media repository
        
        Argument
        slideshow -- the Slideshow to remove
        
        """
        #Remove from data structure
        list = self.allMovies[slideshow.category]
        list.remove(slideshow)

        #Remove from xml
        for node in self._doc.documentElement.childNodes:
            if(node.nodeType == node.ELEMENT_NODE):
                if(node.nodeName == el_slideshow):
                    if(node.attributes[attr_subdir].value == slideshow.uid):
                        self._doc.documentElement.removeChild(node)
                        node.unlink()
                
        #Remove from disk
        sdir = self.getPath(slideshow.uid)
        shutil.rmtree(sdir)
            
    def saveToFile(self):
        """Save the media repository to XML"""            
        file = open(self.getPath(_xmlname), "w")
        #xml.dom.ext.PrettyPrint(self._doc, file)
        file.write(self._doc.toprettyxml(encoding = 'utf-8'))
        #self._doc.writexml(file, 0, 4, '\r\n', 'utf-8')
        file.close() 

    def loadImageData(self, clbProg):
        """Load image data for all Slideshows in the repository
        
        Arguments
        clbProg -- callback that will be called to update progress; shall have 
                   one argument that is a float representing the current load progress

        """
        count = 0.0
        ctr = 0.0
        
        for category in self.allMovies.keys():
            count += len(self.allMovies[category])

        for category in self.allMovies.keys():
            slist = list(self.allMovies[category])
            
            for s in slist:
                try:
                    s.loadImageData()
                except:
                    print('Could not load all images from slideshow ' + s.title)
                    #self.allMovies[category].remove(s)

                ctr += 1
                clbProg(ctr / count)

    def _undoNewFiles(self, dir, backupdir):
        shutil.rmtree(dir, True)
        os.rename(backupdir, dir)

    def isEmpty(self):
        return len(self.allMovies) < 1

    def _copyFiles(self, targetdir, slideshow):
        """Copy all files from a slideshow to a directory
        
        Arguments
        targetdir -- directory to copy files to
        slideshow == slideshow to copy files from
        
        """
        if(slideshow.bgsound != ''):
            shutil.copyfile(slideshow.getPath(slideshow.bgsound), os.path.join(targetdir, slideshow.bgsound))
            
        if(slideshow.video != ''):
            shutil.copyfile(slideshow.getPath(slideshow.video), os.path.join(targetdir, slideshow.video))

        for frame in slideshow.frames:
            if(frame.image != ''):
                shutil.copyfile(frame.getImage(), os.path.join(targetdir, frame.image))
            if(frame.sound != ''):
                shutil.copyfile(frame.getSound(), os.path.join(targetdir, frame.sound))

    def _cull(self):
        """Remove empty slideshows and empty categories"""
        #Cull empty media
        mediaToDelete = []
        
        for mediaList in self.allMovies.values():
            for media in mediaList:
                if((media.type == tpSlideshow) and (len(media.frames) < 1)):
                    mediaToDelete.append(media)
                    
            for media in mediaToDelete:
                mediaList.remove(media)
        
        #Cull empty years
        keysToDelete = []
        
        for i in self.allMovies:
            if(len(self.allMovies[i]) < 1):
                keysToDelete.append(i)
                
        for i in keysToDelete:
            del self.allMovies[i]
            
    def getPrevsize(self):
        """Return a tuple containing size of preview images"""
        return self._prevsize
    
    def getPlaysize(self):
        """Return a tuple containing size of playback images"""
        return self._playsize
    
    def setPrevsize(self, prevsize):
        """Set preview size
        
        Argument
        prevsize -- tuple containing size of preview images
        
        """
        self._prevsize = prevsize
    
    def setPlaysize(self, playsize):
        """Set preview size
        
        Argument
        playsize -- tuple containing size of playback images
        
        """
        self._playsize = playsize

    def getPath(self, filename):
        """Return the path to a file in the repository
        
        Argument
        filename -- the path to the file within the repository
        
        """
        return os.path.normpath(os.path.join(self._topdir, filename))
