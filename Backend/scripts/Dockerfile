FROM postgres:18
COPY monebank.backup /docker-entrypoint-initdb.d/
COPY init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh
