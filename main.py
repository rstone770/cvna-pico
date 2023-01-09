from time import sleep_ms, time
import machine

from machine import Pin, I2C
from random import random
from finhub import Finhub, Quote
from graph import Graph
from lib.ssd1306 import SSD1306_I2C
from marquee import Marquee
from settings import read_settings
from terminal import Terminal
from wifi import wifi_connect

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

display_i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400_000)
display = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, display_i2c)
terminal = Terminal(display, DISPLAY_WIDTH, 56)

settings = read_settings()
finhub = Finhub(settings.finhub_apikey)

def log(*pieces: str):
    for p in pieces:
        terminal.write_line(p)
    
    display.show()

def blit_marquee(marquee: Marquee):
    marquee.blit_to(display, 0, 54)

def blit_graph(graph: Graph):
    graph.blit_to(display, 0, 0)

def sync_display():
    display.show()
    sleep_ms(16)

if not settings.is_valid:
    log("Invalid settings")
else:
    try:
        log("Connecting Wifi")
        ip = wifi_connect(settings.wlan_ssid, settings.wlan_password)

        log("Wifi Connected", f"@{ip}")
        log("Starting")
        
        quote = finhub.get_quote("CVNA")
        marquee = Marquee(quote, width = DISPLAY_WIDTH)
        graph = Graph(width = DISPLAY_WIDTH, height = 54).sample_quote(quote)

        while True:
            blit_graph(graph)

            while marquee.scroll_next():
                blit_marquee(marquee)
                sync_display()

            if time() - quote.requested_on >  settings.pool_interval:
                display.ellipse(DISPLAY_WIDTH - 4, 4, 1, 1, 1, True) # loading indicator
                display.show()

                quote = finhub.get_quote("CVNA")
                marquee.update_quote(quote)
                graph.sample_quote(quote)
            else:
                sleep_ms(2500)
        
    except KeyboardInterrupt:
        machine.reset()
