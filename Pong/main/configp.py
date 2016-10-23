import configparser

config = configparser.ConfigParser()
print(config.read('config.ini'))
for key in config['bitbucket.org']: print(key)