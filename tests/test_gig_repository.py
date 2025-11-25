from lib.gig_repository import GigRepository
from lib.gig import Gig
import pytest

def test_get_gigs(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    gigs = repo.all()
    assert gigs == [
        Gig(1, "2025-12-01 19:30", "Placebo", "Brixton Academy", "London", "SW9 9SL"),
        Gig(2, "2025-12-08 19:30", "Portishead", "Brixton Academy", "London", "SW9 9SL"),
        Gig(3, "2025-12-08 20:00", "Placebo", "The Roundhouse", "London", "NW1 8EH"),
        Gig(4, "2025-12-15 20:30", "Phantogram", "Corn Exchange", "Cambridge", "CB2 3QB")
    ]

def test_get_by_id(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    assert repo.get_by_id(2) == Gig(2, "2025-12-08 19:30", "Portishead", "Brixton Academy", "London", "SW9 9SL")

def test_get_by_id_nothing_found(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    assert repo.get_by_id(100) == None

def test_get_by_location(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    assert repo.get_by_location("London") == [
        Gig(1, "2025-12-01 19:30", "Placebo", "Brixton Academy", "London", "SW9 9SL"),
        Gig(2, "2025-12-08 19:30", "Portishead", "Brixton Academy", "London", "SW9 9SL"),
        Gig(3, "2025-12-08 20:00", "Placebo", "The Roundhouse", "London", "NW1 8EH")
    ]
    assert repo.get_by_location("Cambridge") == [
        Gig(4, "2025-12-15 20:30", "Phantogram", "Corn Exchange", "Cambridge", "CB2 3QB")
    ]

def test_get_by_simple_date_range(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    assert repo.get_by_dates("2025-12-07", "2025-12-09") == [
        Gig(2, "2025-12-08 19:30", "Portishead", "Brixton Academy", "London", "SW9 9SL"),
        Gig(3, "2025-12-08 20:00", "Placebo", "The Roundhouse", "London", "NW1 8EH")
    ]

def test_get_by_dates_invalid_range(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    with pytest.raises(Exception) as e:
        repo.get_by_dates("2025-06-14", "2025-06-12")
    assert str(e.value) == "Past cannot be after future"

def test_get_by_location_and_dates_specific(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    assert repo.get_by_location_and_dates("London", "2025-11-30", "2025-12-02") == [
        Gig(1, "2025-12-01 19:30", "Placebo", "Brixton Academy", "London", "SW9 9SL")
    ]

def test_get_by_location_and_dates_all(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    assert repo.get_by_location_and_dates("All", "2025-12-06", "2025-12-16") == [
        Gig(2, "2025-12-08 19:30", "Portishead", "Brixton Academy", "London", "SW9 9SL"),
        Gig(3, "2025-12-08 20:00", "Placebo", "The Roundhouse", "London", "NW1 8EH"),
        Gig(4, "2025-12-15 20:30", "Phantogram", "Corn Exchange", "Cambridge", "CB2 3QB")
    ]

def test_get_by_band_name(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    assert repo.get_by_band_name("Placebo") == [
        Gig(1, "2025-12-01 19:30", "Placebo", "Brixton Academy", "London", "SW9 9SL"),
        Gig(3, "2025-12-08 20:00", "Placebo", "The Roundhouse", "London", "NW1 8EH")
    ]

def test_add_gig(db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    repo = GigRepository(db_connection)
    repo.add_gig(Gig(None, "2025-12-07 21:00", "Bush", "Corn Exchange", "Cambridge", "CB2 3QB"))
    gigs = repo.all()
    assert gigs == [
        Gig(1, "2025-12-01 19:30", "Placebo", "Brixton Academy", "London", "SW9 9SL"),
        Gig(5, "2025-12-07 21:00", "Bush", "Corn Exchange", "Cambridge", "CB2 3QB"),
        Gig(2, "2025-12-08 19:30", "Portishead", "Brixton Academy", "London", "SW9 9SL"),
        Gig(3, "2025-12-08 20:00", "Placebo", "The Roundhouse", "London", "NW1 8EH"),
        Gig(4, "2025-12-15 20:30", "Phantogram", "Corn Exchange", "Cambridge", "CB2 3QB")
    ]
