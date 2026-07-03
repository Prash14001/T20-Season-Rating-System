# 🏏 T20 Season Rating System
A Python-based cricket analytics project that generates season-wise batting and bowling ratings from ball-by-ball IPL data.
Dataset: Ball-by-ball IPL data (not included in this repository). The project is designed to process compatible ball-by-ball datasets and generate season-wise batting and bowling metrics and ratings.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Domain](https://img.shields.io/badge/Domain-Cricket%20Analytics-orange)

---

# 📖 Project Overview

The **T20 Cricket Analytics & Season Rating System** is a Python-based analytics project designed to objectively evaluate batting and bowling performances over an IPL season.

Rather than relying only on traditional statistics such as **Runs**, **Strike Rate**, or **Wickets**, this project combines multiple performance indicators into a single season rating using **Min-Max Normalization** and a **weighted scoring model**.

The system processes ball-by-ball data, calculates advanced player metrics, filters qualified players, generates season ratings, and exports the results as CSV reports.

---

# 🎯 Objectives

- Build a complete cricket analytics pipeline.
- Generate advanced batting metrics.
- Generate advanced bowling metrics.
- Develop an objective batting rating model.
- Develop an objective bowling rating model.
- Produce season-wise player rankings.

---

# 🏗 Project Workflow

```text
                  Ball-by-Ball IPL Data
                           │
                           ▼
                  Python Data Processing
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
 Batting Metrics Engine               Bowling Metrics Engine
        │                                     │
        ▼                                     ▼
 Batting Rating Engine               Bowling Rating Engine
        │                                     │
        └──────────────────┬──────────────────┘
                           ▼
                  Season Rating Reports
```

---

# 📂 Repository Structure

```text
T20-Cricket-Analytics-Season-Rating-System

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

The batting metrics engine calculates:

- Matches
- Innings
- Runs
- Balls Faced
- Batting Average
- Strike Rate
- Dot Ball %
- Boundary %
- Strike Rotation %
- Powerplay Strike Rate
- Middle Overs Strike Rate
- Death Overs Strike Rate

---

# 🏏 Bowling Metrics

The bowling metrics engine calculates:

- Matches
- Wickets
- Balls Bowled
- Economy
- Bowling Average
- Bowling Strike Rate
- Dot Ball %
- Boundary %
- Powerplay Economy
- Middle Overs Economy
- Death Overs Economy

---

# 📊 Player Qualification

To ensure fair comparison, only qualified players are included in the rating system.

### Batting

Minimum balls faced during the season.

### Bowling

Minimum balls bowled during the season.

(Players not meeting the qualification criteria are excluded from the rating calculations.)

---

# 📈 Rating Methodology

The rating model follows these steps:

1. Calculate season metrics.
2. Filter qualified players.
3. Normalize every metric using **Min-Max Normalization**.
4. Apply weighted scores.
5. Calculate the final season rating.
6. Rank all qualified players.

---

# 📐 Normalization Method

Every metric is converted to a common scale between **0 and 100**.

### Higher is Better

Examples:
- Runs
- Average
- Strike Rate
- Dot Ball %
- Strike Rotation %
- Boundary %

Formula:

Normalized Score =
(Value − Minimum) / (Maximum − Minimum)

---

### Lower is Better

Examples:

- Economy
- Bowling Average
- Bowling Strike Rate
- Boundary %

Formula:

Normalized Score =
(Maximum − Value) / (Maximum − Minimum)

---

# 🏏 Batting Rating Model

| Metric | Weight |
|---------|--------|
| Runs | 25% |
| Average | 20% |
| Strike Rate | 20% |
| Dot Ball % | 10% |
| Boundary % | 10% |
| Strike Rotation % | 5% |
| Powerplay Strike Rate | 2% |
| Middle Overs Strike Rate | 5% |
| Death Overs Strike Rate | 3% |
| **Total** | **100%** |

---

# 🏏 Bowling Rating Model

| Metric | Weight |
|---------|--------|
| Economy | 25% |
| Wickets | 20% |
| Bowling Strike Rate | 15% |
| Bowling Average | 10% |
| Dot Ball % | 10% |
| Boundary % | 8% |
| Powerplay Economy | 4% |
| Middle Overs Economy | 4% |
| Death Overs Economy | 4% |
| **Total** | **100%** |

---

# 🏆 Rating Categories

| Rating | Category |
|---------|----------|
| 85 – 100 | Elite |
| 70 – 84 | Very Good |
| 55 – 69 | Good |
| 40 – 54 | Average |
| Below 40 | Needs Improvement |

---

# ⚙ Technologies Used

- Python
- Pandas
- CSV Processing
- Git
- GitHub

---

# 🚀 Running the Project

Generate Batting Metrics

```bash
python batting_metrics.py
```

Generate Batting Rating

```bash
python batting_rating.py
```

Generate Bowling Metrics

```bash
python bowling_metrics.py
```

Generate Bowling Rating

```bash
python bowling_rating.py
```

---

# 📁 Output

The system generates:

- Batting Metrics CSV
- Batting Rating CSV
- Bowling Metrics CSV
- Bowling Rating CSV

Each report contains ranked season-wise player performances.

---

# 📌 Dataset

This project is designed to process IPL ball-by-ball datasets.

The raw dataset is **not included** in this repository.

---

# 🔮 Future Improvements

- Fielding Rating System
- Venue Adjustments
- Opposition Strength Adjustments
- Match Situation Index
- Interactive Dashboard
- Power BI Integration
- Streamlit Web Application

---

# 👨‍💻 Author

**Prashanth**

Python | Cricket Analytics | Data Analytics

---

# 📜 License

This project is intended for educational and analytical purposes.

---



