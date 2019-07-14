import logging
import vlc
import xml.etree.ElementTree as ET
import os
import sys
import re
from threading import Timer
from time import sleep

class Player(object):
    def play_pause(self):
        logging.debug("play_pause")

    def prev(self):
        logging.debug("prev")
    
    def next(self):
        logging.debug("next")


class WebRadio (Player):
    input = os.path.join( sys.path[0], "webradiosources.xml")
    def __init__(self):
        with open(WebRadio.input) as file:  
            data = file.read()
            xmlstring = re.sub(' xmlns="[^"]+"', '', data, count=1)
            self.tree = ET.fromstring(xmlstring)

        self.media_list = []
        self.current = 0

        for source in self.tree.findall("source"):
            uri = str(source.text)
            name = str(source.get("name"))

            self.media_list.append((name, uri))

        self.vlc_instance = vlc.Instance()
        self.vlc_instance.log_unset()
        self.player = self.vlc_instance.media_player_new()

        self.player.set_mrl(self.media_list[self.current][1])
        self.player.play()

        logging.debug("webradio started")
        self.print_current()

    def print_current(self):
        logging.debug(str(self.current) + " - " + str(self.media_list[self.current]))

        timer = Timer(0.5, self.print_title)
        timer.start()

    def print_title(self):
        cnt = 0
        while (not self.player.is_playing() and cnt < 10):
            sleep(0.1)
        sleep(0.1)

        title = str(self.player.get_media().get_meta(vlc.Meta.Title))
        playing = str(self.player.get_media().get_meta(vlc.Meta.NowPlaying))

        logging.info ("Station: " + title)
        logging.info ("Playing: " + playing)

    def play_pause(self):
        logging.debug("play_pause")
        self.player.pause()

    def prev(self):

        self.current = (self.current-1) % len(self.media_list)
        self.print_current()

        self.player.set_mrl(self.media_list[self.current][1])
        self.player.play()

    def next(self):

        self.current = (self.current+1) % len(self.media_list)

        self.print_current()

        self.player.set_mrl(self.media_list[self.current][1])
        self.player.play()

    def stop(self):
        logging.debug("webradio stopped")
        self.player.stop()
        
