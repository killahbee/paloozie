CREATE TABLE paloozies (
    pid serial PRIMARY KEY,
    name varchar(100),
    description varchar(160),
    born timestamp DEFAULT CURRENT_TIMESTAMP,
    startdate timestamp,
    location_name varchar(64),
    location_street varchar(100),
    location_zip char(5),
    location_state char(2),
    location_city varchar(64)
);

CREATE TYPE rsvp AS ENUM ('going', 'notgoing', 'noresponse');

CREATE TABLE invitations (
    pid int REFERENCES paloozies(pid) ON DELETE CASCADE,
    invitationurl char(42) NOT NULL PRIMARY KEY,
    ishost boolean DEFAULT FALSE,
    useremail varchar(80),
    rsvp rsvp DEFAULT 'noresponse'
);

CREATE TABLE items (
    itemid serial PRIMARY KEY,
    pid int REFERENCES paloozies(pid) ON DELETE CASCADE,
    name varchar(100),
    description text,
    quantity int
);

CREATE TABLE paloozie_urls (
    pid int REFERENCES paloozies(pid) ON DELETE CASCADE,
    url char(36) UNIQUE NOT NULL,
    isadmin boolean DEFAULT FALSE
);

INSERT INTO paloozies (name, description, location_name) VALUES ('Mexican Fiesta', 'Im hosting a potluck to celebrate to Cinco De Mayo!', 'Casa Blanca');

INSERT INTO paloozie_urls (pid, url, isadmin) VALUES ('1', '147999d4e28-76p5eba1r3nbwmtcpz63a4n16ytj9q', FALSE);
INSERT INTO paloozie_urls (pid, url, isadmin) VALUES ('1', '147999d9090-hro2bq8iywndvcx3oegv3er7or2489', TRUE);