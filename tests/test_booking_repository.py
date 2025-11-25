from lib.booking_repository import BookingRepository
from lib.booking import Booking
from lib.gig import Gig
import datetime

def test_get_bookings_for_user(db_connection):
    db_connection.seed("seeds/test_users.sql")
    db_connection.seed("seeds/test_bookings.sql")
    repo = BookingRepository(db_connection)
    bookings = repo.get_bookings(1)
    assert bookings == [
        Booking(1, '2025-11-22 15:43', 1, 1, 1),
        Booking(2, '2025-11-22 15:43', 4, 1, 4)
    ]

def test_get_no_bookings_for_user(db_connection):
    db_connection.seed("seeds/test_users.sql")
    db_connection.seed("seeds/test_bookings.sql")
    repo = BookingRepository(db_connection)
    bookings = repo.get_bookings(100)
    assert bookings == []

def test_make_booking_for_user(db_connection):
    db_connection.seed("seeds/test_users.sql")
    db_connection.seed("seeds/test_bookings.sql")
    repo = BookingRepository(db_connection)
    now = datetime.datetime.now()
    repo.make_booking(2, 1, 2)
    bookings = repo.get_bookings(1)
    assert bookings == [
        Booking(1, '2025-11-22 15:43', 1, 1, 1),
        Booking(2, '2025-11-22 15:43', 4, 1, 4),
        Booking(3, now.strftime("%Y-%m-%d %H:%M"), 2, 1, 2)
    ] or bookings == [
        Booking(1, '2025-11-22 15:43', 1, 1, 1),
        Booking(2, '2025-11-22 15:43', 4, 1, 4),
        Booking(3, (now + datetime.timedelta(0,1)).strftime("%Y-%m-%d %H:%M"), 2, 1, 2)
    ] # handle crossing minute-boundary while test runs
