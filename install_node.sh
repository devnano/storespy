#!/bin/sh
# TODO: this assumes a debian box

curl -sL https://deb.nodesource.com/setup_9.x | bash -

apt-get install nodejs -y 

curl -k -O -L https://www.npmjs.org/install.sh | sh
