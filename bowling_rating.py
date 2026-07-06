import pandas as pd
import os

# ==========================================================
# T20 BOWLING RATING ENGINE
# ==========================================================

OUTPUT_FOLDER = "outputs"

# ==========================================================
# FIND AVAILABLE SEASONS
# ==========================================================

available_seasons = []

for file in os.listdir(OUTPUT_FOLDER):

    if file.startswith("bowling_metrics_") and file.endswith(".csv"):

        season = file.replace("bowling_metrics_", "").replace(".csv", "")

        available_seasons.append(season)

available_seasons = sorted(available_seasons)

# ==========================================================
# HEADER
# ==========================================================

print("=" * 60)
print("             T20 BOWLING RATING ENGINE")
print("=" * 60)

print("\nAvailable Seasons:\n")

for season in available_seasons:
    print(" ", season)

SEASON = input("\nEnter Season: ").strip()

if SEASON not in available_seasons:

    print("\nInvalid Season!")
    exit()

INPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    f"bowling_metrics_{SEASON}.csv"
)

# ==========================================================
# LOAD DATA
# ==========================================================

bowling = pd.read_csv(INPUT_FILE)

print()
print("Season Selected :", SEASON)
print("Players Loaded  :", len(bowling))

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

required_columns = [

    "Bowler",

    "Matches",

    "Balls",

    "Wickets",

    "Economy",

    "Average",

    "Strike Rate",

    "Dot Ball %",

    "Boundary %",

    "PP Economy",

    "Middle Economy",

    "Death Economy"

]

missing = [

    col

    for col in required_columns

    if col not in bowling.columns

]

if len(missing) > 0:

    print("\nERROR!")

    print("\nMissing Columns:\n")

    for col in missing:

        print("-", col)

    exit()

# ==========================================================
# QUALIFICATION
# ==========================================================

bowling = bowling[
    bowling["Balls"] >= 120
].copy()

print("Qualified       :", len(bowling))

# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize(series, reverse=False):

    minimum = series.min()

    maximum = series.max()

    if minimum == maximum:

        return pd.Series(
            100,
            index=series.index
        )

    if reverse:

        return (
            (maximum - series)
            /
            (maximum - minimum)
        ) * 100

    return (
        (series - minimum)
        /
        (maximum - minimum)
    ) * 100

# ==========================================================
# NORMALIZED METRICS
# ==========================================================

bowling["Wickets_N"] = normalize(

    bowling["Wickets"]

)

bowling["Economy_N"] = normalize(

    bowling["Economy"],

    reverse=True

)

bowling["Average_N"] = normalize(

    bowling["Average"],

    reverse=True

)

bowling["SR_N"] = normalize(

    bowling["Strike Rate"],

    reverse=True

)

bowling["Dot_N"] = normalize(

    bowling["Dot Ball %"]

)

bowling["Boundary_N"] = normalize(

    bowling["Boundary %"],

    reverse=True

)

bowling["PP_N"] = normalize(

    bowling["PP Economy"],

    reverse=True

)

bowling["Middle_N"] = normalize(

    bowling["Middle Economy"],

    reverse=True

)

bowling["Death_N"] = normalize(

    bowling["Death Economy"],

    reverse=True

)
# ==========================================================
# BOWLING RATING
# ==========================================================

bowling["Bowling Rating"] = (

    bowling["Economy_N"] * 0.25 +

    bowling["Wickets_N"] * 0.20 +

    bowling["SR_N"] * 0.15 +

    bowling["Average_N"] * 0.10 +

    bowling["Dot_N"] * 0.10 +

    bowling["Boundary_N"] * 0.08 +

    bowling["PP_N"] * 0.04 +

    bowling["Middle_N"] * 0.04 +

    bowling["Death_N"] * 0.04

)

bowling["Bowling Rating"] = bowling["Bowling Rating"].round(2)

# ==========================================================
# RATING TIERS
# ==========================================================

def rating_tier(rating):

    if rating >= 90:
        return "Elite"

    elif rating >= 80:
        return "Excellent"

    elif rating >= 70:
        return "Very Good"

    elif rating >= 60:
        return "Good"

    elif rating >= 50:
        return "Average"

    else:
        return "Below Average"

bowling["Tier"] = bowling["Bowling Rating"].apply(rating_tier)

# ==========================================================
# REMOVE NORMALIZED COLUMNS
# ==========================================================

bowling.drop(

    columns=[

        "Wickets_N",

        "Economy_N",

        "Average_N",

        "SR_N",

        "Dot_N",

        "Boundary_N",

        "PP_N",

        "Middle_N",

        "Death_N"

    ],

    inplace=True

)

# ==========================================================
# SORT BY BOWLING RATING
# ==========================================================

bowling.sort_values(

    by="Bowling Rating",

    ascending=False,

    inplace=True

)

bowling.reset_index(

    drop=True,

    inplace=True

)

# ==========================================================
# REMOVE OLD RANK
# ==========================================================

if "Rank" in bowling.columns:

    bowling.drop(

        columns=["Rank"],

        inplace=True

    )

# ==========================================================
# NEW RANK
# ==========================================================

bowling.insert(

    0,

    "Rank",

    range(

        1,

        len(bowling) + 1

    )

)

# ==========================================================
# FINAL COLUMN ORDER
# ==========================================================

columns = [

    "Rank",

    "Bowler",

    "Bowling Rating",

    "Tier",

    "Matches",

    "Wickets",

    "Balls",

    "Overs",

    "Runs Conceded",

    "Economy",

    "Average",

    "Strike Rate",

    "Dot Ball %",

    "Boundary %",

    "PP Economy",

    "Middle Economy",

    "Death Economy"

]

bowling = bowling[columns]

# ==========================================================
# SAVE OUTPUT
# ==========================================================

output_file = os.path.join(

    OUTPUT_FOLDER,

    f"bowling_rating_{SEASON}.csv"

)

bowling.to_csv(

    output_file,

    index=False

)

# ==========================================================
# SUMMARY
# ==========================================================

print()

print("=" * 60)

print("BOWLING RATING CREATED SUCCESSFULLY")

print("=" * 60)

print(f"Players Rated : {len(bowling)}")

print(f"Output File   : {output_file}")

print()

print("TOP 10 BOWLING RATINGS")

print()

print(

    bowling[

        [

            "Rank",

            "Bowler",

            "Bowling Rating",

            "Tier",

            "Wickets",

            "Economy",

            "Strike Rate"

        ]

    ].head(10)

)

print()

print("=" * 60)

print("PROCESS COMPLETED")

print("=" * 60)