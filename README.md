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
  - Displays results in Mb/s.

Use Case
--------
I live in Australia and have Telstra as my ISP. We are on the NBN with an internet plan of 100Mb/s upload.
The cost of our plan is $95 per month. We never reach the 100Mb/s speed in practise, and generally it is more
like 20Mb/s on an average day (With a max of 60). After many complaints to telstra, I decided to write this program
to give them proof of our inconsistant and slow speeds. 
They apologised once they saw the eveidence and gave us a $20 discount PER MONTH. 

Build and Dependancies (CURRENTLY NOT WORKING)
----------------------------------------------------------

Build dependecies
 - cxFreeze

Runtime Dependencies:
 - plotly
   To get plotly, use:
       'pip install plotly'
        OR 
       'sudo pip install plotly'
   (See https://plot.ly/python/getting-started/ for more details)
 

From ".../scripts":
  maxeCXFreeze.bat
  
Usage
-------
python src/controller/SpeedTester.py

NOTE: All speed results are displayed in Mb/s.

CURRENTLY NOT WORKING
Run the .exe created by the build script. (Found in '.../dist/src')

Contribution
------------
If you want to contribute to solvign a bug, fixing unexpected behaviour or if you have a interesting feature
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
