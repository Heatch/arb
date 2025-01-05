import requests
import json
from check import analyze_arbitrage
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BALL = "basketball_nba"
FOOT = "americanfootball_nfl"
PUCK = "icehockey_nhl"
REGIONS = "us"
REG_MARKET = "h2h"
ODDS_FORMAT = "decimal"
DATE_FORMAT = "iso"

settings = {"basketball": True, "football": False, "hockey": True}

def getSportsOdds(SPORT):
    response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': REG_MARKET,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if response.status_code != 200:
        print(f'Failed to get odds: status_code {response.status_code}, response body {response.text}')
        return None
    
    else:
        odds_json = response.json()
        print('Number of events:', len(odds_json))
        
        # Write the formatted JSON to output.json
        with open(f'{SPORT}.json', 'w') as f:
            json.dump(odds_json, f, indent=4)
        
        # Check the usage quota
        print('Remaining requests', response.headers['x-requests-remaining'])
        print('Used requests', response.headers['x-requests-used'])
        return odds_json

for sport in settings:
    if settings[sport]:
        if sport == "basketball":
            getSportsOdds(BALL)
            analyze_arbitrage(BALL)
        elif sport == "football":
            getSportsOdds(FOOT)
            analyze_arbitrage(FOOT)
        elif sport == "hockey":
            getSportsOdds(PUCK)
            analyze_arbitrage(PUCK)
