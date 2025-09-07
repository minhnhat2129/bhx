import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Doanh thu BHX", layout="wide")
st.title("📊 Dashboard Doanh thu BHX")

# === Bước 1: Load dữ liệu ===
file_path = "/Ngày_Dthu_T8-update-31.8 (tổng).xlsx"
df = pd.read_excel(file_path)

# Chuẩn hóa cột Ngày về datetime
df['Ngày'] = pd.to_datetime(df['Ngày'])

# === Bước 2: Bộ lọc tương tác ===
col1, col2, col3 = st.columns(3)

with col1:
    selected_am = st.multiselect("Chọn AM", options=df['AM'].dropna().unique(), default=None)

with col2:
    selected_sieuthi = st.multiselect("Chọn Siêu thị", options=df['Tên siêu thị'].dropna().unique(), default=None)

with col3:
    date_range = st.date_input("Chọn khoảng ngày", 
                               [df['Ngày'].min(), df['Ngày'].max()])

# Lọc dữ liệu
filtered = df.copy()
if selected_am:
    filtered = filtered[filtered['AM'].isin(selected_am)]
if selected_sieuthi:
    filtered = filtered[filtered['Tên siêu thị'].isin(selected_sieuthi)]
if date_range:
    start_date, end_date = date_range
    filtered = filtered[(filtered['Ngày'] >= pd.to_datetime(start_date)) & 
                        (filtered['Ngày'] <= pd.to_datetime(end_date))]

# === Bước 3: Biểu đồ Doanh thu theo ngày ===
st.subheader("📈 Doanh thu theo ngày")
fig1 = px.line(filtered, x="Ngày", y="Tổng Doanh thu", 
               color="AM", markers=True,
               title="Tổng Doanh thu theo Ngày")
st.plotly_chart(fig1, use_container_width=True)

# === Bước 4: Doanh thu theo Ngày ===
st.subheader("📊 Doanh thu theo Ngày")
fig2 = px.bar(filtered.groupby("Ngày")["Tổng Doanh thu"].sum().reset_index(),
              x="Ngày", y="Tổng Doanh thu", 
              title="Tổng Doanh thu theo Ngày")
st.plotly_chart(fig2, use_container_width=True)

# === Bước 4: Doanh thu theo Thứ ===
st.subheader("📊 Doanh thu theo Thứ")
fig2 = px.bar(filtered.groupby("Thứ")["Tổng Doanh thu"].sum().reset_index(),
              x="Thứ", y="Tổng Doanh thu", 
              title="Tổng Doanh thu theo Thứ")
st.plotly_chart(fig2, use_container_width=True)

# === Bước 4: Doanh thu theo Tuần ===
st.subheader("📊 Doanh thu theo Tuần")
fig2 = px.bar(filtered.groupby("Tuần")["Tổng Doanh thu"].sum().reset_index(),
              x="Tuần", y="Tổng Doanh thu", 
              title="Tổng Doanh thu theo Tuần")
st.plotly_chart(fig2, use_container_width=True)

# === Bước 5: Top 10 Siêu thị Doanh thu cao nhất ===
st.subheader("🏆 Top 10 Siêu thị Doanh thu")
top10 = (filtered.groupby("Tên siêu thị")["Tổng Doanh thu"]
         .sum()
         .reset_index()
         .sort_values(by="Tổng Doanh thu", ascending=False)
         .head(10))

fig3 = px.bar(top10, x="Tên siêu thị", y="Tổng Doanh thu",
              title="Top 10 Siêu thị Doanh thu cao nhất")
st.plotly_chart(fig3, use_container_width=True)

# === Bước 6: Bảng dữ liệu chi tiết ===
st.subheader("📋 Dữ liệu chi tiết")
st.dataframe(filtered)
