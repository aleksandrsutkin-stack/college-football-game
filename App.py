import streamlit as st
import random
import time
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Gridiron CEO", page_icon="🏈", layout="centered")

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    .news-ticker { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px; border: 1px solid #ffeeba; }
    .star-card { background: white; border: 1px solid #ddd; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 8px; }
    .staff-card { background: #f0f4c3; border: 1px solid #dce775; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 5px; }
    .gem-box { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 5px solid #2196f3; margin-bottom: 5px; }
    .summary-card { background: #fafafa; padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA CONFIGURATION ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
POS_WEIGHTS = {"QB": 0.25, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.10}
REGIONS = ["South", "North", "West", "Texas"]

TEAMS_DB = {
    "Georgia": {"tier": 1, "budget": 24000000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BA0C2F", "region": "South"},
    "Ohio State": {"tier": 1, "budget": 24000000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BB0000", "region": "North"},
    "Texas": {"tier": 1, "budget": 25000000, "expect": 10, "coach": 9, "facilities": 10, "color": "#BF5700", "region": "Texas"},
    "Alabama": {"tier": 1, "budget": 22000000, "expect": 10, "coach": 9, "facilities": 9, "color": "#9E1B32", "region": "South"},
    "Oregon": {"tier": 1, "budget": 20000000, "expect": 10, "coach": 9, "facilities": 10, "color": "#154733", "region": "West"},
    "Florida St": {"tier": 2, "budget": 15000000, "expect": 9, "coach": 7, "facilities": 8, "color": "#782F40", "region": "South"},
    "Penn State": {"tier": 2, "budget": 16000000, "expect": 9, "coach": 8, "facilities": 8, "color": "#041E42", "region": "North"},
    "Boise State": {"tier": 3, "budget": 7000000, "expect": 9, "coach": 6, "facilities": 5, "color": "#0033A0", "region": "West"},
    "San Jose State": {"tier": 4, "budget": 4500000, "expect":
