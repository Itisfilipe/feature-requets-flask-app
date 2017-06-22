# Features Request App [![Coverage Status](https://coveralls.io/repos/github/xfilipe/EngineeringMidLevel/badge.svg)](https://coveralls.io/github/xfilipe/EngineeringMidLevel) [![Build Status](https://travis-ci.org/xfilipe/EngineeringMidLevel.svg?branch=master)](https://travis-ci.org/xfilipe/EngineeringMidLevel)

A web application that allows the user to create "feature requests".

Live APP at http://xfilipe.pythonanywhere.com/ but you will need an password to view it. If you are here you should have one but if not just ask me at filipetamaral [AT] gmail [dot] com

## First Considerations
Notice that this application was made in order to show some skills in a set of technologies, many "features" are not implemented because they are time consuming. Also, I have some considerations about the app:

* CI is just for check the app against tests, the front-end build and the deployment must be done manually.
* The app was hosted within pythonanywhere. I'm a linux user and I did some deploys in the past but now it was the only free host that I could have (also the easiest to deploy). Important: free sites have a limited time span, so the app will be online until Thursday 14 September 2017.
* The API doens't match all the requeriments to be considered RESTful and the routes doesn't have full CRUD operations. They are designed just to match the specification. So, for example, you can't delete or edit clients and product areas.
* There's just unit tests! Some people agree that unit tests without integration tests doens't not perform so well to warranty the integrity of the application and others may agree that unit tests if well written are good enoght for that job. I didn't implemented integrations test because is time consuming to do it although I believe that is important to have them along side unit tests.
* Front-end wasn't tested, this may fall into last section where integration tests should be written to check the app UI.
* Front-end maybe is too coupled. Since I don't have enough experience with knockoutJS I'm not qualified to decide if there's a better way to organized the code.
* Product Area has no effect in Clients neither in Priorities. The only complex relation is between Clients and Priorities.
* There's no authentication and any kind of protection for sensitive information.
* The performance of the app wasn't tested.
* I used sqlite for simplicity.
* The last but not less important, I didn't write down how to use the app. If the app does not explain yourself I believe is because the UX is bad/wrong and should be changed.

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
