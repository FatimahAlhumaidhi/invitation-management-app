#!/bin/sh
sudo -u postgres dropdb invitdb
sudo -u postgres createdb invitdb
sudo -u postgres psql invitdb < database.psql
