CREATE TABLE USERS (
	name varchar(255) not null primary key,
	password varchar(255) not null
);

CREATE TABLE TASKS (
	id integer primary key autoincrement,
	title varchar(255) not null,
	content text not null,
	completed boolean not null,
	owner varchar(255) not null references users
);

