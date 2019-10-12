# MustafaBois

To run the program for the first time, do the following:

```Bash
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

Whenever a new requirement is added into your virtual environment, always ensure you do the following before committing and pushing:

```Bash
pip3 freeze > requirements.txt

<...commit and push...>
```

To run the server, type and execute the following commands from the root folder:

```Bash
python3 project/manage.py runserver
```

To load all dummy data, run the following python commands:

First ensure all models reflect in the DB:

```Bash
python3 project/manage.py migrate
```

Then,

```Bash
cd project/
python3 manage.py loaddata fixtures_user fixtures_game fixtures_gamecreator fixtures_gameplayer fixtures_location fixtures_locationuser
```
