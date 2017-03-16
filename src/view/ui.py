from tkinter import *
import tkinter
import tkinter.messagebox as tmb
from errors.calling_errors import *
from speed_test.SpeedTester import *

from plotting import *

class ui(object):

    def __init__(self, sigM, online_graph, local_graph):
        self.fin_init = False
        self.make_online = online_graph
        self.make_local = local_graph
        self.mainSig = sigM
        self.run()

    def printStop(self):
        print("Stopped")

    def run(self):
        self.top = Tk()
        # Declaring Stringvars:
        self.top.title("Speed Tester")
        self.last_completed_run = StringVar()
        self.latest_speed = StringVar()
        self.next_run = StringVar()
        self.delay = StringVar()
        self.status = StringVar()
        self.top.resizable(0, 0)

        top = self.top

        # Initialising StringVars
        self.last_completed_run.set("None")

        self.latest_speed.set(0)

        self.next_run.set(0)

        self.status.set("Inactive.")

        # Setting up the interface. Grid is in total 2x5

        # Column1. Lables in this order:
        Label(top, text="Last successful run: ").grid(row=1, column=1)
        Label(top, text="Last speed (Mb/s): ").grid(row=2, column=1)
        Label(top, text="Next run (s): ").grid(row=3, column=1)
        Label(top, text="Delay (s): ").grid(row=4, column=1)

        # Column2. The values for each column and a "run now" button.
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

    def change_delay(self, new):
        self.delay.set(new)
    def update_next(self, time):
        self.next_run.set(str(time))

    def set_values(self, run_time, speed):
        self.last_completed_run.set(run_time)
        self.latest_speed.set(speed)

    def set_status(self, inStat):
        self.status.set(inStat)

    def setDelay(self, newDelay):
        self.delaynum = newDelay
        self.delay.set(newDelay)

    def getSignal(self):
        return self.mainSig
