psql << EOF
    CREATE USER "subscriber" WITH PASSWORD 'subscriber';
    ALTER ROLE "subscriber" SUPERUSER;
    CREATE DATABASE "subscriber-db";
    GRANT ALL PRIVILEGES ON DATABASE "subscriber-db" to "subscriber";
EOF
