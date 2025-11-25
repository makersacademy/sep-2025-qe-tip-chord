import datetime
from lib.booking import Booking

def test_booking_attributes():
    booking = Booking(135, "2024-06-05 21:21", 1, 2, 3)
    assert booking.id == 135
    assert booking.datetime == datetime.datetime(2024, 6, 5, 21, 21)
    assert booking.gig_id == 1
    assert booking.user_id == 2
    assert booking.ticket_count == 3
