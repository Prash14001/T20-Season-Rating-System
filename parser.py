import os
import json
import pandas as pd

# ==========================================================
# INPUT / OUTPUT PATHS
# ==========================================================

INPUT_FOLDER = "ipl_json"
OUTPUT_FOLDER = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "ball_by_ball.csv")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

rows = []

# ==========================================================
# LOOP THROUGH ALL JSON FILES
# ==========================================================

for file_name in os.listdir(INPUT_FOLDER):

    if not file_name.endswith(".json"):
        continue

    file_path = os.path.join(INPUT_FOLDER, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data.get("info", {})

    match_id = file_name.replace(".json", "")

    # Match Information
    season = str(info.get("season", "")).strip()

    dates = info.get("dates", [])
    match_date = dates[0] if dates else ""

    venue = info.get("venue", "")

    teams = info.get("teams", [])
    team1 = teams[0] if len(teams) > 0 else ""
    team2 = teams[1] if len(teams) > 1 else ""

    innings = data.get("innings", [])

    # ======================================================
    # LOOP THROUGH INNINGS
    # ======================================================

    for innings_no, inning in enumerate(innings, start=1):

        batting_team = inning.get("team", "")

        bowling_team = team2 if batting_team == team1 else team1

        overs = inning.get("overs", [])

        # ==================================================
        # LOOP THROUGH OVERS
        # ==================================================

        for over in overs:

            over_number = over.get("over", 0)

            # Powerplay / Middle / Death
            if over_number < 6:
                phase = "Powerplay"
            elif over_number < 15:
                phase = "Middle"
            else:
                phase = "Death"

            deliveries = over.get("deliveries", [])

            # ==============================================
            # LOOP THROUGH DELIVERIES
            # ==============================================

            for delivery in deliveries:

                ball_number = delivery.get("ball", "")

                batter = delivery.get("batter", "")
                non_striker = delivery.get("non_striker", "")
                bowler = delivery.get("bowler", "")

                runs = delivery.get("runs", {})

                batter_runs = runs.get("batter", 0)
                extras = runs.get("extras", 0)
                total_runs = runs.get("total", 0)

                # Extras Type
                extras_type = ""

                if "extras" in delivery:
                    extras_type = ",".join(delivery["extras"].keys())

                # Wicket Information
                wicket = 0
                dismissal_type = ""
                player_out = ""

                if "wickets" in delivery:

                    wicket = 1

                    dismissal = delivery["wickets"][0]

                    dismissal_type = dismissal.get("kind", "")
                    player_out = dismissal.get("player_out", "")

                # Store Row
                rows.append({

                    "match_id": match_id,
                    "season": season,
                    "date": match_date,
                    "venue": venue,

                    "innings": innings_no,

                    "over": over_number,
                    "ball": ball_number,

                    "phase": phase,

                    "batting_team": batting_team,
                    "bowling_team": bowling_team,

                    "batter": batter,
                    "non_striker": non_striker,
                    "bowler": bowler,

                    "batter_runs": batter_runs,
                    "extras": extras,
                    "extras_type": extras_type,
                    "total_runs": total_runs,

                    "wicket": wicket,
                    "dismissal_type": dismissal_type,
                    "player_out": player_out

                })

# ==========================================================
# CREATE DATAFRAME
# ==========================================================

df = pd.DataFrame(rows)

# ==========================================================
# SAVE CSV
# ==========================================================

df.to_csv(OUTPUT_FILE, index=False)

# ==========================================================
# SUMMARY
# ==========================================================

print("=" * 55)
print("          IPL BALL-BY-BALL PARSER")
print("=" * 55)

print(f"Total Deliveries : {len(df):,}")
print(f"Matches Parsed   : {df['match_id'].nunique():,}")
print(f"Players          : {df['batter'].nunique():,}")

# Handle season values safely
seasons = sorted(df["season"].astype(str).unique())

print(f"Seasons          : {', '.join(seasons)}")

print("-" * 55)
print(f"CSV saved to : {OUTPUT_FILE}")
print("=" * 55)