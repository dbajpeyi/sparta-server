#Sparta

- A sports article API server in Django

Crawls news sites and exposes news article data using Django Rest Framework.
Protects resources using token based session-less auth


#Tools used:
- Django rest framework
    - Expose api endpoints. Makes writing APIs lot easier. Reduces a lot of code

- Django redis cache
    - Used here as a persistent cache. Storing news articles that are new and  user has not liked yet 

- Django rest framework JWT
    - Using this for session less auth. The backend does not store any sessions to keep user logged in

#Caching strategy

The endpoints expose only what is present in redis cache, avoiding the need to touch the DB ever.
Redis is updated with 'fresh' articles when the crawler is updating the databse. Any article that 
is liked/unliked by the user is removed from the redis cache.

#Setup

Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)

Install [redis](http://redis.io/download)
`mkvirtualenv sparta`
```
$git clone git@github.com:dbajpeyi/sparta-server.git
$pip install -r requirements.txt
$cd project
$python manage.py migrate
$python manage.py runserver
```
Server at `https://localhost:8000`

#Running the load-script

From the project directory where `manage.py` is:
```
$python manage.py load_articles
```
  

