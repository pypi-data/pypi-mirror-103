"""
    RTLOC - Manager Lib

    rtloc_manager/apps/position_print_app.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

from rtloc_manager.manager_api import ManagerPositionApp

class PositionPrinter(ManagerPositionApp):
    """ Simple terminal position print app example.
    """
    def __init__(self, manager_config):
        super().__init__()

        self.tags = manager_config.tags

    def run(self):
        while True:
            position_report = self.pop_report()

            if position_report.device_id in self.tags:
                print(position_report)
