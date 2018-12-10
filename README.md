# iReporter

[iReporter](https://vino-jasuba.github.io/iReporter-/) is a digital platform for
citizens to report corruption cases to relevant authorities. Users can also report
on things that need government intervention.

[![Build Status](https://travis-ci.org/vino-jasuba/iReporter-.svg?branch=develop)](https://travis-ci.org/vino-jasuba/iReporter-) [![Coverage Status](https://coveralls.io/repos/github/vino-jasuba/iReporter-/badge.svg?branch=develop)](https://coveralls.io/github/vino-jasuba/iReporter-?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/9b822c57ae21083b11c5/maintainability)](https://codeclimate.com/github/vino-jasuba/iReporter-/maintainability)

## Demo

Project API demo is hosted at [Heroku](https://vino-ireporter.herokuapp.com)

### API endpoints

Prefix `api/v1/` to all api endpoints below

| **HTTP METHOD**   | **URI**  | **ACTION** |
|---|---|---|
|  **GET** |  `incidents/<string:incident_type>` | fetch incident records by `incident_type` field |
| **DELETE, GET, PATCH**  |  `incidents/<int:incident_id>` | get, delete and update incident records with given `incident_id` |
|  **GET, POST** |  `incidents` | get list of all incidents, create incident |
|  **POST** |  `auth/register` | registers a new user |
|  **DELETE, GET, PATCH** |  `users/<int:user_id>`  | get, delete and update user with given `user_id`|
|  **GET** |  `users` | fetch all users |

## Setup

To install and run the project locally:

- Clone the repo `git clone https://github.com/vino-jasuba/iReporter-.git`
- `cd` into iReporter/
- `pip install -r requirements.txt`
- `source env/bin/activate`
- `mv .env.example .env`
- `python run.py`

## Tests

- `pytest app/tests`
