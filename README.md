# SocialIN Park

### Overview
This app finds children's park nearby and also helps toddlers and their parents to socialize with other kids and their parents.

### Features
* Find children's park nearby
* Ratings for all the park as given by parents
* Emergency contact and curator contacts.
* Forum to submit feedback about a park
* See how many parents have **expressed interest to play at a certain time** for a park.
* Social connection with other parents and their children.

### Tech Stack
The codebase is implemented with python+Flask with Postgres db.

* Python 
* Flask for ORM.
* Jinja for templating
* Javascript(ES6), JQuery
* Html/CSS
* Bootstrap
* Postgres as backend database.

## Run the application
1. Make sure you have python, if not, please download it in python.org.
2. Install `Pypi`
3. After checking out, in the home directory of the project, issue `pip install -r requirements.txt`.
4. Run `python createdb childrenparks`
5. Run `python seed.db`
6. Run `python server.py`

You should be good to go. Check `localhost:5000`

Its not yet containerized, but should be trivial to do so. And you can deploy with kubernates/docker-swarm or just as a standalone app in GCP/DigitalOcean, etc...


### Screenshots
![alt text] (screenshot/homepage.png "Homepage with casserole images")

### Contact
For any feedback/suggestions, please feel free to contact suriya.selu@gmail.com
_Contributions welcome_
