CREATE DATABASE IF NOT EXISTS challenge;
USE challenge;

CREATE TABLE USERS(
    name varchar(255) not null primary key,
    password varchar(255) not null
);

CREATE TABLE FLAG(
    flag varchar(255) not null primary key
);

INSERT INTO USERS
    VALUES ('admin', 'admin');

INSERT INTO FLAG
    VALUES('flag{W4tch_y0ur_comm3nts!}');