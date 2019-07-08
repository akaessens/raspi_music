import logging
import signal
import sys
import webradio


class PiRadio(object):

    def __init__(self):
        self.webradio = None
        self.state = "off"

    def input(self, char):
        if self.state == "webradio":
            if char == "x":
                self.webradio.stop()
                self.state = "off"
            elif char == ">":
                self.webradio.next()
            elif char == "<":
                self.webradio.prev()
            elif char == " ":
                self.webradio.play_pause()
        elif self.state == "off":
            if char == "w":
                self.webradio = webradio.WebRadio()
                self.state = "webradio"

def sigint_handler(signum, frame):
    radio.input("x")
    exit(0)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    radio = PiRadio()
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    print ("Controls: \nSpace\tplay/pause\n<\tPrevious\n>\tNext\nx\tStop\nw\tWebradio\nCtrl+C\tExit\n")
    
    while (True):
        char = sys.stdin.read(1)
        radio.input(char)