# main.py
from lib.button import ButtonHandler
from lib.mqtt_control import MQTTControl
from lib.effects import Effects
import ujson, uos, utime
from machine import Pin
import neopixel

# --- Pin & matrix config ---
MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
DATA_PIN = 5  # change if needed

# --- Load config ---
def load_config():
    try:
        with open('config.json') as f:
            return ujson.load(f)
    except:
        return {'effect': 'rainbow', 'brightness': 128}

def save_config(cfg):
    with open('config.json', 'w') as f:
        ujson.dump(cfg, f)

# --- Matrix helpers ---
def xy(x, y):
    if y % 2 == 0:
        i = y * MATRIX_WIDTH + x
    else:
        i = y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
    return i

# --- Init components ---
cfg = load_config()
np = neopixel.NeoPixel(Pin(DATA_PIN), NUM_PIXELS)
effects = Effects(np, xy, MATRIX_WIDTH, MATRIX_HEIGHT)
button = ButtonHandler(27)
mqtt = MQTTControl(cfg, on_command=lambda cmd: handle_command(cmd))

# --- Handle commands from MQTT or button ---
def handle_command(cmd):
    if cmd == 'next':
        effects.next()
    elif cmd == 'prev':
        effects.previous()
    elif cmd.startswith('set:'):
        _, name = cmd.split(':', 1)
        effects.set(name)
    cfg['effect'] = effects.current_name()
    save_config(cfg)

# --- Setup complete ---
effects.set(cfg['effect'])
print('Lamp started. Current effect:', effects.current_name())

# --- Main loop ---
while True:
    effects.update()
    mqtt.check_msg()
    result = button.check()
    if result == 'single': handle_command('next')
    elif result == 'double': handle_command('prev')
    elif result == 'triple': handle_command(f"set:{effects.random_name()}")
    utime.sleep_ms(20)
