import os
import json

class SmaDatabase:
    #(Dict['username' : sma_account])
    account_db = {}

    @classmethod
    def add_account(cls, account):
        """Add account to database, will replace the old one if already exist\n
        Args:\n
        `account` (:SmaAccount: : the smaboy account to add to the database
        """
        cls.account_db[account['username']] = account

    @classmethod
    def load_account_db(cls):
        """Load ../Databases/account_db.json file to database,
        will load nothing if json file is not exist
        """
        file_location = '../Databases/account_db.json'
        if os.path.exists(file_location):
            with open(file_location, "r") as db_file:
                cls.account_db = json.load(db_file)

    @classmethod
    def save_account_db(cls):
        """Save database to ../Databases/account_db.json
        """
        directory = '../Databases'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + '/account_db.json', "w") as db_file:
            json.dump(cls.account_db, db_file)

    @classmethod
    def is_username_exists(cls, username):
        total_account_db = len(cls.account_db)
        if total_account_db == 0:
            # user database is empty
            return False

        if username in cls.account_db:
            # user is exists
            return True

        # user is not exists
        return False
