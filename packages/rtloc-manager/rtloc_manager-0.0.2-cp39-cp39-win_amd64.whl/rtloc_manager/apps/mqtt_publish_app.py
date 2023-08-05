"""
    RTLOC - Manager Lib

    rtloc_manager/apps/mqtt_publish_app.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import paho.mqtt.publish as mqtt
import time

import json

from rtloc_manager.manager_api import ManagerDistanceApp

class MQTTApp:
    def set_config(self, config):
        self.hostname = str(config.mqtt_hostname)
        self.username = str(config.mqtt_username)
        self.password = str(config.mqtt_password)
        self.port = config.mqtt_port
        self.interval = config.mqtt_interval

    def set_topic(self, topic):
        self.topic = topic

    def publish(self):
        mqtt.single(self.topic, payload=json.dumps(self.payload),
                    hostname=self.hostname, port=self.port,
                    auth={"username": self.username, "password": self.password})

class DistancePublisher(ManagerDistanceApp, MQTTApp):
    """ Example MQTT distance publication app.
    """
    def __init__(self):
        super().__init__()

        self.payload = {"ver": 1, "tags": {}}
        self.last_pub = 0

    def run(self):
        while True:
            distance_report = self.pop_report()

            self.payload["tags"][distance_report.device_id] = distance_report.distances_dict

            now = time.time()
            if now - self.last_pub > self.interval:
                self.publish()
                self.last_pub = now
