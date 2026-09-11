import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import joblib

BASE = Path(__file__).parent
DATA_PATH = BASE / "data.csv"
MODEL_PATH = BASE / "model.pkl"
INFO_PATH = BASE / "model_info.json"

st.set_page_config(page_title="Retail FMCG Analytics", page_icon="🛒", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

df = load_data()
model = load_model()
info = json.loads(INFO_PATH.read_text())

st.sidebar.title("🛒 Retail FMCG")
page = st.sidebar.radio("Navigation", ["🏠 Overview", "📊 Analytics", "🔍 Data Quality", "🤖 Machine Learning", "🎯 Prediction"])
st.sidebar.caption("NTI Batch 9 • Advanced Data Analytics")

if page == "🏠 Overview":
    st.title("Retail FMCG Sales Analytics")
    st.subheader("NTI Batch 9 — Advanced Data Analytics")
    st.write("Interactive analytics and Margin prediction for a multi-city Indian FMCG retailer.")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Transactions", f"{len(df):,}")
    c2.metric("Features", f"{df.shape[1]:,}")
    c3.metric("Revenue", f"₹{df['Revenue'].sum()/1e6:.2f}M")
    c4.metric("Margin %", f"{df['Margin_%'].mean()*100:.2f}%")

    st.divider()
    st.markdown("### Project Scope")
    st.markdown("""
    - **Business Analytics:** sales, revenue, margin, customer, channel and inventory analysis.
    - **Machine Learning:** regression modeling with **Margin** as the target.
    - **Deployment:** interactive Streamlit application for exploration and prediction.
    """)
    st.dataframe(df.head(15), use_container_width=True)

elif page == "📊 Analytics":
    st.title("📊 Business Analytics")
    filters = {}
    for col in ["City","Category","Channel","Store_Format","Loyalty_Flag"]:
        if col in df.columns:
            opts = sorted(df[col].dropna().unique().tolist())
            filters[col] = st.sidebar.multiselect(col, opts)
    fdf=df.copy()
    for col,vals in filters.items():
        if vals: fdf=fdf[fdf[col].isin(vals)]

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Transactions", f"{len(fdf):,}")
    c2.metric("Revenue", f"₹{fdf['Revenue'].sum()/1e6:.2f}M")
    c3.metric("Margin", f"₹{fdf['Margin'].sum()/1e6:.2f}M")
    c4.metric("Units", f"{fdf['Units'].sum():,}")

    a,b=st.columns(2)
    if "Category" in fdf:
        x=fdf.groupby("Category",as_index=False)["Revenue"].sum().sort_values("Revenue",ascending=False)
        a.plotly_chart(px.bar(x,x="Category",y="Revenue",title="Revenue by Category"),use_container_width=True)
    if "City" in fdf:
        x=fdf.groupby("City",as_index=False)["Margin"].sum().sort_values("Margin",ascending=False)
        b.plotly_chart(px.bar(x,x="City",y="Margin",title="Margin by City"),use_container_width=True)

    a,b=st.columns(2)
    if "Channel" in fdf:
        x=fdf.groupby("Channel",as_index=False)["Revenue"].sum()
        a.plotly_chart(px.pie(x,names="Channel",values="Revenue",title="Revenue by Channel"),use_container_width=True)
    if "Store_Format" in fdf:
        x=fdf.groupby("Store_Format",as_index=False)["Margin"].sum()
        b.plotly_chart(px.bar(x,x="Store_Format",y="Margin",title="Margin by Store Format"),use_container_width=True)

    if "Invoice_Date" in fdf:
        temp=fdf.copy()
        temp["Date"]=pd.to_datetime(temp["Invoice_Date"],errors="coerce").dt.date
        x=temp.groupby("Date",as_index=False)["Revenue"].sum()
        st.plotly_chart(px.line(x,x="Date",y="Revenue",title="Daily Revenue Trend"),use_container_width=True)

elif page == "🔍 Data Quality":
    st.title("🔍 Data Quality")
    c1,c2=st.columns(2)
    c1.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")
    c2.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")
    miss=df.isna().sum().sort_values(ascending=False)
    miss=miss[miss>0]
    st.subheader("Missing Values")
    st.dataframe(miss.rename("Missing Values"),use_container_width=True)
    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include="all").T,use_container_width=True)

