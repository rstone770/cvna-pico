from array import array
from math import ceil
from framebuf import MONO_VLSB, FrameBuffer
from finhub import Quote

ICON_STATUS_UP = array("h", [0, 7, 4, 0, 7, 7])
ICON_STATUS_DOWN = array("h", [0, 0, 7, 0, 4, 7])

class Marquee:
    def __init__(self, quote: Quote, width: int):
        self.has_pending_draw = True
        self.offset = 0
        self.quote = quote
        self.width = width
        self.height = 10
        self.length = self.width * 3

        buffer = bytearray(self.length * self.height) # bit per pixel
        self.buffer = FrameBuffer(buffer, self.length, self.height, MONO_VLSB)

    def blit_to(self, buffer: FrameBuffer, x: int, y: int):
        offset = self.offset
        source = self.buffer

        if self.has_pending_draw:
            self.has_pending_draw = draw_quote(source, self.quote, self.width)

        buffer.blit(source, x - offset, y)

        if offset > (self.length - self.width):
            buffer.blit(source, x + (self.length - offset), y)

    def is_scrolling(self):
        return (self.offset % self.width) > 0

    def scroll_next(self):
        self.offset = (self.offset + 1) % self.length
        
        return self.is_scrolling()

    def update_quote(self, quote: Quote):
        self.quote = quote
        self.has_pending_draw = True

CH      = 8 # char width
CH_2    = CH << 1
CH1_2   = CH >> 1

def draw_quote(buffer: FrameBuffer, quote: Quote, width: int):
    symbol = quote.symbol
    status_icon = ICON_STATUS_UP
    sign = "+" if quote.delta > 0 else "-"

    if quote.delta < 0:
        status_icon = ICON_STATUS_DOWN

    offset = 0
    buffer.fill(1)
    buffer.poly(offset + CH1_2, 1, status_icon, 0, True)
    buffer.text(f"{symbol} ${quote.price:.2f}", offset + CH_2, 1, 0)

    offset += width
    buffer.poly(offset + CH1_2, 1, status_icon, 0, True)
    buffer.text(f"{symbol} {sign}${abs(quote.delta):.2f}", offset + CH_2, 1, 0)

    offset += width
    buffer.poly(offset + CH1_2, 1, status_icon, 0, True)
    buffer.text(f"{symbol} {quote.percentage:+.2f}%", offset + CH_2, 1, 0)

    return False
