import os
import pandas as pd

# ==========================================================
# SETTINGS
# ==========================================================

OUTPUT_FOLDER = "outputs"
QUALIFICATION_BALLS = 100

# ==========================================================
# AVAILABLE SEASONS
# ==========================================================

available_files = sorted(

    [

        f.replace("batting_metrics_", "").replace(".csv", "")

        for f in os.listdir(OUTPUT_FOLDER)

        if f.startswith("batting_metrics_")

    ]

)

print("=" * 60)
print("             T20 BATTING RATING ENGINE")
print("=" * 60)

print("\nAvailable Seasons:\n")

for season in available_files:
    print(f"  {season}")

SEASON = input("\nEnter Season: ").strip()

input_file = os.path.join(

    OUTPUT_FOLDER,

    f"batting_metrics_{SEASON}.csv"

)

if not os.path.exists(input_file):

    print("\nMetrics file not found!")
    exit()

# ==========================================================
# LOAD METRICS
# ==========================================================

batting = pd.read_csv(input_file)

# Remove Rank from metrics file
# Rating will create its own Rank.

if "Rank" in batting.columns:

    batting.drop(

        columns=["Rank"],

        inplace=True

    )

print()

print("Season Selected :", SEASON)
print("Players Loaded  :", len(batting))

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

required_columns = [

    "Batter",

    "Runs",

    "Balls",

    "Average",

    "Strike Rate",

    "Dot Ball %",

    "Boundary %",

    "Strike Rotation %",

    "PP SR",

    "Middle SR",

    "Death SR"

]

missing = [

    col

    for col in required_columns

    if col not in batting.columns

]

if len(missing) > 0:

    print("\nERROR!")
    print("The following required columns are missing:\n")

    for col in missing:
        print("-", col)

    exit()

# ==========================================================
# QUALIFIED BATTERS
# ==========================================================

batting = batting[

    batting["Balls"] >= QUALIFICATION_BALLS

].copy()

print("Qualified       :", len(batting))

# ==========================================================
# NORMALIZATION FUNCTION
# ==========================================================

def normalize(series, reverse=False):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:

        return pd.Series(

            [100] * len(series),

            index=series.index

        )

    score = (

        (series - minimum)

        /

        (maximum - minimum)

    ) * 100

    if reverse:

        score = 100 - score

    return score

# ==========================================================
# NORMALIZED SCORES
# ==========================================================

batting["Runs Score"] = normalize(

    batting["Runs"]

)

batting["Average Score"] = normalize(

    batting["Average"]

)

batting["Strike Rate Score"] = normalize(

    batting["Strike Rate"]

)

batting["Dot Ball Score"] = normalize(

    batting["Dot Ball %"],

    reverse=True

)

batting["Boundary Score"] = normalize(

    batting["Boundary %"]

)

batting["Rotation Score"] = normalize(

    batting["Strike Rotation %"]

)

batting["PP Score"] = normalize(

    batting["PP SR"]

)

batting["Middle Score"] = normalize(

    batting["Middle SR"]

)

batting["Death Score"] = normalize(

    batting["Death SR"]

)

# ==========================================================
# CONTINUE IN PART 2
# ==========================================================
# ==========================================================
# BATTING RATING (LOCKED)
# ==========================================================

batting["Batting Rating"] = (

    batting["Runs Score"] * 0.25 +

    batting["Average Score"] * 0.20 +

    batting["Strike Rate Score"] * 0.20 +

    batting["Dot Ball Score"] * 0.10 +

    batting["Boundary Score"] * 0.10 +

    batting["Rotation Score"] * 0.05 +

    batting["PP Score"] * 0.02 +

    batting["Middle Score"] * 0.05 +

    batting["Death Score"] * 0.03

)

# ==========================================================
# ROUND RATING
# ==========================================================

batting["Batting Rating"] = batting["Batting Rating"].round(2)

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

batting["Tier"] = batting["Batting Rating"].apply(rating_tier)

# ==========================================================
# SORT
# ==========================================================

batting = batting.sort_values(

    by="Batting Rating",

    ascending=False

)

# ==========================================================
# RANK
# ==========================================================

batting.reset_index(

    drop=True,

    inplace=True

)

batting.insert(

    0,

    "Rank",

    range(1, len(batting) + 1)

)

# ==========================================================
# FINAL COLUMNS
# ==========================================================

batting = batting[

    [

        "Rank",

        "Batter",

        "Batting Rating",

        "Tier",

        "Runs",

        "Average",

        "Strike Rate",

        "Dot Ball %",

        "Boundary %",

        "Strike Rotation %",

        "PP SR",

        "Middle SR",

        "Death SR"

    ]

]

# ==========================================================
# SAVE
# ==========================================================

output_file = os.path.join(

    OUTPUT_FOLDER,

    f"batting_rating_{SEASON}.csv"

)

batting.to_csv(

    output_file,

    index=False

)

# ==========================================================
# SUMMARY
# ==========================================================

print()

print("=" * 60)

print("BATTING RATING CREATED SUCCESSFULLY")

print("=" * 60)

print(f"Players Rated : {len(batting)}")

print(f"Output File   : {output_file}")

print()

print("TOP 10 BATTING RATINGS")

print()

print(

    batting[

        [

            "Rank",

            "Batter",

            "Batting Rating",

            "Tier",

            "Runs",

            "Average",

            "Strike Rate"

        ]

    ].head(10)

)

print()

print("=" * 60)

print("PROCESS COMPLETED")

print("=" * 60)