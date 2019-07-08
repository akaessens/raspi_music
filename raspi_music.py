import logging
import signal
import sys
import webradio
import spotify


class PiRadio(object):

    def __init__(self):
        self.webradio = None
        self.spotify = None
        self.state = "off"

    def input(self, char):
        # OFF 
        if self.state == "off":
            if char == "w":
                self.webradio = webradio.WebRadio()
                self.state = "webradio"
            elif char == "s":
                self.spotify = spotify.Spotify()
                self.state = "spotify"

        # WEBRADIO
        elif self.state == "webradio":
            if char == "x":
                self.webradio.stop()
                self.state = "off"
            elif char == ">":
                self.webradio.next()
            elif char == "<":
                self.webradio.prev()
            elif char == " ":
                self.webradio.play_pause()
 
        # SPOTIFY
        elif self.state == "spotify":
            if char == "x":
                self.spotify.stop()
                self.state = "off"

def sigint_handler(signum, frame):
    radio.input("x")
    exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,format= '%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
    radio = PiRadio()
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    print ("Controls: \nSpace\tplay/pause\n<\tPrevious\n>\tNext\nx\tStop\nw\tWebradio\ns\tSpotify\nCtrl+C\tExit\n")
    
    while (True):
        char = sys.stdin.read(1)
        radio.input(char)