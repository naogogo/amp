#!/usr/bin/env python3

import json
import os
import requests

class Client(object):

    def __init__(self, host, port, scheme):
        self.url = "{0}://{1}:{2}".format(scheme, host, port)

    def search(self, query):
        url = "{0}/search".format(self.url)
        data = {"query": query}

        res = requests.post(url, data=data)
        return res.text

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url


if __name__ == "__main__":

    client = Client(
        os.environ.get("HOST", "localhost"),
        os.environ.get("PORT", "5000"),
        os.environ.get("SCHEME", "http")
    )

    try:
        while True:

            i = input("> ")
            if i == "exit":
                break

            if i.startswith("s "):
                response = json.loads(client.search(i[2:]))
                print(json.dumps(response, indent=2))

    except (EOFError, KeyboardInterrupt):
        pass
