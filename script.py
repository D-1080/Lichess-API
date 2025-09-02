import requests
import json
import pandas as pd

LICHESS_API = "https://lichess.org/api"
USERNAME = "DrNykterstein"  # Change this to your target player
MAX_GAMES = 50              # How many games to fetch

def fetch_user_profile(username):
    url = f"{LICHESS_API}/user/{username}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def fetch_user_games(username, max_games=50):
    url = f"{LICHESS_API}/games/user/{username}"
    params = {
        "max": max_games,
        "moves": "true",
        "opening": "true",
        "clocks": "true",
        "pgnInJson": "true"
    }
    headers = {"Accept": "application/x-ndjson"}
    r = requests.get(url, params=params, headers=headers, stream=True)
    r.raise_for_status()
    print(r)

    games = []
    for line in r.iter_lines():
        if line:
            games.append(json.loads(line.decode("utf-8")))
    return games

def process_games(games):
    rows = []
    for g in games:
        game_id = g.get("id")
        rated = g.get("rated")
        speed = g.get("speed")
        perf = g.get("perf")
        winner = g.get("winner")
        opening_name = g.get("opening", {}).get("name", "Unknown")
        white_name = g["players"]["white"]["user"]["name"] if "user" in g["players"]["white"] else "Anonymous"
        black_name = g["players"]["black"]["user"]["name"] if "user" in g["players"]["black"] else "Anonymous"

        moves = g.get("moves", "")

        rows.append({
            "game_id": game_id,
            "rated": rated,
            "speed": speed,
            "perf": perf,
            "winner": winner,
            "opening": opening_name,
            "white": white_name,
            "black": black_name,
            "moves": moves
        })
    return pd.DataFrame(rows)

def main():
    # 1. Get profile
    print(f"Fetching profile for {USERNAME}...")
    profile = fetch_user_profile(USERNAME)
    print(json.dumps(profile, indent=2))

    # 2. Get last N games
    print(f"\nFetching last {MAX_GAMES} games...")
    games = fetch_user_games(USERNAME, MAX_GAMES)
    print(f"Fetched {len(games)} games.")

    # 3. Process into DataFrame
    df = process_games(games)
    print("\nSample game data:")
    print(df.head())

    # 4. Save to files for later analysis
    df.to_csv(f"{USERNAME}_games.csv", index=False)
    with open(f"{USERNAME}_profile.json", "w") as f:
        json.dump(profile, f, indent=2)

    print(f"\nData saved as {USERNAME}_games.csv and {USERNAME}_profile.json")

if __name__ == "__main__":
    main()

'''
here is the script.py  
We wanted the details of the person.. so we added "DrNykterstein"  But this file is giving all details about the player_games and player_profile files 
'''