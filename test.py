import requests
import pandas as pd

response = requests.get("https://api-web.nhle.com/v1/schedule/now")
data = response.json()

# The response has a "gameWeek" list — each entry is a day with "games"
rows = []
for day in data["gameWeek"]:
    for game in day["games"]:
        rows.append({
            "date": day["date"],
            "away": game["awayTeam"]["commonName"]["default"],
            "home": game["homeTeam"]["commonName"]["default"],
            "away_score": game["awayTeam"].get("score"),
            "home_score": game["homeTeam"].get("score"),
            "state": game["gameState"],  # PRE, LIVE, OFF
        })

df = pd.DataFrame(rows)
print(df)   