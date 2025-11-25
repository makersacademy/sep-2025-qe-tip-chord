import datetime
from lib.gig import Gig

def test_gig_attributes():
    gig = Gig(111, "2024-06-04 19:30", "Placebo", "Brixton Academy", "London", "SW1 2AA")
    assert gig.id == 111
    assert gig.datetime == datetime.datetime(2024, 6, 4, 19, 30)
    assert gig.band == "Placebo"
    assert gig.venue == "Brixton Academy"
    assert gig.location == "London"
    assert gig.postcode == "SW1 2AA"

def test_pretty_datetime():
    gig = Gig(None, "2024-06-04 19:30", None, None, None, None)
    assert gig.datetime_pretty() == "2024-06-04 19:30"
