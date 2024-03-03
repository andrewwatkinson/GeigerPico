from machine import Pin
from LEDInterfacer import LEDInterfacer as LED
from wifi_tools import MQTT
import json
import logging
import time

class GeigerCounter:
    def __init__(self, pin_number, led: LED, display = None):
        self.pin = Pin(pin_number, Pin.IN)
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=self._irq_handler)
        self.count = []
        self.start_time = time.ticks_ms()
        self.danger_threshold = 100
        self.threshold_exceeded = False
        self.previous_cpm = 0
        self.led = led
        self.convert_factor = 0.00812037037037
        self.display = display

    def _irq_handler(self, pin):
        self.led.blink(1, 0.1)
        logging.debug('Geiger counter detected a pulse')
        self.count.append(time.ticks_ms())
        if len(self.count) > self.danger_threshold:
            logging.debug('Danger threshold exceeded')
            self.threshold_exceeded = True
        self.reset()


    @property
    def cpm(self):
        cpm = len(self.count)
        if cpm > self.danger_threshold:
            self.threshold_exceeded = True
        logging.debug(f'CPM: {cpm}')
        if cpm == 0:
            return self.previous_cpm, self.previous_cpm*self.convert_factor
        else:
            self.previous_cpm = cpm
            return round(cpm), cpm*self.convert_factor

    def reset(self):
        # delete all ticks older than 60 seconds
        self.count = [tick for tick in self.count if time.ticks_diff(time.ticks_ms(), tick) < 60000]
        logging.debug("old readings removed")
        self.threshold_exceeded = False