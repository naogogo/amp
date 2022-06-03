#!/usr/bin/env python3

import argparse
import json
import logging
import os
import requests
import sys

class Client(object):

    def __init__(self, host, port, scheme):
        self.logger = logging.getLogger(__name__)
        self.url = "{0}://{1}:{2}".format(scheme, host, port)

    def search(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        parser = argparse.ArgumentParser(
            description="Search for songs in the database"
        )
        parser.add_argument("query", nargs="+")
        args = parser.parse_args(sys.argv[2:])
        query = args.query

        self.logger.info("Search with query `%s'", query)

        url = "{0}/search".format(self.url)
        data = {"query": query}
        print(data)

        res = requests.post(url, data=json.dumps(data), headers=headers)
        print(res.text)
        response = json.loads(res.text)
        print(json.dumps(response, indent=2))

    def play(self, artists=[], albums=[], songs=[]):
        url = "{0}/play".format(self.url)
        data = {
            "artists": artists,
            "albums": albums,
            "songs": songs
        }

        res = requests.post(url, data={data})
        response = json.loads(res.text)
        print(json.dumps(response, indent=2))

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, parser):
        self._parser = parser

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = Client(
        os.environ.get("HOST", "localhost"),
        os.environ.get("PORT", "5000"),
        os.environ.get("SCHEME", "http")
    )

    parser = argparse.ArgumentParser(
        description="Album Music Player",
        usage="""amp <command> [<args>]

The command can be any of:
  search    Search for songs, albums or artists
  play      Play a song
""")
    parser.add_argument("command", help="Subcommand to run")
    args = parser.parse_args(sys.argv[1:2])
    if not hasattr(client, args.command):
        self.logger.error("Unrecognized command `%s'", args.command)
        sys.exit(1)

    getattr(client, args.command)()

