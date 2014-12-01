#! /bin/sh

### BEGIN INIT INFO
# Provides:          tina
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Tina orchestrator
# Description:       Virtual machine and physical resource management service
### END INIT INFO

# Author: Luiz Viana <lviana@include.io>
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
NAME=tinad
DESC="orchestration daemon"

DAEMON=tinad
DAEMON_BIN=/usr/bin/tinad
DAEMON_PIDFILE=/var/run/$DAEMON.pid
SCRIPTNAME=/etc/init.d/$NAME

# Exit if the package is not installed
[ -x "$DAEMON_BIN" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Define LSB log_* functions.
. /lib/lsb/init-functions

sendsigs_omit() {
    OMITDIR=/lib/init/rw/sendsigs.omit.d
    mkdir -p $OMITDIR
    rm -f $OMITDIR/rsyslog
    ln -s $DAEMON_PIDFILE $OMITDIR/rsyslog
}

case "$1" in
  start)
    log_daemon_msg "Starting $DESC" "$DAEMON"
    $DAEMON -a start
    case "$?" in
        0) sendsigs_omit
           log_end_msg 0 ;;
        1) log_progress_msg "already started"
           log_end_msg 0 ;;
        *) log_end_msg 1 ;;
    esac

    ;;
  stop)
    log_daemon_msg "Stopping $DESC" "$DAEMON"
    $DAEMON -a stop
    case "$?" in
        0) log_end_msg 0 ;;
        1) log_progress_msg "already stopped"
           log_end_msg 0 ;;
        *) log_end_msg 1 ;;
    esac

    ;;
  restart)
    $DAEMON -a stop
    $DAEMON -a start
    ;;
  force-reload)
    $DAEMON -a stop
    $DAEMON -a start
    ;;
  createdb)
    $DAEMON -a createdb
    case "$?" in
	0) log_end_msg 0 ;;
	1) log_progress_msg "could not deploy database"
	   log_end_msg 0 ;;
	*) log_end_msg 1 ;;
    esac

    ;;
  status)
    status_of_proc -p $DAEMON_PIDFILE $DAEMON_BIN $DAEMON && exit 0 || exit $?
    ;;
  *)
    echo "Usage: $SCRIPTNAME {start|stop|restart|status}" >&2
    exit 3
    ;;
esac

:
