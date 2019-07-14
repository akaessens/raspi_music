import logging
import subprocess
import sys


class Spotify():

    def __init__(self, args):
        logging.info("Spotify Connect client started.")

        command = "spotifyd --no-daemon"
        if args["v"]:
            out = sys.stdout
        else:
            out = subprocess.PIPE
        self.process = subprocess.Popen(command, stdout=out, shell=True)

    def stop(self):
        self.process.kill()
        logging.info("Stopped Spotify Connect client.")
