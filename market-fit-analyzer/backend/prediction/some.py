# ui.py
import streamlit as st
from model import PasaleModel

# Load model (acts like API)
pasale = PasaleModel("products.csv", "transactions.csv", "shops.csv")

st.set_page_config(page_title="Pasale Insight Lab", layout="wide")
st.title("🌟 Pasale Insight Lab (Simple AI Predictions)")

section = st.sidebar.radio("Choose Section", ["Product Radar", "Price Prediction", "New Launch Simulator"])

# ---------------------------
# Product Radar (analytics only)
# ---------------------------
if section == "Product Radar":
    st.header("Product Analytics")
    product = st.selectbox("Select Product", pasale.df["product_name"].unique())

    st.metric("Total Sales", int(pasale.df[pasale.df["product_name"] == product]["quantity"].sum()))
    st.metric("Average Price", f"Rs. {pasale.df[pasale.df['product_name'] == product]['unit_price'].mean():.2f}")
    st.metric("Unique Shops", pasale.df[pasale.df["product_name"] == product]["shop_id"].nunique())

    # ✅ Top Districts as Table
    st.subheader("Top Districts ")
    top_districts = pasale.top_districts(product).reset_index()
    top_districts.columns = ["District", "Total Sales"]
    st.table(top_districts.style.hide(axis="index"))


    # ✅ Seasonal Trend with month names
    st.subheader("Seasonal Trend")
    trend = pasale.seasonal_trend(product).reset_index()
    trend["month"] = trend["month"].astype(int)
    month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                 7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    trend["Month"] = trend["month"].map(month_map)
    trend = trend[["Month", "quantity"]].rename(columns={"quantity":"Total Sales"})
    st.line_chart(trend.set_index("Month"))

# ---------------------------
# Price Prediction
# ---------------------------
elif section == "Price Prediction":
    st.header("💰 Price Sensitivity ")
    product = st.selectbox("Select Product", pasale.df["product_name"].unique())
    new_price = st.number_input("Enter New Price", min_value=10, max_value=1000, value=100)

    pred = pasale.predict_sales(product, new_price)
    if pred is not None:
        st.success(f"Prediction: At Rs.{new_price}, expected sales ≈ **{pred:.0f} units**")
    else:
        st.warning("Not enough data to predict for this product.")

# ---------------------------
# New Launch Simulator
# ---------------------------
elif section == "New Launch Simulator":
    st.header("New Product Launch (Simple)")
    new_name = st.text_input("New Product Name")
    category = st.selectbox("Select Category", pasale.df["category"].dropna().unique())
    district = st.selectbox("Select District", pasale.df["district"].dropna().unique())
    price = st.number_input("Expected Price", min_value=10, max_value=1000, value=100)

    if new_name:
        result = pasale.new_launch_predict(new_name, price, category, district)
        if result:
            st.success(
                f"Expected sales for **{result['product']}** "
                f"in {result['district']} (Category: {result['category']}) ≈ "
                f"**{result['predicted_sales']:.0f} units/month** at Rs.{result['expected_price']}"
            )
        else:
            st.error("Not enough data to predict for this category/district.")
