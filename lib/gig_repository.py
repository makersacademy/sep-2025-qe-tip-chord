from lib.gig import Gig

class GigRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM gigs')
        gigs = []
        for row in rows:
            gigs.append(Gig(row["id"], row["datetime"], row["band"], row["venue"], row["location"], row["postcode"]))
        return gigs

    def get_by_id(self, gig_id):
        rows = self._connection.execute('SELECT * FROM gigs WHERE id = %s', [gig_id])
        row = rows[0]
        return Gig(row["id"], row["datetime"], row["band"], row["venue"], row["location"], row["postcode"])
