import time

from prawcore.exceptions import PrawcoreException

from cogs.utils.dataIO import dataIO
from prawbot import Praw


class SubscriptionsUpdated(Exception):
    pass


class Stream:
    def __init__(self):
        self.praw = Praw()

    def get_list_of_subs(self):
        master_list = []
        for channel_id, subscriptions in self.settings.items():
            for title, sub_list in subscriptions.items():
                for subreddit in sub_list:
                    if subreddit not in master_list:
                        master_list.append(subreddit)
        return master_list

    def stream_task(self):
        self.settings = dataIO.load_json("data/reddit/settings.json")
        subscriptions_list = self.get_list_of_subs()
        subscriptions = '+'.join(subscriptions_list)

        subreddit = self.praw.subreddit(subscriptions)

        for submission in subreddit.stream.submissions():

            # Check if subscriptions have updated. If so, restart.
            self.settings = dataIO.load_json("data/reddit/settings.json")
            subscriptions_list = self.get_list_of_subs()
            check_subscriptions = '+'.join(subscriptions_list)

            if check_subscriptions != subscriptions:
                raise SubscriptionsUpdated

            self.insert_subreddit(submission.subreddit)
            self.insert_author(submission.author)
            self.insert_submission(submission)

    def insert_subreddit(self, subreddit):

        subreddit = subreddit.display_name.lower()

        query = '''
                INSERT INTO subreddit (subreddit) VALUES ($1);
                '''
        params = (subreddit,)

        self.praw.db.praw_execute(query=query, params=params)

    def insert_author(self, author):

        if author is None:
            return

        author_name = author.name.lower()
        link_karma = author.link_karma
        comment_karma = author.comment_karma
        created = author.created_utc

        query = '''
                INSERT INTO author (author, link_karma, comment_karma, created) VALUES ($1, $2, $3, $4);
                '''
        params = (author_name, link_karma, comment_karma, created)

        self.praw.db.praw_execute(query=query, params=params)

    def insert_submission(self, submission):

        if submission.author is None:
            return

        sub_id = submission.id
        subreddit = submission.subreddit.display_name.lower()
        author = submission.author.name.lower()
        title = submission.title
        body = submission.selftext
        url = submission.url
        created = submission.created_utc

        query = '''
        INSERT INTO submission (sub_id, subreddit, author, title, body, url, created, read) VALUES ($1, $2, $3, $4, $5, $6, $7, DEFAULT);
        '''
        params = (sub_id, subreddit, author, title, body, url, created)

        self.praw.db.praw_execute(query=query, params=params)

    def run(self):
        running = True
        while running:
            try:
                self.stream_task()
            except KeyboardInterrupt:
                print('Termination received. Goodbye!')
                self.praw.db.disconnect()
                running = False
            except SubscriptionsUpdated:
                print("Subscriptions have updated, restarting...")
                time.sleep(10)
            except PrawcoreException:
                print("PrawcoreException occurred, restarting...")
                time.sleep(10)
            except BaseException:
                print("Some type of exception occured, restarting...")
                time.sleep(10)
        return 0
