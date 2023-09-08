#!/bin/bash

#
# Vector Demonstration necessary reqs
#

function install_linux() {
    sudo apt-get install $1
}
function install_darwin() {
    brew install $1
}

function install_package() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        install_linux $1
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        install_darwin $1
    elif [[ "$OSTYPE" == "win32" ]]; then
        echo "WIP"
    else
        echo "Unknown Operating System"
    fi
}

function install_gh() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # https://github.com/cli/cli/blob/trunk/docs/install_linux.md
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install gh
    elif [[ "$OSTYPE" == "win32" ]]; then
        echo "WIP"
    else
        echo "Unknown Operating System"
    fi
}

# heroku cli
which heroku
if ! [ "$?" ]; then
    curl https://cli-assets.heroku.com/install.sh | sh
fi

# github cli
which gh
if ! [ "$?" ]; then
    install_gh
fi
