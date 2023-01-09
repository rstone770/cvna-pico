from framebuf import FrameBuffer

class Terminal:
    def __init__(self, buffer: FrameBuffer, width: int, cursor_y: int):
        self.buffer = buffer
        self.width = width
        self.cursor_y = cursor_y
    
    def write_line(self, s: str): 
        buffer = self.buffer
        width = self.width
        cursor = self.cursor_y
        stride = width >> 3

        for i in range(0, len(s), stride):
            buffer.scroll(0, -10)
            buffer.fill_rect(0, cursor, width, cursor + 10, 0)
            buffer.text(s[i:i + stride], 0, cursor)

        return self
