#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

CONFIG_FILE_NAME="config"

CUR_INSTALL_PATH=$(cd "$(dirname "$0")"; pwd)

rm -rf ${CUR_INSTALL_PATH}/${CONFIG_FILE_NAME} 2>/dev/null

cp -r ../../sources/go-seele-source/${CONFIG_FILE_NAME} .

fab stop_node

fab send_config_file
rm -rf ${CUR_INSTALL_PATH}/${CONFIG_FILE_NAME} 2>/dev/null

fab start_node