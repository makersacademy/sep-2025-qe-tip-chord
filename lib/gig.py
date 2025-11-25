import datetime

class Gig:
    def __init__(self, id, dt, band, venue, location, postcode):
        self.id = id

        # input expected to be in format "%Y-%m-%d %H:%M"
        # should be stored as datetime.datetime()
        # `.strftime("%Y-%m-%d %H:%M")` - for nice formatting
        if type(dt) == str:
            self.datetime = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
        else:
            self.datetime = dt

        self.band = band
        self.venue = venue

        # City/Town/etc.
        self.location = location

        # for maps lookup
        self.postcode = postcode

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def datetime_pretty(self):
        return self.datetime.strftime("%Y-%m-%d %H:%M")
