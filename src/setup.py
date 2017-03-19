from cx_Freeze import setup, Executable

import os

os.environ['TCL_LIBRARY'] = "F:\\Installs\\NewPython\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "F:\\Installs\\NewPython\\tcl\\tk8.6"

includes      = []
include_files = [r"F:\Installs\NewPython\DLLs\tcl86t.dll",
                 r"F:\Installs\NewPython\DLLs\tk86t.dll",
                 r"F:\Installs\NewPython\Lib\site-packages\pkg_resources\_vendor\packaging",
                 r"F:\Installs\NewPython\Lib\site-packages\pkg_resources\_vendor\appdirs.py",
                 r"F:\Installs\NewPython\Lib\site-packages\plotly\graph_objs\graph_objs_tools.py",
                 r"F:\Installs\NewPython\Lib\site-packages\idna\idnadata.py"
                 ]

setup(
    name = "Test",
    version = "1.0",
    options = {"build_exe": {"includes": includes, "include_files": include_files}},
    executables = [Executable("../src/controller/SpeedTester.py", base="Win32GUI")]
)