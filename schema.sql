CREATE TABLE paloozies (
    id uuid PRIMARY KEY DEFAULT uuid_in(md5(now()::text)::cstring),
    name text,
    description text,
    born timestamp DEFAULT CURRENT_TIMESTAMP,
    startdate timestamp,
    location_name text,
    location_street text,
    location_zip varchar(5),
    location_state varchar(2),
    location_city text
);

CREATE TYPE rsvp AS ENUM ('going', 'notgoing', 'noresponse');

CREATE TABLE invitations (
    pid uuid REFERENCES paloozies(id) ON DELETE CASCADE,
    invitationurl uuid PRIMARY KEY DEFAULT uuid_in(md5(now()::text)::cstring),
    ishost boolean DEFAULT FALSE,
    useremail text,
    rsvp rsvp DEFAULT 'noresponse'
);

CREATE TABLE items (
    itemid serial PRIMARY KEY,
    pid uuid REFERENCES paloozies(id) ON DELETE CASCADE,
    name text,
    description text,
    quantity int
);

CREATE TABLE paloozie_urls (
    pid varchar(36),
    url uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    isadmin boolean DEFAULT FALSE
);

-- A "insert paloozie" and "add paloozie urls" transaction
BEGIN;
    WITH paloozie_insert AS (
        INSERT INTO paloozies ( name ) VALUES ( 'foo' ) RETURNING id
    ),
    paloozie_url AS (
        INSERT INTO paloozie_urls ( pid ) VALUES ( (SELECT id FROM paloozie_insert) ) RETURNING pid
    )
    INSERT INTO paloozie_urls ( pid, isadmin ) VALUES ( (SELECT pid FROM paloozie_url), TRUE ) RETURNING pid;
COMMIT;