#DASHBOARD BIKE SHARING
#Nama: Jason Christopher
#email: jasonct03@gmail.com
#Id Dicoding : toxictojo


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.dates as mdates
from babel.numbers import format_currency
sns.set(style='dark')
#load data
@st.cache_resource
def create_df_hour():
    data = pd.read_csv("C:\Streamlit\dataset\Bike-sharing-dataset\cleaned_hour.csv")
    return data
def create_df_day():
    data = pd.read_csv("C:\Streamlit\dataset\Bike-sharing-dataset\cleaned_day.csv")
    return data

df_hour = create_df_hour()
df_day = create_df_day()

#create rentang waktu(date calender)
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

min_date = df_hour['dteday'].min()
max_date = df_hour['dteday'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.title("**Bike Sharing**")
    st.markdown("**Created by Jason Christopher**")
    st.markdown("**email: jasonct03@gmail.com**")
    st.markdown("**ID Dicoding : toxictojo**")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
#data frame sesuai hari    
df_main_hour = df_hour[(df_hour['dteday'] >= str(start_date)) & 
                (df_hour['dteday'] <= str(end_date))]
df_main_day = df_day[(df_day['dteday'] >= str(start_date)) & 
                (df_day['dteday'] <= str(end_date))]

#header
st.header('Bike Sharing Dashboard :bike::person_biking:')

#daily rental
st.subheader('Daily Rental')

col1,col2,col3 = st.columns(3)

with col1:
    total_rental = df_main_hour['cnt'].sum()
    st.metric("Total rental", value=total_rental)
with col2:
    total_casual = df_main_hour['casual'].sum()
    st.metric("Total casual", value=total_casual)
with col3:
    total_registered = df_main_hour['registered'].sum()
    st.metric("Total registered", value=total_registered)

if start_date == end_date: #kalau misal diset pada hari yang sama
    #plot jumlah rental tiap jam (untuk 1 hari saja)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        df_main_hour["hr"],
        df_main_hour["cnt"],
        marker='o',
        linewidth=2,
        color="#09e3b4"
    )

    ax.xaxis.set_major_locator(plt.MaxNLocator(13))
    

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)

    
else:#kalau diset pada hari yang berbeda
    #plot jumlah rental tiap harinya (sesuai tanggal)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        df_main_day["dteday"],
        df_main_day["cnt"],
        marker='o',
        linewidth=2,
        color="#09e3b4"
    )

    ax.xaxis.set_major_locator(plt.MaxNLocator(13))

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)

#plot jumlah total berdasarkan musim
st.subheader('Seasons & Weathers')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

#copy data frame
df_temp = df_main_hour.copy()

#seasons
df_temp["season"] = df_temp.season.apply(lambda x: "Spring" if x == 1 else ("Summer" if x == 2 else ("Fall" if x == 3 else "Winter")))
df_plot = df_temp.groupby(by='season').cnt.sum().sort_values(ascending=False)

df_plot.plot(kind='bar', color=colors, ax=ax[0], width=0.5)
ax[0].set_title('The Total Bicycle Rentals Based on The Season')
ax[0].set_xlabel('Seasons')
ax[0].set_ylabel('Total Bicycle Rentals')
ax[0].tick_params(axis='y')
ax[0].tick_params(axis='x',rotation=0)

#weathers
df_temp["weathersit"] = df_temp.weathersit.apply(lambda x: "Clear, Few clouds,etc" if x == 1 else ("Mist + Cloudy, Mist,etc" if x == 2 else ("Light Snow, Light Rain + Scattered clouds,etc" if x == 3 else "Snow + Fog,etc")))
df_plot1 = df_temp.groupby(by='weathersit').cnt.sum().sort_values(ascending=False)
df_plot1.plot(kind='bar', color=colors, ax=ax[1], width=0.5)
ax[1].set_title('The Total Bicycle Rentals Based on The Weathers')
ax[1].set_xlabel('Weathers')
ax[1].set_ylabel('Total Bicycle Rentals')
ax[1].tick_params(axis='y')
ax[1].tick_params(axis='x',rotation=45) 
st.pyplot(fig)

#total rental : Weekday vs. Working Days vs. Holidays
st.subheader("Daily Rental: Working Days vs. Holidays")

col1,col2 = st.columns(2)



with col1:
    df_workingday_hour= df_main_hour[(df_main_hour['workingday'] == 1)]
    total_workingday = df_workingday_hour['cnt'].sum()
    st.metric("On working day", value=total_workingday)
    
with col2:
    df_holiday_hour = df_main_hour[(df_main_hour['holiday'] == 1)]
    total_holiday = df_holiday_hour['cnt'].sum()
    st.metric("On holiday", value=total_holiday)

df_workingday_day = df_main_day[(df_main_day['workingday'] == 1)]

df_holiday_day = df_main_day[(df_main_day['holiday'] == 1)]
    
if start_date == end_date: #kalau misal diset pada hari yang sama
    #plot jumlah rental tiap jam (untuk 1 hari saja)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        df_workingday_hour["dteday"],
        df_workingday_hour["cnt"],
        label='Working Day',
        marker='o',
        linewidth=2,
        color="#09e3b4"
    )

    ax.xaxis.set_major_locator(plt.MaxNLocator(13))
    

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend()
    st.pyplot(fig)

    
else:#kalau diset pada hari yang berbeda
    #plot jumlah rental tiap harinya (sesuai tanggal)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        df_workingday_day["dteday"],
        df_workingday_day["cnt"],
        label='Working Day',
        marker='o',
        linewidth=2,
        color="#09e3b4"
    )

    ax.xaxis.set_major_locator(plt.MaxNLocator(12))

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend()
    st.pyplot(fig)
    
if start_date == end_date: #kalau misal diset pada hari yang sama
    #plot jumlah rental tiap jam (untuk 1 hari saja)
    fig, ax = plt.subplots(figsize=(16, 8))
        
    ax.plot(
        df_holiday_hour["dteday"],
        df_holiday_hour["cnt"],
        label='Holiday',
        marker='o',
        linewidth=2,
        color="#E30938"
    )

    ax.xaxis.set_major_locator(plt.MaxNLocator(13))
    

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend()
    st.pyplot(fig)

    
else:#kalau diset pada hari yang berbeda
    #plot jumlah rental tiap harinya (sesuai tanggal)
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.plot(
        df_holiday_day["dteday"],
        df_holiday_day["cnt"],
        label='Holiday',
        marker='o',
        linewidth=2,
        color="#E30938"
    )

    ax.xaxis.set_major_locator(plt.MaxNLocator(12))

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend()
    st.pyplot(fig)

#temp&atemp
st.subheader('Temperature & Feeling Temperature')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))

#temp
if start_date == end_date:
    df_main_hour.plot(kind='scatter',x='temp',y='cnt', ax=ax[0]) 
else:
    df_main_day.plot(kind='scatter',x='temp',y='cnt', ax=ax[0]) 
ax[0].set_title('Relationship Between Total Bicycle Rentals and Temperature')
ax[0].set_xlabel('Temperature')
ax[0].set_ylabel('Total Bicycle Rentals')
ax[0].tick_params(axis='y')
ax[0].tick_params(axis='x',rotation=0)

#atemp
if start_date == end_date:
    df_main_hour.plot(kind='scatter',x='atemp',y='cnt', ax=ax[1]) 
else:
    df_main_day.plot(kind='scatter',x='atemp',y='cnt', ax=ax[1]) 
ax[1].set_title('Relationship Between Total Bicycle Rentals and Feeling Temperature')
ax[1].set_xlabel('Feeling Temperature')
ax[1].set_ylabel('Total Bicycle Rentals')
ax[1].tick_params(axis='y')
ax[1].tick_params(axis='x',rotation=0)
st.pyplot(fig)

#Windspeed & Humidity
st.subheader('Windspeed & Humidity')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))

#windspeed
if start_date == end_date:
    df_main_hour.plot(kind='scatter',x='windspeed',y='cnt', ax=ax[0]) 
else:
    df_main_day.plot(kind='scatter',x='windspeed',y='cnt', ax=ax[0]) 
ax[0].set_title('Relationship Between Total Bicycle Rentals and Windspeed')
ax[0].set_xlabel('windspeed')
ax[0].set_ylabel('Total Bicycle Rentals')
ax[0].tick_params(axis='y')
ax[0].tick_params(axis='x',rotation=0)

#Humidity
if start_date == end_date:
    df_main_hour.plot(kind='scatter',x='hum',y='cnt', ax=ax[1]) 
else:
    df_main_day.plot(kind='scatter',x='hum',y='cnt', ax=ax[1]) 
ax[1].set_title('Relationship Between Total Bicycle Rentals and Humidity')
ax[1].set_xlabel('Humidity')
ax[1].set_ylabel('Total Bicycle Rentals')
ax[1].tick_params(axis='y')
ax[1].tick_params(axis='x',rotation=0)
st.pyplot(fig)

