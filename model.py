from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TwitterUser(db.Model):
"""Twitter user. A TwitterUser has (potentially) many MarkovTweets."""

__tablename__ = "users"

screenname = db.Column(db.Unicode(100), nullable=False, primary_key=True)
created_at = db.Column(db.DateTime, nullable=False)

# def __repr__(self):
#     return "<User with user_id %s and email %s>" % (self.user_id, self.email)

class MarkovTweet(db.Model):
"""Tweet generated from Markov chains. A MarkovTweet has one TwitterUser."""

__tablename__ = "markov_tweets"

tweet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
created_at = db.Column(db.DateTime, nullable=False)




def connect_to_db(app, db_uri='postgresql:///tweet_lib'):
    """Connect to the database."""

    # Making the database a default value for the db_uri parameter allows us to
    # pass in a different database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."
