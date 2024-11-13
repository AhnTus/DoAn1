import pandas as pd
from PIL import Image
import streamlit as st
import folium
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv("Final_Project.csv")
df.drop('Unnamed: 0', axis=1, inplace=True)


def run_da_app():
    st.title("Data Analysis Chart")

    # Price with floor number
    st.subheader("Price with floor number")
    df['Floor_No'] = pd.to_numeric(df['Floor_No'], errors='coerce')
    numeric_floors = df[pd.to_numeric(df['Floor_No'], errors='coerce').notnull()]
    floor_median = numeric_floors.groupby('Floor_No')['USD'].median()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=floor_median.index, y=floor_median.values, palette='muted', ax=ax)
    fig.suptitle('Price with floor numbers', fontsize=18, fontweight="bold")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=14)
    plt.xlabel("Floor Number", fontsize=16)
    plt.ylabel("Median Price (USD)", fontsize=16)
    fig.tight_layout()
    st.pyplot(fig)

	# House prices by area and number of bedrooms in each area
    st.subheader("House prices by area and number of bedrooms in each area")
    region = st.selectbox("Select location:", df['Region'].unique())
    bhk2 = df[(df.Region == region) & (df.Bedroom == 2)]
    bhk3 = df[(df.Region == region) & (df.Bedroom == 3)]
    bhk4 = df[(df.Region == region) & (df.Bedroom == 4)]
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(x=bhk2.Area_SqFt, y=bhk2.USD, marker='p', color='blue', label='2 BHK', s=100, ax=ax)
    sns.scatterplot(x=bhk3.Area_SqFt, y=bhk3.USD, marker='o', color='red', label='3 BHK', s=100, ax=ax)
    sns.scatterplot(x=bhk4.Area_SqFt, y=bhk4.USD, marker='*', color='green', label='4 BHK', s=300, ax=ax)
    plt.xlabel("Area (m²)")
    plt.ylabel("Price (USD)")
    plt.title(f"House price at: {region}", fontsize=18, fontweight="bold")
    plt.legend(fontsize=12)
    fig.tight_layout()
    st.pyplot(fig)

    # Price with bedroom and bathroom
    st.subheader("Price with Bedrooms and Bathrooms")
    bedroom_median = df.groupby('Bedroom')['USD'].median()
    bathroom_median = df.groupby('Bathroom')['USD'].median()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    sns.barplot(ax=ax1, x=bedroom_median.index, y=bedroom_median.values, palette='muted')
    sns.barplot(ax=ax2, x=bathroom_median.index, y=bathroom_median.values, palette='muted')
    fig.suptitle('Price with Bedrooms and Bathrooms', fontsize=18, fontweight="bold")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=14)
    ax1.set_xlabel("Number of Bedrooms", fontsize=16)
    ax1.set_ylabel("Median Price (USD)", fontsize=16)
    ax2.set_xlabel("Number of Bathrooms", fontsize=16)
    ax2.set_ylabel("Median Price (USD)", fontsize=16)
    fig.tight_layout()
    fig.subplots_adjust(top=0.93)
    st.pyplot(fig)

    # Price with property age
    st.subheader("Property Age Distribution")
    prop_age_counts = df['Property_Age'].value_counts()
    prop_age_labels = ['1-5 Years', '0-1 Year', '5-10 Years', '10+ Years', 'Under Construction']
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.pie(prop_age_counts, labels=prop_age_labels, autopct='%.2f%%', textprops={'size': 'large'}, explode=[0.005] * len(prop_age_counts))
    plt.legend(loc='upper left')
    plt.title("Price with Property Age", fontsize=18, fontweight='bold')
    fig.text(0.9, 0.15, 'Property Age Distribution', fontsize=13, color='red')
    fig.tight_layout()
    fig.subplots_adjust(top=0.93)
    st.pyplot(fig)

	#Price with SqFt Area
    st.subheader("Price with respect to Square Footage Area")
    group_full = df.groupby('Area_SqFt')['USD'].mean()
    group = group_full.reset_index()
    group = group[group['Area_SqFt'] > 0]
    group = group[group['Area_SqFt'] < 2000]
    x = group['Area_SqFt']
    y = group['USD']
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x=x, y=y, ax=ax)
    fig.suptitle('Price with respect to SqFt Area', fontsize=18, fontweight='bold')
    fig.text(0.9, 0.15, 'Price Distribution by Area', fontsize=13, color='black') 
    fig.tight_layout()
    fig.subplots_adjust(top=0.93)
    st.pyplot(fig)


