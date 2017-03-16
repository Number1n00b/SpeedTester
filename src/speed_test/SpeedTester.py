import sys
sys.path.insert(0, '/home/17766467/Desktop/home_projects/SpeedTester/src')

from file_io.csv_writer import CSVFileWriter
from file_io.util import *
from view.ui import *

from errors.calling_errors import *

from plotting.plotter import *

from connection import speedtest
import signal
import time
import os
import threading

mainDelay = 1200
failureDelay = 300

# A horrible hack that took me forever to do. The reason I had to hack it was because both the speedtest.py module
# and the tkinter module for some reason expect to be in main and to be in full control of main. (speedtest indirecty
# expected this because of using the signal.py module.
#
# Now, since I'm running two threads, one of them obviously cant be main, so I ended up moving tkinter to main, creating
# the signal in main (before initialising the ui) and then passing the signal to the ui module so that the signal THINKS
# it's in main when it really isn't.
#
# I could have also just left it as is and just let the program crash whenever the user clicks close....
#                                                                                      probably would have been worth it.


class SpeedTester(threading.Thread):

    def __init__(self, uiG):
        threading.Thread.__init__(self)
        self.window = uiG
        self.results_file_name = get_path_in_res("Speedtest_Results.txt")
        self.error_file_name = get_path_in_res("ErrorLog.txt")
        self.header = "date,time,ping,down,up,isp,ip,lat,long"

        self.running = True
        self.prevRun = True

        self.delay = mainDelay

        while not self.window.fin_init:
            time.sleep(0.5)

        self.start()

    def run(self):
        while self.running:
            try:
                if self.running:
                    self.window.set_status("Running test.")
                self.test_and_write()

                if self.running:
                    self.window.set_status("Waiting.")

                i = self.delay
                self.updateUITimer(i)
                while i > 0:
                    if not self.running:
                        break
                    time.sleep(1)
                    i -= 1
                    self.updateUITimer(i)
            except Exception as e:
                self.write_failure(e)
                raise e
        print("Finished scheduler.")

    def setDelay(self, newDelay):
        self.delay = newDelay
        if self.running:
            self.window.setDelay(newDelay)


    def updateUITimer(self, time):
        if self.running:
            self.window.update_next(time)


    def test_and_write(self):
        try:
            data = speedtest.shell(self.window.getSignal())
            if not data:
                self.write_failure("Connection cannot be established.")
            else:
                self.updateUI(data)
                self.write_data(data)
                self.setDelay(mainDelay)
                self.prevRun = True
        except Exception as e:
            self.write_failure(e)
            raise e

    def my_fail(self, e):
        print("Failed: " + str(e) + "\n")
        self.setDelay(failureDelay)
        self.prevRun = False

    def updateUI(self, data):
        currdate, currtime = getDateTime()
        date_and_time = currdate + " | " + currtime
        if self.running:
            self.window.set_values(date_and_time, data['down'][0:5])

    def write_data(self, data):
        currdate, currtime = getDateTime()
        line = makecsv(currdate, currtime, data['ping'][0:5], data['down'][0:5], data['up'][0:5], data['isp'], data['ip'], data['lat'],
                       data['long'])

        try:
            if os.path.isfile(self.results_file_name):
                file = open(self.results_file_name, 'a')
                writer = CSVFileWriter(file)
            else:
                file = open(self.results_file_name, 'w')
                writer = CSVFileWriter(file)
                writer.writeline(self.header)

            writer.writeline(line)
            file.close()
        except Exception as e:
            self.write_failure(e)

    def write_failure(self, error):
        self.my_fail(error)
        if not self.running:
            return 0

        currdate, currtime = getDateTime()
        line = makecsv(currdate, currtime, "FAILED", "FAILED", "FAILED", "FAILED", "FAILED", "FAILED", "FAILED")

        try:
            currdate, currtime = getDateTime()

            errorLog = open(self.error_file_name, 'a')
            errorLog.write(currdate + ", " + currtime + " | " + str(error) + "\n")

            if os.path.isfile(self.results_file_name):
                file = open(self.results_file_name, 'a')
                writer = CSVFileWriter(file)
            else:
                file = open(self.results_file_name, 'w')
                writer = CSVFileWriter(file)
                writer.writeline(self.header)

            writer.writeline(line)
            try:
                file.close()
            except Exception as e:
                self.my_fail(e)
        except Exception as e2:
            self.my_fail(e2)


def stop():
    print("stopped")


def unimp(): raise UnimplementedError

if __name__ == "__main__":
    siggyM = signal.signal(signal.SIGINT, stop)
    ui(siggyM, unimp, do_plot)
