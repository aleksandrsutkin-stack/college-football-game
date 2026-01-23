import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# College Football V1 (Streamlit)
# Offseason Pipeline: NIL -> Outreach -> Top 8 Battles
# AI recruiting spend (Proposal G) included
# ==============================================================================

# -----------------------------
# Streamlit config
# -----------------------------
try:
    st.set_page_config(page_title="College Football V1", page_icon="🏈", layout="wide")
except:
    pass

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: 800; }
.small { font-size: 0.9em; color: #666; }
.kpi { background: #f8f9fa; border: 1px solid #e6e6e6; padding: 12px; border-radius: 10px; }
.box { background: white; border: 1px solid #eee; padding: 12px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
.badge { padding: 2px 8px; border-radius: 8px; border: 1px solid #ddd; font-weight: 800; font-size: 0.8em; display: inline-block; }
.badge-green { background: #eaf7ea; border-color: #cfe9cf; color: #1f6c1f; }
.badge-yellow { background: #fff6db; border-color: #ffe6a6; color: #7a5b00; }
.badge-red { background: #fdecec; border-color: #f7caca; color: #8a1a1a; }
.card { border: 1px solid #eee; border-left: 6px solid #ddd; border-radius: 12px; padding: 12px; margin-bottom: 10px; background: white; }
.win { border-left-color: #2e7d32; }
.loss { border-left-color: #c62828; }
.pending { border-left-color: #6c757d; background: #f8f9fa; }
.rival { border: 2px solid #ffc107; background: #fffaf0; }
.hr { border-top: 1px solid #eee; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# STATIC DATA
# ==============================================================================
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}
SCHEMES = {"Offense": ["Air Raid", "Smashmouth", "Pro Style"], "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]}
COUNTERS = {
    "Air Raid": "3-3-5 Cloud",
    "Smashmouth": "4-4 Heavy",
    "Pro Style": "Man Coverage",
    "3-3-5 Cloud": "Smashmouth",
    "4-4 Heavy": "Air Raid",
    "Man Coverage": "Pro Style"
}
TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {"None": "None", "Recruiter": "+10% Recruiting", "Tactician": "+3 Game Boost", "Air Raid": "+2 Scheme", "Smashmouth": "+2 Scheme", "Pro Style": "+2 Scheme"}
BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"]
}

TEAMS_DB = {
    "Georgia": {"color": "#BA0C2F"}, "Alabama": {"color": "#9E1B32"}, "Ohio State": {"color": "#BB0000"},
    "Michigan": {"color": "#00274C"}, "Texas": {"color": "#BF5700"}, "Oklahoma": {"color": "#841617"},
    "Oregon": {"color": "#154733"}, "Washington": {"color": "#4B2E83"}, "Florida St": {"color": "#782F40"},
    "Miami": {"color": "#005030"}, "Penn State": {"color": "#041E42"}, "Notre Dame": {"color": "#0C2340"},
    "LSU": {"color": "#461D7C"}, "Ole Miss": {"color": "#CE1126"}, "Tennessee": {"color": "#FF8200"},
    "Auburn": {"color": "#0C2340"}, "Indiana": {"color": "#990000"}, "Purdue": {"color": "#CEB888"},
    "Colorado": {"color": "#CFB87C"}, "USC": {"color": "#990000"}, "Boise State": {"color": "#0033A0"},
    "San Jose State": {"color": "#0055A2"}, "Texas A&M": {"color": "#500000"}, "Texas Tech": {"color": "#CC0000"},
    "BYU": {"color": "#002E5D"}, "Tulane": {"color": "#006747"}
}

REAL_WORLD_INIT = {
    "Indiana": {"Prestige": 70, "Talent": 86, "Tier": 2, "Rival": "Purdue"},
    "Ohio State": {"Prestige": 95, "Talent": 94, "Tier": 1, "Rival": "Michigan"},
    "Miami": {"Prestige": 88, "Talent": 89, "Tier": 2, "Rival": "Florida St"},
    "Oregon": {"Prestige": 93, "Talent": 92, "Tier": 1, "Rival": "Washington"},
    "Georgia": {"Prestige": 92, "Talent": 96, "Tier": 1, "Rival": "Florida"},
    "Ole Miss": {"Prestige": 86, "Talent": 88, "Tier": 2, "Rival": "Mississippi St"},
    "Texas Tech": {"Prestige": 78, "Talent": 84, "Tier": 3, "Rival": "Baylor"},
    "Texas A&M": {"Prestige": 86, "Talent": 91, "Tier": 2, "Rival": "Texas"},
    "Alabama": {"Prestige": 90, "Talent": 95, "Tier": 1, "Rival": "Auburn"},
    "Notre Dame": {"Prestige": 88, "Talent": 90, "Tier": 2, "Rival": "USC"},
    "BYU": {"Prestige": 75, "Talent": 82, "Tier": 3, "Rival": "Utah"},
    "Texas": {"Prestige": 90, "Talent": 97, "Tier": 1, "Rival": "Oklahoma"},
    "Oklahoma": {"Prestige": 86, "Talent": 90, "Tier": 2, "Rival": "Texas"},
    "Utah": {"Prestige": 78, "Talent": 85, "Tier": 3, "Rival": "BYU"},
    "Vanderbilt": {"Prestige": 72, "Talent": 78, "Tier": 4, "Rival": "Tennessee"},
    "USC": {"Prestige": 85, "Talent": 89, "Tier": 2, "Rival": "Notre Dame"},
    "Michigan": {"Prestige": 90, "Talent": 91, "Tier": 1, "Rival": "Ohio State"},
    "Penn State": {"Prestige": 86, "Talent": 88, "Tier": 2, "Rival": "Ohio State"},
    "LSU": {"Prestige": 88, "Talent": 92, "Tier": 2, "Rival": "Alabama"},
    "Florida St": {"Prestige": 82, "Talent": 87, "Tier": 3, "Rival": "Miami"},
    "Colorado": {"Prestige": 76, "Talent": 85, "Tier": 3, "Rival": "Nebraska"},
    "Boise State": {"Prestige": 74, "Talent": 79, "Tier": 3, "Rival": "Fresno St"},
    "Tulane": {"Prestige": 73, "Talent": 77, "Tier": 3, "Rival": "LSU"}
}

CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Texas A&M", "Ole Miss", "Vanderbilt", "Florida", "Mississippi St"],
    "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington", "Indiana", "Nebraska", "Purdue"],
    "ACC": ["Florida St", "Clemson", "Miami", "Stanford", "Cal", "Louisville", "UNC", "Virginia Tech", "SMU"],
    "Big 12": ["Utah", "TCU", "Baylor", "Texas Tech", "Arizona State", "Colorado", "Kansas State", "Oklahoma St", "BYU", "Arizona"],
    "G5": ["Boise State", "San Jose State", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St", "Fresno St", "Tulane", "Memphis", "Navy", "Army"]
}
ALL_TEAMS = [t for c in CONFERENCES.values() for t in c]


# ==============================================================================
# HELPERS
# ==============================================================================
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def helper_format_cash(amount):
    if amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    return f"${int(amount/1_000)}K"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Tank", "Arch", "Shedeur", "Quinn", "Travis", "Ashton", "Malik", "Jayden"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck", "Jeanty", "Judkins", "McCarthy", "Henderson"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name():
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan", "Kalen", "Mike", "James"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman", "Lanning", "DeBoer", "Norvell", "Franklin"]
    return f"{random.choice(first)} {random.choice(last)}"

def get_letter_grade(val):
    if val >= 9: return "A+"
    if val >= 8: return "A"
    if val >= 7: return "B"
    if val >= 5: return "C"
    if val >= 3: return "D"
    return "F"

def compute_team_needs(roster: dict, n=3):
    # lowest positions are "needs"
    items = sorted(roster.items(), key=lambda kv: kv[1])
    return [p for p, _ in items[:n]]

def add_news(msg: str):
    if "news" not in st.session_state:
        st.session_state.news = []
    st.session_state.news.insert(0, f"• {msg}")
    st.session_state.news = st.session_state.news[:30]

def generate_hotspots():
    hotspots = {}
    for reg in REGION_STRENGTH.keys():
        hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

def get_bowl_name(rank):
    if rank <= 12:
        return "CFP Playoff"
    if rank <= 25:
        return random.choice(BOWL_MAPPING["Elite"])
    if rank <= 40:
        return random.choice(BOWL_MAPPING["High"])
    if rank <= 80:
        return random.choice(BOWL_MAPPING["Mid"])
    return random.choice(BOWL_MAPPING["Low"])

def generate_star_player(position, tier):
    return {
        "id": random.randint(10000, 99999),
        "name": generate_name(),
        "pos": position,
        "rating": min(99, 85 + random.randint(0, 10)),
        "year": "Fr",
        "trait": random.choice(TRAITS)
    }

def generate_ga_coach(role):
    return {
        "name": f"GA {generate_name()}",
        "role": role,
        "off": random.randint(1, 3),
        "def": random.randint(1, 3),
        "recruit": random.randint(1, 2),
        "trait": "None",
        "salary": 0,
        "history": "Former Player",
        "scouted": True
    }


# ==============================================================================
# PROGRAM / FACILITY EFFECTS
# ==============================================================================
def training_unit_boost(training_lvl: int) -> float:
    # modest unit boost, scales gently
    return 0.8 + training_lvl * 0.55

def stadium_home_field(stadium_lvl: int) -> float:
    # stronger at high levels
    return clamp(0.6 * stadium_lvl - 1.0, 0.0, 8.0)

def stadium_night_game_aura(stadium_lvl: int, is_home: bool) -> float:
    # occasional extra juice at home
    if not is_home:
        return 0.0
    if stadium_lvl >= 8 and random.random() < 0.22:
        return random.uniform(0.8, 2.2)
    return 0.0


# ==============================================================================
# ENGINE: TEAM GENERATION
# ==============================================================================
def engine_calculate_revenue(tier, marketing_lvl, inflation):
    base = {1: 40_000_000, 2: 25_000_000, 3: 10_000_000, 4: 5_000_000}.get(tier, 5_000_000)
    marketing_bonus = marketing_lvl * 2_000_000
    total = (base + marketing_bonus) * inflation
    return int(total)

def engine_generate_coach(role, tier):
    cost = random.randint(4_000_000, 8_000_000) if tier == 1 else random.randint(500_000, 3_500_000)
    trait_pool = list(COACH_TRAITS.keys())
    if role == "OC":
