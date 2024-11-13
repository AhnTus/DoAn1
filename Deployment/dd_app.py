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


def run_dd_app():
    img1 = Image.open("Real_Estate.jpg")
    st.image(img1)

    # Display dataset directly
    st.subheader("Dataset information")
    st.dataframe(df.head(10))  # Show the first 10 rows by default

    # Display data summary directly
    st.subheader("Data Describe")
    st.dataframe(df.describe())

    # Display location distribution directly
    st.subheader("Location")
    st.dataframe(df["Region"].value_counts().head(30))
