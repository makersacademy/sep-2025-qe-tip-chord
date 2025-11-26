from lib.gig import Gig
from datetime import date

class GigRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM gigs ORDER BY datetime')
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

    def get_by_dates(self, date_from="2000-01-01", date_to="2100-01-01"):
        if date.fromisoformat(date_from) > date.fromisoformat(date_to):
            raise Exception("Past cannot be after future")
        rows = self._connection.execute('SELECT * FROM gigs WHERE datetime BETWEEN %s AND %s ORDER BY datetime', [date_from + " 00:00", date_to + " 23:59"])
        gigs = []
        for row in rows:
            gigs.append(Gig(row["id"], row["datetime"], row["band"], row["venue"], row["location"], row["postcode"]))
        return gigs

    def get_by_location_and_dates(self, location, date_from="2000-01-01", date_to="2100-01-01"):
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

    def get_by_band_name(self, band_name):
        rows = self._connection.execute('SELECT * FROM gigs WHERE LOWER(band) = LOWER(%s) ORDER BY datetime', [band_name])
        gigs = []
        for row in rows:
            gigs.append(Gig(row["id"], row["datetime"], row["band"], row["venue"], row["location"], row["postcode"]))
        return gigs

    def add_gig(self, gig):
        self._connection.execute('INSERT INTO gigs (datetime, band, venue, location, postcode) VALUES (%s, %s, %s, %s, %s)',
            [gig.datetime, gig.band, gig.venue, gig.location, gig.postcode])
