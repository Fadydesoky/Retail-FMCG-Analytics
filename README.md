# Retail FMCG Sales Analytics — NTI Batch 9

Streamlit deployment for the NTI Advanced Data Analytics project.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Upload the project CSV (`Indian FMCG Retail Sales.csv`) from the sidebar.

## Features

- Dataset overview
- Interactive FMCG business analytics
- Data quality exploration
- Regression model comparison
- Interactive Margin prediction

## Target

`Margin`

The modeling workflow follows the project notebook: remove target/leakage columns, one-hot encode categorical features, use an 80/20 train-test split, scale the features, train regression models, and compare MAE, MSE, RMSE and R².
