FROM mysql:8.0

# The official MySQL image runs any .sql/.sh in this folder on first boot.
COPY init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 3306
# Data dir is /var/lib/mysql — back this with a PersistentVolume in Kubernetes.

