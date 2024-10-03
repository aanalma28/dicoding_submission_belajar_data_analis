import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style="dark")


hour_df = pd.read_csv('hour_df.csv')

# membuat data berdasarkan cuaca
def create_weather_df(df):
    weather_df = df.groupby('weathersit').agg({
        'count': 'sum'
    }).reset_index()
    return weather_df

# membuat data weekday
def create_weekday_rent(df):
    weekday_df = df.groupby('day_of_week').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_df

# membuat data holiday
def create_holiday_rent(df):
    holiday_df = df.groupby('is_holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_df

# membuat data workingday
def create_workingday_rent(df):
    workingday_df = df.groupby('is_workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_df

# membuat data berdasarkan jam
def create_hour_rent(df):
    hour_df = df.groupby('hour')[['casual', 'registered']].sum().reset_index()
    return hour_df

# membuat data penyewa casual
def create_rent(df):
    rent = df.groupby('dateday').agg({
        'count': 'sum'
    }).reset_index()
    return rent

# membuat data penyewa casual
def create_casual_rent(df):
    casual_rent = df.groupby('dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_rent

# membuat data penyewa registered
def create_registered_rent(df):
    registered_rent = df.groupby('dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_rent

# membuat komponen filter
min_date = pd.to_datetime(hour_df['dateday']).dt.date.min()
max_date = pd.to_datetime(hour_df['dateday']).dt.date.max()

with st.sidebar:
    # menambahkan logo
    st.image('https://www.google.com/url?sa=i&url=https%3A%2F%2Fid.pngtree.com%2Ffreepng%2Fillustration-of-a-bicycle-rental-logo-in-vector-format-set-against-a-white-background-vector_10130397.html&psig=AOvVaw3x1CoQr94jn4S8c4JuzNYS&ust=1728046789055000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCKikjIqi8ogDFQAAAAAdAAAAABAE')
    
    # mengambil start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu", min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )

# membuat main_data
main_df = hour_df[(hour_df['dateday'] >= str(start_date)) &
                  (hour_df['dateday'] <= str(end_date))]

rent_df = create_rent(main_df)
casual_rent_df = create_casual_rent(main_df)
registered_rent_df = create_registered_rent(main_df)
weather_rent_df = create_weather_df(main_df)
workingday_rent_df = create_workingday_rent(main_df)
holiday_rent_df = create_holiday_rent(main_df)
weekday_rent_df = create_weekday_rent(main_df)
hour_rent_df = create_hour_rent(main_df)

st.header("Dashboard Bike Sharing Rentals")
col1, col2, col3 = st.columns(3)


with col1:
    st.metric("Registered User", value=registered_rent_df['registered'].sum())
with col2:
    st.metric("Casual User", value=casual_rent_df['casual'].sum())
with col3:
    st.metric("Total User", value=rent_df['count'].sum())

# membuat grafik penyewaan berdasarkan cuaca
st.header("Weather Rent")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x=weather_rent_df['weathersit'],
    y=weather_rent_df['count'],
    data=weather_rent_df,
    palette='viridis',
    ax=ax
)
for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


# membuat visualisasi berdasarkan holiday, weekday, dan workday
st.header("Holiday, Weekday, Workday Rent")
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,15))
sns.barplot(
    x="is_workingday",
    y="count",
    data=workingday_rent_df,
    palette='viridis',
    ax=axes[0]
)
for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
    
axes[0].set_title("Jumlah data pengguna sepeda pada hari kerja")
axes[0].set_xlabel("Hari kerja")
axes[0].set_title("Jumlah pengguna sepeda")

sns.barplot(
    x="is_holiday",
    y="count",
    data=holiday_rent_df,
    palette='viridis',
    ax=axes[1]
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
    
axes[1].set_title("Jumlah data pengguna sepeda pada hari libur")
axes[1].set_xlabel("Hari libur")
axes[1].set_title("Jumlah pengguna sepeda")

sns.barplot(
    x="day_of_week",
    y="count",
    data=weekday_rent_df,
    palette='viridis',
    ax=axes[2]
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
    
axes[2].set_title("Jumlah data pengguna sepeda pada hari seminggu")
axes[2].set_xlabel("Hari seminggu")
axes[2].set_title("Jumlah pengguna sepeda")
st.pyplot(fig)


# membuat visualisasi berdasarkan jam
st.header("Hourly Rent")
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(
    hour_rent_df['hour'],
    hour_rent_df['casual'],
    label='Casual',
    color='blue',
    alpha=0.7
)

ax.bar(
    hour_rent_df['hour'],
    hour_rent_df['registered'],
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


# membuat visualisasi berdasarkan tahun
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

