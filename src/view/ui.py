import tkinter
import tkinter.messagebox as tmb
from tkinter import *

from errors.calling_errors import *
from controller.SpeedTester import *
from plotting import *


class Ui(object):

    def __init__(self, online_graph_function, local_graph_function):
        self.fin_init = False
        self.make_online = online_graph_function
        self.make_local = local_graph_function

        # Create the window.
        self.top = Tk()
        self.top.title("Speed Tester")
        self.top.resizable(0, 0)

        # Declaring StringVars:
        self.last_completed_run = StringVar()
        self.latest_speed = StringVar()
        self.next_run = StringVar()
        self.delay = StringVar()
        self.status = StringVar()

        # Initialising StringVars
        self.last_completed_run.set("None")
        self.latest_speed.set(0)
        self.next_run.set(0)
        self.delay.set("N/A")
        self.status.set("Inactive.")

        self.run()

    def run(self):
        # For convenience.
        top = self.top

        # Setting up the interface. Grid is in total 2x5
        # Column1. Lables in this order:
        Label(top, text="Last successful run: ").grid(row=1, column=1)
        Label(top, text="Last speed (Mb/s): ").grid(row=2, column=1)
        Label(top, text="Next run (s): ").grid(row=3, column=1)
        Label(top, text="Delay (s): ").grid(row=4, column=1)

        # Column2. The values for each column.
        Label(top, textvariable=self.last_completed_run).grid(row=1, column=2)
        Label(top, textvariable=self.latest_speed).grid(row=2, column=2)
        Label(top, textvariable=self.next_run).grid(row=3, column=2)
        Label(top, textvariable=self.delay).grid(row=4, column=2)

        # Status variable
        Label(top, text="Status: ").grid(row=6, column=1)
        Label(top, textvariable=self.status).grid(row=6, column=2)

        # Buttons for creating the graph.
        Button(top, text="Create graph (online)", command=self.try_online).grid(row=7, column=1)
        Button(top, text="Create graph (local)", command=self.try_local).grid(row=7, column=2)

        # Finishing touches.
        for child in top.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.fin_init = True

        try:
            self.main_class = SpeedTester(self)
            self.delaynum = self.main_class.delay
            self.top.mainloop()
        except Exception as e:
            print("SAVED!")
        print("Finished top.mainloop")

        self.main_class.running = False
        return ""

    def try_online(self):
        self.tryRun(self.make_online)

    def try_local(self):
        self.tryRun(self.make_local)

    def tryRun(self, func):
        try:
            func()
        except UnimplementedError as e:
            tmb.showinfo("Unimplemented!", "This function is not yet implemented.")
        except Exception as e2:
            tmb.showinfo("Error", str(e2))

    def close_threads(self):
        self.main_class.running = False
        self.top.destroy()

    def update_ui_next(self, time):
        self.next_run.set(str(time))

    def set_ui_values(self, run_time, speed):
        self.last_completed_run.set(run_time)
        self.latest_speed.set(speed)

    def set_status(self, inStat):
        self.status.set(inStat)

    def set_delay(self, newDelay):
        self.delaynum = newDelay
        self.delay.set(newDelay)