# 📊 Vendor Performance Data Analytics
Analyze, visualize, and track vendor performance using Python, SQLite, and Jupyter Notebooks. Includes data ingestion, transformation, KPIs, and visual insights.

## 📚 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Visualizations](#visualizations)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview
This project provides an end-to-end pipeline to analyze vendor performance using raw CSV files. It includes:
- Data ingestion to a SQLite database
- KPI generation (Profit Margin, Stock Turnover, etc.)
- Data exploration
- Statistical visualization and confidence intervals

## ✅ Features
- 📥 Ingest CSVs into SQLite (`ingestion_db.py`)
- 🧮 Create vendor performance summary (`get_vendor_summary.py`)
- 📊 Visual analysis of top/low vendors (`vendor_performance_analysis.ipynb`)
- 🧼 Cleans and transforms data
- 📈 Generates KPIs for decision-making
- 🧾 Logging for all major steps

## 🗂 Project Structure
├── dataset/
│   └── data/
│       └── [CSV files]
├── logs/
│   └── ingestion_db.log
├── get_vendor_summary.py
├── ingestion_db.py
├── Exploratory data analysis.ipynb
├── vendor_performance_analysis.ipynb
├── inventory.db
└── README.md

## 🧪 Requirements
- Python 3.6+
- pandas
- sqlalchemy
- sqlite3
- matplotlib
- seaborn
- scipy
- Jupyter Notebook

## ⚙️ Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/vendor-performance-analytics.git
cd vendor-performance-analytics

# Install dependencies
pip install -r requirements.txt  # if you prepare one

# Or manually install
pip install pandas sqlalchemy matplotlib seaborn scipy

## 🚀 Usage
### Step 1: Ingest CSV Data
```bash
python ingestion_db.py
###Step 2: Create Vendor Summary
python get_vendor_summary.py
###Step 3: Run EDA & Visualization
Launch Jupyter and open:
Exploratory data analysis.ipynb
vendor_performance_analysis.ipynb

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](LICENSE)




















