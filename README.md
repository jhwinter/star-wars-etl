# star-wars-etl

## How to Run

### Requirements

- [Python 3.8](https://www.python.org/downloads/)
- [pipenv](https://pypi.org/project/pipenv/)
- [Install and Setup MySQL Database locally](https://dev.mysql.com/doc/mysql-getting-started/en/)

### Setup

1. Open a terminal and navigate to project directory
2. Create a `.env` file in the project's root directory that contains 
your database's username, user's password, and the name of the database.
    - Example .env file:
    ```.env 
   DB_USER="test"
   DB_PASS="testing"
   DB_NAME="star_wars"
   ```
3. Run `pipenv install && pipenv shell`

### Execute Tasks

1. Open a terminal and navigate to project's root directory
2. Execute Tasks
    - task one: Run `python3 -m star_wars_etl.task_one`
    - task two: Run `python3 -m star_wars_etl.task_two`

### Execute Tests

1. Open a terminal and navigate to project's root directory
2. Run a single test case: `python3 -m unittest -v star_wars_etl.test.{test_filename}`
    - Example: `python3 -m unittest -v star_wars_etl.test.test_utils`
3. Run all test cases: `python3 -m unittest discover -v -s star_wars_etl/test`

## Task One

Gets 15 random characters and the names of the films they have been in,
inserts the data into a MySQL database, and prints the data to the console.
Example output:
```json
[
    {
        "film": "The Empire Strikes Back",
        "character": [
            "Leia Organa",
            "Obi-Wan Kenobi",
            "Palpatine"
        ]
    },
    {
        "film": "The Phantom Menace",
        "character": [
            "Ratts Tyerel",
            "Rugor Nass",
            "Ki-Adi-Mundi",
            "Ric Olié",
            "Mas Amedda",
            "Obi-Wan Kenobi",
            "Padmé Amidala",
            "Palpatine"
        ]
    },
    {
        "film": "Attack of the Clones",
        "character": [
            "Ki-Adi-Mundi",
            "Mas Amedda",
            "Obi-Wan Kenobi",
            "Padmé Amidala",
            "Palpatine"
        ]
    },
    {
        "film": "A New Hope",
        "character": [
            "Leia Organa",
            "Obi-Wan Kenobi"
        ]
    },
    {
        "film": "Return of the Jedi",
        "character": [
            "Leia Organa",
            "Wicket Systri Warrick",
            "Obi-Wan Kenobi",
            "Arvel Crynyd",
            "Palpatine",
            "Ackbar"
        ]
    },
    {
        "film": "Revenge of the Sith",
        "character": [
            "Leia Organa",
            "Ki-Adi-Mundi",
            "Obi-Wan Kenobi",
            "Padmé Amidala",
            "Palpatine"
        ]
    }
]
```

## Task Two

1. Gets data for the movie "A New Hope". 
2. Replaces the data for each of the endpoints listed in the JSON object 
received from the API Request. 
3. Converts the height and mass of each character 
from metric to U.S. units (mass is replaced by weight). 
4. Removes all cross-referencing material from the replaced data.
5. Writes the data to a JSON file called task_two.json
