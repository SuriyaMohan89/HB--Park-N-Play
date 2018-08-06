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


# Demo
[![Watch the video](https://user-images.githubusercontent.com/36581704/43699886-72373bb0-9905-11e8-8e7c-51dc683276a3.png)](https://www.youtube.com/watch?v=oQxmZ_NqKuQ)

## Screenshots

Some screenshots. There are more pages, but showing some glimpse of it. Please do watch the 1 minute demo video below.

### Search parks
<img width="1471" alt="screen shot 2018-06-09 at 4 20 23 pm" src="https://user-images.githubusercontent.com/36581704/43699923-9e95645c-9905-11e8-8220-a09665011932.png">

## Park ratings
<img width="611" alt="screen shot 2018-06-09 at 4 21 12 pm" src="https://user-images.githubusercontent.com/36581704/43699938-ad1ffc76-9905-11e8-935c-6b930eb006dd.png">

## Rate parks
<img width="595" alt="screen shot 2018-06-09 at 4 21 24 pm" src="https://user-images.githubusercontent.com/36581704/43699966-cad18d7a-9905-11e8-8cd2-604314caa112.png">


### Contact
For any feedback/suggestions, please feel free to contact suriya.selu@gmail.com
_Contributions welcome_
