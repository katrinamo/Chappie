import time

from prawcore.exceptions import PrawcoreException

from prawbot import Praw
from reddit.spam import Spam


class Stream:
    def __init__(self):
        self.praw = Praw()
        self.spam = Spam()

    def stream_task(self):
        subreddit = self.praw.subreddit("healthanxiety")

        for submission in subreddit.stream.submissions():
            self.insert_subreddit(submission.subreddit)
            self.insert_author(submission.author)
            self.insert_submission(submission, 'submission')

            message = submission.title + " " + submission.selftext
            if self.spam.is_spam(message):
                self.insert_submission(submission, 'spam_catch')

    def insert_subreddit(self, subreddit):

        subreddit = subreddit.display_name

        query = '''
                INSERT INTO subreddit (subreddit) VALUES ($1);
                '''
        params = (subreddit,)

        self.praw.db.execute(query=query, params=params)

    def insert_author(self, author):

        if author is None:
            return

        author_name = author.name
        link_karma = author.link_karma
        comment_karma = author.comment_karma
        created = author.created_utc

        query = '''
                INSERT INTO author (author, link_karma, comment_karma, created) VALUES ($1, $2, $3, $4);
                '''
        params = (author_name, link_karma, comment_karma, created)

        self.praw.db.execute(query=query, params=params)

    def insert_submission(self, submission, table):

        if submission.author is None:
            return

        sub_id = submission.id
        subreddit = submission.subreddit.display_name
        author = submission.author.name
        title = submission.title
        body = submission.selftext
        url = submission.url
        created = submission.created_utc

        query = '''
        INSERT INTO $1 (sub_id, subreddit, author, title, body, url, created, read) VALUES ($2, $3, $4, $5, $6, $7, $8, DEFAULT);
        '''
        params = (table, sub_id, subreddit, author, title, body, url, created)

        self.praw.db.execute(query=query, params=params)

    def run(self):
        running = True
        while running:
            try:
                self.stream_task()
            except KeyboardInterrupt:
                print('Termination received. Goodbye!')
                self.praw.db.disconnect()
                running = False
            except PrawcoreException:
                print("PrawcoreException occurred. Sleeping for 10 seconds.")
                time.sleep(10)
        return 0
