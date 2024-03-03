import machine
import time


class LEDInterfacer:
    def __init__(self):
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.off()

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

    def toggle(self):
        self.led.toggle()

    def blink(self, times: int, delay: int):
        for _ in range(times):
            self.toggle()
            time.sleep(delay)
            self.toggle()
            time.sleep(delay)
