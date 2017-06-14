# Features Request App [![Coverage Status](https://coveralls.io/repos/github/xfilipe/EngineeringMidLevel/badge.svg)](https://coveralls.io/github/xfilipe/EngineeringMidLevel) [![Build Status](https://travis-ci.org/xfilipe/EngineeringMidLevel.svg?branch=master)](https://travis-ci.org/xfilipe/EngineeringMidLevel)

"a web application that allows the user to create "feature requests"."

**Live APP at http://xfilipe.pythonanywhere.com/**

## Initial Considerations
Notice that this application was made in order to show some skills in a set of technologies, many "features" are not implemented because they are time consuming and also I have some considerations about the app:

* CI is just for check the app agains tests, the front-end's build and the deployment must be done manually.
* The app was hosted within pythonanywhere. I'm a linux user and I did some deploys in the past but now it was the only free host that I could have (also the easiest to deploy).
* The API is not RESTful and the routes doesn't have full CRUD operations. They are designed just to match the especification. So, for example, you can't delete or edit clients and product areas.
* There's just unit tests! Some people agree that unit tests without integration tests doens't not perform so well to warranty the integrity of the application and others may agree that unit tests if well written are good enoght for that job.
* Front-end wasn't tested, this may fall into last section where integration tests should be written to check the app UI.
* Front-end maybe is too coupled. Since I don't have enough experience with knockoutJS I'm not qualified to decide if theres a better way to organized the code.
* Product Area has no effect in Clients neither in Priorities. The only complex relation is between Clients and Priorities.
* There's no authentication and any kind of protection for sensitive information.
* The performance of the app wasn't tested.

## Technologies used
* **[Python3](https://www.python.org/downloads/)** - A programming language that lets you work more quickly (The universe loves speed!).
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments
* **[Flask](flask.pocoo.org/)** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
* **[Flask-API](http://www.flaskapi.org/)** - Flask API is an implementation of the same web browsable APIs that Django REST framework provides.
* **[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)** - Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application.
* **[KnockoutJS](http://knockoutjs.com/)** – Knockout makes it easier to create rich, responsive UIs with JavaScript.
* It also uses other technologies like npm, webpack, coverage for tests coverage and sqlite as DB.


## Installation / Usage
* First ensure you have [python3](https://www.python.org), [nodejs](https://nodejs.org/en/) and [npm](https://nodejs.org/en/) globally installed in your computer.
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone git@github.com:xfilipe/EngineeringMidLevel.git feature-app
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd feature-app
        ```
    2. Build the front end app. It will build everything and make a copy to backend folder so it can be served by flask server.
       ```
        $ cd frontend
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
    ```

* #### Running It
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ flask run
    ```
    You can now access the app on your local browser by using
    ```
    http://localhost:5000/
    ```

* #### Test it
    Or your terminal, in the backend folder, just run the following command:
    ```
    python -m tests.run
    ```
    It will run all tests and also show the coverage report into terminal


## License
MIT License

Copyright (c) 2017 Jee Githinji Gikera

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