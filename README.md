# simssadb
Please use `pip freeze > requirements.txt` before you merge with develop branch!
When you pull from development branch, please run `pip install -r requirements.txt` first to make sure your virtual environment is up-to-date (otherwise it will throw a bunch of `Module not found` error, and you have to debug them yourselves).

For automatic translation: you need three steps to make the automatic translation work (take French as an example):
- Run `python manage.py makemessages -l fr` to inform Django to record all places that need translation into French
- Run `python manage.py translate_messages -l fr` to use automatic translation from Google to translate
- Run `python manage.py compilemessages -l fr` to apply translations to the final web pages
- Finally, run the server