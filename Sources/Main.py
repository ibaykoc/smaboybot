import SmaboyBot

#Create SmaboyBot instance
SMABOYBOT = SmaboyBot.SmaBot('dodiharyadi', 'dodiituganteng', 5)

#Login Smaboybot
if SMABOYBOT.login():
    print('Login Success')
else:
    print('Login Failed')

SMABOYBOT.get_new_account(6)
# for account in SMABOYBOT.database.account_db:
#     SMABOYBOT.connection.add_friend(account=SMABOYBOT.database.account_db[account])

# SMABOYBOT.connection.add_friend(account=SMABOYBOT.database.account_db['souldier'])

SMABOYBOT.exit()
