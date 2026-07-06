import os
import pandas as pd

# ==========================================================
# SETTINGS
# ==========================================================

INPUT_FILE = "outputs/ball_by_ball.csv"
OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(
    INPUT_FILE,
    dtype={"season": str},
    low_memory=False
)

# ==========================================================
# SELECT SEASON
# ==========================================================

available_seasons = sorted(df["season"].dropna().unique())

print("=" * 60)
print("             T20 BATTING METRICS ENGINE")
print("=" * 60)

print("\nAvailable Seasons:\n")

for season in available_seasons:
    print(f"  {season}")

print("  ALL")

SEASON = input("\nEnter Season (or ALL): ").strip()

if SEASON.upper() == "ALL":

    season_df = df.copy()
    OUTPUT_NAME = "ALL"

else:

    if SEASON not in available_seasons:
        print("\nInvalid Season!")
        exit()

    season_df = df[df["season"] == SEASON]
    OUTPUT_NAME = SEASON

print(f"\nSeason Selected : {OUTPUT_NAME}")
print(f"Deliveries      : {len(season_df)}")

# ==========================================================
# REMOVE WIDES (LEGAL DELIVERIES)
# ==========================================================

legal_deliveries = season_df[
    season_df["extras_type"] != "wides"
]

# ==========================================================
# BASIC AGGREGATIONS
# ==========================================================

runs = (
    season_df
    .groupby("batter")["batter_runs"]
    .sum()
)

balls = (
    legal_deliveries
    .groupby("batter")
    .size()
)

outs = (
    season_df[
        season_df["player_out"] != ""
    ]
    .groupby("player_out")
    .size()
)

fours = (
    season_df[
        season_df["batter_runs"] == 4
    ]
    .groupby("batter")
    .size()
)

sixes = (
    season_df[
        season_df["batter_runs"] == 6
    ]
    .groupby("batter")
    .size()
)

dots = (
    legal_deliveries[
        legal_deliveries["batter_runs"] == 0
    ]
    .groupby("batter")
    .size()
)

singles = (
    legal_deliveries[
        legal_deliveries["batter_runs"] == 1
    ]
    .groupby("batter")
    .size()
)

doubles = (
    legal_deliveries[
        legal_deliveries["batter_runs"] == 2
    ]
    .groupby("batter")
    .size()
)

triples = (
    legal_deliveries[
        legal_deliveries["batter_runs"] == 3
    ]
    .groupby("batter")
    .size()
)

# ==========================================================
# INNINGS WISE DATA
# ==========================================================

innings_scores = (
    season_df
    .groupby(
        ["match_id", "batter"]
    )["batter_runs"]
    .sum()
    .reset_index()
)

innings = (
    innings_scores
    .groupby("batter")
    .size()
)

highest_score = (
    innings_scores
    .groupby("batter")["batter_runs"]
    .max()
)

fifties = (
    innings_scores[
        innings_scores["batter_runs"] >= 50
    ]
    .groupby("batter")
    .size()
)

# ==========================================================
# PHASE STRIKE RATE FUNCTION
# ==========================================================

def phase_strike_rate(data):

    phase_runs = (
        data
        .groupby("batter")["batter_runs"]
        .sum()
    )

    phase_balls = (
        data[
            data["extras_type"] != "wides"
        ]
        .groupby("batter")
        .size()
    )

    return (
        phase_runs /
        phase_balls.replace(0, 1)
    ) * 100

# ==========================================================
# PHASE STRIKE RATES
# ==========================================================

pp_sr = phase_strike_rate(
    season_df[
        season_df["phase"] == "Powerplay"
    ]
)

middle_sr = phase_strike_rate(
    season_df[
        season_df["phase"] == "Middle"
    ]
)

death_sr = phase_strike_rate(
    season_df[
        season_df["phase"] == "Death"
    ]
)

# ==========================================================
# CREATE DATAFRAME
# ==========================================================

batting = pd.DataFrame({

    "Season": OUTPUT_NAME,

    "Runs": runs,

    "Innings": innings,

    "Balls": balls,

    "Outs": outs,

    "Fours": fours,

    "Sixes": sixes,

    "Dots": dots,

    "Singles": singles,

    "Doubles": doubles,

    "Triples": triples,

    "Highest Score": highest_score,

    "50+ Scores": fifties,

    "PP SR": pp_sr,

    "Middle SR": middle_sr,

    "Death SR": death_sr

}).fillna(0)

