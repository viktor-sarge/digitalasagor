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
"""This unit contains the file formats that are supported by Digitala Sagor"""
import language as lng


dlgExportFormats = [(lng.lang[lng.txtExpFileFormat] + ' (dsa)', '*.dsa'), ('zip', '*.zip')]
dlgDefaultExportExt = '.dsa'

dlgImageFormats = [('JPEG', '*.jpg'), ('JPEG', '*.jpeg'), ('GIF', '*.gif'), ('Bitmap', '*.bmp')]
dlgSoundFormats = [('Wave', '*.wav')]

validImageFormats = ['.JPG', '.JPEG']
validSoundFormats = ['.WAV']

""""This is the name that a background sound shall have if the create slideshow 
    from directory feature is used"""
bgsoundname = 'bg'
