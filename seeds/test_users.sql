DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;

-- Then, we recreate them
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    hashed_password VARCHAR(255)
);

-- password for "username" is "password"
INSERT INTO users (username, hashed_password) VALUES ('username', 'scrypt:32768:8:1$GyJxMBmMStc53kgU$14c84080ba5cc61580ece80fb0df7859865f8b9e306d77d29f99f4b410fb845e27207bf2a466bb97c08d843b20be094cdfad1164e5b0a25136037627f63a87fd');
