#!/bin/bash

set -e

DB_NAME="commit_analytics"
DB_USER="postgres"
DB_PASSWORD="0000"
DB_HOST="localhost"
DB_PORT="5432"

echo "Creating user (if not exists)..."
psql -h "$DB_HOST" -p "$DB_PORT" -U postgres  <<EOF
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
        CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASSWORD';
    END IF;
END\$\$;
EOF

echo "Creating database (if not exists)..."
psql -h "$DB_HOST" -p "$DB_PORT" -U postgres <<EOF
SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec
EOF

echo "Applying schema..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f CORE_INIT.sql

echo "Done."
