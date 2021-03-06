import datetime
import os

_pathsep = '/'


def get_path(*args):
    path = ""
    for arg in args:
        path += _pathsep + arg
    return path


def get_path_in_res(*parts):
    res_dir = os.path.realpath(__file__ + "\\..\\..\\..\\res")

    path = res_dir

    for arg in parts:
        path += _pathsep + arg
    return path


def makecsv(*args):
    csv = ""
    for ii in range(0, len(args)):
        csv += args[ii]
        if not ii == len(args) - 1:
            csv += ','
    return csv


def getDateTime():
    now = datetime.datetime.now()
    dateDelim = '/'
    currdate = str(now.year) + dateDelim + str(now.month) + dateDelim + str(now.day)
    currtime = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    return currdate, currtime

