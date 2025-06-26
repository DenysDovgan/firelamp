# lib/effects.py
import utime, urandom, math

class Effects:
    def __init__(self, np, xy_fn, width, height):
        self.np = np
        self.xy = xy_fn
        self.width = width
        self.height = height
        self.effects = {
            'rainbow_snake': self.rainbow_snake,
            'fire_2021': self.fire_2021,
            'magma': self.magma,
            'bouncing_balls': self.bouncing_balls,
            'sinusoid': self.sinusoid,
            'plasma': self.plasma,
            'two_comets': self.two_comets,
            'three_comets': self.three_comets,
            'matrix_rain': self.matrix_rain,
            'lava_lamp': self.lava_lamp,
            'aurora': self.aurora,
            'starfield': self.starfield,
            'color_cycle': self.color_cycle,
            'sparkle': self.sparkle,
            'flame_flicker': self.flame_flicker,
            'confetti': self.confetti,
            'vertical_bars': self.vertical_bars,
            'rainbow_circle': self.rainbow_circle,
            'waterfall': self.waterfall
        }
        self.current_index = 0
        self.frame = 0
        self.set('rainbow_snake')
        self.stars = [(urandom.getrandbits(4), urandom.getrandbits(4)) for _ in range(20)]
        self.comet_pos = 0
        self.comet_dir = 1

    def set(self, name):
        if name in self.effects:
            self.current_index = list(self.effects).index(name)
            self.frame = 0

    def current(self):
        return self.effects[list(self.effects)[self.current_index]]

    def current_name(self):
        return list(self.effects)[self.current_index]

    def next(self):
        self.current_index = (self.current_index + 1) % len(self.effects)
        self.frame = 0

    def previous(self):
        self.current_index = (self.current_index - 1) % len(self.effects)
        self.frame = 0

    def random_name(self):
        return urandom.choice(list(self.effects))

    def update(self):
        self.current()()
        self.np.write()
        self.frame += 1

    def rainbow_snake(self):
        for y in range(self.height):
            for x in range(self.width):
                hue = (x * 10 + self.frame * 4) % 256
                self.np[self.xy(x, y)] = self.hsv_to_rgb(hue, 255, 100)

    def fire_2021(self):
        for y in range(self.height):
            for x in range(self.width):
                flicker = urandom.getrandbits(8) % 100
                r = min(255, 180 + flicker)
                g = max(0, 80 - flicker // 2)
                self.np[self.xy(x, y)] = (r, g, 0)

    def magma(self):
        for y in range(self.height):
            for x in range(self.width):
                value = urandom.getrandbits(8) % 255
                self.np[self.xy(x, y)] = (value, int(value * 0.4), 0)

    def bouncing_balls(self):
        self.np.fill((0, 0, 0))
        for i in range(3):
            y = int(abs(math.sin((self.frame + i * 10) / 10.0) * self.height))
            self.np[self.xy(i * 5 + 5, self.height - 1 - y)] = (255, 255, 0)

    def sinusoid(self):
        self.np.fill((0, 0, 0))
        for x in range(self.width):
            y = int((math.sin((x + self.frame) / 3.0) + 1) * self.height / 2)
            self.np[self.xy(x, y)] = (0, 100, 255)

    def plasma(self):
        for y in range(self.height):
            for x in range(self.width):
                v = int((math.sin(x * 0.3 + self.frame * 0.1) + math.sin(y * 0.3 + self.frame * 0.1)) * 127 + 128)
                self.np[self.xy(x, y)] = self.hsv_to_rgb(v, 255, 255)

    def two_comets(self):
        self.np.fill((0, 0, 0))
        pos1 = self.frame % self.width
        pos2 = self.width - 1 - (self.frame % self.width)
        for y in range(self.height):
            self.np[self.xy(pos1, y)] = (255, 0, 0)
            self.np[self.xy(pos2, y)] = (0, 0, 255)

    def three_comets(self):
        self.np.fill((0, 0, 0))
        for i in range(3):
            pos = (self.frame + i * 5) % self.width
            for y in range(self.height):
                self.np[self.xy(pos, y)] = self.hsv_to_rgb((i * 80 + self.frame * 4) % 256, 255, 255)

    def matrix_rain(self):
        self.np.fill((0, 0, 0))
        for i in range(5):
            col = urandom.getrandbits(4)
            row = self.frame % self.height
            self.np[self.xy(col, row)] = (0, 255, 0)

    def lava_lamp(self):
        for y in range(self.height):
            for x in range(self.width):
                flicker = math.sin((x + self.frame) * 0.2) + math.cos((y + self.frame) * 0.2)
                c = int((flicker + 2) * 63)
                self.np[self.xy(x, y)] = (c, int(c * 0.3), c)

    def aurora(self):
        for y in range(self.height):
            for x in range(self.width):
                h = (math.sin((x + self.frame) * 0.1) + math.cos((y + self.frame) * 0.1)) * 128 + 128
                self.np[self.xy(x, y)] = self.hsv_to_rgb(int(h) % 256, 200, 128)

    def starfield(self):
        self.np.fill((0, 0, 0))
        for i, (x, y) in enumerate(self.stars):
            self.np[self.xy(x, y)] = (255, 255, 255)
            self.stars[i] = (x, (y + 1) % self.height)

    def color_cycle(self):
        color = self.hsv_to_rgb((self.frame * 2) % 256, 255, 255)
        for i in range(self.width * self.height):
            self.np[i] = color

    def sparkle(self):
        self.np.fill((0, 0, 0))
        for _ in range(10):
            i = urandom.getrandbits(8) % (self.width * self.height)
            self.np[i] = (255, 255, 255)

    def flame_flicker(self):
        for y in range(self.height):
            for x in range(self.width):
                r = urandom.getrandbits(8) % 200 + 55
                g = urandom.getrandbits(8) % 50
                self.np[self.xy(x, y)] = (r, g, 0)

    def confetti(self):
        self.np.fill((0, 0, 0))
        for _ in range(20):
            x = urandom.getrandbits(5) % self.width
            y = urandom.getrandbits(5) % self.height
            hue = urandom.getrandbits(8)
            self.np[self.xy(x, y)] = self.hsv_to_rgb(hue, 255, 255)

    def vertical_bars(self):
        for x in range(self.width):
            color = self.hsv_to_rgb((x * 16 + self.frame * 2) % 256, 255, 255)
            for y in range(self.height):
                self.np[self.xy(x, y)] = color

    def rainbow_circle(self):
        cx, cy = self.width // 2, self.height // 2
        for y in range(self.height):
            for x in range(self.width):
                dx, dy = x - cx, y - cy
                angle = math.atan2(dy, dx)
                hue = int((angle + math.pi) / (2 * math.pi) * 256) + self.frame * 2
                self.np[self.xy(x, y)] = self.hsv_to_rgb(hue % 256, 255, 255)

    def waterfall(self):
        for y in range(self.height):
            for x in range(self.width):
                hue = (self.frame * 4 + y * 5) % 256
                self.np[self.xy(x, y)] = self.hsv_to_rgb(hue, 255, 255)

    def hsv_to_rgb(self, h, s, v):
        h = float(h) / 256 * 6
        i = int(h)
        f = h - i
        p = int(v * (1 - s / 255))
        q = int(v * (1 - f * s / 255))
        t = int(v * (1 - (1 - f) * s / 255))
        v = int(v)
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
        return (0, 0, 0)
