echo "$(cat db/init.sql)
DELETE FROM USERS WHERE username = 'admin';
INSERT INTO USERS VALUES('admin', '${ADMIN_PASSWORD}');" | sqlite3 db/app.db
mkfifo "${FIFO_PATH}"
./run/run &
export DAEMON_PID=$!;
gunicorn --workers 2 --worker-class gevent --log-level debug --worker-connections 128 --bind "0.0.0.0:${CHALLENGE_PORT}" --reload 'src.app:app' 