elif page == "🤖 Machine Learning":
    st.title("🤖 Machine Learning")
    st.markdown("### Regression Target: `Margin`")
    st.write("The deployment uses the finalized Linear Regression workflow from the project modeling notebook: feature engineering, categorical encoding, 80/20 train-test split, StandardScaler, and Linear Regression.")

    m=info["metrics"]
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Model","Linear Regression")
    c2.metric("MAE",f"{m['MAE']:.2f}")
    c3.metric("RMSE",f"{m['RMSE']:.2f}")
    c4.metric("R²",f"{m['R2']:.4f}")

    st.info("Deployment model aligned with the executed project modeling workflow and its final Linear Regression results.")

elif page == "🎯 Prediction":
    st.title("🎯 Margin Prediction")
    st.write("Enter a transaction profile and predict its gross margin using the finalized Linear Regression model.")

    # The executed project model uses these original business features.
    # Product is intentionally excluded because the modeling notebook removes
    # categorical columns with more than 100 unique values.
    input_cols = [
        "City", "Store_Format", "Category", "Brand", "Channel", "Payment_Mode",
        "Units", "Cost_Price", "Selling_Price", "Stock_On_Hand",
        "Reorder_Level", "Lead_Time_Days", "Customer_Age",
        "Customer_Gender", "Loyalty_Flag"
    ]

    values = {}
    cols = st.columns(2)
    for i, col in enumerate(input_cols):
        with cols[i % 2]:
            if pd.api.types.is_numeric_dtype(df[col]):
                med = float(df[col].median())
                if col == "Units":
                    values[col] = st.number_input(col, min_value=1, max_value=100, value=int(round(med)))
                elif col == "Customer_Age":
                    values[col] = st.number_input(col, min_value=18.0, max_value=65.0, value=med)
                elif col == "Loyalty_Flag":
                    values[col] = st.selectbox(col, [0, 1], index=int(round(med)))
                else:
                    values[col] = st.number_input(col, value=med)
            else:
                opts = sorted(df[col].dropna().astype(str).unique().tolist())
                values[col] = st.selectbox(col, opts)

    prediction_date = st.date_input("Invoice Date", value=pd.Timestamp("2024-06-15").date())

    if st.button("Predict Margin", type="primary"):
        row = pd.DataFrame([values])

        # Match the executed notebook's feature engineering exactly.
        if pd.isna(values["Customer_Age"]):
            row["Customer_Age_Missing"] = 1
            row["Customer_Age"] = df["Customer_Age"].median()
        else:
            row["Customer_Age_Missing"] = 0

        row["Year"] = prediction_date.year
        row["Month"] = prediction_date.month
        row["Day"] = prediction_date.day
        row["Day_of_Week"] = prediction_date.weekday()

        row["Revenue_Calc"] = row["Units"] * row["Selling_Price"]
        row["Cost_Calc"] = row["Units"] * row["Cost_Price"]
        row["Margin_Calc"] = row["Revenue_Calc"] - row["Cost_Calc"]

        # Reproduce the notebook's categorical handling.
        categorical_cols = row.select_dtypes(include=["object"]).columns.tolist()
        for col in categorical_cols:
            if col in row.columns and df[col].nunique() > 100:
                row = row.drop(columns=[col])

        row = pd.get_dummies(
            row,
            columns=row.select_dtypes(include=["object"]).columns.tolist(),
            drop_first=True,
            dtype=np.int8
        )
        row = row.apply(pd.to_numeric, errors="coerce")

        # Align columns with the exact 47-feature training matrix.
        expected_features = getattr(model, "feature_names_in_", None)
        if expected_features is not None:
            row = row.reindex(columns=expected_features, fill_value=0)

        prediction = model.predict(row)[0]
        st.success(f"Predicted Margin: ₹{prediction:,.2f}")

st.divider()
st.caption("Retail FMCG Sales • 100,000 records • Calendar Year 2024 • NTI Batch 9")
