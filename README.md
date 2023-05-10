# simssadb

Since this repository has submodule, when you clone it, please use `git clone --recursive git@github.com:ELVIS-Project/simssadb.git`, so that the submodule can also be cloned.

## Installation and Setup for Development (Mac)

* Make sure you have ``homebrew`` and python 3.6 or above installed
* Install PostgreSQL with ``brew install postgresql``
* Start the PostgreSQL server with ``brew services start postgresql``
* Set up environment variables with: ``cat env.txt >> ~/.bash_profile`` and ``source ~/.bash_profile`` (NOTE: If you use PyCharm or other IDE, please restart the IDE for the environmental settings to work!)
* Start a virtual environment with ``python3 -m venv venv``
* Start virtual environment ``source venv/bin/activate``
* Install python packages ``pip install -r requirements.txt``
* Setup database:

  ```bash
  > createdb `whoami`
  > createdb ${POSTGRES_DB}
  > createuser ${POSTGRES_USER} -d -e -l -r -s
  > psql -d ${POSTGRES_DB} -c "ALTER DATABASE $POSTGRES_DB OWNER TO $POSTGRES_USER;"
  > psql ${POSTGRES_DB} -c "ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
  ```
  * If an error occurs, reassign ``source ~/.bash_profile`` before setting up the database
* Make migrations: ``python manage.py makemigrations``
* Migrate: ``python manage.py migrate``
* Start a server to see if it worked: ``python manage.py runserver``
* Go to ``http://127.0.0.1:8000`` on your web browser

[Developer documentation](https://elvis-project.github.io/simssadb/html/index.html)
