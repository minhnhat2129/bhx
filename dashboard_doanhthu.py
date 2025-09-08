import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Doanh thu BHX", layout="wide")
st.title("📊 Dashboard Doanh thu Miền Tháng 8")

# === Bước 1: Load dữ liệu ===
df = pd.read_excel("dthuT8.xlsx")
df['Ngày'] = pd.to_datetime(df['Ngày'])

# Nếu file không có sẵn cột "Thứ" thì tự tạo
if 'Thứ' not in df.columns:
    df['Thứ'] = df['Ngày'].dt.day_name(locale='vi_VN')

# === Bước 2: Bộ lọc AM, Siêu thị, Ngày (theo 3 cột ngang) ===
col1, col2, col3 = st.columns(3)

with col1:
    ams = df['AM'].dropna().unique()
    am_chon = st.multiselect("Chọn QLTP", sorted(ams), default=ams)

with col2:
    sieuthis = df[df['AM'].isin(am_chon)]['Tên siêu thị'].dropna().unique()
    sieuthi_chon = st.multiselect("Chọn Siêu thị", sorted(sieuthis), default=sieuthis)

with col3:
    ngay_min, ngay_max = df['Ngày'].min(), df['Ngày'].max()
    ngay_chon = st.date_input("Chọn khoảng ngày", [ngay_min, ngay_max])

# Xử lý chọn ngày (1 ngày hoặc khoảng)
if isinstance(ngay_chon, list) and len(ngay_chon) == 2:
    start_date, end_date = pd.to_datetime(ngay_chon[0]), pd.to_datetime(ngay_chon[1])
else:
    start_date, end_date = ngay_min, ngay_max

# Lọc dữ liệu
df_filtered = df[
    (df['AM'].isin(am_chon)) &
    (df['Tên siêu thị'].isin(sieuthi_chon)) &
    (df['Ngày'].between(start_date, end_date))
]

# === Bước 3: Biểu đồ Doanh thu theo Thứ ===
st.subheader("📊 Doanh thu theo Thứ")
grouped_thu = df_filtered.groupby('Thứ')['Tổng Doanh thu'].sum().reset_index()
fig1 = px.bar(grouped_thu, x='Thứ', y='Tổng Doanh thu',
              title="Tổng Doanh thu theo Thứ",
              text=grouped_thu['Tổng Doanh thu'] / 1_000_000)
fig1.update_traces(texttemplate='%{text:.1f}M', textposition='outside')
fig1.update_yaxes(title="Doanh thu (VND)", tickformat=",.0f")
st.plotly_chart(fig1, use_container_width=True)

# === Bước 4: Biểu đồ Doanh thu theo Ngày (cột) ===
st.subheader("📊 Doanh thu theo Ngày")
grouped_ngay = df_filtered.groupby('Ngày')['Tổng Doanh thu'].sum().reset_index()
fig2 = px.bar(grouped_ngay, x='Ngày', y='Tổng Doanh thu',
              title="Tổng Doanh thu theo Ngày",
              text=grouped_ngay['Tổng Doanh thu'] / 1_000_000)
fig2.update_traces(texttemplate='%{text:.1f}M', textposition='outside')
fig2.update_yaxes(title="Doanh thu (VND)", tickformat=",.0f")
st.plotly_chart(fig2, use_container_width=True)

# === Bước 5: Biểu đồ Doanh thu theo Ngày (line chart) ===
st.subheader("📈 Số bill theo Ngày")
fig3 = px.line(df_filtered, x="Ngày", y="Tổng số bill",
               color="Tên siêu thị", markers=True,
               title="Số bill theo ngày",
               text=df_filtered['Tổng số bill'])
fig3.update_traces(textposition="top center")
fig3.update_yaxes(title="Tổng số bill")
st.plotly_chart(fig3, use_container_width=True)

# === Bước 5: Biểu đồ Doanh thu theo Ngày (line chart) ===
st.subheader("📈 Số đơn online theo Ngày")
fig3 = px.line(df_filtered, x="Ngày", y="Tổng số bill online",
               color="Tên siêu thị", markers=True,
               title="Số đơn online theo Ngày",
               text=df_filtered['Tổng số bill online'])
fig3.update_traces(textposition="top center")
fig3.update_yaxes(title="Số đơn online")
st.plotly_chart(fig3, use_container_width=True)

# === Bước 6: Top 10 Siêu thị ===
st.subheader("🏆 Top 10 Siêu thị Doanh thu")
top10 = (df_filtered.groupby("Tên siêu thị")["Tổng Doanh thu"]
         .sum()
         .reset_index()
         .sort_values(by="Tổng Doanh thu", ascending=False)
         .head(10))
fig4 = px.bar(top10, x="Tên siêu thị", y="Tổng Doanh thu",
              title="Top 10 Siêu thị Doanh thu",
              text=top10['Tổng Doanh thu'] / 1_000_000)
fig4.update_traces(texttemplate='%{text:.1f}M', textposition='outside')
fig4.update_yaxes(title="Doanh thu (VND)", tickformat=",.0f")
st.plotly_chart(fig4, use_container_width=True)

# === Bước 7: Hiển thị bảng dữ liệu chi tiết ===
st.subheader("📑 Dữ liệu chi tiết")
st.dataframe(df_filtered)
