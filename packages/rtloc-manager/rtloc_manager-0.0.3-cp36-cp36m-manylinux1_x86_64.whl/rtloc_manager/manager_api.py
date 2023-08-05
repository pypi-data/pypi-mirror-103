"""
    RTLOC - Manager Lib

    rtloc_manager/manager_api.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

    This file defines the manager interface that can be implemented
    to extend the manager functionality.

"""

import queue

class ManagerApp():
    """ IMPORTANT: Don't build apps that inherit directly from ManagerApp.
    Use ManagerDistanceApp or ManagerPositionApp instead.
    """
    DISTANCE_TYPE = 1
    POSITION_TYPE = 2

    def __init__(self):
        self._report_queue = queue.Queue()

    def _feed_report(self, report):
        self._report_queue.put(report)

    def pop_report(self):
        """ Pop report from the internal report queue 
        """
        return self._report_queue.get()

    def run(self):
        """ Run the application main loop.

        Implementation note:
        ====================
        Use self.pop_report() to control the speed of the app loop.

        Depending on the app type, distance or position reports will
        result from a pop operation.
        """
        raise NotImplementedError


class ManagerDistanceApp(ManagerApp):
    """ Interface for manager application that is fed with distance data.
    """
    def __init__(self):
        super().__init__()

        self.type = ManagerApp.DISTANCE_TYPE

    def feed_report(self, distance_report):
        """ Callback to feed distance report to the app.

        Args:
            distance_report (DistanceReport): distance_report
        """
        self._feed_report(distance_report)


class ManagerPositionApp(ManagerApp):
    """ Interface for manager application that is fed with position data.
    """
    def __init__(self):
        super().__init__()

        self.type = ManagerApp.POSITION_TYPE

    def feed_report(self, position_report):
        """ Callback to feed position report to the app

        Args:
            position_report (PositionReport): position report 
        """
        self._feed_report(position_report)


class ManagerInterface:
    """ Interface for manager data interface.

    NOTE: The implementation of this interface should not be considered
    by regular users.
    """
    def read_data(self):
        """ Get distance data from an abstract interface.
        This function is assumed to be implemented as a blocking
        function call, until new data becomes available.

        Only returning new data will create some room for
        apps to act on the data and not putting too much
        pressure on the CPU.

        Returns:
            list: distance report list
        """
        raise NotImplementedError
        return distance_reports

    def stop(self):
        """ Properly terminate the interface
        """
        raise NotImplementedError

    def is_symmetrical(self):
        """ Return whether or not this interface is fully symmetrical, i.e.,
        whether or not this interface has access to all measurements from all devices.
        """
        raise NotImplementedError


class DistanceReport:
    def __init__(self, device_id, distances_dict):
        """ Distance report object.

        Args:
            device_id (int): id of the measurement tag
            distances_dict (dict): dictionary with remote device ids as keys,
            and distances in centimeter as value.
        """
        self.device_id = device_id
        self.distances_dict = distances_dict

    def __repr__(self):
        return "{}: {}".format(self.device_id, self.distances_dict)


class PositionReport:
    def __init__(self, device_id, position):
        """ Position report format.

        Args:
            device_id (int): device or tag id
            position (Position): position (x, y, z) of the device with given device_id
        """
        self.device_id = device_id
        self.position = position

    def __repr__(self):
        return "{}: ({}, {}, {})".format(self.device_id, self.position.x,
                                         self.position.y, self.position.z)
