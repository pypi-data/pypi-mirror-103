"""
    RTLOC - Manager Lib

    rtloc_manager/interfaces/uart.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import time
import threading

import rtloc_uart.uart as uart

from rtloc_manager.manager_api import ManagerInterface, DistanceReport

class UARTInterface(ManagerInterface):
    def __init__(self, config):
        self.port = config.serial_port

        self.distances_dict = {}
        self.data_available = False

        device_id_set = False
        while not device_id_set:
            try:
                self.device_id = uart.get_distancer_internal_address(port=self.port)
                device_id_set = True
                print("Device internal address found to be {}.".format(self.device_id))
            except AssertionError:
                print("Could not read device internal address. Retrying...")

        threading.Thread(target=uart.start_streaming_distances,
                         args=(self.rtloc_uart_callback,), kwargs={"port": self.port},
                         daemon=True)\
                             .start()

    def rtloc_uart_callback(self, distances_dict):
        self.distances_dict = distances_dict
        self.data_available = True

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
        while not self.data_available:
            time.sleep(0.01)

        self.data_available = False

        distance_report = DistanceReport(self.device_id, self.distances_dict)

        return [distance_report]

    def stop(self):
        """ Properly stop the interface
        """
        uart.stop_streaming_distances(port=self.port)

    def is_symmetrical(self):
        """ This interface is not symmetrical
        """
        return False
