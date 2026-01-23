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
POS_WEIGHTS = {"QB": 0.25, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.10}
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
    if amount >= 1000000:
        return f"${amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"${amount/1000:.0f}K"
    return f"${int(amount)}"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers"]
    return f"{random.choice(first)} {random.choice(last)}"

def calculate_saban_score(career_stats, prestige):
    wins = career_stats['w'] * 1
    bowls = career_stats['bowl_w'] * 5
    titles = career_stats['titles'] * 50
    prest = prestige * 0.5
    return int(wins + bowls + titles + prest)

def get_bowl_name(rank):
    if rank <= 12: return "CFP Playoff"
    elif rank <= 18: return random.choice(BOWL_MAPPING["Elite"])
    elif rank <= 25: return random.choice(BOWL_MAPPING["High"])
    elif rank <= 40: return random.choice(BOWL_MAPPING["Mid"])
    else: return random.choice(BOWL_MAPPING["Low"])

def generate_initial_roster(tier):
    base = 64
    if tier == 1: base = 90
    elif tier == 2: base = 82
    elif tier == 3: base = 74
    
    roster = {}
    for p in POSITIONS:
        roster[p] = min(99, max(40, base + random.randint(0, 6)))
    return roster

def generate_star_player(position, tier):
    base = 75
    if tier == 1: base = 92
    elif tier == 2: base = 86
    
    star = {}
    star["id"] = random.randint(10000, 99999)
    star["name"] = generate_name()
    star["pos"] = position
    star["rating"] = min(99, base + random.randint(2, 6))
    star["year"] = random.choice(["Fr", "So", "Jr", "Sr"])
    star["trait"] = random.choice(list(TRAITS.keys()))
    return star

def calculate_ovr(roster, stars, OC, DC):
    off_sum = sum(roster[p] for p in ["QB", "RB", "WR", "OL"])
    off_rating = off_sum / 4
    
    def_sum = sum(roster[p] for p in ["DL", "LB", "DB"])
    def_rating = def_sum / 3
    
    off_rating += (OC - 5) * 1.5 
    def_rating += (DC - 5) * 1.5 
    
    star_boost = 0
    for s in stars:
        if s['trait'] == "🧠 General":
            star_boost += 2
            
    return int((off_rating * 0.5) + (def_rating * 0.5) + star_boost)

def generate_schedule(my_team_name):
    pool = [t for t in OPPONENT_POOL if t != my_team_name]
    return random.sample(pool, 12)

# MODIFIED: Accepts the full opponent database to look up real ratings
def play_game(my_rating, opponent_name, coach_lvl, stars, opponents_db):
    if "FCS" in opponent_name:
        opp_rating = random.randint(55, 65)
    else:
        # Default to 75 if not found, otherwise use persistent rating
        opp_rating = opponents_db.get(opponent_name, 75)
        # Add slight variance so they aren't static robots
        opp_rating += random.randint(-2, 2)
    
    rating_diff = my_rating - opp_rating
    execution_bonus = (coach_lvl - 5) * 0.5 
    
    trait_impact = 0
    clutch = False
    
    for s in stars:
        if s['trait'] == "😤 Enforcer":
            trait_impact += 2 
        if s['trait'] == "❄️ Clutch" and abs(rating_diff) < 8:
            trait_impact += 5
            clutch = True
    
    final_margin = rating_diff + execution_bonus + trait_impact + random.randint(-8, 8)
    
    my_score = 0
    opp_score = 0
    res = ""
    
    if final_margin > 0:
        res = "W"
        my_score = int(28 + (final_margin / 1.5))
        opp_score = int(my_score - final_margin)
    else:
        res = "L"
        opp_score = int(30 + (abs(final_margin) / 1.5))
        my_score = int(opp_score - abs(final_margin))
        
    result = {}
    result["result"] = res
    result["score"] = f"{max(0,my_score)}-{max(0,opp_score)}"
    result["ovr"] = opp_rating
    result["clutch"] = clutch
    result["my_power"] = int(my_rating + execution_bonus + trait_impact)
    return result

def process_recruiting(budget, allocations, scout_lvl, prestige, inflation):
    results = {"roster_updates": {}, "gems": [], "cost": 0, "booster_bonus": 0}
    total_cost = sum(allocations.values())
    
    if total_cost > budget:
        return None
    
    results["cost"] = total_cost
    scout_eff = 1.0 + (scout_lvl / 10.0)
    prestige_bonus = 1.0 + (prestige / 200.0)
    
    for pos, amount in allocations.items():
        if amount > 0:
            buying_power = amount / (800000 * inflation)
            rating_gain = buying_power * scout_eff * prestige_bonus
            
            gem_prob = (scout_lvl * 4) / 100.0
            thresh = 250000 * inflation
            
            if amount > thresh and random.random() < gem_prob:
                rating_gain += 5 
                new_star = generate_star_player(pos, 1)
                new_star['year'] = "Fr"
                new_star['name'] = f"{new_star['name']} (GEM)"
                results["gems"].append(new_star)
                results["booster_bonus"] += random.randint(2, 5) * 100000
            
            results["roster_updates"][pos] = rating_gain
    return results

# --- 5. INITIALIZATION ---

if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP'
    st.session_state.year = 2026
    st.session_state.budget = 0
    st.session_state.prestige = 50
    st.session_state.job_security = 100
    st.session_state.booster_morale = 80
    st.session_state.roster = {}
    st.session_state.stars = []
    st.session_
