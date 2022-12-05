# Tark (Transcript Archive)

[![Dependency Compatibility Check](https://github.com/Ensembl/tark/actions/workflows/dep_check.yml/badge.svg)](https://github.com/Ensembl/tark/actions/workflows/dep_check.yml)
[![Documentation Status](https://readthedocs.org/projects/tark/badge/?version=latest)](http://tark.readthedocs.io/en/latest/?badge=latest) 
[![Coverage Status](https://coveralls.io/repos/github/Ensembl/tark/badge.svg?branch=master)](https://coveralls.io/github/Ensembl/tark)

Tark (Transcript Archive)

An archive of all transcripts and its sequences from Ensembl, RefSeq and other sources. Provides RESTful data access through endpoints and also provides tools to visualize the data and compare the transcripts.


# Requirements
- Python 3.6
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

Provide the right credentials to connect to the tark database in secrets.py (created from secrets_template.py)

```
cp tark/tark/settings/secrets_template.py tark/tark/settings/secrest.py
```


Run the migrate step with --fake-initial (No need to run the migrations as the database is already there and it is not managed by Django)
```
cd tark/
./manage.py migrate --fake-initial
```

Start the development server
cd tark/tark
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

