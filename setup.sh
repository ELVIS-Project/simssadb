#!/bin/bash

# Install dependencies with homebrew
brew install python3
brew upgrade python3
brew install postgres
brew upgrade postgres
brew install elasticsearch@5.6

# Start postgresql and elasticsearch and keep them running
brew services start postgresql
brew services start elasticsearch@5.6

#Setup environment
cat env.txt >> ~/.bash_profile
source ~/.bash_profile

# Set up database
createdb ${POSTGRES_DB}
createuser ${POSTGRES_USER} -d -e -l -r -s
psql -d ${POSTGRES_DB} -c "ALTER DATABASE $POSTGRES_DB OWNER TO $POSTGRES_USER;"
psql ${POSTGRES_DB} -c "ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"

# Set up python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install python packages
pip install -r requirements.txt

# Make migrations and apply them
python manage.py makemigrations
python manage.py migrate

# Start server to see if it worked
python manage.py runserver