numeric_columns = batting.columns.drop("Season")

batting[numeric_columns] = batting[
    numeric_columns
].apply(pd.to_numeric)

# ==========================================================
# ADVANCED METRICS
# ==========================================================

# Batting Average
# If never dismissed, average equals total runs.

batting["Average"] = batting.apply(
    lambda x: x["Runs"]
    if x["Outs"] == 0
    else x["Runs"] / x["Outs"],
    axis=1
)

# Strike Rate

batting["Strike Rate"] = (
    batting["Runs"] /
    batting["Balls"].replace(0, 1)
) * 100

# Dot Ball %

batting["Dot Ball %"] = (
    batting["Dots"] /
    batting["Balls"].replace(0, 1)
) * 100

# Boundary Runs

batting["Boundary Runs"] = (
    batting["Fours"] * 4 +
    batting["Sixes"] * 6
)

# Boundary %

batting["Boundary %"] = (
    batting["Boundary Runs"] /
    batting["Runs"].replace(0, 1)
) * 100

# Balls Per Boundary

batting["Balls per Boundary"] = (
    batting["Balls"] /
    (
        batting["Fours"] +
        batting["Sixes"]
    ).replace(0, 1)
)

# Strike Rotation %

batting["Strike Rotation %"] = (
    (
        batting["Singles"] +
        batting["Doubles"] +
        batting["Triples"]
    )
    /
    batting["Balls"].replace(0, 1)
) * 100

# ==========================================================
# QUALIFICATION FLAG
# ==========================================================

# Qualified if batter has faced at least
# 100 legal deliveries.

batting["Qualified"] = (
    batting["Balls"] >= 100
)

# ==========================
# CONTINUE IN PART 2
# ==========================
# ==========================================================
# REMOVE HELPER COLUMNS
# ==========================================================

batting.drop(
    columns=[
        "Dots",
        "Singles",
        "Doubles",
        "Triples",
        "Boundary Runs"
    ],
    inplace=True
)

# ==========================================================
# ROUND VALUES
# ==========================================================

round_columns = [

    "Average",

    "Strike Rate",

    "Dot Ball %",

    "Boundary %",

    "Balls per Boundary",

    "Strike Rotation %",

    "PP SR",

    "Middle SR",

    "Death SR"

]

batting[round_columns] = batting[
    round_columns
].round(2)

# ==========================================================
# REORDER FINAL COLUMNS
# ==========================================================

batting = batting[

    [

        "Season",

        "Runs",

        "Innings",

        "Balls",

        "Outs",

        "Average",

        "Strike Rate",

        "Fours",

        "Sixes",

        "Dot Ball %",

        "Boundary %",

        "Balls per Boundary",

        "Strike Rotation %",

        "PP SR",

        "Middle SR",

        "Death SR",

        "Highest Score",

        "50+ Scores",

        "Qualified"

    ]

]

# ==========================================================
# SORT
# ==========================================================

batting = batting.sort_values(

    by="Runs",

    ascending=False

)

# ==========================================================
# ADD RANK
# ==========================================================

batting.insert(

    0,

    "Rank",

    range(1, len(batting) + 1)

)


# ==========================================================
# PLAYER NAME COLUMN
# ==========================================================

batting.reset_index(inplace=True)

batting.rename(

    columns={

        "index": "Batter"

    },

    inplace=True

)

columns = ["Rank", "Batter"] + [
    col for col in batting.columns
    if col not in ["Rank", "Batter"]
]

batting = batting[columns]

# ==========================================================
# SAVE
# ==========================================================

output_file = os.path.join(

    OUTPUT_FOLDER,

    f"batting_metrics_{OUTPUT_NAME}.csv"

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
print("BATTING METRICS CREATED SUCCESSFULLY")
print("=" * 60)

print(f"Players Analysed : {len(batting)}")
print(f"Output File      : {output_file}")

print()
print("TOP 10 RUN SCORERS")
print()

print(

    batting[
        [
            "Rank",
            "Batter",
            "Runs",
            "Average",
            "Strike Rate",
            "Qualified"
        ]
    ].head(10)

)
print()

print("=" * 60)
print("PROCESS COMPLETED")
print("=" * 60)