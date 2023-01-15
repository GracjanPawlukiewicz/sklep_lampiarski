UPDATE ps_shop_url SET domain="localhost:8080",domain_ssl="localhost:8080",physical_uri="/";
UPDATE ps_configuration SET value=0 WHERE name="PS_SSL_ENABLED_EVERYWHERE";
UPDATE ps_configuration SET value=0 WHERE name="PS_SSL_ENABLED";
DELETE FROM ps_module WHERE id_module>64;