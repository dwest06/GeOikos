#!/bin/bash

# variables de Conf de la Base de Datos
dbname=oikosdb
dbusername=oikos


sudo -u postgres dropdb $dbname >> /dev/null
sudo -u postgres dropuser $dbusername >> /dev/null
sudo -u postgres createuser $dbusername
sudo -u postgres createdb $dbname
sudo -u postgres psql << EOF
alter user $dbusername with password 'oikos123456';
alter role $dbusername set client_encoding to 'utf8';
alter role $dbusername set default_transaction_isolation to 'read committed';
alter role $dbusername set timezone to 'utc';
grant all privileges on database $dbname to $dbusername ;\q
EOF
