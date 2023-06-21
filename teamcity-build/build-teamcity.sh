#!/usr/bin/env bash
set -x

# clone django into the repo.
rm -rf _django_repo
git clone --depth 1 --single-branch --branch cockroach-4.2.x https://github.com/timgraham/django _django_repo

# install the django requirements.
cd _django_repo/tests/
pip install --user -e ..
pip install --user -r requirements/py3.txt
if [[ -z "${USE_PSYCOPG2}" ]]; then
    pip install --user -r requirements/postgres.txt
else
    pip install --user psycopg2
fi
cd ../..

# install the django-cockroachdb backend.
pip install --user .

cd _django_repo/tests/

# Bring in the settings needed to run the tests with cockroach.
cp ../../teamcity-build/cockroach_settings.py .
cp ../../teamcity-build/cockroach_gis_settings.py .

# Run the tests!
python3 ../../teamcity-build/runtests.py basic
