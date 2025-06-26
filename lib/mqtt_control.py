# lib/mqtt_control.py
import network
import utime
import ubinascii
from umqtt.simple import MQTTClient

class MQTTControl:
    def __init__(self, config, on_command):
        self.config = config
        self.on_command = on_command
        self.client = None
        self.connect_wifi()
        self.connect_mqtt()

    def connect_wifi(self):
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        if not sta_if.isconnected():
            print('Connecting to Wi-Fi...')
            sta_if.connect(self.config.get('wifi_ssid', 'YOUR_SSID'), self.config.get('wifi_password', 'YOUR_PASS'))
            while not sta_if.isconnected():
                utime.sleep(0.5)
        print('Wi-Fi connected:', sta_if.ifconfig())

    def connect_mqtt(self):
        client_id = b'esp32_' + ubinascii.hexlify(network.WLAN().config('mac'))
        self.client = MQTTClient(client_id.decode(), self.config.get('mqtt_host', 'broker.hivemq.com'))
        self.client.set_callback(self._on_msg)
        try:
            self.client.connect()
            topic = self.config.get('mqtt_topic', 'esp32/lamp')
            self.client.subscribe(topic.encode())
            print('MQTT subscribed to', topic)
        except Exception as e:
            print('MQTT connection failed:', e)

    def _on_msg(self, topic, msg):
        try:
            command = msg.decode()
            print('MQTT command:', command)
            self.on_command(command)
        except Exception as e:
            print('Error handling MQTT message:', e)

    def check_msg(self):
        try:
            self.client.check_msg()
        except:
            pass
