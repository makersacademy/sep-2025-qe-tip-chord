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
