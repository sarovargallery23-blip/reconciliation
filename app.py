import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Sales Analysis Tool")

# File Upload
uploaded_file = st.file_uploader("Upload Sales CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 1. High Selling SKU Analysis
    st.subheader("High Selling SKUs")
    sku_data = df.groupby('SKU')['quantity'].sum().sort_values(ascending=False).head(10).reset_index()
    
    # 2. Graph
    fig, ax = plt.subplots()
    sns.barplot(data=sku_data, x='quantity', y='SKU', ax=ax)
    st.pyplot(fig)
    
    # 3. Order ID Wise Table
    st.subheader("Order ID Wise Sales")
    order_wise = df.groupby('order_id').agg({'quantity': 'sum', 'invoiceamount': 'sum'})
    st.write(order_wise)
