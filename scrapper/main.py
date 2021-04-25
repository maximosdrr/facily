import requests
from src.scrapper import Scrapper
from src.config_objects import getScrapperConfigObjects


scrapperConfigs = getScrapperConfigObjects()

for config in scrapperConfigs:
    contestType = config['type']
    url = config['base_url']
    lastContest = config['lastContest']
    scrapper = Scrapper(contestType, url, lastContest)
    scrapper.scrapp()

# requests.post('http://localhost:3000/contest/save-todo',
#               json={'type': 'TESTE', 'index': 1231})
