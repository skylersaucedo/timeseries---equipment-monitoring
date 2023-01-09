"""
final data viz with bokeh
"""

import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import Range1d, LinearAxis, Label, Div
from bokeh.models import Span

from skyler_detector import skyler_custom_detector

def main():
    """
    Use Bokeh and Arundo API to visualize detector in interactive env.
    """
    df = pd.read_csv('sensor_data.csv', index_col="datetime", parse_dates=True)

    df = skyler_custom_detector(df)

    time = df.index
    power = df['system power']
    flow = df['pump flow']
    p_tank = df['lube tank pressure']
    p_gearbox = df['lube gearbox pressure']
    t_gearbox = df['lube gearbox temperature']
    score = df['score']

    # params for visualization
    tools_to_show = 'box_zoom, pan, save, hover, reset, tap, wheel_zoom, lasso_select'
    w = 1000
    h = 250

    # make bokeh figures

    f_pow = figure(title="power", x_axis_type="datetime", width=w, height=h, tools=tools_to_show, title_location='above', align='center')
    f_f = figure(title="flow", x_axis_type="datetime", width=w, height=h, tools=tools_to_show, title_location='above', align='center')
    f_pre = figure(title="pressure", x_axis_type="datetime", width=w, height=h, tools=tools_to_show, title_location='above', align='center')
    f_temp = figure(title="temperature", x_axis_type="datetime", width=w, height=h, tools=tools_to_show, title_location='above', align='center')

    f_score = figure(title="detector score", width=w, height=h, tools=tools_to_show, title_location='above', align='center')

    # add data to figs

    f_pow.line(time,power, legend_label="power", line_width=3, line_color="red")

    # different scales for power and flow

    f_pow.yaxis.axis_label = r"$$\color{red} power $$"
    f_pow.extra_y_ranges = {"y2": Range1d(start=0, end = 15)}
    f_pow.add_layout(LinearAxis(y_range_name = "y2", axis_label = r"$$\color{blue} flow $$"), 'right')
    f_pow.line(time,flow, legend_label="flow", line_width=3, line_color="blue", y_range_name = "y2")
    f_pow.yaxis[0].major_label_text_color = "red"
    f_pow.yaxis[1].major_label_text_color = "blue"

    #f_f.line(time,flow, legend_label="flow", line_width=3, line_color="black")

    f_pre.line(time,p_tank, legend_label="lube tank pressure", line_width=3, line_color="blue")
    f_pre.y_range=Range1d(7, 15)

    f_score.line(time, score, legend_label="detector score", line_width=3, line_color="cyan")

    # different scales for pressures

    f_pre.yaxis.axis_label = r"$$\color{blue} lube tank pressure $$"
    f_pre.extra_y_ranges = {"y2": Range1d(start=40, end = 60)}
    f_pre.add_layout(LinearAxis(y_range_name = "y2", axis_label = r"$$\color{red} lube gearbox pressure $$"), 'right')
    f_pre.line(time,p_gearbox, legend_label="lube gearbox pressure", line_width=3, line_color="red", y_range_name = "y2")

    f_pre.yaxis[0].major_label_text_color = "blue"
    f_pre.yaxis[1].major_label_text_color = "red"

    # add temp line

    f_temp.line(time,t_gearbox, legend_label="temp", line_width=3, line_color="orange")

    # link time ranges together

    f_pow.x_range = f_f.x_range = f_pre.x_range = f_temp.x_range = f_score.x_range

    # add line where good data lives

    good_data = Span(location=pd.to_datetime('2019-11-06 13:00:00'), dimension='height', line_color='green',line_dash='dashed', line_width=3)

    f_pow.add_layout(good_data)
    f_pre.add_layout(good_data)
    f_temp.add_layout(good_data)
    f_score.add_layout(good_data)

    # add line where failure occurs

    failure = Span(location=pd.to_datetime('2019-11-10 16:00:00'), dimension='height', line_color='magenta',line_dash='dashed', line_width=3)

    f_pow.add_layout(failure)
    f_pre.add_layout(failure)
    f_temp.add_layout(failure)
    f_score.add_layout(failure)

    #assemble plots in a column

    plots = column([f_pow, f_pre, f_temp, f_score])

    show(column(Div(text="<h1>" + "results" + "</h1>"), plots))

    output_file("final_detector_behavior.html")



if __name__ == '__main__':
    main()