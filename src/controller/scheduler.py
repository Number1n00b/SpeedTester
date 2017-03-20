import threading
import time

from file_io.csv_writer import CSVFileWriter
from file_io.util import *

from speedtester import speedtest

success_delay = 1200
failureDelay = 300

class Scheduler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.interface = None

        self.results_file_name = get_path_in_res("Speedtest_Results.txt")
        self.error_file_name = get_path_in_res("ErrorLog.txt")
        self.header = "date,time,ping,down,up"

        self.previous_run_success = True

        self.delay = success_delay
        self.should_quit = False

        self.start()

    def add_ui_elements(self, interface):
        self.interface = interface

    def exit(self):
        self.should_quit = True
        self.interface = None

    def run(self):
        first_run = True

        while not self.should_quit:
            if self.interface is not None:
                try:
                    if first_run:
                        self.interface.set_status("Running test.")
                        self.test_and_write()
                        first_run = False

                    self.interface.set_status("Waiting.")

                    # Reset the countdown
                    count_down = self.delay
                    if self.interface is not None:
                        self.interface.update_ui_next_timer(count_down)
                    else:
                        self.should_quit = True

                    while count_down > 0 and self.interface is not None:
                        time.sleep(1)
                        count_down -= 1
                        if self.interface is not None:
                            self.interface.update_ui_next_timer(count_down)
                        else:
                            self.should_quit = True

                    # Now we can run the test!
                    self.interface.set_status("Running test.")
                    self.test_and_write()

                except Exception as e:
                    self.log_failure_to_file(e)
                else:
                    self.should_quit = True

        print("Finished scheduler.")

    def set_delay(self, new_delay):
        self.delay = new_delay
        self.interface.change_delay(new_delay)

    def test_and_write(self):
        try:
            data = speedtest.shell()
            if not data:
                self.handle_test_failure("Connection cannot be established.")
            else:
                self.update_ui(data)
                self.write_data_to_csv(data)
                self.set_delay(success_delay)
                self.previous_run_success = True
        except Exception as e:
            self.handle_test_failure(e)

    def handle_test_failure(self, e):
        self.set_delay(failureDelay)
        self.previous_run_success = False
        self.log_failure_to_file(e)

    def update_ui(self, data):
        currdate, currtime = getDateTime()
        date_and_time = currdate + " | " + currtime
        self.interface.update_ui_test_results(date_and_time, data['down'][0:5])

    def write_data_to_csv(self, data):
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
            self.log_failure_to_file(e)

    def log_failure_to_file(self, error):
        if self.should_quit:
            return 0

        currdate, currtime = getDateTime()
        line = makecsv(currdate, currtime, "FAILED", "FAILED", "FAILED")

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
                print("Error occured while closing file.")
        except Exception as e2:
            print("Error occured while logging an error... oops.")