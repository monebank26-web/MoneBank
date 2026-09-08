#!/bin/bash
set -e

pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner \
  /docker-entrypoint-initdb.d/monebank.backup