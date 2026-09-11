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
    st.write("The deployment model uses the same project logic: target/leakage columns are excluded, categorical variables are encoded, numerical missing values are imputed, features are scaled, and the data is split 80/20.")

    m=info["metrics"]
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Model","Linear Regression")
    c2.metric("MAE",f"{m['MAE']:.2f}")
    c3.metric("RMSE",f"{m['RMSE']:.2f}")
    c4.metric("R²",f"{m['R2']:.4f}")

    st.info("This deployment artifact was retrained from the supplied project CSV with a robust preprocessing pipeline so missing customer age/gender values do not break prediction.")

elif page == "🎯 Prediction":
    st.title("🎯 Margin Prediction")
    st.write("Enter a transaction profile and predict its gross margin.")

    drop=["Margin","Margin_%","Revenue","Cost","Invoice_ID"]
    feature_df=df.drop(columns=drop)
    if "Invoice_Date" in feature_df:
        feature_df=feature_df.drop(columns=["Invoice_Date"])

    original_cols=feature_df.columns.tolist()
    values={}
    cols=st.columns(2)
    for i,col in enumerate(original_cols):
        with cols[i%2]:
            if pd.api.types.is_numeric_dtype(feature_df[col]):
                med=float(feature_df[col].median()) if pd.notna(feature_df[col].median()) else 0.0
                if col=="Customer_Age":
                    values[col]=st.number_input(col,18.0,65.0,med)
                elif col=="Units":
                    values[col]=st.number_input(col,1,100, int(round(med)))
                elif col in ["Loyalty_Flag"]:
                    values[col]=st.selectbox(col,[0,1],index=int(round(med)))
                else:
                    values[col]=st.number_input(col,value=med)
            else:
                opts=sorted(feature_df[col].dropna().astype(str).unique().tolist())
                values[col]=st.selectbox(col,opts)

    if st.button("Predict Margin",type="primary"):
        row=pd.DataFrame([values])
        # model handles preprocessing internally; add a valid date-derived row only if model expects it
        # The saved pipeline was trained after decomposing Invoice_Date, so create date defaults.
        # Since Invoice_Date was dropped from user inputs, supply a representative date.
        row["Invoice_Year"]=2024
        row["Invoice_Month"]=6
        row["Invoice_Day"]=15
        row["Invoice_Hour"]=12
        row["Invoice_DayOfWeek"]=5
        prediction=model.predict(row)[0]
        st.success(f"Predicted Margin: ₹{prediction:,.2f}")

st.divider()
st.caption("Retail FMCG Sales • 100,000 records • Calendar Year 2024 • NTI Batch 9")
