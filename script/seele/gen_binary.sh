#!/bin/sh

set -e

BINARY_NAME='node'

CUR_PATH=$(cd "$(dirname "$0")"; pwd)

if [ ! -f "$CUR_PATH/gen_binary.sh" ]; then
    echo "$0 must be run from the root of the repository."
    exit 2
fi

# Create fake Go workspace if it doesn't exist yet.
workspace="$PWD/build/_workspace"
root="$PWD"
seeledir="$workspace/src/github.com/seeleteam"
if [ ! -L "$seeledir/go-seele" ]; then
    mkdir -p "$seeledir"
    cd "$seeledir"
    echo $PWD
    ln -s "$GOPATH/src/github.com/seeleteam/go-seele" go-seele
    cd "$root"
fi

# Set up the environment to use the workspace.
GOPATH="$workspace"
export GOPATH

# Run the command inside the workspace.
cd "$seeledir/go-seele"
PWD="$seeledir/go-seele"

echo $PWD

SOURCES_ADDRESS_SHORT='github.com/seeleteam/go-seele'
# git fetch --all
repo_name=`git remote -vv|grep "${SOURCES_ADDRESS_SHORT}.*fetch"|awk {'print $1'}`

git fetch -v ${repo_name} master
git reset --hard ${repo_name}/master

make ${BINARY_NAME}

cp build/${BINARY_NAME} ${CUR_PATH}/bin
# Launch the arguments with the configured environment.
exec "$@"
