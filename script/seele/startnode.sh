#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

host=
password=
seele=false
index=

while getopts "h:p:i:s" arg
do
    case $arg in
        h)
            host=$OPTARG
            #echo "h's arg:$OPTARG"
        ;;
        p)
            password=$OPTARG
            #echo "p's arg:$OPTARG"
        ;;
        i)
            index=$OPTARG
        ;;

        s)
            seele=true
        ;;

        ?) 
            echo "Usage: startnode -h user@host -p password -i index [-s]"
            exit 1
        ;;
    esac
done

hostandport=${host}":22"

# start go-seele
if [ $seele != false ]; then
    if [[ $index == *[!0-9]* ]]; then
        echo -e  "[INFO]==========start seele[$hostandport]...=========="
        fab set_node:$hostandport,password=$password start_node
    else
        echo -e  "[INFO]==========start seele[$hostandport]...=========="
        fab set_node:$hostandport,password=$password start_node:$index
    fi
fi