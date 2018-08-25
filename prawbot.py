import praw

from cogs.utils.dataIO import dataIO
from cogs.utils.database import Database


class Praw(praw.Reddit):
    def __init__(self):
        self.config = dataIO.load_json("data/chappie/config.json")
        self.db = Database(database=self.config["DATABASE"],
                           user=self.config["DATABASE_USER"],
                           password=self.config["DATABASE_PASSWORD"],
                           host=self.config["DATABASE_HOST"],
                           port=self.config["DATABASE_PORT"])

        super().__init__(client_id=self.config["REDDIT_CLIENT_ID"],
                         client_secret=self.config["REDDIT_CLIENT_SECRET"],
                         password=self.config["REDDIT_PASSWORD"],
                         user_agent=self.config["REDDIT_USER_AGENT"],
                         username=self.config["REDDIT_USERNAME"])
