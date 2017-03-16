import plotly
from plotly.graph_objs import *
from file_io.util import *
from file_io.csv_reader import CSVHeaderReader
import datetime

def do_plot():
    plotfile = get_path_in_res('SpeedTest_plot.html')
    data_file = get_path_in_res('Speedtest_Results.txt')

    reader = CSVHeaderReader(data_file)

    columns = ['date', 'time', 'ping', 'down', 'up']

    loaded_data = reader.readfile(columns)

    date_time = []
    up = []
    down = []
    ping = []

    for row in loaded_data:
        if not row[3] == "FAILED":
            to_parse = row[0] + " | " + row[1]
            date_time.append(parse_datetime(to_parse))
            ping.append(row[2])
            down.append(row[3])
            up.append(row[4])

    x = date_time
    y = list(map(float, up))
    z = list(map(float, down))
    k = list(map(float, ping))

    upBar = Bar(
        x=x,
        y=y,
        name="Up"
    )
    downBar = Bar(
        x=x,
        y=z,
        name="Down"
    )
    pingBar = Bar(
        x=x,
        y=k,
        name="Ping"
    )

    data = [upBar, downBar, pingBar]
    layout = Layout(
        barmode='group'
    )

    fig = Figure(data=data, layout=layout)
    plot_url = plotly.offline.plot(fig, filename=plotfile)


def parse_datetime(date_time):
    stripped = "".join(date_time.split(' '))

    formatted = stripped.replace('|', '/')
    formatted = formatted.replace(':', '/')

    str_result = []

    for x in formatted.split('/'):
        str_result.append(x)

    result = []
    for str in str_result:
        result.append(int(str))

    return datetime.datetime(result[0], result[1], result[2], result[3], result[4])