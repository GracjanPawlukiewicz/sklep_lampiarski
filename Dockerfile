FROM prestashop/prestashop:1.7.8.7-apache
COPY backup/*.tar.gz /tmp/
COPY post_install.sh /tmp/post-install-scripts/
COPY backup/apache-selfsigned.crt /etc/ssl/certs/
COPY backup/apache-selfsigned.key /etc/ssl/private/
COPY backup/default-ssl.conf /etc/apache2/sites-available/
RUN a2enmod ssl
RUN a2ensite default-ssl
RUN apt-get update && apt-get install -y memcached libmemcached-dev zlib1g-dev \
	&& pecl install memcached \
	&& docker-php-ext-enable memcached  