import logging
import vlc
import xml.etree.ElementTree

class Player(object):
    def play_pause(self):
        logging.debug("play_pause")

    def prev(self):
        logging.debug("prev")
    
    def next(self):
        logging.debug("next")


class WebRadio (Player):
    input = "webradiosources.xml"
    def __init__(self):

        self.tree = xml.etree.ElementTree.parse(WebRadio.input).getroot()
        self.media_list = []
        self.current = 0

        for source in self.tree.findall("source"):
            name = str(source.text)
            uri = str(source.get("uri"))

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
        