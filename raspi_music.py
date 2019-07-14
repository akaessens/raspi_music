import logging
import sys
import webradio
import spotify
import argparse


class PiRadio():

    def __init__(self, args):
        self.webradio = None
        self.spotify = None
        self.state = "off"

        self.args = args

    def input(self, char):
        logging.debug("input: " + char)
        # OFF
        if self.state == "off":
            if char == "w":
                self.webradio = webradio.WebRadio(self.args)
                self.state = "webradio"
            elif char == "s":
                self.spotify = spotify.Spotify(self.args)
                self.state = "spotify"
            elif char == "x":
                logging.info("Stopped.")

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

        logging.debug("state: " + self.state)


if __name__ == '__main__':

    control_desc = ("Controls:\n"
                    "  Space       play/pause\n"
                    "  <           Previous\n"
                    "  >           Next\n"
                    "  x           Stop\n"
                    "  w           Webradio\n"
                    "  s           Spotify\n"
                    "  Ctrl+C      Exit\n")

    parser = argparse.ArgumentParser(
        description="WebRadio and Spotify Connect Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=control_desc
    )

    parser.add_argument('--v', action='store_true', help='Verbose logging')
    parser.add_argument('--w', action='store_true', help='Start with WebRadio')
    parser.add_argument('--s', action='store_true', help='Start with Spotify')

    args = parser.parse_args()

    level = logging.INFO
    if args.v:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S')

    args_dict = vars(args)
    radio = PiRadio(args_dict)

    if args.w:
        radio.input("w")
    elif args.s:
        radio.input("s")

    try:
        while True:
            char = sys.stdin.read(1)
            if char != "\n":
                radio.input(char)

    except KeyboardInterrupt:
        print()
        radio.input("x")
        exit(0)
