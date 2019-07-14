import logging
import subprocess
import sys


class Spotify():

    def __init__(self, args):
        logging.info("Spotify Connect client started.")

        command = "spotifyd --no-daemon"
        
        self.process = subprocess.Popen(command, shell=True)

    def stop(self):
        self.process.kill()
        logging.info("Stopped Spotify Connect client.")
