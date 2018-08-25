import antispam

from prawbot import Praw


class Spam:
    def __init__(self):
        self.praw = Praw()
        self.antispam = antispam.Detector("spam.json")

    def training_submissions(self, column):

        query = '''
                SELECT * FROM $1;
                '''
        params = (column,)

        rows = self.praw.db.execute(query=query, params=params, is_select=True, fetch_all=True)
        return rows

    def spam_train(self):

        spam_training = self.training_submissions('spam')
        ham_training = self.training_submissions('ham')

        for s_sub in spam_training:
            if s_sub['body'] is not None:
                self.antispam.train(s_sub[0], True)

        for h_sub in ham_training:
            if h_sub['body'] is not None:
                self.antispam.train(h_sub[0], False)

    def is_spam(self, message):
        self.spam_train()
        return self.antispam.is_spam(message)

    def spam_score(self, message):
        self.spam_train()
        return self.antispam.score(message)

    def add_to_spam(self, message):

        query = '''
                INSERT INTO spam_training (spam) VALUES $1
                '''
        params = (message,)

        self.praw.db.execute(query=query, params=params)

    def add_to_ham(self, message):

        query = '''
                INSERT INTO spam_training (ham) VALUES $1
                '''
        params = (message,)

        self.praw.db.execute(query=query, params=params)
