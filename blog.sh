#!/bin/bash
# author: Luocy
# time: 2020/03/29
# copyright: © 2020 Luocy <luocy77@gmail.com>

env_args="-Xms128m -Xmx128m"

show_help() {
  echo -e "\r\n\tWeclome using yblog"
  echo -e "\r\nUsage: sh blog.sh init|start|stop|restart|status|log|access|error"
  exit
}

if [ $# -eq 0 ]; then
  show_help
else
  if [ "$2" != "" ]; then
    env_args="$2"
  fi
  case "$1" in
  "init")
    celery -A wsgi:celery worker -l info
    ;;
  "start")
    sudo supervisorctl start yblog
    ;;
  "stop")
    sudo supervisorctl stop yblog
    ;;
  "restart")
    sudo supervisorctl restart yblog
    ;;
  "status")
    sudo supervisorctl status yblog
    ;;
  "log")
    tail -f /data/www/YBlog/logs/yblog.log
    ;;
  "access")
    tail -f /data/www/YBlog/logs/yblog_access.log
    ;;
  "error")
    tail -f /data/www/YBlog/logs/yblog_error.log
    ;;
  esac
fi
