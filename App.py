import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# MODULE: CONFIGURATION & DATA
# ==============================================================================
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
POS_WEIGHTS = {"QB": 0.25, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.10}
REGIONS = ["South", "North", "West", "Texas"]

TEAMS_DB = {
    "Georgia": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BA0C2F", "region": "South"},
    "Ohio State": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BB0000", "region": "North"},
    "Texas": {"tier": 1, "budget": 25_000_000, "expect": 10, "coach": 9, "facilities": 10, "color": "#BF5700", "region": "Texas"},
    "Alabama": {"tier": 1, "budget": 22_000_000, "expect": 10, "coach": 9, "facilities": 9, "color": "#9E1B32", "region": "South"},
    "Oregon": {"tier": 1, "budget": 20_000_000, "expect": 10, "coach": 9, "facilities": 10, "color": "#154733", "region": "West"},
    "Florida St": {"tier": 2, "budget": 15_000_000, "expect": 9, "coach": 7, "facilities": 8, "color": "#782F40", "region": "South"},
    "Penn State": {"tier": 2, "budget": 16_000_000, "expect": 9, "coach": 8, "facilities": 8, "color": "#041E42", "region": "North"},
    "Boise State": {"tier": 3, "budget": 7_000_000, "expect": 9, "coach": 6, "facilities": 5, "color": "#0033A0", "region": "West"},
    "San Jose State": {"tier": 4, "budget": 4_500_000, "expect": 6, "coach": 5, "facilities": 3, "color": "#0055A2", "region": "West"},
}

OPPONENT_POOL = [
    "USC", "Michigan", "LSU", "Clemson", "Notre Dame", "Oklahoma", "Miami",
    "Tennessee", "Auburn", "Texas A&M", "Wisconsin", "UCLA", "Iowa",
    "Stanford", "Cal", "Arizona State", "Washington", "Utah", "TCU",
    "Baylor", "Texas Tech", "Okla State", "Kansas State", "North Carolina",
    "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St"
]

TRAITS = {
    "None": {"desc": "No special ability", "effect": 0},
    "❄️ Clutch": {"desc": "+10 in Close Games", "effect": 5},
    "🚀 Speedster":
