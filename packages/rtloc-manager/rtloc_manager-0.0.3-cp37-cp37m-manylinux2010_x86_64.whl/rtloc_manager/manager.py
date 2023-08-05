"""
    RTLOC - Manager Lib

    rtloc_manager/manager.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import time
import queue
import threading

from rtloc_manager.manager_api import ManagerApp, ManagerDistanceApp
from rtloc_manager.database import ManagerDistanceDatabase, ManagerPositionDatabase
from rtloc_manager.core.autopos import AutoPos


class Manager:
    """ Core manager class that supports the following functionality:

    * add_frontend(...)
    * add_app(...)
    * set_interface(...)
    * run()

    """
    def __init__(self, config):
        self.config = config
        self.interface = None
        self.frontend = None

        self.anchor_positions_known = False

        self.distance_apps = []
        self.position_apps = []

        self.working = False
        self.no_app_active = False

        self.threads = []

        self._if_queue = queue.Queue()

        self._init_database()

    def add_frontend(self, frontend):
        """ Add frontend to this manager.

        Frontend must be added prior to running the manager.

        Args:
            frontend (ManagerFrontend): manager frontend
        """
        self.frontend = frontend

    def add_app(self, app):
        """ Add application block to this manager.

        Application(s) must be added prior to running the manager.

        Args:
            app (ManagerApp): manager application
        """
        if self.no_app_active:
            # not accepting apps at this time
            return

        if app.type == ManagerApp.DISTANCE_TYPE:
            self.distance_apps.append(app)
        elif app.type == ManagerApp.POSITION_TYPE:
            self.position_apps.append(app)

    def _get_nb_distance_apps(self):
        return len(self.distance_apps)

    def _get_nb_positioning_apps(self):
        return len(self.position_apps)

    def set_interface(self, interface):
        """ Add data interface to this manager.

        Interface must be added prior to running the manager.

        Args:
            interface (ManagerInterface): manager interface
        """
        self.interface = interface

    def _init_database(self):
        """ Initialize internal distance and position representation and filtering.
        """
        if self.config is None:
            raise NoConfigError

        self.distance_database = ManagerDistanceDatabase(self.config)
        self.position_database = ManagerPositionDatabase(self.config)

    def _start_apps(self):
        """ Launch each connected app in a separate thread
        """
        for apps in self.distance_apps + self.position_apps:
            thread = threading.Thread(target=apps.run, daemon=True)
            thread.start()
            self.threads.append(thread)

    def _prune_thread_queue(self):
        """ Remove app threads that have finished from the queue
        """
        self.threads = [t for t in self.threads if t.is_alive()]

    def _work(self):
        """ Worker loop
        """
        if self.working:
            print("Work not started, because other work is still being performed")
            return

        self.working = True
        anchor_positions_shared = False

        # inform database about symmetry support in interface
        self.distance_database.set_interface_symmetrical(self.interface.is_symmetrical())

        while True:
            # pop distance reports from interface report queue
            reports = self._if_queue.get()

            # assuming nog position apps for now
            for report in reports:
                if not report.distances_dict:
                    # no distances
                    continue

                self.distance_database.update_from_report(report)
                filtered_report = self.distance_database.get_distance_report(report.device_id)

                if filtered_report is None:
                    # tag is ignored
                    continue

                for app in self.distance_apps:
                    app.feed_report(filtered_report)

                if filtered_report.device_id in self.position_database.anchors:
                    # don't spam fixed anchro positions
                    continue

                if self._get_nb_positioning_apps() > 0:
                    self.position_database.update_tag_position_from_report(filtered_report)
                    position_report = self.position_database.get_position_report(filtered_report.device_id)

                for app in self.position_apps:
                    # first time: communicate anchor positions to apps
                    if not anchor_positions_shared:
                        for anchor in self.position_database.anchors:
                            anchor_position_report = self.position_database.get_position_report(anchor)
                            app.feed_report(anchor_position_report)
                            print("ANCHOR POSIION:", anchor_position_report)

                    app.feed_report(position_report)

                if not anchor_positions_shared:
                    anchor_positions_shared = True

            # TODO this probably also needs app removal, rather than just thread pruning
            # to prevent app data queues from growing
            # TODO: potentially let the app keep track of its thread info to ease the above TODO
            self._prune_thread_queue()
            if (len(self.threads) == 0):
                self.working = False
                print("All work finished.")
                break

    def _auto_positioning_needed(self):
        """ Check whether or not auto positioning is needed
        """
        if self._get_nb_positioning_apps() > 0:
            if not self.position_database.anchor_positions_known():
                return True

        return False

    def _start_no_app_mode(self, duration):
        self.no_app_active = True

        self.distance_apps_copy = self.distance_apps
        self.position_apps_copy = self.position_apps

        self.distance_apps = [self._NoOperationsApp(duration)]
        self.position_apps = []

        # start apps means starting the no operations app
        self._start_apps()

    def _stop_no_app_mode(self):
        if not self.no_app_active:
            return

        self.distance_apps = self.distance_apps_copy
        self.position_apps = self.position_apps_copy

        self.no_app_active = False

    def _no_app_mode(self, duration):
        """ No app mode runs the main work loop without real work. This mode is used
        to gather initial measurements without acting on these measurements.
        """
        self._start_no_app_mode(duration)
        print("Gathering measurements in no app mode for {} s...".format(duration))
        self._work()
        self._stop_no_app_mode()

    def _auto_position_anchors(self):
        """ Perform auto positioning
        """
        if not self.interface.is_symmetrical():
            raise AutoPositioningNotSupported

        # temporarily change distance filtering parameter
        tmp_alpha = self.distance_database.alpha
        self.distance_database.alpha = 0.05

        # perform measurements in no app mode
        self._no_app_mode(10)

        self.distance_database.alpha = tmp_alpha

        # Get data from database and perform auto positioning
        autopos = AutoPos(len(self.position_database.anchors))

        distance_measurements = []
        for anchor in self.position_database.anchors:
            distance_report = self.distance_database.get_distance_report(anchor)
            for other_anchor in self.position_database.anchors:
                # distance to self is handled by the distance database (set to 0)
                distance_measurements.append(distance_report.distances_dict[other_anchor])

        autopos.compute(distance_measurements)
        anchor_positions = autopos.get_position_estimates()

        # Update position database
        for anchor_idx, position in enumerate(anchor_positions):
            anchor = self.position_database.anchors[anchor_idx]
            self.position_database.set_device_position(anchor, position)

    def run(self):
        """ Start manager execution.
        """
        # launch interface thread
        interface_thread = threading.Thread(target=self._run_interface, daemon=True)
        interface_thread.start()

        # launch core manager thread
        manager_thread = threading.Thread(target=self._run_manager, daemon=True)
        manager_thread.start()

        if self.frontend is not None:
            # run frontend eventloop
            # NOTE: it is super important that this event loop runs in the main thread!!
            self.frontend.event_loop()
        else:
            self._fake_event_loop()

        self.interface.stop()
        print("Interface stopped. Goodbye!")

    def _run_manager(self):
        """ Start core manager execution.
        """
        if self._get_nb_distance_apps() > 0:
            if self.config.distancing_parameters_invalid():
                # don't do anything, return prematurely
                # raise?
                return

        if self._get_nb_positioning_apps() > 0:
            if self.config.positioning_parameters_invalid():
                # don't do anything, return prematurely
                # raise ?
                return

        if self._auto_positioning_needed():
            self._auto_position_anchors()
        else:
            self._no_app_mode(1)

        self._start_apps()
        self._work()

    def _fake_event_loop(self):
        """ Infinite while loop event loop for the case that no frontend
        is used.
        """
        try:
            while(True):
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def _run_interface(self):
        """ Runner for interface thread
        """
        while True:
            # read data waits for new data to become available
            self._if_queue.put(self.interface.read_data())

    """ Nested no ops class
    """
    class _NoOperationsApp(ManagerDistanceApp):
        def __init__(self, duration):
            """ No operations app that runs for the given duration in seconds.
            This app enables distance measurement gathering without immediately acting
            on the data.
            """
            super().__init__()

            self.duration = duration
            self.iteration = 0
            self.running = True

        # overwrite feed report function to prevent potting up memory in the data queue
        def feed_report(self, distance_report):
            pass

        def run(self):
            while(self.running):
                time.sleep(1)
                self.iteration += 1

                if self.iteration >= self.duration:
                    self.running = False


""" Manager configuration class
"""
import yaml
from bunch import Bunch

class ManagerConfig(Bunch):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    @staticmethod
    def from_yaml(yaml_file):
        """ Create a manager config object from the given yaml file.

        Args:
            yaml_file (str): path to yaml config file

        Returns:
            ManagerConfig: manager configuration object
        """
        with open(yaml_file) as yaml_fh:
            config_dict = yaml.safe_load(yaml_fh)
            return ManagerConfig(config_dict)

    @staticmethod
    def from_mqtt(mqtt_args):
        raise NotImplementedError

    def distancing_parameters_invalid(self):
        invalid = False

        if len(self.tags + self.anchors) >= self.nb_slots:
            print("ERROR: Too many tags and anchors were given for the available number of slots.")
            invalid = True

        return invalid

    def positioning_parameters_invalid(self):
        invalid = False

        nb_anchors = len(self.anchors)
        if nb_anchors < 3:
            print("ERROR: A minimum of 3 anchors is needed for positioning. Only {} was/were given.".format(nb_anchors))
            invalid = True

        return invalid


class NoConfigError(Exception):
    pass

class AutoPositioningNotSupported(Exception):
    pass
