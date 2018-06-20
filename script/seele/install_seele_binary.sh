#!/bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

BINARY_NAME='node'

CUR_INSTALL_PATH=$(cd "$(dirname "$0")"; pwd)
rm -f ${CUR_INSTALL_PATH}/${BINARY_NAME} 2>/dev/null

./gen_binary.sh

fab install_from_binary

# rm -f ${CUR_INSTALL_PATH}/bin/${BINARY_NAME} 2>/dev/null

./send_config.sh