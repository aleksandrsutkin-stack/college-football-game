import streamlit as st
import random
import time
import pandas as pd

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Gridiron CEO", page_icon="🏈", layout="centered")

# --- 2. CSS STYLING ---
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
REGIONS = ["South", "North", "West", "Texas"]

TEAMS_DB = {}
TEAMS_DB["Georgia"] = {"tier": 1, "budget": 24000000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BA0C2F", "region": "South"}
TEAMS_DB["Ohio State"] = {"tier": 1, "budget": 24000000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BB0000", "region": "North"}
TEAMS_DB["Texas"] = {"tier": 1, "budget": 25000000, "expect": 10, "coach": 9, "facilities": 10, "color": "#BF5700", "region": "Texas"}
TEAMS_DB["Alabama"] = {"tier": 1, "budget": 22000000, "expect": 10, "coach": 9, "facilities": 9, "color": "#9E1B32", "region": "South"}
TEAMS_DB["Oregon"] = {"tier": 1, "budget": 20000000, "expect": 10, "coach": 9, "facilities": 10, "color": "#154733", "region": "West"}
TEAMS_DB["Florida St"] = {"tier": 2, "budget": 15000000, "expect": 9, "coach": 7, "facilities": 8, "color": "#782F40", "region": "South"}
TEAMS_DB["Penn State"] = {"tier": 2, "budget": 16000000, "expect": 9, "coach": 8, "facilities": 8, "color": "#041E42", "region": "North"}
TEAMS_DB["Boise State"] = {"tier": 3, "budget": 7000000, "expect": 9, "coach": 6, "facilities": 5, "color": "#0033A0", "region": "West"}
TEAMS_DB["San Jose State"] = {"tier": 4, "budget": 4500000, "expect": 6, "coach": 5, "facilities": 3, "color": "#0055A2", "region": "West"}

OPPONENT_POOL = [
    "USC", "Michigan", "LSU", "Clemson", "Notre Dame", "Oklahoma", "Miami",
    "Tennessee", "Auburn", "Texas A&M", "Wisconsin", "UCLA", "Iowa",
    "Stanford", "Cal", "Arizona State", "Washington", "Utah", "TCU",
    "Baylor", "Texas Tech", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St"
]

BOWL_MAPPING = {}
BOWL_MAPPING["Elite"] = ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"]
BOWL_MAPPING["High"] = ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl", "ReliaQuest Bowl"]
BOWL_MAPPING["Mid"] = ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl", "Sun Bowl", "Pinstripe Bowl"]
BOWL_MAPPING["Low"] = ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl", "Frisco Bowl", "Myrtle Beach Bowl"]

TRAITS = {}
TRAITS["None"] = {"desc": "No special ability", "effect": 0}
TRAITS["❄️ Clutch"] = {"desc": "+10 in Close Games", "effect": 5}
TRAITS["🚀 Speedster"] = {"desc": "High Variance Scoring", "effect": 0}
TRAITS["🧠 General"] = {"desc": "Boosts Offense +2", "effect": 3}
TRAITS["😤 Enforcer"] = {"desc": "Lowers Opponent Score", "effect": 3}

HEADLINES = [
    "Rumor: Offensive Coordinator considering NFL jobs.",
    "Boosters reportedly 'furious' after rival loss.",
    "Analyst: 'This team recruits the South better than anyone.'",
    "Breaking: 5-Star QB spotted at campus steakhouse.",
    "Stadium renovations approved by the board.",
    "Polls: Voters skeptical of strength of schedule."
]

# --- 4. HELPER FUNCTIONS ---

def format_cash(amount):
    if amount >= 1000000: return f"${amount/1000000:.1f}M"
    elif amount >= 1000: return f"${amount/1000:.0f}K"
    return f"${int(amount)}"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers"]
    return f"{random.choice(first)} {random.choice(last)}"

def calculate_saban_score(career_stats, prestige):
    wins = career_stats['w'] * 1
    bowls = career_stats['bowl_w'] * 5
    titles = career_stats['
