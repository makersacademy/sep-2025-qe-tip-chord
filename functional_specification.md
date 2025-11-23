## Giga - Functional Specification

* Document version: 1.0
* Authors: Jo (Product Manager), Lou (Development Manager)
* Date: 2025-11-23

## Authentication & Accounts

| Id | Item | Status |
| --- | --- | --- |
| AA001 | New user can sign up with username and password |  |
| AA002 | Signed up users can log in if providing correct credentials |  |
| AA003 | Logged in users can log out |  |
| AA004 | Bookings of tickets belong to specific signed up users |  |
| AA005 | Passwords are not stored in plain text |  |
| AA006 | Account page only accessible to logged in users, otherwise prompts for login|  |
| AA007 | Booking of tickets only accessible to logged in users |  |

## Design

| Id | Item | Status |
| --- | --- | --- |
| DE001 | Menu bar accessible from all pages |  |
| DE002 | Menu bar allows immediate access to all the main pages |  |
| DE003 | Home page to welcome new users and just logged in users |  |
| DE004 | Gigs page showing gigs |  |
| DE005 | Account page showing a user's booked gigs (if logged in) |  |
| DE006 | About page includes details about the site |  |
| DE007 | Logged in users can log out |  |
| DE008 | Logged out users can log in |  |

## Gigs

| Id | Item | Status |
| --- | --- | --- |
| GI001 | Can click through from gigs to individual bands |  |
| GI002 | Gigs can be listed, ordered by date |  |
| GI003 | Gigs have an associated band, venue, location (city), postcode and date + time |  |
| GI004 | Google map of venue displayed alongside individual gig |  |
| GI005 | Gigs in the past are displayed differently when listed |  |

## Bookings

| Id | Item | Status |
| --- | --- | --- |
| BK001 | Can click through from gigs to see more details and how to book tickets |  |
| BK002 | Gigs can be booked by an individual user |  |
| BK003 | Numbers of free tickets can be specified when booking |  |
| BK004 | Only one booking per gig is permitted |  |
| BK005 | Bookings can be cancelled |  |
| BK006 | A booking has a maximum of 8 tickets |  |

## API

| Id | Item | Status |
| --- | --- | --- |
| AP001 | Root level /api resource, explaining basic usage |  |
| AP002 | Sub-level resource types can be specified by name |  |
| AP003 | Sub-level resource types: gigs, bands, accounts, bookings |  |
| AP004 | Subset of resources of type gig can be returned via date and location filters |  |
| AP005 | Individual resources of a specific type can be specified by name or id (type dependent) |  |
| AP006 | Gigs can be booked |  |
| AP007 | Bookings can be cancelled |  |

## Other

| Id | Item | Status |
| --- | --- | --- |
| OT001 | All dates in ISO format (YYYY-MM-DD) |  |
| OT002 | Setup instructions for running the server locally |  |
| OT003 | Bookings are free with no money exchanged |  |
| OT004 | Chrome Desktop support only, minimum resolution 1280 × 1024 |  |
