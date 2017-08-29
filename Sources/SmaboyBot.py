from SmaboyDatabase import SmaDatabase
import SmaboyConnection

class SmaBot:

    database = SmaDatabase()
    connection = SmaboyConnection.SmaCon()

    username: ''
    password: ''

    @classmethod
    def __init__(cls, username, password, perconnection_delay=5):
        cls.username = username
        cls.password = password
        cls.database.load_account_db()
        cls.connection.perconnection_delay = perconnection_delay

    @classmethod
    def login(cls):
        return cls.connection.login(cls.username, cls.password)

    @classmethod
    def get_new_account(cls, total=1):
        stop_searching_account = False
        stop_searching_username = False
        total_new_account = 0
        page = 1

        while not stop_searching_account:
            new_usernames = []
            usernames = None
            while not stop_searching_username:
                #Get username from smaboy browse page
                usernames = cls.connection.get_username_from_browse(index=page)
                if usernames is None:
                    #reach user limit; stop searching
                    print('all user in website has received')
                    stop_searching_account = True
                    stop_searching_username = True
                else:
                    #check if username exists
                    for username in usernames:
                        if not cls.database.is_username_exists(username):
                            #found new username
                            new_usernames.append(username)
                    total_new_usernames = len(new_usernames)
                    if total_new_usernames > 0:
                        #Found new username; stop searching
                        stop_searching_username = True
                    else:
                        #Not found any new username; continue searching on the next page
                        page += 1

            if not stop_searching_account:
                #Get username account and add to database
                for username in new_usernames:
                    account = cls.connection.get_account(username)
                    #check if account can be retreieved
                    if account is not None:
                        #Account retrieved
                        cls.database.add_account(account)
                        total_new_account += 1
                        if total_new_account >= total:
                            stop_searching_account = True
                            break
                    else:
                        print('cannot retreived username: %s' % username)
                if total_new_account < total:
                #Not enough new account; continue searching on the next page
                    stop_searching_username = False
                    page += 1
        print('%d new account added, Search until page: %d'
              % (total_new_account, page))

    @classmethod
    def exit(cls):
        cls.database.save_account_db()
