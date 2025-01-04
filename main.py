import requests
import json
from check import analyze_arbitrage
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BALL = "basketball_nba"
FOOT = "americanfootball_nfl"
REGIONS = "us"
REG_MARKET = "h2h"
ODDS_FORMAT = "decimal"
DATE_FORMAT = "iso"

h2h_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{BALL}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': REG_MARKET,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if h2h_response.status_code != 200:
    print(f'Failed to get odds: status_code {h2h_response.status_code}, response body {h2h_response.text}')

else:
    odds_json = h2h_response.json()
    print('Number of events:', len(odds_json))
    
    # Write the formatted JSON to output.json
    with open('nba.json', 'w') as f:
        json.dump(odds_json, f, indent=4)
    
    # Check the usage quota
    print('Remaining requests', h2h_response.headers['x-requests-remaining'])
    print('Used requests', h2h_response.headers['x-requests-used'])

h2h_response_foot = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{FOOT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': REG_MARKET,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if h2h_response_foot.status_code != 200:
    print(f'Failed to get odds: status_code {h2h_response_foot.status_code}, response body {h2h_response_foot.text}')

else:
    odds_json = h2h_response_foot.json()
    print('Number of events:', len(odds_json))
    
    # Write the formatted JSON to output.json
    with open('nfl.json', 'w') as f:
        json.dump(odds_json, f, indent=4)
    
    # Check the usage quota
    print('Remaining requests', h2h_response_foot.headers['x-requests-remaining'])
    print('Used requests', h2h_response_foot.headers['x-requests-used'])

analyze_arbitrage("basketball")
analyze_arbitrage("football")
