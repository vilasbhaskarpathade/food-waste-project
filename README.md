# 🥗 Food Wastage Management System

> **Connecting surplus food with people who need it most** — a data-driven platform bridging food providers and receivers to reduce waste and fight hunger.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)](https://vilasbhaskarpathade-food-waste-project-app-mvihnj.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

---

## 📌 Overview

Every day, **tonnes of surplus food** are discarded by restaurants, grocery stores, supermarkets, and catering services — while millions face food insecurity. This project tackles that gap head-on.

The **Food Wastage Management System** is a centralized platform that:
- Lets **food providers** list their surplus food items
- Lets **receivers** (NGOs, individuals in need) discover and claim available food
- Delivers **data-driven insights** to optimize redistribution efficiency

---

## 🌐 Live Demo

🔗 **Try it now →** https://vilasbhaskarpathade-food-waste-project-app-mvihnj.streamlit.app/

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit |
| **Backend / Logic** | Python |
| **Database** | SQLite (production), MySQL (development) |
| **ORM** | SQLAlchemy |
| **Data Processing** | Pandas |
| **Visualizations** | Plotly |
| **Analysis / EDA** | Jupyter Notebook |
| **Query Language** | SQL |

---

## 📂 Project Workflow

```
CSV Files (Raw Data)
        ↓
Data Cleaning & EDA  ──→  Jupyter Notebook
        ↓
SQL Database  ──────────→  SQLite / MySQL
        ↓
Streamlit App  ─────────→  Dashboard · Analytics · CRUD
```

---

## ✨ Features

### 📊 Interactive Dashboard
Real-time KPIs and visual summaries including:
- Total food quantity available
- Total registered providers & receivers
- Total claims made
- City-wise food distribution
- Food type & claim status breakdowns

### 📋 Food Listings Management
- Browse all active food listings
- Search and filter by item, city, or category
- Analyze meal types and food categories at a glance

### 🔍 SQL Analysis Queries
Pre-built analytical queries covering:
- Total food quantity across listings
- Top contributing providers
- Food type distribution
- Claim status percentages
- Receiver activity patterns
- Meal type trends
- Monthly claim trends
- City-wise listing analysis

### ⚙️ CRUD Operations
Full create-read-update-delete support:
- **Add** new food listings
- **Update** existing records
- **Delete** expired or claimed entries
- **View** live database state in real time

### 📈 Data Visualizations
Interactive Plotly charts:
- Bar charts · Pie charts · Line charts
- Trend analysis & distribution analysis

---

## 📁 Dataset

Four CSV datasets power the system:

| Dataset | Description |
|---|---|
| `providers_data.csv` | Food provider details (restaurants, stores, etc.) |
| `receivers_data.csv` | Receiver details (NGOs, individuals) |
| `food_listings_data.csv` | Available surplus food listings |
| `claims_data.csv` | Food claim records and statuses |

---

## 🗄️ Database Design

**4 relational tables** connected via foreign keys:

```
Providers ──────────────────┐
  provider_id (PK)           │
  name, type, city, contact  │
                             ↓
Food Listings ───────────→ Claims
  listing_id (PK)            claim_id (PK)
  food_name, quantity        food_id (FK)
  expiry_date, food_type     receiver_id (FK)
  meal_type                  claim_status
  provider_id (FK)           timestamp

Receivers ──────────────────┘
  receiver_id (PK)
  name, type, city, contact
```

---

## 📊 Key Insights

Analysis of the data revealed several important patterns:

- 🏆 **Provider concentration** — A small number of providers contribute a disproportionately large share of food
- 🌆 **City-level imbalance** — Certain cities have high food availability but low claim rates
- 🥦 **Vegetarian dominance** — Vegetarian food makes up the majority of listings
- 🍽️ **Meal timing** — Lunch and dinner are the most commonly listed meal types
- ⏱️ **Expiry urgency** — Food nearing expiry requires prioritized allocation
- 📉 **Supply-demand gap** — Some regions have surplus supply with insufficient receiver engagement

### Advanced Analytics
- Supply vs. demand gap mapping
- High food wastage risk zone identification
- Provider efficiency scoring
- Receiver reliability metrics
- Monthly claim trend forecasting
- Expiry risk analysis & resource optimization

---

## 🚧 Challenges Faced

| Challenge | How It Was Handled |
|---|---|
| Data quality issues | Thorough cleaning & null handling in Jupyter |
| Multi-table relationships | Careful foreign key design and join queries |
| MySQL → SQLite migration | Rewrote queries for SQLite compatibility |
| Streamlit Cloud deployment | Switched to file-based SQLite for portability |
| Database compatibility | Environment-aware database configuration |

---

## ▶️ Run Locally

### 1. Clone the Repository
```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
cd food-wastage-management-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the App
```bash
streamlit run app.py
```

### Requirements
```
streamlit
pandas
sqlalchemy
plotly
```

---

## 🔮 Future Enhancements

- [ ] 🤖 AI-based food demand prediction
- [ ] 📍 Real-time food tracking & routing
- [ ] 📱 Mobile application (Android / iOS)
- [ ] 🔔 Automated expiry & availability notifications
- [ ] 🌍 Multi-city expansion & geo-visualization
- [ ] 📧 Provider-receiver direct messaging

---

## 🎯 Learning Outcomes

This project provided hands-on experience with:
- Relational database design and SQL query writing
- Data analysis and EDA using Pandas
- Building interactive dashboards with Streamlit
- Data visualization with Plotly
- Cloud deployment on Streamlit Cloud
- End-to-end analytical project workflow

---

## 👨‍💻 Developed By

**Vilas Pathade**
B.Tech — Information Technology

*Passionate about Data Analytics, Data Science, and AI/ML*

---

> *"The world produces enough food to feed everyone. The challenge is distribution — and data can solve it."*
