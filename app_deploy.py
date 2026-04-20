import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Food Waste System", layout="wide")

st.title("🥗 Food Wastage Management System")

providers = pd.read_csv("data/providers_data.csv")
food = pd.read_csv("data/food_listings_data.csv")
claims = pd.read_csv("data/claims_data.csv")

providers.columns = providers.columns.str.strip().str.lower()
food.columns = food.columns.str.strip().str.lower()
claims.columns = claims.columns.str.strip().str.lower()

df = food.merge(providers, on="provider_id", how="left")

page = st.sidebar.radio("Menu", ["Dashboard", "Food Listings", "Analysis"])
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Food", int(df['quantity'].sum()))
    col2.metric("Listings", df.shape[0])
    col3.metric("Providers", providers.shape[0])

    st.subheader("Top Cities")
    st.bar_chart(df['location'].value_counts())
elif page == "Food Listings":
    search = st.text_input("Search food")
    data = df.copy()

    if search:
        data = data[data['food_name'].str.contains(search, case=False, na=False)]

    st.dataframe(data)
elif page == "Analysis":
    st.subheader("Meal Type")
    st.bar_chart(df['meal_type'].value_counts())

    st.subheader("Food Type")
    st.bar_chart(df['food_type'].value_counts())

    st.subheader("Claim Status")
    st.bar_chart(claims['status'].value_counts())