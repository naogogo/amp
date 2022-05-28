#!/usr/bin/env python3

import logging
import pykakasi

class Language(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.kakasi = pykakasi.kakasi()

    def convert(self, string):
        result = ""

        try:
            results = self.kakasi.convert(string)
            for r in results:
                result += r["hepburn"]
        except:
            self.logger.warn("Error converting string %s", string)

        return result

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def kakasi(self):
        return self._kakasi

    @kakasi.setter
    def kakasi(self, kakasi):
        self._kakasi = kakasi
