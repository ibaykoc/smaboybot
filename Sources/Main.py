import SmaboyBot

#Create SmaboyBot instance
SMABOYBOT = SmaboyBot.SmaBot('dodiharyadi', 'dodiituganteng', 5)

#Login Smaboybot
if SMABOYBOT.login():
    print('Login Success')
else:
    print('Login Failed')

SMABOYBOT.get_new_account(1)

SMABOYBOT.exit()
