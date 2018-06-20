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
            echo "Usage: stopnode -h user@host -p password -i index [-s]"
            exit 1
        ;;
    esac
done

hostandport=${host}":22"

# stop seele 
if [ $seele != false ]; then
    if [[ $index == *[!0-9]* ]]; then
        echo -e  "[INFO]==========stop seele[$hostandport]...=========="
        fab set_node:$hostandport,password=$password stop_node
    else
        echo -e  "[INFO]==========stop seele[$hostandport]...=========="
        fab set_node:$hostandport,password=$password stop_node:$index
    fi
fi