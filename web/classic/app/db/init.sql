CREATE TABLE IF NOT EXISTS USERS(
	username varchar(255) not null primary key,
	password varchar(255) not null
);

CREATE TABLE IF NOT EXISTS POSTS(
	id integer primary key,
	creator varchar(255) not null references USERS,
	title varchar(255) not null,
	content text not null
);