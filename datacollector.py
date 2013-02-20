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
import datetime
from language import lang, txtNewSession

_statisticdatafile = 'statistik.txt'
_timeformat = '%y%m%d %H:%M:%S'
_maxIdleSeconds = 60

class DataCollector:
    """Collect data about how the program is used"""
    def __init__(self):
        """Initiate the DataCollector"""
        self._datafile = open(_statisticdatafile, 'a')
        self._latestAction = datetime.datetime(year = datetime.MINYEAR, month = 1, day = 1)

    def addStatisticLine(self, text):
        """Add a line of text; a time stamp will be inserted automatically
        
        Argument
        text -- the text to add
        
        """
        self.detect()
        self._datafile.write(self._getTimestamp() + text + '\r\n')
        self._datafile.flush()
        
    def detect(self):
        """Detect user interaction; used for determining when a new session begins"""
        dt = datetime.datetime.now()
        td = dt - self._latestAction
        self._latestAction = dt
        
        if(td.seconds > _maxIdleSeconds):
            self._datafile.write('\n' + self._getTimestamp() + txtNewSession + '\n')
            self._datafile.flush()

    def reset(self):
        """Reset the detection"""
        self._latestAction = datetime.datetime.now()
        
    def _getTimestamp(self):
        """Return a timestamp"""
        return self._latestAction.strftime(_timeformat) + '> '
