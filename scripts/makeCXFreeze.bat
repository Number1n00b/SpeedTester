@echo off
title Creating exe...

cd ../src

python setup.py bdist_msi

echo "Setting up dependencies..."

SET fileToMove=%CD%\build\exe.win32-3.5
SET destination=%CD%\..\dist

move %fileToMove%\packaging\*.py %fileToMove%\pkg_resources\_vendor\packaging
move %fileToMove%\appdirs.py %fileToMove%\pkg_resources\_vendor
move %fileToMove%\graph_objs_tools.py %fileToMove%\plotly\graph_objs
move %fileToMove%\idnadata.py %fileToMove%\idna

echo moving %fileToMove%
echo to %destination%

move /Y %fileToMove% %destination%

ren %destination%\exe.win32-3.5 auto_created

echo Finished build

pause