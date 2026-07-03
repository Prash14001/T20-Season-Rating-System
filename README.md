# 🏏 T20 Season Rating System
A Python-based cricket analytics project that generates season-wise batting and bowling ratings from ball-by-ball IPL data.
Dataset: Ball-by-ball IPL data (not included in this repository). The project is designed to process compatible ball-by-ball datasets and generate season-wise batting and bowling metrics and ratings.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Analytics](https://img.shields.io/badge/Domain-Cricket%20Analytics-orange)

---

# 📖 Overview

The **T20 Season Rating System** is an end-to-end cricket analytics project developed in Python to objectively evaluate player performances across an IPL season.

Instead of relying solely on traditional statistics such as **Runs**, **Strike Rate**, or **Wickets**, this project combines multiple batting and bowling metrics into a single season rating using **Min-Max Normalization** and a **weighted scoring model**.

The system automatically processes ball-by-ball data, calculates advanced player metrics, ranks qualified players, and exports the results as CSV files.

---

# 🎯 Project Objectives

- Build a complete analytics pipeline from raw ball-by-ball cricket data.
- Calculate advanced batting performance metrics.
- Calculate advanced bowling performance metrics.
- Develop objective batting and bowling rating models.
- Generate season-wise player rankings.
- Produce reproducible analytics outputs using Python.

---

# 🏗️ Project Workflow

```text
                     Ball-by-Ball IPL Data
                              │
                              ▼
                    Python Data Processing
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
     Batting Metrics Engine             Bowling Metrics Engine
            │                                   │
            ▼                                   ▼
     Batting Rating Engine             Bowling Rating Engine
            │                                   │
            └─────────────────┬─────────────────┘
                              ▼
                    Season-wise CSV Outputs
```

---

# 📂 Repository Structure

```text
T20-Season-Rating-System
│
├── batting_metrics.py
├── batting_rating.py
├── bowling_metrics.py
├── bowling_rating.py
│
├── outputs/
│
├── presentation/
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🏏 Batting Metrics

The Batting Metrics Engine calculates the following performance indicators:

| Metric | Description |
|----------|-------------|
| Matches | Matches Played |
| Innings | Innings Batted |
| Runs | Total Runs Scored |
| Balls Faced | Balls Faced |
| Average | Batting Average |
| Strike Rate | Runs per 100 Balls |
| Dot Ball % | Percentage of Dot Balls |
| Boundary % | Percentage of Boundaries |
| Powerplay Strike Rate | Strike Rate (Overs 1–6) |
| Middle Overs Strike Rate | Strike Rate (Overs 7–15) |
| Death Overs Strike Rate | Strike Rate (Overs 16–20) |
| 30+ Scores | Innings of 30 or More |
| 50+ Scores | Half-centuries |
| 100s | Centuries |
| Highest Score | Highest Individual Score |

---

# 🏏 Bowling Metrics

The Bowling Metrics Engine calculates:

| Metric | Description |
|----------|-------------|
| Matches | Matches Played |
| Wickets | Total Wickets |
| Balls Bowled | Legal Deliveries |
| Economy | Runs Conceded per Over |
| Average | Runs Conceded per Wicket |
| Strike Rate | Balls per Wicket |
| Dot Ball % | Percentage of Dot Balls |
| Boundary % | Percentage of Boundary Balls |
| Powerplay Economy | Economy (Overs 1–6) |
| Middle Overs Economy | Economy (Overs 7–15) |
| Death Overs Economy | Economy (Overs 16–20) |

---

# 📊 Batting Rating Model

The Batting Rating is calculated using normalized metrics and weighted scoring.

| Metric | Weight |
|----------|--------|
| Batting Average | 20% |
| Strike Rate | 20% |
| Runs | 15% |
| Dot Ball % | 10% |
| Boundary % | 10% |
| Powerplay Strike Rate | 10% |
| Middle Overs Strike Rate | 5% |
| Death Overs Strike Rate | 10% |

---

# 📊 Bowling Rating Model

The Bowling Rating is calculated using normalized metrics and weighted scoring.

| Metric | Weight |
|----------|--------|
| Economy | 25% |
| Wickets | 20% |
| Strike Rate | 15% |
| Bowling Average | 10% |
| Dot Ball % | 10% |
| Boundary % | 8% |
| Powerplay Economy | 4% |
| Middle Overs Economy | 4% |
| Death Overs Economy | 4% |

---

# ⚙️ Technologies Used

- Python
- Pandas
- CSV Processing
- Git
- GitHub

---

# 🚀 How to Run

### Generate Batting Metrics

```bash
python batting_metrics.py
```

### Generate Batting Ratings

```bash
python batting_rating.py
```

### Generate Bowling Metrics

```bash
python bowling_metrics.py
```

### Generate Bowling Ratings

```bash
python bowling_rating.py
```

---

# 📈 Sample Output

### Batting Ratings

```text
Rank   Batter              Rating
1      Shubman Gill        79.93
2      Suryakumar Yadav    73.58
3      Heinrich Klaasen    71.73
```

### Bowling Ratings

```text
Rank   Bowler              Rating
1      Anrich Nortje       76.50
2      Harshal Patel       72.82
3      Avesh Khan          72.26
```

---

# 📊 Rating Methodology

```text
Load Ball-by-Ball Data
          │
          ▼
Calculate Player Metrics
          │
          ▼
Qualification Filter
          │
          ▼
Min-Max Normalization
          │
          ▼
Weighted Rating Model
          │
          ▼
Generate Season Ratings
          │
          ▼
Export CSV Reports
```

---

# 📁 Output

The project generates season-wise CSV reports for:

- Batting Metrics
- Batting Ratings
- Bowling Metrics
- Bowling Ratings

---

# 📌 Dataset

This project is designed to work with **ball-by-ball IPL datasets**.

The raw dataset is **not included** in this repository. Users can supply a compatible ball-by-ball dataset to generate metrics and ratings.

---

# 🔮 Future Improvements

- Fielding Rating System
- Venue-adjusted Ratings
- Opposition Strength Adjustment
- Match Situation Index
- Interactive Dashboard (Streamlit)
- Performance Visualizations
- Web Application

---

# 👨‍💻 Author

**Prashanth**

Python • Cricket Analytics • Data Analytics

---

# 🙏 Acknowledgements

This project was developed as a personal cricket analytics initiative to explore data-driven player evaluation using Python and statistical methods.

---

