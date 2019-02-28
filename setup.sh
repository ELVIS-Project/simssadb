#!/bin/bash

# Django app (simmsadb) variables
# The app is reading those with os.getenv()

# Django settings
export SIMSSADB_HOSTS=['*']
export SIMSSADB_DEBUG=True
export SIMSSADB_SECRET_KEY="f1(1=m5ze=@ne023nnabwz(%x^j+8!y+py&n#lwvo0&(#c"

# postgres settings
export POSTGRES_DB=simssadb
export SIMSSADB_DB_HOST=localhost
export SIMSSADB_DB_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=debug

# email settings
export SIMSSADB_EMAIL_HOST=smtp.gmail.com
export SIMSSADB_EMAIL_HOST_USER=@gmail.com
export SIMSSADB_EMAIL_HOST_PASSWORD=PASSWORD
export SIMSSADB_EMAIL_PORT=587

# haystack settings
export SIMSSADB_HAYSTACK_URL=http://elasticsearch:9200/

# Install dependencies with homebrew
brew install python3
brew upgrade python3
brew install postgres
brew upgrade postgres
brew install elasticsearch@5.6

# Start postgresql and elasticsearch and keep them running
brew services start postgresql
brew services start elasticsearch@5.6

# Set up database
createdb $POSTGRES_DB
createuser $POSTGRES_USER -d -e -l -r -s
psql -d $POSTGRES_DB -c "ALTER DATABASE $POSTGRES_DB OWNER TO $POSTGRES_USER;"
psql $POSTGRES_DB -c "ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"

# Set up python virtual environment
python3 -m venv venv
. venv/bin/activate

# Install python packages
pip install -r requirements.txt

# Make migrations and apply them
python manage.py makemigrations
python manage.py migrate

# Start server to see if it worked
python manage.py runserver