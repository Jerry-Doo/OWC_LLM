# -*- encoding: utf-8 -*-
'''
@File    :   web_chat.py
@Time    :   2025/04/11
@Author  :   Yansong Du 
@Contact :   dys24@mails.tsinghua.edu.cn
'''

import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Optical Wireless Communication Expert Q&A System", layout="centered", page_icon="🔬")

# Custom CSS styles for UI improvements
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(45deg, #f6d365, #fda085);  /* Gradient background */
            font-family: 'Times New Roman', serif;  /* Changed font to Times New Roman */
        }
        h1 {
            font-size: 3em;
            font-weight: bold;  /* Added bold for title */
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #4CAF50;  /* Green button */
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            padding: 15px 30px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:hover {
            background-color: #45a049;  /* Button hover effect */
            transform: scale(1.05);  /* Slightly enlarge button on hover */
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
        }
        .stTextInput>div>input {
            border-radius: 12px;
            padding: 15px;
            font-size: 18px;
            width: 100%;
            margin-bottom: 25px;
            border: 2px solid #ddd;
            transition: all 0.3s ease;
        }
        .stTextInput>div>input:focus {
            border-color: #4CAF50;  /* Green border on focus */
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.4);  /* Glow effect on focus */
        }
        .stAlert {
            background-color: #ffcccc; /* Warning box color */
            color: #ff4d4d;
            font-size: 16px;
        }
        .stSuccess {
            background-color: #e0ffe0; /* Success box color */
            color: #28a745;
            font-size: 16px;
        }
        .stMarkdown {
            font-size: 1.1em;
            text-align: center;
            color: #555;
        }
        .stTextInput {
            margin-top: 20px;
        }
        .stSpinner>div {
            color: #4CAF50;  /* Green spinner color */
        }
        
        /* Make all text bold */
        * {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title and introduction with improved layout
st.title("🔬 Optical Wireless Communication Expert Q&A System")
st.markdown("👋 Enter your question about optical wireless communication, and I'll provide a professional answer.")

# Backend API URL
API_URL = "http://localhost:8000/chat"

# User input field within a card-like box
question = st.text_input("Please enter your question:", placeholder="For example: What is Optical Wireless Communication?")

# Send button with enhanced UI
if st.button("Send"):
    if not question.strip():
        st.warning("⚠️ The question cannot be empty, please try again.")
    else:
        with st.spinner("⏳ Generating the answer, please wait..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question}
                )
                if response.status_code == 200:
                    answer = response.json().get("response", "❌ Unable to parse the model's response.")
                    st.success("✅ Here is the answer:")
                    st.write(f"<div style='font-size:18px; line-height:1.8;'>{answer}</div>", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Request failed: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection failed. Please ensure the backend is running. Error message: {str(e)}")
