#!/bin/bash
CONTAINER=sklep_lampiarski-Lumos-1
docker exec -w /var/www/html/ $CONTAINER tar -czf /tmp/img.tar.gz img
docker cp $CONTAINER:/tmp/img.tar.gz backup/img.tar.gz
docker exec -w /var/www/html/ $CONTAINER tar -czf /tmp/modules.tar.gz modules
docker cp $CONTAINER:/tmp/modules.tar.gz backup/modules.tar.gz
docker exec -w /var/www/html/ $CONTAINER tar -czf /tmp/mails.tar.gz mails
docker cp $CONTAINER:/tmp/mails.tar.gz backup/mails.tar.gz
docker exec -w /var/www/html/ $CONTAINER tar -czf /tmp/localization.tar.gz localization
docker cp $CONTAINER:/tmp/localization.tar.gz backup/localization.tar.gz
docker exec -w /var/www/html/ $CONTAINER tar -czf /tmp/themes.tar.gz themes
docker cp $CONTAINER:/tmp/themes.tar.gz backup/themes.tar.gz
docker exec $CONTAINER rm /tmp/*.tar.gz
