# SpeedTester
=================

Intorduction
-------------
This is a small python based UI which uses SpeedTest.net to test the user's internet speed at regular intervals. 
The data is logged to a csv file and the user can easily create a plot of the data for visual inspection.

This tool:
  - Is written in Python
  - Uses Tkinter for the GUI
  - Uses an adaption of Matt Mart'z command line speedtest application. (See https://github.com/sivel/speedtest-cli)
  - Is used via the UI
  - Supports differing intervals for speed test, based on if the previous speed test failed.
     e.g Use regular intervals of 15 minutes, if previous test failed, test again in 5 minutes.
  - Allows for instalation using cxFreeze. 
  - Tested on Windows 64 bit.


Build Description and Dependancies
----------------------------------

CURRENTLY NOT WORKING

Build dependecies
 - xcFreeze

Runtime Dependencies:
 - plotly


From ".../scripts":
  maxeCXFreeze.bat
  
Usage
-------
python src/speed_test/SpeedTester.py

CURRENTLY NOT WORKING
Run the .exe created by the build script. (Found in '.../dist/src')

Contribution
------------
If you want to contribute to solcign a bug, unexpected behaviour or if you have a interesting feature
in your mind which fits to this tool, please add an issue / feature request.

Pull requests are always welcome.


License
----------

This program is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation;
either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General
Public License along with this program; if not, see
<http://www.gnu.org/licenses/>.
