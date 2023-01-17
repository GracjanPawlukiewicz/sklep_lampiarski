#!/bin/bash
# Usage: ./init_db [full|createonly]
MODE="full"
if [ "$#" -eq 1 ]; then
    MODE=$1
fi

DB_CONT="actina15.maas"
DB_GLOB_USER="root"
DB_GLOB_PWD="student"
DB_NAME_USER="BE_171547"
DB_PWD="lampexpol"
BACKUP_FILE="backup/1673996584-214241ee.sql.gz"
DOMAIN="localhost:17154" # Review change for deployment

echo "DROP DATABASE IF EXISTS ${DB_NAME_USER};
CREATE DATABASE ${DB_NAME_USER};
CREATE USER IF NOT EXISTS '${DB_NAME_USER}'@'%' IDENTIFIED BY '${DB_PWD}';
GRANT ALL PRIVILEGES ON ${DB_NAME_USER}.* TO '${DB_NAME_USER}'@'%';" | docker exec -i $DB_CONT mysql -u $DB_GLOB_USER -p$DB_GLOB_PWD

if [ "$MODE" = "createonly" ]; then
    echo "Skipping backup restoration"
    exit 0
fi

zcat $BACKUP_FILE | docker exec -i $DB_CONT mysql -u $DB_NAME_USER -p$DB_PWD -D $DB_NAME_USER

echo "UPDATE ps_shop_url SET domain='${DOMAIN}',domain_ssl='${DOMAIN}',physical_uri='/';" | docker exec -i $DB_CONT mysql -u $DB_NAME_USER -p$DB_PWD -D $DB_NAME_USER
