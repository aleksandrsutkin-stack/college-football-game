import streamlit as st
import random
import time
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gridiron CEO", page_icon="🏈", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
        text-align: center;
    }
    .star-card {
        background-color: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .star-name { font-size: 1.2em; font-weight: bold; color: #1e3a8a; }
    .star-trait { font-size: 0.9em; color: #d97706; font-weight: 600; }
    .star-rating { font-size: 1.5em; float: right; font-weight: bold; color: #10b981; }
    .legacy-card {
        background-color: #fff8e1;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffecb3;
        text-align: center;
        margin-bottom: 20px;
    }
    .gem-box {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #2196f3;
        margin-bottom: 5px;
    }
    .news-ticker {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffeeba;
        font-style: italic;
        margin-bottom: 15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIG & DATA ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
POS_WEIGHTS = {"QB": 0.20, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.15}

FIRST_NAMES = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Stone", "General", "Maverick"]
LAST_NAMES = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Downs", "Bond", "Nix", "Penix", "Bowers", "Sayin", "Manning"]

HEADLINES = [
    "BREAKING: Ohio State lands 5-star QB from Texas!",
    "RUMOR: Coach Prime considering NFL offers?",
    "ANALYSIS: SEC defenses looking softer this year.",
    "ALUMNI: Boosters demanding a National Title run.",
    "RECRUITING: Top WR decommits from Alabama.",
    "INJURY REPORT: Star players resting for playoffs.",
    "POLLS: Georgia unanimous #1 in preseason rankings.",
    "SCANDAL: NCAA investigating improper benefits at rival school."
]

TRAITS = {
    "None": {"desc": "No special ability", "effect": 0},
    "❄️ Clutch": {"desc": "+10 Rating in 4th Qtr/Close Games", "effect": 1},
    "🚀 Speedster": {"desc": "High Variance Scoring (Big Plays)", "effect": 2},
    "🧠 Field General": {"desc": "Boosts entire Offense +2", "effect": 3},
    "😤 Enforcer": {"desc": "Opponent scores less (Intimidation)", "effect": 4},
}

TEAMS_DB = {
    "Georgia": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BA0C2F"},
    "Ohio State": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BB0000"},
    "Texas": {"tier": 1, "budget": 25_000_000, "expect": 10, "coach": 9, "facilities": 10, "color": "#BF5700"},
    "Alabama": {"tier": 1, "budget": 22_000_000, "expect": 10, "coach": 9, "facilities": 9, "color": "#9E1B32"},
    "Florida St": {"tier": 2, "budget": 15_000_000, "expect": 9, "coach": 7, "facilities": 8, "color": "#782F40"},
    "Penn State": {"tier": 2, "budget": 16_000_000, "expect": 9, "coach": 8, "facilities": 8, "color": "#041E42"},
    "Boise State": {"tier": 3, "budget": 7_000_000, "expect": 9, "coach": 6, "facilities": 5, "color": "#0033A0"},
    "Vanderbilt": {"tier": 3, "budget": 8_000_000, "expect": 5, "coach": 5, "facilities": 4, "color": "#866D4B"},
    "San Jose State": {"tier": 4, "budget": 4_500_000, "expect": 6, "coach": 5, "facilities": 3, "color": "#0055A2"},
}

OPPONENT_POOL = [
    "USC", "Michigan", "LSU", "Clemson", "Notre Dame", "Oklahoma", "Miami",
    "Tennessee", "Auburn", "Texas A&M", "Wisconsin", "UCLA", "Iowa",
    "Stanford", "Cal", "Arizona State", "Washington", "Utah", "TCU",
    "Baylor", "Texas Tech", "Okla State", "Kansas State", "North Carolina",
    "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St"
]

# --- HELPERS ---
def generate_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_star_player(position, tier):
    base = 94 if tier == 1 else (88 if tier == 2 else 80)
    rating = min(99, base + random.randint(0, 5))
    trait_name = random.choice(list(TRAITS.keys()))
    if tier == 4 and random.random() > 0.3: 
        trait_name = "None"
        
    return {
        "id": random.randint(1000,9999),
        "name": generate_name(),
        "pos": position,
        "rating": rating,
        "year": random.choice(["Fr", "So", "Jr", "Sr"]),
        "trait": trait_name
    }

def calculate_ovr(roster, stars):
    base_ovr = sum(roster[p] * w for p, w in POS_WEIGHTS.items())
    star_bonus = 0
    for s in stars:
        diff = max(0, s['rating'] - roster[s['pos']])
        star_bonus += (diff * POS_WEIGHTS[s['pos']])
        if s['trait'] == "🧠 Field General": 
            star_bonus += 2
    return int(round(base_ovr + star_bonus, 0))

def calculate_saban_score():
    w = st.session_state.career_stats['w']
    bw = st.session_state.career_stats['bowl_w']
    natty = st.session_state.career_stats['titles']
    prest = st.session_state.prestige
    return int((w * 1) + (bw * 5) + (natty * 50) + (prest * 0.5))

def format_cash(amount):
    if amount >= 1_000_000:
        return f"${int(amount/1_000_000)}M"
    elif amount >= 1_000:
        return f"${int(amount/1_000)}K"
    return f"${int(amount)}"

# --- STATE INIT ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP'
    st.session_state.year = 2026
    st.session_state.budget = 0
    st.session_state.prestige = 50
    st.session_state.job_security = 100
    st.session_state.start_prestige = 50 
    st.session_state.start_rating = 0    
    st.session_state.roster = {} 
    st.session_state.stars = []
    st.session_state.hall_of_fame = []
    st.session_state.record = {"w": 0, "l": 0}
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
    st.session_state.facilities = {"Marketing": 1, "Training": 1, "Stadium": 1}
    st.session_state.staff = {"Coach": 5, "Scout": 5, "Coach_Sal": 3000000, "Scout_Sal": 500000}
    st.session_state.rank = 0
    st.session_state.inflation = 1.0
    st.session_state.team_color = "#333333"
    st.session_state.current_headline = random.choice(HEADLINES)

# --- SCREENS ---

def run_setup():
    st.title("🏆 Gridiron CEO V2.6")
    st.markdown("### Dynasty Mode")
    
    col1, col2 = st.columns(2)
    with col1: 
        name = st.text_input("AD Name", "Coach Prime")
    with col2: 
        diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    sorted_teams = sorted(TEAMS_DB.keys(), key=lambda x: (TEAMS_DB[x]['tier'], x))
    team = st.selectbox("Choose School", sorted_teams, format_func=lambda x: f"{x} (Tier {TEAMS_DB[x]['tier']})")
    d = TEAMS_DB[team]
    
    st.info(f"**{team}** | Tier {d['tier']} | Budget: ${d['budget']:,}")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = d.get('color', '#333333')
        
        mult = 1.0
        if "Hard" in diff: mult = 0.75
        elif "Easy" in diff: mult = 1.25
            
        st.session_state.budget = int(d['budget'] * mult)
        st.session_state.win_expect = d['expect']
        st.session_state.prestige = 95 - (d['tier'] * 12)
        st.session_state.start_prestige = st.session_state.prestige
        
        base_rtg = 92 if d['tier'] == 1 else (84 if d['tier'] == 2 else 74)
        if d['tier'] == 4: base_rtg = 65
        st.session_state.roster = {p: min(99, max(40, base_rtg + random.randint(-5, 5))) for p in POSITIONS}
        
        st.session_state.stars = []
        st.session_state.stars.append(generate_star_player("QB", d['tier']))
        if d['tier'] < 4:
            st.session_state.stars.append(generate_star_player("LB", d['tier']))
            
        st.session_state.team_rating = calculate_ovr(st.session_state.roster, st.session_state.stars)
        st.session_state.start_rating = st.session_state.team_rating
        st.session_state.facilities['Training'] = d['facilities']
        st.session_state.facilities['Marketing'] = d['facilities']
        st.session_state.facilities['Stadium'] = d['facilities']
        
        base = max(4, 9 - d['tier'])
        st.session_state.staff = {"Coach": base, "Scout": base, "Coach_Sal": base*400000, "Scout_Sal": base*150000}
        
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    saban = calculate_saban_score()
