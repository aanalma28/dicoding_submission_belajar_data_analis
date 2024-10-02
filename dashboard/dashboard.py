import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style="dark")


hour_df = pd.read_csv('hour_df.csv')

st.header("Dashboard Bike Sharing Rentals")
col1, col2, col3 = st.columns(3)


with col1:
    st.metric("Registered User", value=hour_df.registered.sum())
with col2:
    st.metric("Casual User", value=hour_df.casual.sum())
with col3:
    st.metric("Total User", value=hour_df['count'].sum())
    
st.header("Weather Rent")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='weathersit',
    y='count',
    data=hour_df,
    palette='viridis',
    ax=ax
)
ax.set_title('Jumlah Penyewa Sepeda Berdasarkan Cuaca')
ax.set_xlabel('Cuaca')
ax.set_ylabel('Jumlah Penyewa')
st.pyplot(fig)


st.header("Holiday, Weekday, Workday Rent")
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,15))

sns.barplot(
    x="is_workingday",
    y="count",
    data=hour_df,
    palette='viridis',
    ax=axes[0]
)
axes[0].set_title("Jumlah data pengguna sepeda pada hari kerja")
axes[0].set_xlabel("Hari kerja")
axes[0].set_title("Jumlah pengguna sepeda")

sns.barplot(
    x="is_holiday",
    y="count",
    data=hour_df,
    palette='viridis',
    ax=axes[1]
)
axes[1].set_title("Jumlah data pengguna sepeda pada hari libur")
axes[1].set_xlabel("Hari libur")
axes[1].set_title("Jumlah pengguna sepeda")

sns.barplot(
    x="day_of_week",
    y="count",
    data=hour_df,
    palette='viridis',
    ax=axes[2]
)
axes[2].set_title("Jumlah data pengguna sepeda pada hari seminggu")
axes[2].set_xlabel("Hari seminggu")
axes[2].set_title("Jumlah pengguna sepeda")
st.pyplot(fig)


st.header("Hourly Rent")
hours = hour_df.groupby('hour')[['casual', 'registered']].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(
    hours['hour'],
    hours['casual'],
    label='Casual',
    color='blue',
    alpha=0.7
)

ax.bar(
    hours['hour'],
    hours['registered'],
    label='Registered',
    color='green',
    alpha=0.7
)

ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewa')
ax.set_title('Jumlah Penyewa Sepeda Berdasarkan Jam')
ax.legend()
ax.grid(True)
st.pyplot(fig)


st.header("Yearly Rent")
hour_df['month'] = pd.Categorical(hour_df['month'], 
    categories=[
        'January', 'February', 'March', 'April', 'May', 
        'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

monthly_counts = hour_df.groupby(['year', 'month']).agg({
    'count': 'sum'
}).reset_index()

years = monthly_counts['year'].unique()

colors = plt.cm.viridis(range(len(years)))
marker = ['o', 's', '^', 'D', 'V']

fig, ax = plt.subplots(figsize=(10, 5))
for i, year in enumerate(years):
    data_per_year = monthly_counts[monthly_counts['year'] == year]
    ax.plot(data_per_year['month'], data_per_year['count'], 
            label='Tahun {}'.format(year), color=colors[i], marker=marker[i])

ax.set_title("Jumlah total sepeda yang disewakan berdasarkan Bulan dan Tahun")
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.legend(title="Tahun", loc="upper right")
ax.set_xticks(range(12))
ax.set_xticklabels([
    'January', 'February', 'March', 'April', 'May', 
    'June', 'July', 'August', 'September', 'October', 'November', 'December'], rotation=45)

plt.tight_layout()
st.pyplot(fig)

