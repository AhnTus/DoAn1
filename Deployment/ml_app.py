import pickle
import numpy as np
import pandas as pd
import streamlit as st
import folium
import random
from random import choice
from streamlit_folium import folium_static

# Load dữ liệu và mô hình
df = pd.read_csv("Final_Project.csv")
dfmap = pd.read_csv("Map_Location.csv")
pickle_in = open('regression_model.pkl', 'rb')
reg = pickle.load(pickle_in)

# Dữ liệu tọa độ tĩnh
predefined_locations = {
    "Marine Drive, Mumbai, Maharashtra": (18.9441, 72.8235),
    "Colaba, Mumbai, Maharashtra": (18.9067, 72.8147),
    "Bandra West, Mumbai, Maharashtra": (19.0544, 72.8402),
    "Andheri West, Mumbai, Maharashtra": (19.1197, 72.8462),
    "Juhu Beach, Mumbai, Maharashtra": (19.0989, 72.8265)
}

# Hàm lấy tọa độ từ địa chỉ
def get_coordinates(address):
    return predefined_locations.get(address, (None, None))

# Hàm dự đoán giá
def predict_price(Area_SqFt, Floor_No, Bedroom, Bathroom, Location):
    # Số lượng vùng tối đa có thể xử lý
    max_location_count = 8
    x = np.zeros(max_location_count)
    
    # Kiểm tra các giá trị đầu vào
    if Area_SqFt <= 0 or Floor_No < 0 or Bedroom <= 0 or Bathroom <= 0:
        return 0
    
    x[0] = Area_SqFt
    x[1] = Floor_No
    x[2] = Bedroom
    x[3] = Bathroom

    # Lấy danh sách các vùng (Region) có trong dữ liệu, giới hạn tối đa là 8 vùng
    location_list = df['Region'].sort_values().unique()[:max_location_count]
    
    # Kiểm tra nếu Location người dùng chọn có trong danh sách và gán giá trị cho x
    if Location in location_list:
        location_index = np.where(location_list == Location)[0][0]
        x[4 + location_index] = 1
    
    predicted_price = reg.predict([x])[0]
    return max(predicted_price, 0)

# Giao diện ứng dụng
def run_ml_app():
    # Khởi tạo session_state cho địa chỉ ngẫu nhiên và tọa độ nếu chưa có
    if "random_address" not in st.session_state:
        st.session_state.random_address = None
    if "lat" not in st.session_state:
        st.session_state.lat = None
    if "lon" not in st.session_state:
        st.session_state.lon = None
    
    # Chọn Location và hiển thị trên bản đồ
    st.subheader("Select Location to Display on Map")
    
    # Chọn Location ngẫu nhiên hay Location người dùng chọn
    location_choice = st.radio("Choose location type", ("Random", "Select"))
    
    # Địa chỉ ngẫu nhiên
    if location_choice == "Random":
        if st.button("Generate Random Location"):
            random_address = random.choice([ 
                "Marine Drive, Mumbai, Maharashtra", 
                "Colaba, Mumbai, Maharashtra", 
                "Bandra West, Mumbai, Maharashtra", 
                "Andheri West, Mumbai, Maharashtra", 
                "Juhu Beach, Mumbai, Maharashtra"
            ])
            st.session_state.random_address = random_address  # Cập nhật địa chỉ ngẫu nhiên

        # Hiển thị địa chỉ ngẫu nhiên và tìm tọa độ
        if st.session_state.random_address:
            st.write(f"Random Address: {st.session_state.random_address}")
            lat, lon = get_coordinates(st.session_state.random_address)
            if lat and lon:
                st.session_state.lat = lat
                st.session_state.lon = lon
            else:
                st.warning(f"No coordinates found for {st.session_state.random_address}.")
        
        selected_location = st.session_state.random_address

    else:
        # Chọn Location từ danh sách
        selected_location = st.selectbox("Select the Location", df['Region'].sort_values().unique())

        # Cập nhật tọa độ trong session_state khi người dùng chọn địa điểm
        if selected_location != st.session_state.get('selected_location', None):
            location_row = dfmap[dfmap['Region'] == selected_location]
            if not location_row.empty:
                lat, lon = location_row.iloc[0]['Latitude'], location_row.iloc[0]['Longitude']
                st.session_state.lat = lat
                st.session_state.lon = lon
            else:
                # Sinh tọa độ ngẫu nhiên trong phạm vi cho phép nếu không có tọa độ
                lat = random.uniform(18.9752264, 19.2777851)
                lon = random.uniform(72.8147689, 73.1213724)
                st.session_state.lat = lat
                st.session_state.lon = lon
            st.session_state.selected_location = selected_location  # Cập nhật địa điểm đã chọn

    # Hiển thị bản đồ với tọa độ đã lưu
    if st.session_state.lat and st.session_state.lon:
        location_map = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=14)
        folium.Marker([st.session_state.lat, st.session_state.lon], popup=f"Region: {selected_location}").add_to(location_map)
        folium_static(location_map)
    
    # Giao diện nhập liệu
    st.subheader("Property Details")
    Area_SqFt = st.slider("Select Total Area in SqFt", 500, int(max(df['Area_SqFt'])), step=100)
    Floor_No = st.selectbox("Enter Floor Number", range(26))
    Bathroom = st.selectbox("Enter Number of Bathrooms", df['Bathroom'].sort_values().unique())
    Bedroom = st.selectbox("Enter Number of Bedrooms", df['Bedroom'].sort_values().unique())
    
    # Tính toán giá
    st.subheader("Prediction")
    if st.button("Calculate Price"):
        result = predict_price(Area_SqFt, Floor_No, Bedroom, Bathroom, selected_location)
        if result == 0:
            st.warning("The predicted price is invalid (negative or zero). Please check the input values or retrain your model.")
        else:
            st.success(f'Total Price in USD: ${result:,.2f}')

if __name__ == '__main__':
    run_ml_app()
