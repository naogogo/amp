#!/usr/bin/env python

import pykakasi

class ArtistList(object):

        DB_FIND_SELECT_QUERY = """
SELECT id FROM artists
"""

        def __init__(self):
                self.artists = []

        def like(self, what):
                return "%%{0}%%".format(what)

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
                        params += (self.like(s), self.like(s))
                return params

        def find(self, con, title):
                artists = []
                res = con.execute(self.DB_FIND_SELECT_QUERY + self.where(title), self.where_params(title)).fetchall()
                for row in res:
                        artist = Artist()
                        artist.from_db_by_id(con, row[0])
                        artists.append(artist)

                self.artists = artists

        @property
        def artists(self):
                return self._artists

        @artists.setter
        def artists(self, artists):
                self._artists = artists

class Artist(object):

        create_query = """
CREATE TABLE IF NOT EXISTS artists (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        title           TEXT,
        title_s         TEXT
);
"""

        DB_ID_SELECT_QUERY = """
SELECT * FROM artists WHERE id = ?
"""

        DB_TITLE_SELECT_QUERY = """
SELECT * FROM artists WHERE title = ?
        """

        def __init__(self):
                self.id = 0
                self.title = None

        def from_db_by_id(self, con, id):
                res = con.execute(self.DB_ID_SELECT_QUERY, (id,)).fetchall()
                if len(res) != 1:
                        return False
                row = res[0]

                self.id = row[0]
                self.title = row[1]

                return True

        def from_db_by_title(self, con, title):
                res = con.execute(self.DB_TITLE_SELECT_QUERY, (title,)).fetchall()
                if len(res) != 1:
                        return False
                row = res[0]

                self.id = row[0]
                self.title = row[1]

                return True

        def to_dict(self):
            return {
                "id": self.id,
                "title": self.title,
            }

        @property
        def id(self):
                return self._id

        @id.setter
        def id(self, id):
                self._id = int(id)

        @property
        def title(self):
                return self._title

        @title.setter
        def title(self, title):
                self._title = title

        def __eq__(self, other):
                if not isinstance(other, Artist):
                        return False

                if not self.title == other.title:
                        return False

                return True

        @property
        def title_s(self):
                return self._title_s

        @title_s.setter
        def title_s(self, title_s):
                self._title_s = title_s
