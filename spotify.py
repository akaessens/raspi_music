from webradio import Player
import logging
import subprocess


class Spotify(Player):

    def __init__(self):
        logging.debug("spotifyd started")
        self.process = subprocess.Popen("spotifyd --no-daemon", shell=True)

    def stop(self):
        self.process.kill()
        logging.debug("stopped spotifyd")
