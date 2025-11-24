from lib.booking import Booking

class BookingRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_bookings(self):
        rows = self._connection.execute('SELECT * FROM bookings')
        bookings = []
        for row in rows:
            bookings.append(Booking(row["id"], row["datetime"], row["gig_id"], row["user_id"], row["ticket_count"]))
        return bookings
