#!/usr/bin/env python

class Artist(object):

    create_query = """
        CREATE TABLE IF NOT EXISTS artists (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT,
            title_s TEXT
        );
    """

    insert_query = """
        INSERT INTO artists (
            title,
            title_s
        ) VALUES (
            ?,
            ?
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
        self.path = None

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

    def to_database(self, cursor):
        return cursor.execute(self.insert_query, (
            self.title,
            self.title_s,
        ))

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
