# Mastermind

Mastermind is a code-breaking game for two players. One player becomes the codemaker , the other the codebreaker . 
The codemaker chooses a pattern of four color code pegs (duplicates allowed) and the codebreaker tries to guess it, in
both order and color. Each guess is made by placing a row of color code pegs on the decoding board. Once placed, the 
codemaker provides feedback by placing from zero to four key pegs in the small holes of the row with the guess. A black 
key peg (small red in the image) is placed for each code peg from the guess which is correct in both color and position. 
A white key peg indicates the existence of a correct color code peg placed in the wrong position.

## Configure Project

Configure a virtual environment with Python3 and install the requirements.

`virtualenv --python=python3 env`  
`source env/bin/activate`  
`pip install -r requirements`  
`python manage.py migrate`  

Also, create a superuser.

`python manage.py createsuperuser`

The project is already configured to run with local environment settings.

### Run Local

Local environment works with a SQLite database for simplicity but another database could be easily
configured editing the local.py file in settings folder. 

`python manage.py runserver`    
`python manage.py runserver --settings=mastermind.settings.local`

### Run Prod

Once Wsgi is already configured in production server, we need to set-up the following environment 
variables: SECRET_KEY, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST and DATABASE_PORT.  

`python manage.py runserver --settings=mastermind.settings.prod`

### Test

Unittests are using a SQLite database stored in memory.

`python manage.py test --settings=mastermind.settings.unittest`

## Endpoints

### /api-auth/login/

This URL will show the login form template to create a valid session.

### POST /games

Creates a new game. This endpoint does not require more data than the user session. The game
pattern will be generated randomly.

HTTP 201 Created code will be returned on success alongside with the created Game data.

```json
{
  "id": 4,
  "pattern_1": "GREEN",
  "pattern_2": "RED",
  "pattern_3": "YELLOW",
  "pattern_4": "RED",
  "created_by": "test",
  "created_at": "2018-09-13T20:06:33.846425Z"
}
```

### POST /games/<game_id>/guess

Creates a new guess checking the number of black and white pegs. 

We need to send the guess pattern as follows:

```json
{
  "guess_1": "RED",
  "guess_2": "GREEN",
  "guess_3": "BLUE",
  "guess_4": "PURPLE"
}
```

HTTP 200 OK code will be returned on success alongside with the created Guess data.

```json
{
  "game": 1,
  "guess_1": "RED",
  "guess_2": "GREEN",
  "guess_3": "BLUE",
  "guess_4": "PURPLE",
  "black": 2,
  "white": 1,
  "created_by": "test",
  "created_at": "2018-09-13T20:06:33.846425Z"
}
```

### GET /games/<game_id>/history

Retrieves a list of all guesses for the given game ordered by creation date descending.