"""
    RTLOC - Manager Lib

    rtloc_manager/frontend/frontend.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, pyqtSignal

from rtloc_manager.frontend.ui import rtloc
from rtloc_manager.manager_api import ManagerPositionApp

import pyqtgraph as pg

class _PositionGUI(QtWidgets.QMainWindow, rtloc.Ui_RTLOC):
    data_ready = pyqtSignal(int, list, list)

    def __init__(self, parent=None):
        # boiler plate
        super().__init__(parent)
        self.setupUi(self)

        # property inits
        self.positioning_anchors = False
        self.positioning_tags = False
        self.anchor_positions_known = False

        self.plotting_data = {}

        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_status_progress)

        # initialize custom GUI elements
        self.create_plotting_area()

        # listeners
        self.btnAnchors.clicked.connect(self.button_anchors_clicked)
        self.btnTags.clicked.connect(self.button_tags_clicked)

        self.data_ready.connect(self.update_plot)

        self.update_ui()

    def update_ui(self):
        if self.positioning_anchors:
            self.btnAnchors.setText("Stop positioning anchors")
        else:
            self.btnAnchors.setText("Start positioning anchors")

        if self.positioning_tags:
            self.btnTags.setText("Stop positioning tags")
        else:
            self.btnTags.setText("Start positioning tags")

        self.btnTags.setEnabled(self.anchor_positions_known)

    def button_anchors_clicked(self):
        if self.positioning_anchors:
            self.stop_positioning_anchors()
        else:
            self.start_positioning_anchors()

        self.update_ui()

    def button_tags_clicked(self):
        if self.positioning_tags:
            self.stop_positioning_tag()
        else:
            self.start_positioning_tag()

        self.update_ui()

    # def start_positioning_anchors(self):
    #     # anchor_collection will keep track of the result
    #     nb_anchors = len(self.get_anchors())
    #     if nb_anchors < 3:
    #         QtWidgets.QMessageBox.critical(self, "need more anchors",
    #                                        "A minimum of three anchors is required. (only {} given)"\
    #                                            .format(nb_anchors))
    #         return

    #     self.anchor_collection = AnchorCollection(self.get_anchors())

    #     self.autoPositionWorker = AutoPositioningWorker(self.listener, self.anchor_collection)
    #     self.autoPositionWorker.ready.connect(self.draw_anchors)

    #     self.listener.bind_socket()
    #     self.autoPositionWorker.start()

    #     self.start_status_progress("Performing auto-positioning for anchors")
    #     self.positioning_anchors = True

    # def stop_positioning_anchors(self):
    #     self.listener.stop_callback_loop()
    #     self.listener.close_socket()
    #     self.stop_status_progress()
    #     self.positioning_anchors = False
    #     self.anchor_positions_known = True

    # def start_positioning_tag(self):
    #     self.anchor_collection.set_tag(self.get_tags()[0])
    #     print(self.anchor_collection.tag.addr)

    #     self.anchor_collection.set_location_figure_axes(self.axes)
    #     self.anchor_collection.set_plot_anchors(self.draw_anchors)

    #     position_engine = PositionEngine(len(self.anchor_collection.anchors))
    #     position_engine.set_anchor_positions([anchor.position for anchor in self.anchor_collection.anchors])

    #     self.anchor_collection.set_engine(position_engine)

    #     self.tagPositionWorker = TagPositioningWorker(self.listener, self.anchor_collection)

    #     self.listener.bind_socket()
    #     self.tagPositionWorker.start()

    #     self.start_status_progress("Tracking tag")
    #     self.positioning_tags = True

    # def stop_positioning_tag(self):
    #     self.listener.stop_callback_loop()
    #     self.listener.close_socket()
    #     self.stop_status_progress()
    #     self.positioning_tags = False

    def start_status_progress(self, message):
        self.status_message = message
        self.status_nb_dots = 0
        self.progress_timer.start(300)

    def stop_status_progress(self):
        self.progress_timer.stop()
        self.statusbar.clearMessage()

    def update_status_progress(self):
        self.status_nb_dots += 1
        self.statusbar.showMessage(self.status_message + "."*self.status_nb_dots)

        if self.status_nb_dots == 3:
            self.status_nb_dots = 0

    def create_plotting_area(self):
        # create plotting canvas
        self.plotting_area = pg.PlotWidget()

        self.plotting_area.setAspectLocked()

        # set size policy for the plot object
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)
        self.plotting_area.setSizePolicy(sizePolicy)

        # add canvas widget to UI
        self.plotGrid.addWidget(self.plotting_area)

    def create_plotting_data(self, device_id, **kwargs):
        """ Create a plotting data object for the given device id
        """
        self.plotting_data[device_id] = pg.ScatterPlotItem(**kwargs)
        self.plotting_area.addItem(self.plotting_data[device_id])

        # add anchor address in plot
        self.plotting_data[str(device_id) + "_text"] = pg.TextItem(str(device_id))        
        self.plotting_area.addItem(self.plotting_data[str(device_id) + "_text"])

    def get_plotting_data(self, plotting_data_key):
        return self.plotting_data[plotting_data_key]

    def update_plot(self, device_id, x, y):
        plotting_data = self.get_plotting_data(device_id)
        plotting_data.setData(x, y)

        plotting_data = self.get_plotting_data(str(device_id) + "_text")
        plotting_data.setPos(x[-1], y[-1])

    # def get_anchors(self):
    #     anchors = utils.parse_input_text(self.anchorsList.toPlainText())
    #     anchors = [Anchor(anchor, None) for anchor in anchors]

    #     return anchors

    # def get_tags(self):
    #     tags = utils.parse_input_text(self.tagsList.toPlainText())
    #     tags = [Tag(tag) for tag in tags]

    #     return tags

class ManagerFrontend():
    def __init__(self, config):
        super().__init__()

        self.anchors = config.anchors
        self.tags = config.tags

        self.app = QtWidgets.QApplication(sys.argv)
        self.ui = _PositionGUI()

        # init plotting data
        for device in config.tags + config.anchors:
            if device in config.tags:
                self.ui.create_plotting_data(device, pen=pg.mkPen(width=5, color="b"), symbol="o")
            else:
                self.ui.create_plotting_data(device, pen=pg.mkPen(width=5, color="r"), symbol="+")

        self.ui.anchorsList.setText(("{}\n"*len(self.anchors)).format(*self.anchors))
        self.ui.tagsList.setText(("{}\n"*len(self.tags)).format(*self.tags))

    def event_loop(self):
        self.ui.show()
        self.app.exec_()

    def get_data_ready_signal(self):
        return self.ui.data_ready

class PositionGUIPlotter(ManagerPositionApp):
    X = 0
    Y = 1

    def __init__(self, config):
        super().__init__()

        self.tags = config.tags
        self.anchors = config.anchors

        self.local_plotting_data = {}

        for device in config.tags + config.anchors:
            self.local_plotting_data[device] = {self.X: [], self.Y: []}

    def run(self):
        while True:
            position_report = self.pop_report()

            if position_report.device_id in self.anchors:
                self.plot_anchor_position(position_report)

            if position_report.device_id in self.tags:
                self.plot_tag_position(position_report)

    def set_data_ready_signal(self, data_ready_signal):
        self.data_ready_signal = data_ready_signal

    def plot_anchor_position(self, position_report):
        self.plot_tag_position(position_report)

    def plot_tag_position(self, position_report):
        dev_id = position_report.device_id

        self.local_plotting_data[dev_id][self.X] = self.local_plotting_data[dev_id][self.X][-4:]
        self.local_plotting_data[dev_id][self.X].append(position_report.position.x)

        self.local_plotting_data[dev_id][self.Y] = self.local_plotting_data[dev_id][self.Y][-4:]
        self.local_plotting_data[dev_id][self.Y].append(position_report.position.y)

        # actually change data, that will get plotted by the event loop
        self.data_ready_signal.emit(dev_id, self.local_plotting_data[dev_id][self.X], self.local_plotting_data[dev_id][self.Y])
