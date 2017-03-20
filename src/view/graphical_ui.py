import tkinter.messagebox as tmb
from tkinter import *

from errors.calling_errors import *

from controller import scheduler

class GUI(object):

    def __init__(self, plot_online_callback, plot_local_callback, test_scheduler):
        self.running = False

        self.test_scheduler = test_scheduler

        self.make_online_graph = plot_online_callback
        self.make_local_graph = plot_local_callback

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
        Button(top, text="Create graph (online)", command=self.protected_graph_online).grid(row=7, column=1)
        Button(top, text="Create graph (local)", command=self.protected_graph_local).grid(row=7, column=2)

        # Finishing touches.
        for child in top.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.running = True

        self.test_scheduler.add_ui_elements(self)

        top.mainloop()

        self.test_scheduler.exit()

        print("GUI exiting.")

        self.running = False

    def protected_graph_local(self):
        try:
            self.make_local_graph()
        except UnimplementedError as e:
            tmb.showinfo("Unimplemented!", "This function is not yet implemented.")
        except Exception as e2:
            tmb.showinfo("Error", str(e2))

    def protected_graph_online(self):
        try:
            self.make_online_graph()
        except UnimplementedError as e:
            tmb.showinfo("Unimplemented!", "This function is not yet implemented.")
        except Exception as e2:
            tmb.showinfo("Error", str(e2))

    def close_window(self):
        self.top.destroy()

    def update_ui_next_timer(self, next_test_time):
        self.next_run.set(str(next_test_time))

    def update_ui_test_results(self, run_time, speed):
        self.last_completed_run.set(run_time)
        self.latest_speed.set(speed)

    def set_status(self, new_stat):
        self.status.set(new_stat)

    def change_delay(self, new_delay):
        self.delay.set(new_delay)
