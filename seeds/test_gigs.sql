DROP TABLE IF EXISTS gigs CASCADE;
DROP SEQUENCE IF EXISTS gigs_id_seq;

-- Then, we recreate them
CREATE SEQUENCE IF NOT EXISTS gigs_id_seq;
CREATE TABLE gigs (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP,
    band VARCHAR(255),
    venue VARCHAR(255),
    location VARCHAR(255),
    postcode VARCHAR(255)
);

INSERT INTO gigs (datetime, band, venue, location, postcode) VALUES ('2025-12-01 19:30', 'Placebo', 'Brixton Academy', 'London', 'SW9 9SL');
INSERT INTO gigs (datetime, band, venue, location, postcode) VALUES ('2025-12-08 19:30', 'Portishead', 'Brixton Academy', 'London', 'SW9 9SL');
INSERT INTO gigs (datetime, band, venue, location, postcode) VALUES ('2025-12-08 20:00', 'Placebo', 'The Roundhouse', 'London', 'NW1 8EH');
INSERT INTO gigs (datetime, band, venue, location, postcode) VALUES ('2025-12-15 20:30', 'Phantogram', 'Corn Exchange', 'Cambridge', 'CB2 3QB');
