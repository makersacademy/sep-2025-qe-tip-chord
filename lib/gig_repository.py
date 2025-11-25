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
        if rows == []:
            return None
        else:
            row = rows[0]
            return Gig(row["id"], row["datetime"], row["band"], row["venue"], row["location"], row["postcode"])

    def get_by_location(self, location):
        rows = self._connection.execute('SELECT * FROM gigs WHERE LOWER(location) = LOWER(%s) ORDER BY datetime', [location])
        gigs = []
        for row in rows:
            gigs.append(Gig(row["id"], row["datetime"], row["band"], row["venue"], row["location"], row["postcode"]))
        return gigs

    def get_by_dates(self, date_from="1900-01-01", date_to="3000-01-01"):
        rows = self._connection.execute('SELECT * FROM gigs WHERE datetime BETWEEN %s AND %s ORDER BY datetime', [date_from, date_to])
        gigs = []
        for row in rows:
            gigs.append(Gig(row["id"], row["datetime"], row["band"], row["venue"], row["location"], row["postcode"]))
        return gigs

    def get_by_location_and_dates(self, location, date_from="1900-01-01", date_to="3000-01-01"):
        if location == "All":
            gigs_by_location = self.all()
        else:
            gigs_by_location = self.get_by_location(location)
        gigs_by_dates = self.get_by_dates(date_from, date_to)
        matches = []
        for gig in gigs_by_location:
            if gig in gigs_by_dates:
                matches.append(gig)
        return matches
