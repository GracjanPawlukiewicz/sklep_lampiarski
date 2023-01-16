FROM prestashop/prestashop:1.7.8.7-apache
COPY backup/modules.tar.gz /tmp/
COPY backup/img.tar.gz /tmp/

# Create /tmp/post-install-scripts/extract_backup.sh
RUN mkdir -p /tmp/post-install-scripts
RUN echo "tar -xf /tmp/modules.tar.gz -C /var/www/html && rm /tmp/modules.tar.gz" > /tmp/post-install-scripts/extract_backup.sh
RUN echo "tar -xf /tmp/img.tar.gz -C /var/www/html && rm /tmp/img.tar.gz" >> /tmp/post-install-scripts/extract_backup.sh
RUN chmod +x /tmp/post-install-scripts/extract_backup.sh
