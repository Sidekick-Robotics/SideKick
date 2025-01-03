"""
A file to handle receiving and parsing graphing data and to
display the data onto a graph.
"""

import time

import pyqtgraph as pg
import numpy as np

from globals import SK_LITE_OFF_QSS, SK_LITE_ON_QSS
from globals import GRAPH_BEGINNING, GRAPH_ENDING
from globals import NUM_OF_DATA_PTS, COLOUR_ORDER

class Graph:
    """
    Sets up the graphing object to show it on the screen.

    Attributes:
        key (string): the string that says the data belongs to the graph
        graph_data (list): all of the graph data for this graph
        plots (list): the plots on the pyqtgraph object
        labels (list): the label for each variable on the graph
        graph (pyqtgraph): the graph object
        legend (pyqtgraph.addLegend): the style of the graph

    Methods:
        decode_graph_data:
            Picks out the graph data from the raw data

            Args:
                raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
            Returns:
                graph_data (list): holds the values for the graph

        set_graph_data:
            Gets the graph data and puts it in the form to be plotted

            Args:
                raw_data (list): a list of all raw data

        update_plots:
            Adds or removes old plots.

            Args:
                num_of_plots (int): the number of plots

        update_graph:
            To update the graphs displayed on the main GUI
    """

    def __init__(self, key="0"):
        # variable definitions
        self.resize = True
        self.key = key
        self.graph_data = []
        self.plots = []
        self.labels = []

        # pyqtgraph definitions
        self.graph = pg.PlotWidget()
        self.legend = self.graph.addLegend()

        # Modify look of graphs
        self.graph.setMenuEnabled(False)
        self.graph.setBackground('#2b2b35')
        self.legend.setLabelTextColor("#FFFFFF")
        self.graph.getAxis(
            'left').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis(
            'bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis("left").setTextPen((255, 255, 255))
        self.graph.getAxis("bottom").setTextPen((255, 255, 255))

    def clear_graph(self):
        """
        Removes all data from graph
        """
        for item in self.plots:
            self.graph.removeItem(item)

        self.graph_data = []
        self.plots = []
        self.labels = []

    def decode_graph_data(self, raw_input:str) -> list:
        """
        Picks out the graph data from the raw data

        Args:
            raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        Returns:
            graph_data (list): holds the values for the graph
        """

        raw_list = []
        graph_data = []
        raw_input = raw_input.split(GRAPH_BEGINNING)

        for i, data in enumerate(raw_input):
            if GRAPH_ENDING in data:
                raw_list.append(raw_input[i].split(GRAPH_ENDING)[0])

        for graph in raw_list:

            graph = graph.split(",")
            name, key, data = graph[0], graph[1], graph[2]

            if key != self.key:
                continue

            if name not in self.labels:
                self.labels.append(name)

            is_num = data.replace("-", "").replace(".", "").isnumeric()

            if -1 < data.count("-") < 2 and -1 < data.count(".") < 2 and is_num:
                graph_data.append(float(data))
                if float(data) > 60:
                    print(data)
            else:
                graph_data.append(np.nan)
                print(f"<<< ERROR >>> Decoding graph data! {raw_input}")

        return graph_data

    def set_graph_data(self, raw_data:list):
        """
        Gets the graph data and puts it in the form to be plotted

        Args:
            raw_data (list): a list of all raw data
        """

        if not raw_data:
            return

        plots = []

        for data in raw_data:
            data = self.decode_graph_data(data)
            if data:
                for i, point in enumerate(data):
                    if i < len(plots):
                        plots[i].append(point)
                    else:
                        plots.append([point])

        for i, plot in enumerate(plots):
            if i < len(self.graph_data):
                self.graph_data[i] += plot
                while len(self.graph_data[i]) > NUM_OF_DATA_PTS:
                    self.graph_data[i].pop(0)
            else:
                self.graph_data.append(plot)

    def update_plots(self, num_of_plots:int):
        """
        Adds or removes old plots.

        Args:
            num_of_plots (int): the number of plots
        """
        # remove all graphs
        for item in self.plots:
            self.graph.removeItem(item)

        # add new graphs
        for i in range(num_of_plots):
            self.plots.append(self.graph.plot([0],[0], name=self.labels[i]))

    def update_graph(self):
        """
        To update the graphs displayed on the main GUI
        """

        plots = self.graph_data

        # if there is a change in the number of plots, update
        if len(plots) != len(self.plots):
            self.update_plots(len(plots))

        # replace the data with the latest data
        for index, plot in enumerate(self.plots):
            # if the amount of plots is not equal throughout
            # then delete all plots and break from the update loop
            if len(plots)-1 < index:
                self.update_plots(0)
                self.plots = []
                self.labels = []
                self.graph_data = []
                break
            # update plot
            pen = pg.mkPen(color=COLOUR_ORDER[index%len(COLOUR_ORDER)])
            plot.setData(np.array(plots[index], dtype=float), pen=pen)


class Widgets:
    """
    Super class to DeviceManagerWindow, FileManagerWindow, and RecordLight

    Attributes:
        show (bool): whether or not to display the GUI
        width (int): the width of the widget
        height (int): the height of the widget

    Methods:
        get_show:
            Returns:
                bool: whether or not to show the GUI
        get_height:
            Returns:
                int: the height of the widget
        get_width:
            Returns:
                int: the width of the widget
    """

    def __init__(self, state=False, width=0, height=0):
        self.show = state
        self.width = width
        self.height = height

    def update_show(self):
        """
        converts show to not show
        """
        self.show = not self.show

    def get_show(self):
        """
        Returns:
            bool: whether or not to show the GUI
        """
        return self.show

    def get_height(self):
        """
        Returns:
            int: the height of the widget
        """
        return int(self.height)

    def get_width(self):
        """
        Returns:
            int: the width of the widget
        """
        return int(self.width)


class RecordLight(Widgets):
    """
    Blinks the record light
    This class inherits Widgets

    Attributes:
        blinking (bool): wether or not the record light is meant to blink
        running (bool): while the the app is running

    Methods:
        threaded_blink:
            blinks the light every 0.5 seconds

        update_recording:
            changes the recording status

        terminate_record:
            stops the threaded loop
    """

    def __init__(self):
        super().__init__(True)

        self.blinking = False
        self.running = True

    def threaded_blink(self):
        """
        blinks the light every 0.5 seconds
        """
        while self.running:
            if self.blinking:
                self.update_show()
            else:
                self.show = True

            time.sleep(0.75)

    def update_recording(self):
        """
        changes the recording status
        """
        self.blinking = not self.blinking

    def start_recording(self):
        """
        If not already record, record.
        """
        self.blinking = True

    def end_recording(self):
        """
        If recording, stop.
        """
        self.blinking = False

    def terminate_record(self):
        """
        stops the threaded loop
        """
        self.running = False

class SideMenu:
    """
    A class to control showing and hiding menus.

    Attributes:
        widgets_file (list): a list of widgets for the file side menu
        widgets_device (list): a list of widgets for the device side menu
        layout (pyqt layout): the layout that holds both side menus
        showing_file (bool): whether the file widgets are being shown
        showing_device (bool): whether the device widgets are being shown
    
    Methods:
        show_side_menu:
            Updates the side menu to show the correct one.

            Args:
                file (bool) whether to update file being displayed
                device (bool) whether to update device being displayed
        
        hide_menu:
            Hides the entire display (used on startup).
    """

    def __init__(self, widgets_file, widgets_device, layout):

        self.widgets_file = widgets_file
        self.widgets_device = widgets_device
        self.layout = layout

        self.showing_file = False
        self.showing_device = False

    def show_side_menu(self, file=False, device=False):
        """
        Updates the side menu to show the correct one.

        Args:
            file (bool) whether to update file being displayed
            device (bool) whether to update device being displayed
        """
        if file:
            self.showing_file = not self.showing_file
            self.showing_device = False
        elif device:
            self.showing_device = not self.showing_device
            self.showing_file = False

        if self.showing_device:
            self.widgets_file.setVisible(self.showing_file)
            self.widgets_device.setVisible(self.showing_device)
        elif self.showing_file:
            self.widgets_device.setVisible(self.showing_device)
            self.widgets_file.setVisible(self.showing_file)

        self.layout.setVisible(
            self.showing_file or self.showing_device)

    def hide_menu(self):
        """
        Hides the entire display (used on startup).
        """
        self.layout.setVisible(False)

class SideKickLite:
    """
    Converts the sidekick lite button to a checkbox
    """

    def __init__(self, widget, startup_state):
        self.state = startup_state
        self.button = widget
        self.button.clicked.connect(self.update_state)

        self.update_style_sheet()

    def update_state(self):
        """
        Changes the boolean state variable and updates the stylesheet.
        """
        self.state = not self.state
        self.update_style_sheet()

    def update_style_sheet(self):
        """
        Sets the stylesheet to the correct type for the state.
        """
        if self.state:
            self.button.setStyleSheet(SK_LITE_ON_QSS)
            self.button.setText("SideKick Lite: ON")
        else:
            self.button.setStyleSheet(SK_LITE_OFF_QSS)
            self.button.setText("SideKick Lite: OFF")
