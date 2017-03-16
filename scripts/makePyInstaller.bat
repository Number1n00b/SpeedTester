@echo off
title Creating exe...

cd ..

pyinstaller --windowed --onefile -n SpeedTester.exe src/speed_test/SpeedTester.py

SET fileToMove=%CD%\src\dist;
SET destination=%CD%\dist;

REM echo moving %fileToMove%

REM echo to %destination%

REM move /Y %fileToMove% %destination%

REM pause

REM echo deleting %fileToMove%

REM RD /S %fileToMove%


echo
echo
echo

echo Finished build

pause