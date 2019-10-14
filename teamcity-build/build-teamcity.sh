#!/usr/bin/env bash
set -x

# install the cockroach-django driver.
pip3 install psycopg2-binary
pip3 install .

# clone django into the repo.
git clone --depth 1 --single-branch --branch stable/2.2.x https://github.com/django/django _django_repo

# install the django requirements.
cd _django_repo/tests/
pip3 install -e ..
pip3 install -r requirements/py3.txt
pip3 install -r requirements/postgres.txt

# download and start cockroach
wget "https://binaries.cockroachdb.com/cockroach-v19.2.0-beta.20190930.linux-amd64.tgz"
tar -xvf cockroach-v19.2*
cp cockroach-v19.2*/cockroach cockroach_exec
./cockroach_exec start --insecure &

# Bring in the settings needed to run the tests with cockroach.
cp ../../teamcity-build/cockroach_settings.py .

# Run the tests!
python3 ../../teamcity-build/runtests.py