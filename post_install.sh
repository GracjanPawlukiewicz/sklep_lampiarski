#!/bin/bash
tar -xf /tmp/modules.tar.gz -C /var/www/html && rm /tmp/modules.tar.gz
tar -xf /tmp/img.tar.gz -C /var/www/html && rm /tmp/img.tar.gz
tar -xf /tmp/mails.tar.gz -C /var/www/html && rm /tmp/mails.tar.gz
tar -xf /tmp/localization.tar.gz -C /var/www/html && rm /tmp/localization.tar.gz
tar -xf /tmp/themes.tar.gz -C /var/www/html && rm /tmp/themes.tar.gz
chown -R www-data:www-data /var/www/html
