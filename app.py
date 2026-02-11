import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Analysis Tool", layout="wide")

st.title("📊 Sales & SKU Analysis Tool")
st.write("Upload your sales report CSV to analyze order-wise sales and high-selling SKUs.")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose your Sales CSV file", type="csv")

if uploaded_file is not None:
    # Load Data
    df = pd.read_csv(uploaded_file)
    
    # --- ANALYSIS 1: SKU & Price Analysis ---
    st.subheader("🚀 High Selling SKU Analysis")
    
    sku_analysis = df.groupby('SKU').agg({
        'quantity': 'sum',
        'invoiceamount': 'sum',
        'seller_price': 'mean',
        'article_type': 'first'
    }).reset_index()

    sku_analysis.rename(columns={
        'quantity': 'Total Quantity Sold',
        'invoiceamount': 'Total Revenue',
        'seller_price': 'Avg Selling Price'
    }, inplace=True)

    # Sort to get top sellers
    sku_analysis = sku_analysis.sort_values(by='Total Quantity Sold', ascending=False)

    # --- GRAPH REPRESENTATION ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Top 10 SKUs by Quantity")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=sku_analysis.head(10), x='Total Quantity Sold', y='SKU', palette='viridis', ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.write("Top 10 Data Table")
        st.dataframe(sku_analysis[['SKU', 'Total Quantity Sold', 'Avg Selling Price']].head(10))

    # --- ANALYSIS 2: Order ID Wise Import/Analysis ---
    st.divider()
    st.subheader("📦 Order ID Wise Summary")
    
    order_summary = df.groupby('order_id').agg({
        'SKU': 'count',
        'quantity': 'sum',
        'invoiceamount': 'sum',
        'order_status': 'first',
        'customer_delivery_state_code': 'first'
    }).reset_index()

    order_summary.rename(columns={
        'SKU': 'Unique SKUs',
        'quantity': 'Total Items',
        'invoiceamount': 'Order Value'
    }, inplace=True)

    st.dataframe(order_summary, use_container_width=True)

    # --- DOWNLOAD BUTTONS ---
    st.sidebar.header("Download Reports")
    csv_sku = sku_analysis.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download SKU Analysis", data=csv_sku, file_name="sku_analysis.csv", mime="text/csv")
    
    csv_order = order_summary.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download Order Summary", data=csv_order, file_name="order_summary.csv", mime="text/csv")

else:
    st.info("Please upload a CSV file to begin.")
