# simssadb

## Instalation and Setup for Development (Mac)

* Make sure you have homebrew and python 3.6 or above installed
* Install PostgreSQL with ``brew install postgresql``
* Start the PostgreSQL server with ``brew services start postgresql``
* Install Elastic Search with ``brew install elasticsearch@5.6``
* Start Elastic Search with ``brew services start elasticsearch@5.6``
* Set up environment variables with: ``cat env.txt >> ~/.bash_profile`` and ``source ~/.bash_profile``
* Start a virtual enviroment with ``python3 -m venv venv``
* Start virtual environment ``source venv/bin/activate``
* Install python packages ``pip install -r requirements.txt``
* Setup database:
  ```bash
  > createdb ${POSTGRES_DB}
  > createuser ${POSTGRES_USER} -d -e -l -r -s
  > psql -d ${POSTGRES_DB} -c "ALTER DATABASE $POSTGRES_DB OWNER TO $POSTGRES_USER;"
  > psql ${POSTGRES_DB} -c "ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
  ```
 * Make migrations: ``python manage.py makemigrations``
 * Migrate: ``python manage.py migrate``
 * Start a server to see if it worked: ``python manage.py runserver``
 * Go to ``http://127.0.0.1:8000`` on your web browser

Developer documentation: https://elvis-project.github.io/simssadb/html/index.html
