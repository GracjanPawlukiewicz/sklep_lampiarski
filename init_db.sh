#!/bin/bash
# Usage: ./init_db [full|createonly]
MODE="full"
if [ "$#" -eq 1 ]; then
    MODE=$1
fi

DB_HOST="127.0.0.1"
DB_PORT="3307"
DB_GLOB_USER="root"
DB_GLOB_PWD="student"
DB_NAME_USER="Lumos"
DB_PWD="lampexpol"
BACKUP_FILE="backup/1671232069-61a49c55.sql.bz2"
DOMAIN="localhost:8080"
DOMAIN_SSL="localhost:10001"

echo "DROP DATABASE IF EXISTS ${DB_NAME_USER};
CREATE DATABASE ${DB_NAME_USER};
CREATE USER IF NOT EXISTS '${DB_NAME_USER}'@'%' IDENTIFIED BY '${DB_PWD}';
GRANT ALL PRIVILEGES ON ${DB_NAME_USER}.* TO '${DB_NAME_USER}'@'%';" | mysql -u $DB_GLOB_USER -p$DB_GLOB_PWD -h $DB_HOST -P $DB_PORT

if [ "$MODE" = "createonly" ]; then
    echo "Skipping backup restoration"
    exit 0
fi

bunzip2 < $BACKUP_FILE | mysql -u $DB_NAME_USER -p$DB_PWD -h $DB_HOST -P $DB_PORT -D $DB_NAME_USER

echo "UPDATE ps_shop_url SET domain='${DOMAIN}',domain_ssl='${DOMAIN_SSL}',physical_uri='/';
UPDATE ps_configuration SET value=0 WHERE name='PS_SSL_ENABLED_EVERYWHERE';
UPDATE ps_configuration SET value=0 WHERE name='PS_SSL_ENABLED';" | mysql -u $DB_NAME_USER -p$DB_PWD -h $DB_HOST -P $DB_PORT -D $DB_NAME_USER
