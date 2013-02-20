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
import zipfile
import os
import os.path
from datamodel import DataModel
import tkFileDialog
from tkMessageBox import showerror
import shutil
import fileformat as ff
import spmanager as spm
import language as lng
from language import lang

_exportdir = 'exportdata'
_importdir = 'importdata'

def _addsubdir(zip, archroot, srcdir):
    """Add all files in a folder to a zipfile recursively
    
    Arguments
    zip -- the ZipFile to add the files to
    archroot -- the root directory in the zip file
    srcdir -- the folder to add
    
    """
    for file in os.listdir(srcdir):
        fullname = os.path.join(srcdir, file)

        if(os.path.isdir(fullname)):
            _addsubdir(zip, os.path.join(archroot, file), fullname)
        else:
            archname = os.path.join(archroot, file)
            
            zip.write(fullname, archname)

def pack(srcdir, tgtfile):
    """Pack a zipfile
    
    Arguments
    srcdir -- the directory to pack into the zipfile
    tgtfile -- the zipfile to create
    
    """
    zip = zipfile.ZipFile(tgtfile, 'w')
    
    archroot = os.path.basename(srcdir)
    zip.write(srcdir, archroot)
    _addsubdir(zip, archroot, srcdir)
    zip.close()

def unpack(srcfile, tgtdir):
    """Unpack a zipfile
    
    Arguments
    srcfile -- the zipfile to unpack
    tgtdir -- the directory to unpack the zipfile into
    
    """
    zip = zipfile.ZipFile(srcfile, 'r')
    zip.extractall(tgtdir)

def export(items, tempdir):
    """Export a list of items
    
    Arguments
    items -- list of items to export
    tempdir -- directory to use for the export operation
    
    """
    initdir = spm.spmanager.getFirstPath([spm.ExportFolder, 
                                          spm.ImportFolder, 
                                          spm.MostRecentFolder])
    
    filenamepath = tkFileDialog.asksaveasfilename(initialdir = initdir, 
                                                  filetypes = ff.dlgExportFormats, 
                                                  defaultextension = ff.dlgDefaultExportExt)
        
    if(len(filenamepath) < 1):
        return
    
    spm.spmanager.setPath(spm.ExportFolder, os.path.dirname(filenamepath))
    
    #Create export dir and datamodel
    dmdir = os.path.join(tempdir, _exportdir)
    
    if(os.path.exists(dmdir)):
       shutil.rmtree(dmdir)
       
    os.makedirs(dmdir)
    
    dm = DataModel(dmdir)
    
    #Add all slideshows
    for item in items:
        if(not dm.addSlideshow(item, True)):
            showerror(lang[lng.txtExportError], lang[lng.txtCouldNotExport] + item.title)
            shutil.rmtree(dmdir)
            return

    #Save and zip
    dm.saveToFile()
    pack(dmdir, filenamepath)
    shutil.rmtree(dmdir)

def getImportDm(tempdir):
    """Show an open dialog for selecting a zipfile and create a datamodel from that zipfile
    
    Argument
    tempdir -- directory to use for the zipfile and the datamodel
    
    """
    initdir = spm.spmanager.getFirstPath([spm.ImportFolder, 
                                          spm.ExportFolder, 
                                          spm.MostRecentFolder])
    
    filenamepath = tkFileDialog.askopenfilename(initialdir = initdir, 
                                                filetypes = ff.dlgExportFormats, 
                                                defaultextension = ff.dlgDefaultExportExt)

    if(len(filenamepath) < 1):
        return None
    
    spm.spmanager.setPath(spm.ImportFolder, os.path.dirname(filenamepath))
    
    #Create import dir
    unpackdir = os.path.join(tempdir, _importdir)
    
    if(os.path.exists(unpackdir)):
       shutil.rmtree(unpackdir)
       
    os.makedirs(unpackdir)

    #Unpack file and create datamodel
    try:
        unpack(filenamepath, unpackdir)
        dmdir = os.path.join(unpackdir, _exportdir)
        dm = DataModel(dmdir, loadfromfile = True)
        return dm
    except:
        showerror(lang[lng.txtCorruptImportTitle], lang[lng.txtCorruptImport])
        return None
