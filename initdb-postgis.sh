#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
#export PGUSER="$POSTGRES_USER"

#psql -U postgres  -h "postgres_GHG" -c "CREATE ROLE ghg WITH LOGIN PASSWORD 'GHG';"

# create databases
psql -U postgres  -h "postgres_GHG" -c "CREATE DATABASE ghgdb;"

psql -U postgres  -h "postgres_GHG" -c "ALTER USER postgres PASSWORD 'GHG';"

# add extensions to databases
psql -U postgres  -h "postgres_GHG" gis -c "CREATE EXTENSION IF NOT EXISTS postgis;"
