"""
    RTLOC - Manager Lib

    rtloc_manager/database.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import time

import numpy as np

from rtloc_manager.manager_api import DistanceReport, PositionReport
from rtloc_manager.core.engine import Position, PositionEngine


class ManagerDistanceDatabase:
    def __init__(self, manager_config):
        # distance management
        self.distance_matrix = np.zeros((manager_config.nb_slots,
                                         manager_config.nb_slots))
        self.timing_matrix = np.zeros((self.distance_matrix.shape))

        # address management
        self.addresses = [0] * manager_config.nb_slots
        self.addresses_free = [True] * manager_config.nb_slots

        self.ignore_list = manager_config.ignore_list

        # filtering parameters
        self.inval_t = manager_config.dist_invalidate_delay
        self.alpha = manager_config.dist_smoothing_const

    def set_interface_symmetrical(self, interface_symmetrical):
        self.interface_symmetrical = interface_symmetrical

    def update_distance(self, device_id, remote_device_id, distance):
        """ Dual filtering (smoothing and symmetrical averaging) distance update
        """
        if not self._is_address_valid(device_id) or not self._is_address_valid(remote_device_id):
            # don't update for invalid address
            return

        if not self._is_distance_valid(distance):
            return

        dev_slot = self._get_address_slot(device_id)
        remote_dev_slot = self._get_address_slot(remote_device_id)

        # SMOOTHING
        filt_distance = (1 - self.alpha) * self.distance_matrix[dev_slot, remote_dev_slot] + self.alpha * distance

        # SYMMETRICAL AVERAGING
        if self.interface_symmetrical:
            # incorporate far end distance knowledge
            filt_distance += self.distance_matrix[remote_dev_slot, dev_slot]
            filt_distance /= 2

        # update internal representation
        self._update_distance(dev_slot, remote_dev_slot, filt_distance)

        if self.interface_symmetrical:
            # don't update time for the symmetrical update, because this is not based on own measurements
            self._update_distance(remote_dev_slot, dev_slot, filt_distance, update_time=False)
        else:
            # in the assymetrical case, the device completely manages the remote slot as well
            self._update_distance(remote_dev_slot, dev_slot, filt_distance)

    def _update_distance(self, row_slot, column_slot, dist, update_time=True):
        self.distance_matrix[row_slot, column_slot] = dist
        if update_time:
            self.timing_matrix[row_slot, column_slot] = time.time()

    def update_from_report(self, report):
        """ Update internal representation from a distance report based on
        the update_distance method.
        """
        device_id = report.device_id

        # iterate over dictionary keys
        for remote_device_id in report.distances_dict:
            self.update_distance(device_id, remote_device_id,
                                 report.distances_dict[remote_device_id])

        # prune old distances from database
        self.invalidate()

    def get_distance_report(self, device_id):
        """ Return the distance report for the given device_id
        """
        distances_dict = {}

        if not self._is_address_valid(device_id):
            # return empty dict for invalid address
            return None

        row_slot = self._get_address_slot(device_id)

        # add self distance
        distances_dict[device_id] = 0

        for remote_device_id in self.addresses:
            if self._is_address_valid(remote_device_id):
                column_slot = self._get_address_slot(remote_device_id)

                distances_dict[remote_device_id] = self.distance_matrix[row_slot, column_slot]

        return DistanceReport(device_id, distances_dict)

    def get_all_distance_reports(self):
        """ Return a list of all distance reports present in the internal
        database.
        """
        reports = []

        for slot, free in enumerate(self.addresses_free):
            if not free:
                device_id = self.addresses[slot]
                reports.append(self.get_distance_report(device_id))

        return reports

    def invalidate(self):
        """ Invalidate distances that have not been received recently
        """
        self.distance_matrix[self.timing_matrix < (time.time() - self.inval_t)] = 0
        self._free_invalidated_address_slots()

    def _is_distance_valid(self, dist):
        if dist == 0 or dist == 65534:
            return False
        else:
            return True

    def _is_address_valid(self, address):
        if address == 0 or address == 255 or address in self.ignore_list:
            return False
        else:
            return True

    def _get_address_slot(self, address):
        try:
            slot = self.addresses.index(address)
        except ValueError:
            slot = self._assign_address_slot(address)

        return slot

    def _assign_address_slot(self, address):
        try:
            slot = self.addresses_free.index(True)
        except ValueError:
            raise NoFreeAddressSlotError

        # assign slot to given address
        self.addresses[slot] = address
        self.addresses_free[slot] = False

        return slot

    def _free_invalidated_address_slots(self):
        for slot, free in enumerate(self.addresses_free):
            if not free:
                if np.sum(self.distance_matrix[slot,:]) == 0:
                    # print("Device {} is invalidated".format(self.addresses[slot]))
                    self.addresses[slot] = 0
                    self.addresses_free[slot] = True


class ManagerPositionDatabase:
    NB_ANCHORS_USED_PER_POSITION = 3

    def __init__(self, manager_config):
        # copy anchor and tag IDs
        self.anchors = manager_config.anchors
        self.tags = manager_config.tags

        self.alpha = manager_config.pos_smoothing_const

        # position dict to keep positions of both anchors and tags
        self.position_dict = {}

        # set anchor positions if given (if not all given, the given ones will be overwritten
        # by the auto positioning procedure).
        for anchor in self.anchors:
            try:
                self.position_dict[anchor] =  Position(*manager_config.anchor_positions[anchor])
            except (KeyError, TypeError):
                # anchor position not known
                pass

        # init tag position to abritrary value
        for tag in self.tags:
            self.position_dict[tag] = Position(0, 0, 0)

        # position engine
        self.engine = PositionEngine(self.NB_ANCHORS_USED_PER_POSITION)

    def anchor_positions_known(self):
        """ Return whether or not all anchor positions are known.
        """
        for anchor in self.anchors:
            if self.get_device_position(anchor) is None:
                return False

        # all position are in the position dict
        return True

    def get_device_position(self, device_id):
        """ Returns position for the given device if known.
        Otherwise returns None.
        """
        try:
            return self.position_dict[device_id]
        except KeyError:
            return None

    def set_device_position(self, device_id, position):
        """ Set the position of given device based on the given
        Position object.
        """
        self.position_dict[device_id] = position

    def feed_anchor_positions_to_engine(self, anchors):
        positions = [self.get_device_position(anchor) for anchor in anchors]
        self.engine.set_anchor_positions(positions)

    def update_tag_position_from_report(self, ranging_report):
        if ranging_report.device_id not in self.tags:
            # this tag is device is not to be tracked
            return

        previous_tag_position = self.get_device_position(ranging_report.device_id)

        # assume not all anchors are within measurement reach
        measurements = []
        reachable_anchors = []
        for anchor in self.anchors:
            try:
                measurements.append(ranging_report.distances_dict[anchor])
                reachable_anchors.append(anchor)
            except KeyError:
                pass

        if len(reachable_anchors) < self.NB_ANCHORS_USED_PER_POSITION:
            raise NotEnoughAnchorMeasurements

        # select the NB_ANCHORS_USED_PER_POSITION closest anchors for positioning
        sorted_idxs = np.argsort(measurements)

        measurements = np.array(measurements)[sorted_idxs[:self.NB_ANCHORS_USED_PER_POSITION]].tolist()
        reachable_anchors = np.array(reachable_anchors)[sorted_idxs[:self.NB_ANCHORS_USED_PER_POSITION]].tolist()

        self.feed_anchor_positions_to_engine(reachable_anchors)

        new_tag_position = self.engine.compute_tag_position(measurements, previous_tag_position)

        # perform position smoothing
        new_tag_position.x = (1 - self.alpha) * previous_tag_position.x + self.alpha * new_tag_position.x
        new_tag_position.y = (1 - self.alpha) * previous_tag_position.y + self.alpha * new_tag_position.y
        new_tag_position.z = (1 - self.alpha) * previous_tag_position.z + self.alpha * new_tag_position.z

        self.set_device_position(ranging_report.device_id, new_tag_position)

    def get_position_report(self, device_id):
        return PositionReport(device_id, self.get_device_position(device_id))


""" Custom exceptions
"""
class NoFreeAddressSlotError(Exception):
    pass

class NotEnoughAnchorMeasurements(Exception):
    pass
