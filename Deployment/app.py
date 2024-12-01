import json
import pickle
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

# Importing the smaller apps
from ml_app import run_ml_app
from dd_app import run_dd_app
from da_app import run_da_app

# CSS for improved styling
def apply_styles():
    st.markdown("""
    <style>
        /* Nền tổng quan */
        .main {
            background-color: #F3F4F6;
        }

        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: #ffffff;
            border-radius: 10px;
        }

        /* Màu chữ chung */
        .css-1d391kg p, .css-1d391kg ul, .css-1d391kg li {
            color: #1F2937;
            font-family: 'Arial', sans-serif;
        }

        /* Tiêu đề chính */
        h1 {
            color: #2563EB;
            font-size: 32px;
            font-weight: bold;
        }

        /* Tiêu đề phụ */
        h2 {
            color: #2563EB;
            font-size: 24px;
        }

        /* Nút hành động */
        .stButton > button {
            background-color: #10B981;
            color: white;
            font-size: 18px;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
        }

        .stButton > button:hover {
            background-color: #059669;
        }

        /* Chatbot ở Sidebar */
        .chatbot-section {
            background-color: #f7f7f7;
            padding: 15px;
            border-radius: 10px;
            margin-top: 30px;
        }

        /* Tooltip hoặc cảnh báo */
        .css-1d391kg .warning {
            background-color: #F59E0B;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

import json
import streamlit as st

import requests

def load_faq():
    """Load FAQ data from JSON file."""
    response = requests.get("https://raw.githubusercontent.com/AhnTus/STWeb-HousePricePrediction/refs/heads/main/Deployment/faq_data.json")
    data = response.json()
    return data["faq"]

def search_faq(query, faq_data):
    """Search for FAQ questions containing the query."""
    result = [item for item in faq_data if query.lower() in item["question"].lower()]
    return result if result else None

def follow_up_question(last_answer):
    """Generate follow-up question based on the answer."""
    if "price prediction" in last_answer.lower():
        return "Would you like to predict the price for a specific property?"
    return None

def chatbot_sidebar():
    """Chatbot section in the sidebar."""
    faq_data = load_faq()
    
    # Create a set to store displayed answers
    displayed_answers = set()

    # Sidebar Chatbot UI
    with st.sidebar:
        st.subheader("💬 Chatbot")
        
        # User can type a custom question
        user_question = st.text_input("Ask a question:")

        if user_question:
            # Search for related questions in FAQ
            search_result = search_faq(user_question, faq_data)
            if search_result:
                for item in search_result:
                    if item["answer"] not in displayed_answers:  # Only show if answer is not already displayed
                        st.info(f"**Answer:** {item['answer']}")
                        displayed_answers.add(item["answer"])  # Add answer to the set
                follow_up = follow_up_question(search_result[0]["answer"])
                if follow_up:
                    st.write(f"🤔 Follow-up Question: {follow_up}")
            else:
                st.warning("Sorry, I couldn't find an answer to your question.")

        else:
            questions = [item["question"] for item in faq_data]
            selected_question = st.selectbox("Or choose from the FAQs:", [""] + questions)
            if selected_question:
                for item in faq_data:
                    if item["question"] == selected_question:
                        if item["answer"] not in displayed_answers:  # Only show if answer is not already displayed
                            st.info(f"**Answer:** {item['answer']}")
                            displayed_answers.add(item["answer"])  # Add answer to the set
                        follow_up = follow_up_question(item["answer"])
                        if follow_up:
                            st.write(f"🤔 Follow-up Question: {follow_up}")
                        break

def enhanced_homepage():
    st.markdown("""
    <div style="background-color:#33CCFF;padding:15px;border-radius:10px;margin-bottom:20px;">
        <h1 style="color:white;text-align:center;">🏠 Welcome to Real Estate Price Prediction!</h1>
        <p style="color:white;text-align:center;font-size:18px;">
            Your one-stop solution for accurate, AI-driven home price insights. 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features Section
    st.markdown("""
    <div style="margin-bottom:30px;">
        <h2 style="text-align:center;color:#333;">✨ Key Features</h2>
        <ul style="font-size:18px;line-height:1.8;">
            <li>🌍 <b>Explore Market Trends</b>: Access robust datasets and dynamic visualizations to understand real estate trends.</li>
            <li>📈 <b>Predict Home Prices</b>: Use AI-powered predictive models to get accurate property valuations.</li>
            <li>💬 <b>Chatbot Assistance</b>: Instant support for your questions about property insights.</li>
            <li>🗺️ <b>Interactive Map</b>: View properties on an intuitive map interface for better decision-making.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Why Choose Us Section
    st.markdown("""
    <div style="background-color:#f7f7f7;padding:15px;border-radius:10px;">
        <h2 style="color:#333;text-align:center;">🤔 Why Choose Us?</h2>
        <p style="font-size:18px;text-align:justify;">
            At <b>Real Estate Price Prediction</b>, we are committed to empowering you with the best tools for your property investments. Here's why we stand out:
        </p>
        <ul style="font-size:18px;line-height:1.8;">
            <li>💡 **State-of-the-art Technology**: Leverage advanced AI and ML models for precision.</li>
            <li>📊 **Data-Driven Insights**: Back every decision with comprehensive data analytics.</li>
            <li>🔒 **Secure and Private**: Your data remains safe with our robust security practices.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Call-to-Action Section
    st.markdown("""
    <div style="text-align:center;margin-top:30px;">
        <h2 style="color:#33CCFF;">Ready to Make Smarter Property Decisions? 🏡</h2>
        <p style="font-size:18px;">
            Start exploring market insights, predicting home prices, and making data-driven decisions today!
        </p>
        <a href="#" style="background-color:#33CCFF;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;font-size:18px;">
            🚀 Get Started Now!
        </a>
    </div>
    """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.markdown("""<div style="background-color:#33CCFF;padding:10px;border-radius:10px;text-align:center;">
        <h1 style="color:white;">Real Estate Price Prediction</h1></div>""", unsafe_allow_html=True)

    menu = ["🏠 Home", "📊 Data Description", "📈 Data Analysis", "💵 Prediction", "🗺️ Map"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "🏠 Home":
        enhanced_homepage()
    elif choice == "📊 Data Description":
        run_dd_app()
    elif choice == "📈 Data Analysis":
        run_da_app()
    elif choice == "💵 Prediction":
        run_ml_app()
    elif choice == "🗺️ Map":
        url_to_html = "https://raw.githubusercontent.com/AhnTus/STWeb-HousePricePrediction/refs/heads/main/Deployment/mumbai_property.html"
        response = requests.get(url_to_html)
        html_data = response.text
        st.subheader("Map view:")
        components.html(html_data, height=500)

    # Always show chatbot on the sidebar
    chatbot_sidebar()

if __name__ == "__main__":
    main()
