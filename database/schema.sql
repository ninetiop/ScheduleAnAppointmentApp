CREATE TABLE clientapp."user"
(
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);

ALTER TABLE IF EXISTS clientapp."user"
    OWNER to admin;