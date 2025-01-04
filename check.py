import json

def analyze_arbitrage(mode):
    template = {
        "event": {"home": "", "away": ""}, 
        "fanduel/betmgm": {"home": 0, "away": 0, "roi": 0}, 
        "fanduel/betrivers": {"home": 0, "away": 0, "roi": 0}, 
        "fanduel/draftkings": {"home": 0, "away": 0, "roi": 0}, 
        "betmgm/betrivers": {"home": 0, "away": 0, "roi": 0}, 
        "betmgm/draftkings": {"home": 0, "away": 0, "roi": 0}, 
        "betrivers/draftkings": {"home": 0, "away": 0, "roi": 0}
    }

    # Determine file based on mode
    if (mode.lower() == "basketball") or (mode.lower() == "b"):
        file = "nba.json"
    elif (mode.lower() == "football") or (mode.lower() == "f"):
        file = "nfl.json"
    else:
        raise ValueError("Invalid mode. Use 'basketball'/'b' or 'football'/'f'")

    # Read JSON data
    with open(file) as f:
        h2h_json = json.load(f)

    all_data = []
    relevant = ["fanduel", "betmgm", "betrivers", "draftkings"]

    # Process each event
    for event in h2h_json:
        data = template.copy()
        odds = {bookie: [] for bookie in relevant}
        home = event["home_team"]
        away = event["away_team"]
        data["event"] = {"home": home, "away": away}

        # Get odds for each bookmaker
        for bookie in event["bookmakers"]:
            if bookie["key"] in relevant:
                key = bookie["key"]
                odds[key].extend(bookie["markets"][0]["outcomes"])
        
        # Calculate ROIs for each combination
        bookie_pairs = [
            ("fanduel", "betmgm"),
            ("fanduel", "betrivers"),
            ("fanduel", "draftkings"),
            ("betmgm", "betrivers"),
            ("betmgm", "draftkings"),
            ("betrivers", "draftkings")
        ]

        for bookie1, bookie2 in bookie_pairs:
            combo_key = f"{bookie1}/{bookie2}"
            try:
                home_odds = 1/(odds[bookie1][0]["price"])
                away_odds = 1/(odds[bookie2][1]["price"])
                roi = 1 - (home_odds + away_odds)
                data[combo_key] = {"home": home_odds, "away": away_odds, "roi": roi}
            except (KeyError, IndexError, ZeroDivisionError):
                pass
        
        all_data.append(data)

    # Find best opportunities
    all_opportunities = []
    for event in all_data:
        event_name = f"{event['event']['home']} vs {event['event']['away']}"
        for bookie_combo in event.keys():
            if bookie_combo != 'event':
                roi = event[bookie_combo]['roi']
                if roi != 0:
                    all_opportunities.append((event_name, bookie_combo, roi))

    # Sort and display results
    sorted_opportunities = sorted(all_opportunities, key=lambda x: x[2], reverse=True)
    
    print(f"\nTop 5 Arbitrage Opportunities for {file}:")
    for i, opportunity in enumerate(sorted_opportunities[:5], 1):
        print(f"\n{i}. Event: {opportunity[0]}")
        print(f"Bookmaker Combination: {opportunity[1]}")
        print(f"ROI: {opportunity[2]:.2%}")
        print("-" * 50)

    return sorted_opportunities  # Return the full list in case you want to do more analysis
