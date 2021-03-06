#!/usr/bin/env python3

from album import Album
from language import Language

import logging

class AlbumList(object):

    DB_FIND_SELECT_QUERY = """
        SELECT id FROM albums
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.albums = []
        self.language = Language()

    def from_json(self, connection, data):
        counter = 0
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION;")

        for row in data:
            counter += 1
            album = Album()
            album.from_json(cursor, row)
            try:
                album.title_s = self.language.convert(row["album"])
            except:
                album.title_s = ""

            if album in self.albums:
                continue

            self.albums.append(album)
            album.to_database(cursor)

        cursor.execute("COMMIT;")
        cursor.close()

        self.logger.info("Processed %d entries, added %d albums", counter, len(self.albums))

    def where(self, where):
        i = 0
        query = ""
        ss = where.strip().split()
        for s in ss:
            if i > 0:
                query += "AND "
            else:
                query += "WHERE "
            query += "(title LIKE ? OR title_s LIKE ?) "
            i += 1
        return query

    def where_params(self, where):
        params = ()
        ss = where.strip().split()
        for s in ss:
            w = "%%{0}%%".format(s)
            params += (w, w)
        return params


    def find(self, con, title):
        albums = []

        res = con.execute(self.DB_FIND_SELECT_QUERY + self.where(title), self.where_params(title)).fetchall()
        for row in res:
            album = Album()
            album.from_db_by_id(con, row[0])
            albums.append(album)

        self.albums = albums

    @property
    def albums(self):
        return self._albums

    @albums.setter
    def albums(self, albums):
        self._albums = albums

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language
