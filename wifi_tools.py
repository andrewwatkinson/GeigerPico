import network, rp2, time
import machine
from umqtt.simple import MQTTClient
import logging

class wifi:
    def __init__(self, ssid: str, password: str, country: str = "GB"):
        self.ssid = ssid
        self.password = password
        self.country = country
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.config(pm=0xa11140)
        self.wlan.active(True)
        rp2.country(self.country)

    def connect(self):
        self.wlan.connect(self.ssid, self.password)
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            logging.info("waiting to connect:")
            time.sleep(1)
        logging.info(f"{self.wlan.ifconfig()}")

    def disconnect(self):
        self.wlan.disconnect()

    @property
    def isconnected(self):
        return self.wlan.isconnected()

    @property
    def ifconfig(self):
        # format the ifconfig properly
        output_object = {}
        ifconfig = self.wlan.ifconfig()
        output_object["ip"] = ifconfig[0]
        output_object["subnet"] = ifconfig[1]
        output_object["gateway"] = ifconfig[2]
        output_object["dns"] = ifconfig[3]

        return output_object


class MQTT:
    def __init__(self, client_id: str, mqtt_server: str, keepalive: int = 60, port: int = 1883):
        self.client_id = client_id
        self.mqtt_server = mqtt_server
        self.keepalive = keepalive

    def connect(self):
        self.client = MQTTClient(self.client_id, self.mqtt_server, keepalive=self.keepalive)
        try:
            self.client.connect()
        except OSError as e:
            self.reconnect()

        logging.info(f"Connected to mqtt server: {self.mqtt_server}")

    def reconnect(self):
        logging.error("failed to connect to mqtt server, reconnecting")
        time.sleep(5)
        machine.reset()
        try:
            self.client = self.connect()
        except OSError as e:
            self.client = self.reconnect()

    def publish(self, topic: str, message: str):
        logging.info(f"publishing to {topic} message: {message}")
        self.client.publish(topic, message)

    def disconnect(self):
        self.client.disconnect()
        logging.info("disconnected")
