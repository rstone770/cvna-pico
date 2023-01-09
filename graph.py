from math import floor
from framebuf import FrameBuffer, MONO_VLSB
from finhub import Quote

STEPS = 32

class Graph:
    def __init__(self, width: int, height: int)  -> None:
        self.steps = STEPS
        self.stride = int(width / STEPS)
        self.width = width
        self.height = height
        self.has_pending_draw = True
        self.samples: list[Quote] = []
        
        buffer = bytearray(width * height)
        self.buffer = FrameBuffer(buffer, width, height, MONO_VLSB)

    def sample_quote(self, quote: Quote):
        self.samples.insert(0, quote)
        self.has_pending_draw = True
        
        if len(self.samples) > self.steps:
            self.samples.pop()

        return self

    def blit_to(self, buffer: FrameBuffer, x: int, y: int):
        source = self.buffer

        if self.has_pending_draw:
            self.has_pending_draw = draw_graph(source, self.samples, self.width, self.height, self.stride)

        buffer.blit(source, x, y)

def nf(v: float, min: float, max: float):
    return (v - min) / (max - min)  
    
def draw_scale(buffer: FrameBuffer, width: int, height: int):
    buffer.vline(0, 0, height - 2, 1)
    buffer.hline(0, height - 2, width, 1)

def draw_points(buffer: FrameBuffer, samples: list[Quote], width: int,  height: int, stride: int):
    max_y = max(sample.price for sample in samples)
    min_y = min(sample.price for sample in samples)

    if max_y - min_y <= 0.01:
        if min_y <= 0.01:
            min_y = 0.00
            max_y = 0.05
        else:
            min_y = max_y - 0.01
            max_y = max_y + 0.01

    max_h = height - 3
    max_w = width - 8
    tail: Quote | None = None

    for i, s in enumerate(reversed(samples)):
        if tail is None:
            tail = s
        else:
            x_1 = stride * (i - 1) + 2
            y_1 = int(nf(tail.price, min_y, max_y) * max_h)
            x_2 = min((stride * (i - 1)) + stride + 2, max_w)
            y_2 = int(nf(s.price, min_y, max_y) * max_h)
            tail = s

            buffer.line(x_1, y_1, x_2, y_2, 1)

            if x_2 >= max_w:
                break

def draw_graph(buffer: FrameBuffer, samples: list[Quote], width: int,  height: int, stride: int):
    buffer.fill(0)

    if len(samples) > 1:
        draw_points(buffer, samples, width, height, stride)

    draw_scale(buffer, width, height)

    return False
