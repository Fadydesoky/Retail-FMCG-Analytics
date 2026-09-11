# 🛒 Retail FMCG Sales Analytics — NTI Batch 9

[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://retail-fmcg-analytics.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](License)

## 📌 Project Overview

This project was developed as part of **NTI Batch 9 — Advanced Data Analytics**.

The project focuses on analyzing an **Indian FMCG Retail Sales dataset for 2024** to discover business insights related to sales, revenue, profitability, customer behavior, store performance, and inventory.

The project combines:

- 📊 Exploratory Data Analysis (EDA)
- 🧹 Data Quality & Cleaning
- 📈 Business Analytics & Visualization
- 🤖 Regression-based Machine Learning
- 📉 Model Evaluation
- 🌐 Interactive Streamlit Deployment

## 🎯 Project Objectives

The main objectives are to:

1. Analyze sales and profitability across FMCG categories and brands.
2. Compare online, offline, and omnichannel performance.
3. Understand customer and loyalty behavior.
4. Explore inventory and stockout-related patterns.
5. Evaluate store-format efficiency.
6. Build a regression model to predict **Margin**.
7. Deploy the analytical solution as an interactive web application.

## 🗂️ Dataset

**Dataset:** Indian FMCG Retail Sales — 2024

- **Records:** 100,000
- **Variables:** 21
- **Period:** Full year 2024
- **Domain:** FMCG Retail
- **Target Variable:** `Margin`

The dataset contains information related to products, customers, sales, revenue, cost, stores, cities, sales channels, payment methods, loyalty, inventory, reorder points, lead times, and dates.

## 🔍 Key Business Questions

The analysis addresses questions such as:

- Which product categories and brands are the most profitable?
- How do online and offline channels compare?
- How does loyalty behavior relate to purchasing patterns?
- Which products or stores may face higher inventory risk?
- Which store formats perform more efficiently?

## 🧠 Machine Learning

The modeling workflow includes:

1. Target and leakage/redundant columns removal.
2. Feature preparation and categorical encoding.
3. Missing-value handling.
4. 80/20 train-test split.
5. Feature scaling.
6. Regression model training.
7. Evaluation using:
   - MAE
   - MSE
   - RMSE
   - R²

### Final Deployment Model

**Linear Regression**

| Metric | Score |
|---|---:|
| MAE | 19.28 |
| RMSE | 27.64 |
| R² | 0.863 |

> The deployed model predicts **Margin** from the available business and transactional features.

## 📊 Streamlit Application

The deployed application contains five main sections:

### 🏠 Overview
High-level KPIs and an overview of the FMCG dataset.

### 📊 Analytics
Interactive business visualizations covering sales, profitability, customers, channels, and stores.

### 🧹 Data Quality
Exploration of missing values, duplicates, and dataset quality indicators.

### 🤖 Machine Learning
Model information, evaluation metrics, and the regression workflow.

### 🔮 Prediction
Interactive **Margin Prediction** using the trained model.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data manipulation & analysis |
| NumPy | Numerical computing |
| Scikit-learn | Machine Learning |
| Plotly | Interactive visualization |
| Streamlit | Web application & deployment |
| Git & GitHub | Version control |
| Power BI | Business intelligence & dashboarding |

## 📁 Project Structure

```text
Retail-FMCG-Analytics/
│
├── app.py                 # Streamlit application
├── data.csv               # FMCG dataset
├── model.pkl              # Trained ML pipeline
├── model_info.json        # Model metadata & metrics
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── LICENSE                # MIT License
```

## 🚀 Run Locally

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Fadydesoky/Retail-FMCG-Analytics.git
cd Retail-FMCG-Analytics

pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Live Demo

**Streamlit Application:**

https://retail-fmcg-analytics.streamlit.app/

## 👥 Prepared By

### NTI Batch 9 — Advanced Data Analytics

1. **Fady Desoky Saeed Abdelaziz**
2. **Marwan Tamer Mohamed Ahmed**
3. **Farah Ali Said Ali**
4. **Maria Ayman Maurice Nashed**

## 📜 License

This project is licensed under the **MIT License**.

See the [License](License) file for details.

---

### ⭐ NTI Batch 9 — Advanced Data Analytics

**Retail FMCG Sales Analytics | 2024**
