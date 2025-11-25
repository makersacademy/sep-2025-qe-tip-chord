#!/bin/bash
set -e

# Modify pg_hba.conf
cat > "$PGDATA/pg_hba.conf" << EOF
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
host    all             all             0.0.0.0/0               trust
EOF

# Set proper permissions
chown postgres:postgres "$PGDATA/pg_hba.conf"
chmod 600 "$PGDATA/pg_hba.conf"

# Create the runner role and grant necessary permissions
psql -U postgres -d postgres -c "CREATE ROLE runner WITH LOGIN SUPERUSER PASSWORD 'runner';"
