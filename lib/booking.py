import datetime

class Booking:
    def __init__(self, id, dt, gig_id, user_id, ticket_count):
        self.id = id

        # input expected to be in format "%Y-%m-%d %H:%M"
        # should be stored as datetime.datetime()
        # `.strftime("%Y-%m-%d %H:%M")` - for nice formatting
        if type(dt) == str:
            self.datetime = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
        else:
            self.datetime = dt

        self.gig_id = gig_id
        self.user_id = user_id
        self.ticket_count = ticket_count

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def datetime_pretty(self):
        return self.datetime.strftime("%Y-%m-%d %H:%M")

    def jsonify(self):
        return {
            "id": self.id,
            "datetime": self.datetime_pretty(),
            "gig_id": self.gig_id,
            "user_id": self.user_id,
            "ticket_count": self.ticket_count
        }
