## Tweet Gen 2.0

Tweet Gen 2.0 is a web app designed to generate Tweets simulating the voice of a Twitter user whose screen name you supply. Enter the screen name of a Twitter user and click "Make a Tweet" to get a new Tweet in the author's writing style. Generally speaking, the more Tweets the author has already published, the better the "likeness" will be: the words and their sequence are determined by Markov chains built from their past Tweets. Also, the chains are cached remotely to provide faster results for common queries.

#### Built with...

* Python
* Flask
* jQuery
* JavaScript
* Twitter API
* Python-Twitter library
* AJAX
* Flask-Cache
* Redis

#### Installation

To run Tweet Gen 2.0 locally, you'll need to install [Redis](https://redis.io/) if you haven't already. You'll also need a [Twitter](https://twitter.com/) account (with an associated phone number) in order to get the Twitter credentials you'll need to provide.

First, visit https://apps.twitter.com and create a new application to obtain your Twitter consumer key and secret and your access token and access token secret. Save them in a secrets.sh file in the format shown below:
```
export TWITTER_CONSUMER_KEY="XXXXXXXXXXXXXXXXXXXXX"
export TWITTER_CONSUMER_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
export TWITTER_ACCESS_TOKEN_KEY="XXXXXXXXXXXXXXXXXXXXXX"
export TWITTER_ACCESS_TOKEN_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

Then, create and activate a virtual environment:
```
virtualenv env
```
```
source env/bin/activate
```
Then you can install the dependencies using pip install:

```
pip install -r requirements.txt
```
Finally, source your secrets.sh file and run the server file.
```
source secrets.sh
```
```
python server.py
```
#### TODO

* Polish UI
* Handle tweeted URLs better (or remove entirely)



