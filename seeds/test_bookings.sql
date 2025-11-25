DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;

-- Then, we recreate them
CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP, -- of the booking
    gig_id INTEGER,
    user_id INTEGER,
    ticket_count INTEGER,
    constraint fk_gig foreign key(gig_id)
      references gigs(id),
    constraint fk_user foreign key(user_id)
      references users(id)
);

INSERT INTO bookings (datetime, gig_id, user_id, ticket_count) VALUES ('2025-11-22 15:43', 1, 1, 1);
INSERT INTO bookings (datetime, gig_id, user_id, ticket_count) VALUES ('2025-11-22 15:43', 4, 1, 4);
