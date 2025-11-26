import datetime
from lib.booking import Booking

def test_booking_attributes():
    booking = Booking(135, "2024-06-05 21:21", 1, 2, 3)
    assert booking.id == 135
    assert booking.datetime == datetime.datetime(2024, 6, 5, 21, 21)
    assert booking.gig_id == 1
    assert booking.user_id == 2
    assert booking.ticket_count == 3

def test_pretty_datetime():
    booking = Booking(135, "2024-06-05 21:21", 1, 2, 3)
    assert booking.datetime_pretty() == "2024-06-05 21:21"

def test_jsonify_object():
    booking = Booking(135, "2024-06-05 21:21", 1, 2, 3)
    assert booking.jsonify() == {
        "id": 135,
        "datetime": "2024-06-05 21:21",
        "gig_id": 1,
        "user_id": 2,
        "ticket_count": 3
    }
