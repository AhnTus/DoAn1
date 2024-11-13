import pickle
from PIL import Image
import streamlit as st
import streamlit.components.v1 as stc

# importing the smaller apps
from ml_app import run_ml_app
from dd_app import run_dd_app
from da_app import run_da_app

html_temp = """
			<div style="background-color:#33CCFF;padding:10px;border-radius:10px">
			<h1 style="color:white;text-align:center;"> Real Estate Price Prediction</h1>
			</div>
			"""

def main():
	stc.html(html_temp)

	menu = ["Home", "Data Description","Data Analysis","Prediction", "Map"]
	choice = st.sidebar.selectbox("Menu", menu)

	if choice=="Home":
		img1 = Image.open("Realty_Growth.jpg")
		st.image(img1)
		st.write("""
				## Accurate home price prediction is key to smart investing!

				Powered by cutting-edge AI, our tool offers precise home value predictions. By inputting your property details, you can obtain an instant estimate based on real-time market data. Make smarter investment choices with our state-of-the-art valuation service.
				
				Our app provides a comprehensive platform for real estate analysis.
				 1. Utilize our robust dataset and customizable visualizations for in-depth market analysis.
				 2. Employ our predictive model to obtain accurate home valuations.
				""")
		return
	elif choice=="Data Description":
		run_dd_app()
		return
	elif choice=="Data Analysis":
		run_da_app()
		return
	elif choice == "Prediction":
		run_ml_app()
		return
	else:
		path_to_html = ("mumbai_property.html")

		with open(path_to_html,'r') as f: 
			html_data = f.read()

		st.subheader("Map view:")
		st.components.v1.html(html_data,height=500)
		
# main()
if __name__ == "__main__":
    main()
