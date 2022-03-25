# Tark (Transcript Archive)

[![Dependency Compatibility Check](https://github.com/Ensembl/tark/actions/workflows/dep_check.yml/badge.svg)](https://github.com/Ensembl/tark/actions/workflows/dep_check.yml)
[![Documentation Status](https://readthedocs.org/projects/tark/badge/?version=latest)](http://tark.readthedocs.io/en/latest/?badge=latest) 
[![Build Status](https://travis-ci.org/Ensembl/tark.svg?branch=master)](https://travis-ci.org/Ensembl/tark) 
[![Coverage Status](https://coveralls.io/repos/github/Ensembl/tark/badge.svg?branch=master)](https://coveralls.io/github/Ensembl/tark)

Tark (Transcript Archive)

An archive of all transcripts and its sequences from Ensembl, RefSeq and other sources. Provides RESTful data access through endpoints and also provides tools to visualize the data and compare the transcripts.


# Requirements
- pyenv and pyenv-virtualenv or virtualenvwrapper
- Python 3.6+
- MySQL 5.6+


Installation
------------
Clone the project from git

```

git clone https://github.com/Ensembl/tark.git


```

Create the Python environment (using virtualenv or python3 -m venv or any environment tool)

```
mkvirtualenv tarkenv 
workon tarkenv

cd tark
pip install -r requirements.txt 

```

Provide the right credentials to connect to the tark database in secrets.py (created from secrets_template.py)

```
cd tark/tark/tark/settings
cp secrets_template.py secrets.py

```

Provide the right credentials to connect to the django manager database in base.py
Note: All the django's management table while running the migration step will be created in tark_django_manager
```
cd tark/tark/tark/settings

Look in the following section of base.py
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tark_django_manager',
            'USER': 'xxxx',
            'PASSWORD': 'xxxx',
            'HOST': 'localhost',
            'PORT': '3306',

```


Update the log file location in `local.py` (point this to somewhere writable location)
```
LOG_FILE = os.path.join(BASE_DIR, '../../logs/tark.log')
```


Run the migrate step with --fake-initial (No need to run the migrations as the database is already there and it is not managed by Django)
```
./manage.py migrate --fake-initial
```

Start the development server
cd tark/tark
```
 ./manage.py runserver 0:9000
```

Check in the browsesr
```
http://localhost:9000/
```

