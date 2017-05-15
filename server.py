import os
import twitter
from random import choice

# Create an instance of the twitter.Api class and authenticate with consumer key
# and secret and oAuth key and secret.
api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

user = "BarackObama"

# Create a list of user's statuses from newest to oldest, excluding replies.
# 200 is the maximum allowed by the python-twitter library.
timeline = api.GetUserTimeline(screen_name=user,
                               exclude_replies=True,
                               count=200)

# Extract Tweet strings from statuses to create new list without metadata.
tweet_strings = [status.text for status in timeline]

# Concatenate strings into a single string.
i = 0
markov_base = ""
for i in range(len(tweet_strings)):
    markov_base = markov_base + tweet_strings[i]


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains. A
    chain will be a key that consists of a tuple of (word1, word2) and the value
    would be a list of the word(s) that follow those two words in the input
    text. For example:
        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'],
         ('there', 'mary'): ['hi'],
         ('mary', 'hi': ['there']}
    """

    chains = {}
    words = text_string.split()
    for counter in range(len(words)-2):
        first_word = words[counter]
        second_word = words[counter + 1]
        bi_gram = (first_word, second_word)
        # check if we've already added this bigram as a key in the chains dict
        third_words = chains.get(bi_gram, [])
        if third_words == []:  # if list of third words is empty
            chains[bi_gram] = [words[counter + 2]]
            # adds new key-value pair to chains dictionary
        else:
            third_words.append(words[counter + 2])
            # append word after n-gram to list

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""
    # chooses first bi-gram from chains dictionary
    bi_gram = choice(markov_chains.keys())
    # chooses the next word randomly from that bi-gram's value (which is a list)
    third_word = choice(chains[bi_gram])
    # Stores first word in the bi-gram, second word in the bi-gram, and randomly
    # chosen third word as the beginning of our new text
    text = bi_gram[0] + " " + bi_gram[1] + " " + third_word
    # Loops through bi_grams produced in this way until creating a bi_gram that
    # is not in the dictionary
    while chains.get((bi_gram[1], third_word), 0) != 0:
        # Create new bi_gram from 2nd word in previous one and previous third
        # word
        bi_gram = (bi_gram[1], third_word)
        # Choose new third word randomly from value for bi_gram in dictionary
        third_word = choice(chains[bi_gram])
        # Add bi_gram and third word to stored text
        text = text + " " + third_word

    if len(text) >= 140:
        text = text[:140]

    return text

markov_chains = make_chains(markov_base)
print make_text(markov_chains)
