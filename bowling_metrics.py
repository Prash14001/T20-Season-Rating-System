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
print("             T20 BOWLING METRICS ENGINE")
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

    season_df = df[
        df["season"] == SEASON
    ].copy()

    OUTPUT_NAME = SEASON

print("\nSeason Selected :", OUTPUT_NAME)
print("Deliveries      :", len(season_df))

# ==========================================================
# LEGAL DELIVERIES
# ==========================================================

legal_deliveries = season_df[
    ~season_df["extras_type"].fillna("").str.lower().isin(
        ["wides", "noballs", "no ball", "no_ball"]
    )
].copy()

# ==========================================================
# RUNS CONCEDED
# (Exclude Byes & Leg Byes)
# ==========================================================

season_df["Bowler Runs"] = season_df["batter_runs"]

season_df.loc[
    season_df["extras_type"]
    .fillna("")
    .str.lower()
    .isin(["wides", "noballs", "no ball", "no_ball"]),
    "Bowler Runs"
] += season_df["extras"]

runs_conceded = (

    season_df

    .groupby("bowler")["Bowler Runs"]

    .sum()

)

# ==========================================================
# MATCHES
# ==========================================================

matches = (

    season_df

    .groupby("bowler")["match_id"]

    .nunique()

)

# ==========================================================
# LEGAL BALLS
# ==========================================================

balls = (

    legal_deliveries

    .groupby("bowler")

    .size()

)

# ==========================================================
# WICKETS
# (Only wickets credited to bowler)
# ==========================================================

bowler_wickets = [

    "bowled",

    "caught",

    "lbw",

    "stumped",

    "caught and bowled",

    "hit wicket"

]

wickets = (

    season_df[

        season_df["dismissal_type"]

        .fillna("")

        .str.lower()

        .isin(bowler_wickets)

    ]

    .groupby("bowler")

    .size()

)

# ==========================================================
# DOT BALLS
# ==========================================================

dot_balls = (

    legal_deliveries[

        (legal_deliveries["batter_runs"] == 0)

        &

        (legal_deliveries["extras"] == 0)

    ]

    .groupby("bowler")

    .size()

)

# ==========================================================
# BOUNDARY BALLS
# ==========================================================

boundary_balls = (

    legal_deliveries[

        legal_deliveries["batter_runs"]

        .isin([4, 6])

    ]

    .groupby("bowler")

    .size()

)

# ==========================================================
# PHASE ECONOMY FUNCTION
# ==========================================================

def phase_economy(data):

    legal = data[
        ~data["extras_type"]
        .fillna("")
        .str.lower()
        .isin(["wides", "noballs", "no ball", "no_ball"])
    ]

    phase_runs = (

        data

        .groupby("bowler")["Bowler Runs"]

        .sum()

    )

    phase_balls = (

        legal

        .groupby("bowler")

        .size()

    )

    overs = phase_balls / 6

    economy = (

        phase_runs /

        overs.replace(0, 1)

    )

    return economy

# ==========================================================
# PHASE ECONOMY
# ==========================================================

pp = season_df[
    season_df["phase"] == "Powerplay"
]

middle = season_df[
    season_df["phase"] == "Middle"
]

death = season_df[
    season_df["phase"] == "Death"
]

pp_economy = phase_economy(pp)

middle_economy = phase_economy(middle)

death_economy = phase_economy(death)

# ==========================================================
# CREATE DATAFRAME
# ==========================================================

bowling = pd.DataFrame({

    "Season": OUTPUT_NAME,

    "Matches": matches,

    "Wickets": wickets,

    "Balls": balls,

    "Runs Conceded": runs_conceded,

    "Dot Balls": dot_balls,

    "Boundary Balls": boundary_balls,

    "PP Economy": pp_economy,

    "Middle Economy": middle_economy,

    "Death Economy": death_economy

}).fillna(0)

# IMPORTANT
# This fixes the Bowler column issue.

bowling.index.name = "Bowler"

numeric_columns = bowling.columns.drop("Season")

bowling[numeric_columns] = bowling[
    numeric_columns
].apply(pd.to_numeric)
# ==========================================================
# OVERS
# ==========================================================

bowling["Overs"] = bowling["Balls"] / 6

# ==========================================================
# ECONOMY
# ==========================================================

bowling["Economy"] = (

    bowling["Runs Conceded"] /

    bowling["Overs"].replace(0, 1)

)

# ==========================================================
# BOWLING AVERAGE
# ==========================================================

bowling["Average"] = (

    bowling["Runs Conceded"] /

    bowling["Wickets"].replace(0, 1)

)

# ==========================================================
# STRIKE RATE
# ==========================================================

bowling["Strike Rate"] = (

    bowling["Balls"] /

    bowling["Wickets"].replace(0, 1)

)

# ==========================================================
# DOT BALL %
# ==========================================================

bowling["Dot Ball %"] = (

    bowling["Dot Balls"] /

    bowling["Balls"].replace(0, 1)

) * 100

# ==========================================================
# BOUNDARY %
# ==========================================================

bowling["Boundary %"] = (

    bowling["Boundary Balls"] /

    bowling["Balls"].replace(0, 1)

) * 100

# ==========================================================
# QUALIFICATION
# ==========================================================

bowling["Qualified"] = bowling["Balls"] >= 120

# ==========================================================
# REMOVE HELPER COLUMNS
# ==========================================================

bowling.drop(

    columns=[

        "Dot Balls",

        "Boundary Balls"

    ],

    inplace=True

)

# ==========================================================
# ROUND VALUES
# ==========================================================

round_columns = [

    "Overs",

    "Economy",

    "Average",

    "Strike Rate",

    "Dot Ball %",

    "Boundary %",

    "PP Economy",

    "Middle Economy",

    "Death Economy"

]

bowling[round_columns] = bowling[
    round_columns
].round(2)

# ==========================================================
# REORDER COLUMNS
# ==========================================================

bowling = bowling[

    [

        "Season",

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

        "Death Economy",

        "Qualified"

    ]

]

# ==========================================================
# SORT
# ==========================================================

bowling = bowling.sort_values(

    by="Wickets",

    ascending=False

)

# ==========================================================
# ADD RANK
# ==========================================================

bowling.insert(

    0,

    "Rank",

    range(1, len(bowling) + 1)

)

# ==========================================================
# PLAYER NAME COLUMN
# ==========================================================

bowling.reset_index(inplace=True)

# ==========================================================
# FINAL COLUMN ORDER
# ==========================================================

bowling = bowling[

    [

        "Rank",

        "Bowler",

        "Season",

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

        "Death Economy",

        "Qualified"

    ]

]

# ==========================================================
# SAVE
# ==========================================================

output_file = os.path.join(

    OUTPUT_FOLDER,

    f"bowling_metrics_{OUTPUT_NAME}.csv"

)

bowling.to_csv(

    output_file,

    index=False

)

# ==========================================================
# SUMMARY
# ==========================================================

qualified_bowlers = bowling["Qualified"].sum()

print()

print("=" * 60)

print("BOWLING METRICS CREATED SUCCESSFULLY")

print("=" * 60)

print(f"Bowlers Analysed  : {len(bowling)}")

print(f"Qualified Bowlers : {qualified_bowlers}")

print(f"Output File       : {output_file}")

print()

print("TOP 10 WICKET TAKERS")

print()

print(

    bowling[

        [

            "Rank",

            "Bowler",

            "Wickets",

            "Economy",

            "Strike Rate",

            "Qualified"

        ]

    ].head(10)

)

print()

print("=" * 60)

print("PROCESS COMPLETED")

print("=" * 60)