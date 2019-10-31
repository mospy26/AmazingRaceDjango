# Amazing Race - An amazing race game facilitator built in Django

## Getting it set up for the first time
1. `git clone https://github.sydney.edu.au/Internet-Software-Platform-2019/MustafaBois.git`
1. `cd MustafaBois`
1. `python3 -m venv venv`
1. `source ./venv/bin/activate`
1. `pip3 install -r requirements.txt`
1. `cd project/`
1. `python3 manage.py makemigrations AmazingRaceApp`
1. `python3 manage.py migrate`
1. `python3 manage.py createsuperuser`
1. Enter Username and Password
1. `python3 manage.py loadjson`
1. `python3 manage.py runserver`
1. Open your preffered browser
1. Navigate to `http://127.0.0.1:8000/`
1. Have fun!

## Schema/Database model changes
1. Make any changes to your models as and when needed/required
1. Perform a migration `python3 manage.py makemigrations AmazingRaceApp`, then `python3 manage.py migrate`

## Adding new model
1. Navigate to `MustafaBois/project/AmazingRaceApp/models.py` with `cd`
1. Create new model in that python file
1. Navigate to `MustafaBois/project/AmazingRaceApp/admin.py` to register the new model in django's admin page
1. Add your model to Django admin by adding the line `admin.site.register(<YOUR NEW MODEL NAME>)`
1. Navigate to `http://127.0.0.1:8000/admin` and test your model!
1. Perform a migration `python3 manage.py maskemigrations application`, then `python3 manage.py migrate`

## Adding CSS files to the website
1. Paste the resource in `MustafaBois/project/AmazingRaceApp/templates/css`
1. make sure to add `{% load static %}` -- insert at the top of the html file where you are using this css file
1. Go to your tag and the `href` tag should be formatted: `href="{% static 'css/<NAME OF YOUR CSS FILE>' %}"`

## Adding JavaScript files to the website
1. Paste the resource in `MustafaBois/project/AmazingRaceApp/templates/js`
1. make sure to add `{% load static %}` -- insert at the top of the html file where you are using this js file
1. Go to your tag and the `href` should be formatted: `href="{% static 'js/<NAME OF YOUR JS FILE>' %}"`

## Adding new python packages
1. Add a line to the `MustafaBois/requirements.txt` file making note of the specific version required
1. Stop your server if its running
1. Navigate to the root directory and type `pip3 install -r requirements.txt` -- make sure your virtual environment is running; if not type `source ./venv/bin/activate`
1. Then type `pip3 install -r requirements.txt` to install your new dependencies
1. `cd project` -- change directory to project/
1. `python3 manage.py runserver`

-- TODO - Shrawani   
## Resource Accessibility/Security
* Organisations - admin has all, user only gets for their own
* Orders - admin has all, user gets/puts for their own
* Services - admin has all, user only gets
* Users - admin has all, user can get/put at the 'me' endpoint
* Addresses - admin has all, user has gets
* Roles - admin has all, user has none
