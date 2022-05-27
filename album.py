#!/usr/bin/env python3

from artist import Artist

class AlbumList(object):

        DB_FIND_SELECT_QUERY = """
SELECT id FROM albums
"""

        def __init__(self):
                self.albums = []

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

class Album(object):

        create_query = """
CREATE TABLE IF NOT EXISTS albums (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        title           TEXT,
        title_s         TEXT,
        artist          INTEGER,
        date            INTEGER,
        disc            INTEGER
);
"""

        DB_ID_SELECT_QUERY = """
SELECT * FROM albums WHERE id = ?
"""

        DB_TITLE_SELECT_QUERY = """
SELECT * FROM albums WHERE artist = ? AND title = ? AND date = ? AND disc = ?
        """

        def __init__(self):
                self.id = 0
                self.title = None
                self.artist = None
                self.date = 0
                self.disc = 0
                self.path = None


        def from_db_by_id(self, con, id):
                res = con.execute(self.DB_ID_SELECT_QUERY, (id, )).fetchall()
                if len(res) != 1:
                        return False

                row = res[0]

                artist = Artist()
                if not artist.from_db_by_id(con, row[3]):
                        return False

                self.id = row[0]
                self.title = row[1]
                self.artist = artist
                self.date = row[4]
                self.disc = row[5]
                self.path = "{0}/{1} - {2}{3}".format(
                    self.artist.title,
                    self.date,
                    self.title,
                    "/Disc" + str(self.disc) if self.disc > 0 else ""
                )

                return True

        def from_db_by_title(self, con, artist, title, date, disc):
                artist_o = Artist()
                if not artist_o.from_db_by_title(con, artist):
                        return False

                res = con.execute(self.DB_TITLE_SELECT_QUERY, (artist_o.id, title, date, disc)).fetchall()
                if len(res) != 1:
                        return False

                row = res[0]

                artist = Artist()
                if not artist.from_db_by_id(con, row[3]):
                        return False

                self.id = row[0]
                self.title = row[1]
                self.artist = artist
                self.date = row[4]
                self.disc = row[5]
                self.path = "{0}/{1} - {2}{3}".format(
                    self.artist.title,
                    self.date,
                    self.title,
                    "/Disc" + str(self.disc) if self.disc > 0 else ""
                )

                return True

        def from_json(self, con, data):
                self.title = data["album"]
                self.date = data["date"]
                try:
                        self.disc = data["disc"]
                except KeyError:
                        self.disc = 0

                artist = Artist()

                try:
                        if not artist.from_db_by_title(con, data["albumartist"]):
                                return False
                except KeyError:
                        if not artist.from_db_by_title(con, data["artist"]):
                                return False

                if artist.id == 0:
                        return False

                self.artist = artist
                return True

        def to_dict(self):
            return {
                "id": self.id,
                "title": self.title,
                "artist": self.artist.to_dict(),
                "date": self.date,
                "disc": self.disc,
                "path": self.path,
            }

        @property
        def path(self):
            return self._path

        @path.setter
        def path(self, path):
            self._path = path

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

        @property
        def artist(self):
                return self._artist

        @artist.setter
        def artist(self, artist):
                if artist and not isinstance(artist, Artist):
                        raise Exception("not isinstance Artist")

                self._artist = artist

        @property
        def date(self):
                return self._date

        @date.setter
        def date(self, date):
                self._date = int(date)

        @property
        def disc(self):
                return self._disc

        @disc.setter
        def disc(self, disc):
                self._disc = int(disc)

        def __eq__(self, other):
                if not isinstance(other, Album):
                        return False

                if not self.title == other.title:
                        return False

                if not self.artist == other.artist:
                        return False

                if not self.date == other.date:
                        return False

                if not self.disc == other.disc:
                        return False

                return True

