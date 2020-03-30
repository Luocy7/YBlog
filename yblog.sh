#!/bin/bash
# author: Luocy
# time: 2020/03/29
# copyright: © 2020 Luocy <luocy77@gmail.com>


env_args="-Xms128m -Xmx128m"

show_help(){
    echo -e "\r\n\tWeclome using yblog"
    echo -e "\r\nUsage: sh yblog.sh start|stop|reload|status|log"
    exit
}

if [ $# -eq 0 ]
 then
    show_help
else
    if [ "$2" != "" ]
    then
        env_args="$2"
    fi
    case "$1" in
        "start")
            supervisorctl start yblog
            ;;
        "stop")
            supervisorctl stop yblog
            ;;
        "restart")
	          supervisorctl restart yblog
            ;;
        "status")
            supervisorctl status yblog
            ;;
        "log")
            tail -f logs/yblog.log
            ;;
    esac
fi