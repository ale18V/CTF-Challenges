sqlite3 db/app.db < db/init.sql
mkfifo "${APP_FIFO_PATH}"
./run/run &
export DAEMON_PID=$!;
echo "Port: ${APP_SERVER_PORT}"
mkdir logs
touch logs/app.log
gunicorn --workers 2 --worker-class gevent --log-level debug --worker-connections 128 --bind "0.0.0.0:${APP_SERVER_PORT}" --reload 'src:create_app()' 
