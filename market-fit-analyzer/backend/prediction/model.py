# model.py
import pandas as pd
import numpy as np

class PasaleModel:
    def __init__(self, products_csv, transactions_csv, shops_csv):
        # Load and merge data
        products = pd.read_csv(products_csv)
        transactions = pd.read_csv(transactions_csv)
        shops = pd.read_csv(shops_csv)

        self.df = transactions.merge(products, on="product_id", how="left")
        self.df = self.df.merge(shops, on="shop_id", how="left")

        self.df["transaction_time"] = pd.to_datetime(self.df["transaction_time"])
        self.df["month"] = self.df["transaction_time"].dt.month

    # ---------------------------
    # Insights
    # ---------------------------
    def top_districts(self, product, top_n=5):
        return (self.df[self.df["product_name"] == product]
                    .groupby("district")["quantity"].sum()
                    .sort_values(ascending=False)
                    .head(top_n))

    def seasonal_trend(self, product):
        return (self.df[self.df["product_name"] == product]
                    .groupby("month")["quantity"].sum())

    # ---------------------------
    # Simple Price Prediction
    # ---------------------------
    def predict_sales(self, product, new_price):
        """Basic price sensitivity using average sales and elasticity."""
        df_prod = self.df[self.df["product_name"] == product]
        if df_prod.empty:
            return None

        avg_sales = df_prod["quantity"].mean()
        avg_price = df_prod["unit_price"].mean()

        # elasticity factor (very simple rule)
        elasticity = -0.5  # -0.5 means 10% price rise → ~5% sales drop
        pct_change_price = (new_price - avg_price) / avg_price
        predicted_sales = avg_sales * (1 + elasticity * pct_change_price)

        return max(predicted_sales, 0)

    # ---------------------------
    # New Product Prediction
    # ---------------------------
    def new_launch_predict(self, new_product_name, price, category, district):
        """Estimate sales for a new product based on category + district averages."""
        subset = self.df[(self.df["category"] == category) & (self.df["district"] == district)]
        if subset.empty:
            subset = self.df[self.df["category"] == category]

        if subset.empty:
            return None

        avg_sales = subset["quantity"].mean()
        avg_price = subset["unit_price"].mean()

        # adjust with price difference
        elasticity = -0.5
        pct_change_price = (price - avg_price) / avg_price
        predicted_sales = avg_sales * (1 + elasticity * pct_change_price)

        return {
            "product": new_product_name,
            "category": category,
            "district": district,
            "expected_price": price,
            "predicted_sales": max(predicted_sales, 0)
        }
