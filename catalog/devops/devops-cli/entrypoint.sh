#!/bin/bash

my_script_file_path=$0

echo "Starting up ..."

function show_help(){

  echo $0
  local arg_pattern=$(cat "${my_script_file_path}" | egrep -i '(if \[\[ .\$arg)')
  echo -e "${arg_pattern}" | while read arg;do
    local pattern=$(cut -d@ -f1 <<< ${arg##*=~})
    local help_txt=$(cut -d@ -f2 <<< ${arg##*=~})
    echo " $pattern ${help_txt//]/}"
  done
}

if [[ "$*" =~ .*--help.* ]];then 
  show_help
  exit 0
fi

PREFIX=eval

for arg in "${@}";do
    shift
  if [[ "$arg" =~ ^--no-run-ssh$|^-no-ssh$|'@Do start SSH service - optional' ]]; then NO_RUN_SSH=true;continue;fi
  if [[ "$arg" =~ ^--dry$|'@Dry run, only echo commands' ]]; then PREFIX=echo;continue;fi
  set -- "$@" "$arg"
done

if [[ -z $NO_RUN_SSH ]];then
  echo "Exposing docker socket via ${DOCKER_HOST_PORT}"
  screen -dm sudo bash -c "(echo 'Exposing docker socket via socat ...';socat -d -d TCP-L:${DOCKER_HOST_PORT},fork UNIX:/var/run/docker.sock)"
  echo "Starting SSH Service ..."
  sudo /usr/sbin/sshd -D -o ListenAddress=0.0.0.0
  echo "Shutting down ..."
fi
