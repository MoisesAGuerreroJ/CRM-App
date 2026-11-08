# CRM Application

A lightweight, self-hosted customer and contact management application built with Flask, MySQL, HTML, CSS, and JavaScript.

## Requirements

- Docker Engine
- Docker Compose plugin

## Local setup

1. Clone the repository.
2. Create your local environment file and set unique passwords:

   ```bash
   cp .env.example .env
   ```

3. Create your private application configuration:

   ```bash
   cp config/local.example.json config/local.json
   ```

   Edit `config/local.json` to define the labels and options used by your local forms. This file is intentionally excluded from Git.

4. Start the application:

   ```bash
   docker compose up -d
   ```

5. Open <http://localhost:8080>.

The web interface and API are bound to the local machine. MySQL is not published on a host port and persists data in the `mysql_data` Docker volume.

## Configuration

- `.env`: database credentials and runtime settings. Never commit this file.
- `config/local.json`: private presentation labels and form options. Never commit this file.
- `.env.example` and `config/local.example.json`: safe templates without real credentials or business-specific values.

## Stop the application

```bash
docker compose down
```

This preserves the database volume. To remove the database permanently, use `docker compose down -v` only after making and verifying a backup.

## Security note

Credentials previously committed to a public repository should be considered compromised and rotated. Removing them from the current source does not erase them from Git history.
