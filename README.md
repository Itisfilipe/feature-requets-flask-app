# Features Request App [![Coverage Status](https://coveralls.io/repos/github/Itisfilipe/EngineeringMidLevel/badge.svg)](https://coveralls.io/github/Itisfilipe/EngineeringMidLevel) [![Build Status](https://travis-ci.org/Itisfilipe/EngineeringMidLevel.svg?branch=master)](https://travis-ci.org/Itisfilipe/EngineeringMidLevel)

A web application that allows the user to create `feature requests`.

## Technologies used
* **[Python3](https://www.python.org/downloads/)** - A programming language that lets you work more quickly (The universe loves speed!).
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments
* **[Flask](flask.pocoo.org/)** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
* **[Flask-API](http://www.flaskapi.org/)** - Flask API is an implementation of the same web browsable APIs that Django REST framework provides.
* **[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)** - Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application.
* **[KnockoutJS](http://knockoutjs.com/)** – Knockout makes it easier to create rich, responsive UIs with JavaScript.
* **[Bootstrap](http://getbootstrap.com/)** – Bootstrap is the most popular HTML, CSS, and JS framework for developing responsive, mobile first projects on the web.
* It also uses other technologies like npm, webpack, coverage for tests coverage and sqlite as DB.


## Installation / Usage
* First ensure you have [python3](https://www.python.org), [nodejs](https://nodejs.org/en/) and [npm](https://nodejs.org/en/) globally installed in your computer.
* After this, ensure you have installed virtualenv globally as well. If not, run this as root:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone https://github.com/xfilipe/EngineeringMidLevel.git feature-app
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd feature-app
        ```
    2. Build the front end app. It will build everything and make a copy of index.html to backend folder so it can be served by flask.
       ```
        $ cd frontend
        $ npm install
        $ npm run buildprod
        ```
    3. Go to backend folder and then create and fire up your virtual environment in python3:
        ```
        $ cd ../backend
        $ virtualenv -p python3 venv
        ```

* #### Environment Variables
    You need to add some variables to the environment in order to run the app :
    ```
    source venv/bin/activate
    export FLASK_APP=run.py
    export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
    export APP_SETTINGS="production"
    ```

* #### Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
    (venv)$ pip install -r requirements-dev.txt
    ```

* #### Running It
    On your terminal, inside of backend folder, run the server using this one simple command:
    ```
    (venv)$ flask run
    ```
    You can now access the app on your local browser by using
    ```
    http://localhost:5000/
    ```

* #### Test it
    Or your terminal, **inside the backend folder**, run the following command:
    ```
    python -m tests.run
    ```
    It will run all tests and also show the coverage report into terminal


## License
MIT License

Copyright (c) 2017 Filipe Teixeira Amaral

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
