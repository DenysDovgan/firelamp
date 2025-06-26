# lib/button.py
from machine import Pin
import utime

class ButtonHandler:
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.last_state = 1
        self.last_time = utime.ticks_ms()
        self.clicks = 0
        self.hold_time = 1000  # ms
        self.timeout = 400     # time between clicks
        self.last_click_time = 0

    def check(self):
        now = utime.ticks_ms()
        state = self.pin.value()

        if self.last_state == 1 and state == 0:
            # button pressed
            self.last_time = now
        elif self.last_state == 0 and state == 1:
            # button released
            dt = utime.ticks_diff(now, self.last_time)
            if dt > 20:
                self.clicks += 1
                self.last_click_time = now

        self.last_state = state

        # Check if it's time to evaluate clicks
        if self.clicks > 0 and utime.ticks_diff(now, self.last_click_time) > self.timeout:
            result = None
            if self.clicks == 1:
                result = 'single'
            elif self.clicks == 2:
                result = 'double'
            elif self.clicks >= 3:
                result = 'triple'
            self.clicks = 0
            return result

        return None
