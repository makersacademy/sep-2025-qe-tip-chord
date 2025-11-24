# Welcome to Giga!

Giga - the gig booking site that'll be _huge_.

## Installation

* Clone this repository locally, `cd` into it
* `python3 -m venv giga_venv`
* `source giga_venv/bin/activate`
* `pip install -r requirements.txt`
* Create the databases specified in `lib/database_connection.py` - `giga` and `giga_test`
* Seed the production database e.g. `psql -h 127.0.0.1 giga -f seeds/test_gigs.sql -f seeds/test_bookings.sql`
* Run the server with `python app.py`
