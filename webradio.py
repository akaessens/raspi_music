import logging
import vlc
import xml.etree.ElementTree as ET
import os
import sys
import re
from threading import Timer
from time import sleep


@vlc.CallbackDecorators.LogCb
def log_callback(data, level, ctx, fmt, args):
    if level > 0:
        logging.debug("VLC: " + fmt.decode('UTF-8'), args)
    pass


class WebRadio():
    filename = os.path.join(sys.path[0], "webradiosources.xml")

    def __init__(self, args):
        logging.info("WebRadio started.")
        logging.debug("WebRadio sources file: " + WebRadio.filename)

        with open(WebRadio.filename) as file:
            data = file.read()
            xmlstring = re.sub(' xmlns="[^"]+"', '', data, count=1)
            self.tree = ET.fromstring(xmlstring)

        self.media_list = []
        self.current = 0

        for source in self.tree.findall("source"):
            uri = str(source.text)
            name = str(source.get("name"))

            self.media_list.append((name, uri))
            logging.debug("found source: " + name + " - " + uri)

        logging.debug("added sources: " + str(len(self.media_list)))

        self.vlc_instance = vlc.Instance()
        if args["v"] == 2:
            self.vlc_instance.log_set(log_callback, None)
        else:
            self.vlc_instance.log_unset()

        self.player = self.vlc_instance.media_player_new()

        startup_uri = self.media_list[self.current][1]

        self.player.set_mrl(startup_uri)
        self.player.play()

        self.print_current()

    def print_current(self):
        logging.debug("source nr  : " + str(self.current))
        logging.debug("source uri : " + self.media_list[self.current][1])
        logging.debug("source name: " + self.media_list[self.current][0])

        timer = Timer(0.5, self.print_title)
        timer.start()

    def print_title(self):
        logging.debug("Reading metadata")

        cnt = 0
        while (not self.player.is_playing() and cnt < 10):
            sleep(0.1)
            cnt += 1
        sleep(0.1)

        title = str(self.player.get_media().get_meta(vlc.Meta.Title))
        playing = str(self.player.get_media().get_meta(vlc.Meta.NowPlaying))

        logging.info("Station: " + title)
        logging.info("Playing: " + playing)

    def play_pause(self):
        logging.debug("play_pause")
        self.player.pause()

    def prev(self):
        logging.debug("prev")
        self.current = (self.current - 1) % len(self.media_list)
        self.print_current()

        self.player.set_mrl(self.media_list[self.current][1])
        self.player.play()

    def next(self):
        logging.debug("next")
        self.current = (self.current + 1) % len(self.media_list)

        self.print_current()

        self.player.set_mrl(self.media_list[self.current][1])
        self.player.play()

    def stop(self):
        logging.info("webradio stopped")
        self.player.stop()

    def list_stations(self):
        logging.info("Listing " + str(len(self.media_list)) + " Stations")
        for source in self.media_list:
            if self.media_list.index(source) == self.current:
                logging.info("* " + source[0] + " - " + source[1])
            else:
                logging.info("  " + source[0] + " - " + source[1])
