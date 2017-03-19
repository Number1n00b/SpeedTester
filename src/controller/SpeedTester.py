import threading
import signal
import time
import os

# Append the path of the project so that the files can be found.
import sys
sys.path.append(os.path.realpath(__file__) + "\\..\\..")

import view.ui
from file_io.util import *
from file_io.csv_writer import CSVFileWriter

from errors.calling_errors import *
from plotting.plotter import *

from speedtester import speedtest

success_delay = 1200
failureDelay = 300
main_signal = 0

# A hack. The reason I had to do it was because both the speedtest.py module
# and the tkinter module for some reason expect to be in main and to be in full control of main. (speedtest indirecty
# expected this because of using the signal.py module.
#
# Now, since I'm running two threads, one of them obviously cant be main, so I ended up moving tkinter to main, creating
# the signal in main (before initialising the view) and then passing the signal to the view module so that the signal THINKS
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
        self.header = "date,time,ping,down,up"

        self.running = True
        self.previous_run_success = True

        self.delay = success_delay

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
                self.update_UITimer(i)
                while i > 0:
                    if not self.running:
                        break
                    time.sleep(1)
                    i -= 1
                    self.update_UITimer(i)
            except Exception as e:
                self.write_failure(e)
                raise e
        print("Finished scheduler.")

    def set_delay(self, new_delay):
        self.delay = new_delay
        if self.running:
            self.window.set_delay(new_delay)

    def update_UITimer(self, new_time):
        if self.running:
            self.window.update_ui_next(new_time)

    def test_and_write(self):
        try:
            data = speedtest.shell(main_signal)
            if not data:
                self.write_failure("Connection cannot be established.")
            else:
                self.update_ui(data)
                self.write_data(data)
                self.set_delay(success_delay)
                self.previous_run_success = True
        except Exception as e:
            self.write_failure(e)
            raise e

    def handle_test_exception(self, e):
        print("Failed: " + str(e) + "\n")
        self.set_delay(failureDelay)
        self.previous_run_success = False

    def update_ui(self, data):
        currdate, currtime = getDateTime()
        date_and_time = currdate + " | " + currtime
        if self.running:
            self.window.set_ui_values(date_and_time, data['down'][0:5])

    def write_data(self, data):
        currdate, currtime = getDateTime()
        #line = makecsv(currdate, currtime, data['ping'][0:5], data['down'][0:5], data['up'][0:5], data['isp'], data['ip'], data['lat'],
        #               data['long'])
        line = makecsv(currdate, currtime, data['ping'][0:5], data['down'][0:5], data['up'][0:5])

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
        self.handle_test_exception(error)
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
                self.handle_test_exception(e)
        except Exception as e2:
            self.handle_test_exception(e2)


def stop(signum, frame):
    print("stopped")
    print("Info: " + str(signum) + ", " + str(frame))


# A placeholder function for creating an online plot, since I have not implemented it yet.
def unimp(): raise UnimplementedError

if __name__ == "__main__":
    # Create the signal to use for speed tests.
    main_signal = signal.signal(signal.SIGINT, handler=stop)

    # Create the UI.
    view.ui.Ui(unimp, do_plot)
