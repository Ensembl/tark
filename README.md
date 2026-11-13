# Tark (Transcript Archive)

[![Dependency Compatibility Check](https://github.com/Ensembl/tark/actions/workflows/dep_check.yml/badge.svg)](https://github.com/Ensembl/tark/actions/workflows/dep_check.yml)
[![Documentation Status](https://readthedocs.org/projects/tark/badge/?version=latest)](http://tark.readthedocs.io/en/latest/?badge=latest) 
[![Coverage Status](https://coveralls.io/repos/github/Ensembl/tark/badge.svg?branch=master)](https://coveralls.io/github/Ensembl/tark)

Tark (Transcript Archive)

An archive of all transcripts and its sequences from Ensembl, RefSeq and other sources. Provides RESTful data access through endpoints and also provides tools to visualize the data and compare the transcripts.


# Requirements
- Python 3.12 (matching the Docker image and dependency checks)
- MySQL 5.6+


Installation
------------
Clone the project from git

```

git clone https://github.com/Ensembl/tark.git


```

Create the Python environment (using virtualenv or python3 -m venv or any environment tool)

```
python3 -m venv virtualenv
source ./virtualenv/bin/activate

cd tark
pip install -r requirements.txt 

```

The supplied `tark/tark/settings/secrets.py` reads database credentials from
environment variables. Export these in the same terminal used to start Django,
replacing the example values with your MySQL connection details:

```sh
export DATABASE_HOST='127.0.0.1'
export DATABASE_PORT='3306'
export DATABASE_NAME='your_tark_database'
export DATABASE_USER='your_mysql_user'
export DATABASE_PASSWORD='your_mysql_password'
export DEBUG='1'
export DJANGO_ALLOWED_HOSTS='localhost 127.0.0.1'
```

`DATABASE_NAME` selects the transcript archive database; Django also connects to
`tark_django_manager` on the same server using the same credentials. Both databases
must exist and be accessible to that user. Use your server's hostname and port if
MySQL is remote. An empty `DATABASE_HOST` uses the MySQL client's default local
connection. A `.env` file is not loaded automatically.

Alternatively, create `tark/tark/settings/secrets.py` from
`tark/tark/settings/secrets_template.py` and fill in its values directly. Keep
credentials out of version control.


Run the migrate step with --fake-initial (No need to run the migrations as the database is already there and it is not managed by Django)
```
cd tark/
./manage.py migrate --fake-initial
```

Start the development server

From the directory containing `manage.py`:
```
 ./manage.py runserver localhost:9000
```

Check in the browsesr
```
http://localhost:9000/
```

Run all the tests in the package:
```
./manage.py test --settings=tark.settings.test
```

### MySQL authentication errors on macOS

If startup reports that `mysql_native_password` cannot be loaded from a MySQL 9
directory, the Python driver is linked to a client library that does not provide
the authentication method requested by the server. Changing `PATH` alone does not
change an already compiled driver.

For this project's pinned `mysqlclient==2.2.8`, if Homebrew `mysql@8.0` and `pkg-config` are already
installed on Apple Silicon, rebuild the driver from the repository root:

```sh
PKG_CONFIG_PATH="/opt/homebrew/opt/mysql@8.0/lib/pkgconfig" ARCHFLAGS='-arch arm64' \
  appenv/bin/python -m pip install --force-reinstall --no-deps \
  --no-binary=mysqlclient --no-cache-dir mysqlclient==2.2.8
appenv/bin/python -c 'import MySQLdb; print(MySQLdb.get_client_info())'
```

The last command should report `8.0.x`. Restart Django after rebuilding.

### Using Docker

From the repository root, use `compose.yaml` to build and run the application
with the database variables exported in your current shell:

```sh
docker compose up --build -d
docker compose logs -f web
```

Open <http://localhost:8000/>. Set `APP_PORT` before starting Compose to use a
different local port. Docker must be running.

API documentation is available at `/api/`, with the OpenAPI schema at
`/api/schema/`. It uses drf-spectacular; the legacy django-rest-swagger integration
is incompatible with the current Django REST Framework version. Existing custom
filter descriptions are included through an OpenAPI extension.

Compose requires `DATABASE_HOST`, `DATABASE_NAME`, `DATABASE_USER`, and
`DATABASE_PASSWORD`; the password may be explicitly exported as an empty string.
`DATABASE_PORT` defaults to `3306`. It also passes through `SECRET_KEY`, `DEBUG`,
`DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and `DJANGO_ENVIRONMENT`, with
local development defaults defined in `compose.yaml`. Export a `SECRET_KEY` for
any shared deployment.
Shell values take precedence over any Compose `.env` file.

Shared deployments set `DJANGO_CSRF_TRUSTED_ORIGINS` to a space-separated list of
public origins, including the scheme (for example, `https://dev-tark.ensembl.org`
for staging and `https://tark.ensembl.org` for production). The Kubernetes overlays
set these values per environment. This is separate from `DJANGO_ALLOWED_HOSTS`,
which contains hostnames without a scheme. Local same-origin HTTP requests do
not require trusted origins. When using a reverse proxy, it must preserve the
public host and correctly set `X-Forwarded-Proto` for Django's existing
`SECURE_PROXY_SSL_HEADER` setting. After changing a Kubernetes ConfigMap, restart
the deployment so its processes load the updated environment.

This connects to your existing MySQL server. For MySQL running on your Mac, use
`export DATABASE_HOST='host.docker.internal'`; `localhost` and `127.0.0.1` inside
the container refer to the container itself. For a remote database, keep its
reachable hostname and port. Both the archive database and `tark_django_manager`
must be accessible using the exported credentials.

After changing exported variables, run `docker compose up -d` again to recreate
the container with the updated environment. To stop and remove it:

```sh
docker compose down
```
