import os
import twitter
from random import choice
from flask import Flask, render_template, request
from flask_cache import Cache

# Create Flask app
app = Flask(__name__)
cache = Cache(app, config={
              'CACHE_TYPE': 'redis',
              'CACHE_KEY_PREFIX': 'flask-cache',
              'CACHE_REDIS_HOST': 'localhost',
              'CACHE_REDIS_PORT': '6379',
              'CACHE_REDIS_URL': 'redis://localhost:6379',
              'CACHE_DEFAULT_TIMEOUT': '50'
              })

# Create an instance of the twitter.Api class and authenticate with consumer key
# and secret and oAuth key and secret.
api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


@app.route("/")
def load_page():
    """Return page."""

    return render_template("tweet_gen.html")


@app.route("/tweet_gen", methods=["GET"])
def get_markov_tweet():
    # TODO: Write docstring: """ """

    twitter_user = request.args.get("twitter-username")

    # Create a list of user's statuses from newest to oldest, excluding replies.
    # 200 is the maximum allowed by the python-twitter library.
    timeline = api.GetUserTimeline(screen_name=twitter_user,
                                   exclude_replies=True,
                                   count=200)

    # Extract Tweet strings from statuses to create new list without metadata.
    tweet_strings = [status.text for status in timeline]

    # Concatenate strings into a single string.
    index = 0
    markov_base = ""
    for index in range(len(tweet_strings)):
        markov_base = markov_base + tweet_strings[index]

    @cache.cached()
    def make_chains(text_string):
        """Takes input text as a string; returns a dictionary of Markov chains.
        The key will be a tuple comprising two words that appear consecutively
        in the input text (first_word, second_word), and its value is a list of
        the word(s) that follow the pair (aka the bi_gram) whenever it appears
        in the input text. For example:
            >>> make_chains("hi there mary hi there juanita")
            {('hi', 'there'): ['mary', 'juanita'],
             ('there', 'mary'): ['hi'],
             ('mary', 'hi'): ['there']}
        """

        chains = {}
        words = text_string.split()
        for counter in range(len(words)-2):
            first_word = words[counter]
            second_word = words[counter + 1]
            bi_gram = (first_word, second_word)
            # Check if this bi_gram has already been added as a key
            third_words = chains.get(bi_gram, [])
            # If not, add new key-value pair of bi_gram and consecutive word
            if third_words == []:
                chains[bi_gram] = [words[counter + 2]]
            # If so, append consecutive word to value list
            else:
                third_words.append(words[counter + 2])

        return chains

    def make_tweet(chains):
        """Takes a dictionary of Markov chains; returns a string with a maximum
        of 140 characters that reflects the probabilities captured by the
        chains."""

        # Choose a bi-gram from chains dictionary randomly
        bi_gram = choice(chains.keys())
        # Choose a word randomly from that bi-gram's value (which is a list) in the
        # chains dictionary
        third_word = choice(chains[bi_gram])
        # Store the first and second words in the bi-gram and the third word chosen
        # from its associated list as the beginning of the new string to be returned
        text = bi_gram[0] + " " + bi_gram[1] + " " + third_word
        # Loop through dictionary, continuously concatenating string until creating
        # a bi_gram not in the dictionary
        while chains.get((bi_gram[1], third_word), 0) != 0:
            # Create new bi_gram from 2nd word in previous one and previous third
            # word
            bi_gram = (bi_gram[1], third_word)
            # Choose new third word randomly from value list for the bi_gram in the
            # chains dictionary
            third_word = choice(chains[bi_gram])
            # Add new third word to stored text
            text = text + " " + third_word

        if len(text) >= 140:
            text = text[:140]

        text_words = text.split(" ")

        # Make a reasonable attempt to prevent 140-character cut-off from
        # causing the string to end in the middle of a word
        if (" " + text_words[-1] + " ") not in markov_base:
            shortened_text = text_words[0:-1]
            text = ""
            for word in shortened_text:
                text = text + " " + word

        # Optionally: Uncomment below to always capitalize first word if first
        # character is a letter
        # if text[0].isalpha():
        #    text = text.capitalize()

        return text

    markov_chains = make_chains(markov_base)
    return make_tweet(markov_chains)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
