import json


class db_structure(object):
    data_fields = ['albumartist', 'artist', 'title', 'album', 'tracknumber']

    def __init__(self,
                 albumartist,
                 artist,
                 title,
                 album,
                 tracknumber):
        self.albumartist = albumartist
        self.artist = artist
        self.title = title
        self.album = album
        if tracknumber:
            t = type(tracknumber)
            if t is str or t is unicode:
                s = tracknumber.split('/')[0]
                s = s.split('.')[0]
                self.tracknumber = int(s)
            else:
                self.tracknumber = tracknumber
        else:
            self.tracknumber = None

        self.name_dict = dict(zip(self.data_fields, [self.albumartist,
                                                     self.artist,
                                                     self.title,
                                                     self.album,
                                                     self.tracknumber]))

    def __iter__(self):
        return iter([self.albumartist,
                     self.artist,
                     self.title,
                     self.album,
                     self.tracknumber])

    def __getitem__(self, k):
        return self.name_dict[k]

    def __repr__(self):
        return repr((self.albumartist,
                     self.artist,
                     self.title,
                     self.album,
                     self.tracknumber))

    def to_list(self):
        return [self.albumartist,
                self.artist,
                self.title,
                self.album,
                self.tracknumber]


class MusicDB(object):

    """
    Functions to use from outside:
    get_albums_from_artist,
    get_artists_from_album,
    get_title, num_songs
    """

    def __init__(self, filename='music.db'):
        self.music_db = list()  # main db
        self.artist_db = set()  # set of all artists
        self.title_db = set()
        self.initialized = False


    def load(self, l):
        try:
            db = json.loads(l) # maybe *l
            db = map(lambda x: db_structure(*x), db)
            self._update_(db)
        except Exception, e:
            print e



    def _update_(self, db):
        """
        Updates DBS with album and artist entries
        """
        self.artist_db = self._find(db, 'album', 'albumartist')
        self.music_db = db
        self.initialized = True


    def _find(self, db, wanted, t):
        """
        Finds wanted e.g. 'artist'
        for args e.g. 'album'
        in db
        """
        def crawl_db(key):
            """
            Return set of all DB entries of key
            """
            s = set()
            for e in db:
                s.add(e[key])
            return s

        d = dict()
        for n in crawl_db(t):
            w = set()
            for a in self._filter_by(db, t, n):
                name = a[wanted]
                if name:
                    w.add(a[wanted])
                else:
                    w.add("unknown")
            d[n] = w
        return d

    def _get(self, key, db, name):
        return self._filter_by(db, key, name)

    def get_album(self, name):
        return self._sort_by(self._get('album', self.music_db, name),
                             'tracknumber')
    
    def get_title(self, db, name):
        return self._get('title', db, name)

    def get_artist(self, db, name):
        return self._get('artist', db, name)

    def get_albums_from_artist(self, name):
        a = list()
        if name not in self.artist_db:
            return None
        return self.artist_db[name]
        
    def _sort_by(self, db, t):
        return sorted(db, key=lambda db_structure: db_structure.name_dict[t])

    
    def _filter_by(self, db, t, name):
        l = []
        return filter(lambda x: name == x.name_dict[t], db)
