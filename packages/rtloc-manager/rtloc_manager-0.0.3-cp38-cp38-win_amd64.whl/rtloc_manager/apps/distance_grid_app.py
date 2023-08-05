"""
    RTLOC - Manager Lib

    rtloc_manager/apps/distance_grid_app.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import curses

import numpy as np

from rtloc_manager.manager_api import ManagerDistanceApp


class DistanceGrid(ManagerDistanceApp):
    def __init__(self, manager_config):
        super().__init__()

        self.nb_slots = manager_config.nb_slots

        self.distances_matrix = np.zeros((self.nb_slots, self.nb_slots), dtype="int")
        self.slot_addresses = np.array([0] * self.nb_slots)

    def update_distance_matrix(self, device_id, remote_ids, dists_to_remote):
        global reset_counter

        # reset when devices appear / disappear
        if remote_ids != self.slot_addresses[self.slot_addresses != 0].tolist():
            self.slot_addresses.fill(0) 
            self.distances_matrix.fill(0)

            # rebuild adress slot list
            for slot_idx, remote_id in enumerate(remote_ids):
                self.slot_addresses[slot_idx] = remote_id

        addr_slot_idx = np.where(self.slot_addresses == device_id)[0][0]

        for slot_idx, dist in enumerate(dists_to_remote):
            self.distances_matrix[addr_slot_idx, slot_idx] = dist

    def run(self):
        self.run = True

        self.ui = curses.initscr()

        while self.run:
            data = self.pop_report()

            device_id = data.device_id
            remote_ids = list(data.distances_dict.keys())
            remote_ids.sort()

            dists_to_remote = [data.distances_dict[remote_id] for remote_id in remote_ids]

            self.update_ui(device_id, remote_ids, dists_to_remote)

    def distances_repr(self):
        result = (" addr |\t" + ("{:5d} \t" * self.nb_slots)).format(*self.slot_addresses)
        result += "\n"

        result += "-" * (8 * (self.nb_slots + 1))
        result += "\n"

        for slot_idx, distances in enumerate(self.distances_matrix):
            # remove distance info to self
            tmp_distances = distances.tolist()
            tmp_distances[slot_idx] = 0

            result += ("{:5d} |\t" + ("{:5d} \t" * (self.nb_slots))).format(self.slot_addresses[slot_idx], *tmp_distances)
            result += "\n"

        result += "\nPush [CTRL + C] to close app\n"

        return result

    def update_ui(self, device_id, remote_ids, dists_to_remote):
        # update internal data
        self.update_distance_matrix(device_id, remote_ids, dists_to_remote)

        self.ui.addstr(0, 0, self.distances_repr())
        self.ui.refresh()

    def close(self):
        curses.endwin()
        quit()
