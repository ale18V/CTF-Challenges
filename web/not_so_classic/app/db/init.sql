CREATE TABLE IF NOT EXISTS USERS(
	id integer primary key,
	username varchar(255) not null unique,
	password varchar(255) not null
);

CREATE TABLE IF NOT EXISTS POSTS(
	id integer primary key,
	title varchar(255) not null,
	content text not null,
	creator_id integer not null references USERS,
	image_id blob not null,
	foreign key (creator_id, image_id) references UPLOADS
);

CREATE TABLE IF NOT EXISTS POST_SHARES(
	post_id integer not null references POSTS,
	user_id integer not null references USERS,
	primary key (post_id, user_id)
);

CREATE TABLE IF NOT EXISTS UPLOADS(
	id blob not null,
	uploader_id integer not null references USERS,
	primary key (id, uploader_id)
);

CREATE TRIGGER PRESERVE_ADMIN_POSTS
BEFORE DELETE ON POSTS
WHEN OLD.creator_id = (SELECT id FROM USERS WHERE username = 'admin')
BEGIN
	SELECT RAISE(ABORT, "Sorry the admin posts can't be deleted");
END;