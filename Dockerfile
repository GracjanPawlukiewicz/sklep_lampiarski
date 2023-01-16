FROM prestashop/prestashop:1.7.8.7-apache
COPY backup/*.tar.gz /tmp/
COPY post_install.sh /tmp/post-install-scripts/
