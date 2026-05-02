-- Create dedicated databases for each service sharing this postgres instance.
SELECT 'CREATE DATABASE openwebui' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'openwebui')\gexec
SELECT 'CREATE DATABASE litellm'   WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'litellm')\gexec
