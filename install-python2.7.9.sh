#!/bin/sh
apt-get update && apt-get -y install libssl-dev

wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar xfz Python-2.7.9.tgz

cd Python-2.7.9/
./configure --prefix /usr/local/lib/python2.7.9 --enable-ipv6 --with-ensurepip=install
make
make install

ln -s /usr/local/lib/python2.7.9/bin/python /usr/bin/python2.7.9
ln -s /usr/local/lib/python2.7.9/bin/pip /usr/bin/pip2.7.9