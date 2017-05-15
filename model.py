from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
# """ """
# __tablename__ = "users"
# def __repr__(self):
#    return "<User with user_id %s and email %s>" % (self.user_id, self.email)

#class Tweets(db.Model):

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
