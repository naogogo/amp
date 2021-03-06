#!/usr/bin/env python3

import logging
import mpd

from album import *

class Player(object):

    def __init__(self, host="localhost", port=6600):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.client = mpd.MPDClient()
        self.timeout = 3

    def begin(self):
        try:
            self.client.command_list_ok_begin()
        except ConnectionError:
            self.connect()
            self.client.command_list_ok_begin()

    def end(self):
        self.client.command_list_end()

    def play_artist(self, cursor, artist):
        self.begin()
        self.client.stop()
        self.client.clear()

        self.client.add(artist.path)
        self.client.play(0)

        self.end()

    def play_album(self, album):
        self.begin()
        self.client.stop()
        self.client.clear()

        self.client.add(album.path)
        self.client.play(0)

        self.end()


    def play_song(self, cursor, song):
        album = Album()
        album.from_db_by_id(song.album.id)

        self.begin()
        self.client.stop()
        self.client.clear()

        self.client.add(album.path)
        self.client.play(song.track - 1)

        self.end()

    def connect(self):
        self.client.connect(self.host, self.port)

    def play(self, cursor, albums=[]):
        albumlist = []
        for album in albums:
            a = Album()
            a.from_db_by_id(cursor, album)
            albumlist.append(a)

        self.command_list_ok_begin()
        self.client.stop()
        self.client.clear()
        for a in albumlist:
            self.client.add(a.path)
        self.client.command_list_end()

    def disconnect(self):
        self.client.close()
        self.client.disconnect()

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def timeout(self):
        return self.client.timeout

    @timeout.setter
    def timeout(self, timeout):
        self.client.timeout = timeout

    @property
    def idletimeout(self):
        return self.client.idletimeout

    @idletimeout.setter
    def idletimeout(self, idletimeout):
        self.client.idletimeout = idletimeout

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger
