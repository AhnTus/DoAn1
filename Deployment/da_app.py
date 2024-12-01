import pandas as pd
from PIL import Image
import streamlit as st
import folium
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_folium import folium_static  
import requests
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("https://raw.githubusercontent.com/AhnTus/STWeb-HousePricePrediction/refs/heads/main/Deployment/Final_Project.csv")
df.drop('Unnamed: 0', axis=1, inplace=True)
dfmap = pd.read_csv("https://raw.githubusercontent.com/AhnTus/STWeb-HousePricePrediction/refs/heads/main/Deployment/Map_Location.csv")

def run_da_app():

    # Hiển thị ảnh banner
    url = "https://github.com/user-attachments/assets/bc2088b2-d77e-4627-9d12-f320cb360b36"
    response = requests.get(url)
    img1 = Image.open(BytesIO(response.content))
    st.image(img1, caption="Analyzing Real Estate Data")

    # Price with floor number
    st.subheader("Price with Floor Number")
    df['Floor_No'] = pd.to_numeric(df['Floor_No'], errors='coerce')
    numeric_floors = df[pd.to_numeric(df['Floor_No'], errors='coerce').notnull()]
    floor_median = numeric_floors.groupby('Floor_No')['USD'].median()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=floor_median.index, y=floor_median.values, palette='muted', ax=ax)
    fig.suptitle('Price vs Floor Number', fontsize=18, fontweight="bold")
    ax.set_xlabel("Floor Number", fontsize=14)
    ax.set_ylabel("Median Price (USD)", fontsize=14)
    st.pyplot(fig)

    # House prices by area and number of bedrooms in each area
    st.subheader("House Prices by Area and Number of Bedrooms")
    region = st.selectbox("Select Location", df['Region'].unique())
    bhk2 = df[(df.Region == region) & (df.Bedroom == 2)]
    bhk3 = df[(df.Region == region) & (df.Bedroom == 3)]
    bhk4 = df[(df.Region == region) & (df.Bedroom == 4)]
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(x=bhk2.Area_SqFt, y=bhk2.USD, marker='p', color='blue', label='2 BHK', s=100, ax=ax)
    sns.scatterplot(x=bhk3.Area_SqFt, y=bhk3.USD, marker='o', color='red', label='3 BHK', s=100, ax=ax)
    sns.scatterplot(x=bhk4.Area_SqFt, y=bhk4.USD, marker='*', color='green', label='4 BHK', s=300, ax=ax)
    ax.set_xlabel("Area (m²)", fontsize=14)
    ax.set_ylabel("Price (USD)", fontsize=14)
    ax.set_title(f"House Prices in {region}", fontsize=18, fontweight="bold")
    ax.legend()
    st.pyplot(fig)

    # Price with Bedroom and Bathroom
    st.subheader("Price by Bedroom and Bathroom")
    bedroom_median = df.groupby('Bedroom')['USD'].median()
    bathroom_median = df.groupby('Bathroom')['USD'].median()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    sns.barplot(ax=ax1, x=bedroom_median.index, y=bedroom_median.values, palette='muted')
    sns.barplot(ax=ax2, x=bathroom_median.index, y=bathroom_median.values, palette='muted')
    fig.suptitle('Price vs Bedroom and Bathroom', fontsize=18, fontweight="bold")
    ax1.set_xlabel("Number of Bedrooms", fontsize=14)
    ax1.set_ylabel("Median Price (USD)", fontsize=14)
    ax2.set_xlabel("Number of Bathrooms", fontsize=14)
    ax2.set_ylabel("Median Price (USD)", fontsize=14)
    fig.tight_layout()
    fig.subplots_adjust(top=0.93)
    st.pyplot(fig)

    # Property Age Distribution (Pie chart)
    st.subheader("Price vs Property Age")
    prop_age_counts = df['Property_Age'].value_counts()
    prop_age_labels = ['1-5 Years', '0-1 Year', '5-10 Years', '10+ Years', 'Under Construction']
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.pie(prop_age_counts, labels=prop_age_labels, autopct='%.2f%%', textprops={'size': 'large'}, explode=[0.005] * len(prop_age_counts))
    plt.legend(loc='upper left')
    plt.title("Price Distribution by Property Age", fontsize=18, fontweight='bold')
    fig.tight_layout()
    st.pyplot(fig)

    # Price with SqFt Area (Scatter plot)
    st.subheader("Price vs Square Footage Area")
    group_full = df.groupby('Area_SqFt')['USD'].mean()
    group = group_full.reset_index()
    group = group[group['Area_SqFt'] > 0]
    group = group[group['Area_SqFt'] < 2000]
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=group, x='Area_SqFt', y='USD', ax=ax)
    fig.suptitle('Price Distribution by SqFt Area', fontsize=18, fontweight='bold')
    fig.tight_layout()
    st.pyplot(fig)

    # Interactive Price Distribution by Region (Plotly)
    st.subheader("Interactive Price Distribution by Region")
    fig = px.box(df, x='Region', y='USD', color='Region', title="Price Distribution by Region")
    st.plotly_chart(fig)

    # Interactive Scatterplot: Area vs Price with Plotly
    st.subheader("Interactive Area vs Price")
    fig = px.scatter(df, x='Area_SqFt', y='USD', color='Region', size='Bedroom', hover_data=['Region', 'Bedroom', 'Bathroom'], title="Area vs Price")
    st.plotly_chart(fig)

    # # Interactive Map: Price by Region
    # st.subheader("Price by Region on Map")
    # region_map = folium.Map(location=[dfmap['Latitude'].mean(), dfmap['Longitude'].mean()], zoom_start=10)
    # for _, row in dfmap.iterrows():
    #     folium.Marker([row['Latitude'], row['Longitude']], popup=f"Price: ${row['USD']}").add_to(region_map)
    # folium_static(region_map)  
