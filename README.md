# Welcome to Giga!

Giga - the gig booking site that'll be _huge_.

## Installation

* Clone this repository locally, `cd` into it
* `python3 -m venv giga_venv`
* `source giga_venv/bin/activate`
* `pip install -r requirements.txt`
* Create the databases specified in `lib/database_connection.py` - `giga` and `giga_test`
* Seed the production database e.g. `psql -h 127.0.0.1 giga -f seeds/test_gigs.sql -f seeds/test_users.sql -f seeds/test_bookings.sql`
* Run the server with `python app.py`

## Adding Users

Users can be added to the "users" table with values of a username (string) and a
password generated via a hash.

The following example shows steps that can be used to generate a hashed
password, starting with your virtual environment activated:

```python
(giga_venv) % python
>>> from werkzeug.security import generate_password_hash
>>> generate_password_hash("mypassword123")
'scrypt:32768:8:1$IuT0ev03aikfxfuB$724fc6b7123b7eb74b7bc9084b8a0cdd2be087cac401bf93e057191babcd8c5f9b3a93d3e27188bd756b40ac333b026297878d9cc35928099dd454f53f015370'
```

The `scrypt` string can be inserted into the table - see the existing seed file
for reference.
