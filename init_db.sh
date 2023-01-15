#!/bin/bash
echo "DROP DATABASE IF EXISTS prestashop; CREATE DATABASE prestashop;" | mysql -u root -pstudent -h 127.0.0.1 -P 3307
bunzip2 < backup/1671232069-61a49c55.sql.bz2 | mysql -u root -pstudent -h 127.0.0.1 -P 3307 -D prestashop
cat init_db.sql | mysql -u root -pstudent -h 127.0.0.1 -P 3307 -D prestashop
