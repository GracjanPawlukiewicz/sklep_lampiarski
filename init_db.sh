#!/bin/bash
# Usage: ./init_db [full|createonly]
MODE="full"
if [ "$#" -eq 1 ]; then
    MODE=$1
fi

DB_CONT="mysql"
DB_GLOB_USER="root"
DB_GLOB_PWD="student"
DB_NAME_USER="Lumos"
DB_PWD="lampexpol"
BACKUP_FILE="backup/1671232069-61a49c55.sql.bz2"
DOMAIN="localhost:8080" # Unused
DOMAIN_SSL="localhost:10001"

echo "DROP DATABASE IF EXISTS ${DB_NAME_USER};
CREATE DATABASE ${DB_NAME_USER};
CREATE USER IF NOT EXISTS '${DB_NAME_USER}'@'%' IDENTIFIED BY '${DB_PWD}';
GRANT ALL PRIVILEGES ON ${DB_NAME_USER}.* TO '${DB_NAME_USER}'@'%';" | docker exec -i $DB_CONT mysql -u $DB_GLOB_USER -p$DB_GLOB_PWD

if [ "$MODE" = "createonly" ]; then
    echo "Skipping backup restoration"
    exit 0
fi

bunzip2 < $BACKUP_FILE | docker exec -i $DB_CONT mysql -u $DB_NAME_USER -p$DB_PWD -D $DB_NAME_USER

echo "UPDATE ps_shop_url SET domain='${DOMAIN}',domain_ssl='${DOMAIN_SSL}',physical_uri='/';" | docker exec -i $DB_CONT mysql -u $DB_NAME_USER -p$DB_PWD -D $DB_NAME_USER
