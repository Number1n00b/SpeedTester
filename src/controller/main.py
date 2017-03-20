from errors.calling_errors import UnimplementedError

import signal
import os

from controller.scheduler import Scheduler

# Append the path of the project so that the files can be found.
import sys
sys.path.append(os.path.realpath(__file__) + "\\..\\..")

# Placeholder for unimplemented functionality.
def unimplemented():
    raise UnimplementedError

# Set up local plotting import.
try:
    from plotting.plotter import do_plot as local_plot_function
except ImportError as e:
    local_plot_function = unimplemented
    print("Import failed!")
    print(e)
    print("Local plotting disabled.")

# Set up online plotting import.
try:
    from plotting import do_online_plot as online_plot_function
except ImportError as e:
    online_plot_function = unimplemented
    print("Import failed!")
    print(e)
    print("Online plotting disabled.")

# Set up the ui imports.
try:
    from view.graphical_ui import GUI as availabe_ui
except ImportError as e:
    print("Import failed!")
    print(e)
    print("\nUsing command-line interface instead.")
    from view.command_line_ui import CUI as availabe_ui


def init():
    # Create the scheduler.
    test_scheduler = Scheduler()

    # Create the UI and Scheduler.
    availabe_ui(online_plot_function, local_plot_function, test_scheduler)


if __name__ == "__main__":
    init()

# main_signal = signal.signal(signal.SIGINT, handler=stop_signal)
