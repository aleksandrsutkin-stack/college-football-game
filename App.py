import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# ZONE 1: CONFIGURATION & STATIC DATA (The Universe)
# ==============================================================================
try:
    st.set_page_config(page_title="College Football Mogul V7.2", page_icon="🏈", layout="wide")
except:
    pass

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    
    /* DASHBOARD WIDGETS */
    .security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    .security-safe { color: #28a745; font-weight: bold; }
    .security-warm { color: #fd7e14; font-weight: bold; }
    .security-hot { color: #dc3545; font-weight: bold; }
    
    /* FINANCIAL REPORT BOX */
    .finance-alert { background-color: #d1e7dd; color: #0f5132; border: 1px solid #badbcc; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    .nil-alert { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-size: 1.2em; font-weight: bold; }
    
    /* GAME CARDS */
    .game-card { padding: 10px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #ddd; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .game-card-win { border-left: 5px solid #28a745; }
    .game-card-loss { border-left: 5px solid #dc3545; }
    .game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
    .game-card-rival { border: 2px solid #ffc107 !important; background-color: #fffbf0 !important; }
    
    .card-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 5px;}
    .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.85em; }
    .stat-row { display: flex; justify-content: space-between; }
    
    /* STAFF CARDS */
    .staff-card { background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    .staff-role { font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .staff-name { font-size: 1.1em; font-weight: 800; color: #333; }
    .badge { padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; margin-right: 5px; display: inline-block;}
    .badge-tier-s { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .badge-tier-a { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .badge-tier-f { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .badge-trait { background: #e2e3e5; color: #383d41; }

    .recruiting-intel { background-color: #e0f7fa; border-left: 5px solid #006064; padding: 15px; margin-bottom: 20px; border-radius: 4px; }
    .bracket-box { background-color: #2c3e50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# CONSTANTS
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}
SCHEMES = {"Offense": ["Air Raid", "Smashmouth", "Pro Style"], "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]}
COUNTERS = {"Air Raid": "3-3-5 Cloud", "Smashmouth": "4-4 Heavy", "Pro Style": "Man Coverage", "3-3-5 Cloud": "Smashmouth", "4-4 Heavy": "Air Raid", "Man Coverage": "Pro Style"}
TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {"None": "None", "Recruiter": "+10% Recruiting", "Tactician": "+3 Game Boost", "Air Raid": "+2 Scheme", "Smashmouth": "+2 Scheme", "Pro Style": "+2 Scheme"}
BOWL_MAPPING = {"Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"], "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"], "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"], "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"]}

# DATABASE
TEAMS_DB = {
    "Georgia": {"color": "#BA0C2F"}, "Alabama": {"color": "#9E1B32"}, "Ohio State": {"color": "#BB0000"}, 
    "Michigan": {"color": "#00274C"}, "Texas": {"color": "#BF5700"}, "Oklahoma": {"color": "#841617"},
    "Oregon": {"color": "#154733"}, "Washington": {"color": "#4B2E83"}, "Florida St": {"color": "#782F40"}, 
    "Miami": {"color": "#005030"}, "Penn State": {"color": "#041E42"}, "Notre Dame": {"color": "#0C2340"},
    "LSU": {"color": "#461D7C"}, "Ole Miss": {"color": "#CE1126"}, "Tennessee": {"color": "#FF8200"}, 
    "Auburn": {"color": "#0C2340"}, "Indiana": {"color": "#990000"}, "Purdue": {"color": "#CEB888"},
    "Colorado": {"color": "#CFB87C"}, "USC": {"color": "#990000"}, "Boise State": {"color": "#0033A0"}, 
    "San Jose State": {"color": "#0055A2"}
}

REAL_WORLD_INIT = {
    "Indiana": {"Prestige": 99, "Talent": 86, "Tier": 1, "Rival": "Purdue"},
    "Ohio State": {"Prestige": 95, "Talent": 94, "Tier": 1, "Rival": "Michigan"},
    "Miami": {"Prestige": 94, "Talent": 89, "Tier": 1, "Rival": "Florida St"},
    "Oregon": {"Prestige": 93, "Talent": 92, "Tier": 1, "Rival": "Washington"},
    "Georgia": {"Prestige": 92, "Talent": 96, "Tier": 1, "Rival": "Florida"},
    "Ole Miss": {"Prestige": 91, "Talent": 88, "Tier": 1, "Rival": "Mississippi St"},
    "Texas Tech": {"Prestige": 90, "Talent": 84, "Tier": 2, "Rival": "Baylor"},
    "Texas A&M": {"Prestige": 89, "Talent": 91, "Tier": 2, "Rival": "Texas"},
    "Alabama": {"Prestige": 85, "Talent": 95, "Tier": 1, "Rival": "Auburn"},
    "Notre Dame": {"Prestige": 87, "Talent": 90, "Tier": 1, "Rival": "USC"},
    "BYU": {"Prestige": 86, "Talent": 82, "Tier": 2, "Rival": "Utah"},
    "Texas": {"Prestige": 84, "Talent": 97, "Tier": 1, "Rival": "Oklahoma"},
    "Oklahoma": {"Prestige": 83, "Talent": 90, "Tier": 2, "Rival": "Texas"},
    "Utah": {"Prestige": 82, "Talent": 85, "Tier": 2, "Rival": "BYU"},
    "Vanderbilt": {"Prestige": 80, "Talent": 78, "Tier": 3, "Rival": "Tennessee"},
    "USC": {"Prestige": 79, "Talent": 89, "Tier": 2, "Rival": "Notre Dame"},
    "Michigan": {"Prestige": 78, "Talent": 91, "Tier": 2, "Rival": "Ohio State"},
    "Penn State": {"Prestige": 77, "Talent": 88, "Tier": 2, "Rival": "Ohio State"},
    "LSU": {"Prestige": 76, "Talent": 92, "Tier": 2, "Rival": "Alabama"},
    "Florida St": {"Prestige": 70, "Talent": 87, "Tier": 3, "Rival": "Miami"},
    "Colorado": {"Prestige": 75, "Talent": 85, "Tier": 2, "Rival": "Nebraska"},
    "Boise State": {"Prestige": 72, "Talent": 79, "Tier": 3, "Rival": "Fresno St"},
    "Tulane": {"Prestige": 74, "Talent": 77, "Tier": 3, "Rival": "LSU"}
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
# ZONE 2: HELPER FUNCTIONS & GENERATORS (Stateless)
# ==============================================================================

def helper_format_cash(amount): return f"${amount/1000000:.1f}M" if amount >= 1000000 else f"${int(amount/1000)}K"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Arch", "Shedeur", "Quinn", "Travis", "Ashton"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck", "Jeanty", "Judkins"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name():
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan", "Kalen"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman", "Lanning", "DeBoer"]
    return f"{random.choice(first)} {random.choice(last)}"

def get_letter_grade(val):
    if val >= 9: return "A+"
    elif val >= 8: return "A"
    elif val >= 7: return "B"
    elif val >= 5: return "C"
    elif val >= 3: return "D"
    else: return "F"

def calculate_saban_score(career_stats, prestige):
    return int((career_stats['w'] * 1) + (career_stats['bowl_w'] * 5) + (career_stats['titles'] * 50) + (prestige * 0.5))

def get_bowl_name(rank):
    if rank <= 12: return "CFP Playoff"
    elif rank <= 25: return random.choice(BOWL_MAPPING["Elite"])
    elif rank <= 40: return random.choice(BOWL_MAPPING["High"])
    elif rank <= 80: return random.choice(BOWL_MAPPING["Mid"])
    else: return random.choice(BOWL_MAPPING["Low"])

def generate_star_player(position, tier):
    return {"id": random.randint(10000, 99999), "name": generate_name(), "pos": position, "rating": min(99, 85 + random.randint(0, 10)), "year": "Fr", "trait": random.choice(TRAITS)}

def generate_ga_coach(role):
    return {"name": f"GA {generate_name()}", "role": role, "off": random.randint(1, 3), 
            "def": random.randint(1, 3), "recruit": random.randint(1, 2), "trait": "None", "salary": 50000, "history": "Former Player", "scouted": True}

# ==============================================================================
# ZONE 3: THE ENGINE (Math & Logic)
# ==============================================================================

def engine_calculate_revenue(tier, marketing_lvl, inflation):
    # Safe fallback
    if not tier: tier = 3
    base = {1: 40000000, 2: 25000000, 3: 10000000, 4: 5000000}.get(tier, 5000000)
    marketing_bonus = marketing_lvl * 2000000
    total = (base + marketing_bonus) * inflation
    return int(total)

def engine_generate_coach(role, tier):
    cost = random.randint(4000000, 8000000) if tier == 1 else random.randint(500000, 3500000)
    trait_pool = list(COACH_TRAITS.keys())
    if role == "OC": trait_pool = ["Air Raid", "Smashmouth", "Pro Style", "Recruiter", "Tactician"]
    base = 8 if tier == 1 else (5 if tier == 2 else 1)
    
    histories = ["Former SEC Coordinator", "Promoted from G5", "Ex-NFL Assistant", "High School Legend", "Analyst at Blue Blood"]
    
    return {
        "name": generate_coach_name(), 
        "role": role, 
        "off": min(10, base + random.randint(0, 3)), "def": min(10, base + random.randint(0, 3)), "recruit": min(10, base + random.randint(0, 3)), 
        "trait": random.choice(trait_pool), 
        "salary": cost, "history": random.choice(histories), "scouted": False 
    }

def engine_generate_roster(tier, base_ovr=None):
    base = base_ovr if base_ovr else (90 if tier == 1 else 74)
    roster = {}
    for p in POSITIONS: roster[p] = min(99, max(40, base + random.randint(-4, 4)))
    return roster

def engine_generate_schedule(my_team, my_conf, rival):
    conf_foes = [t for t in CONFERENCES.get(my_conf, CONFERENCES['G5']) if t != my_team]
    if len(conf_foes) >= 8: schedule = random.sample(conf_foes, 8)
    else: schedule = conf_foes
    needed = 12 - len(schedule)
    non_conf = [t for t in ALL_TEAMS if t not in CONFERENCES.get(my_conf, []) and t != my_team]
    schedule += random.sample(non_conf, min(len(non_conf), needed))
    
    if rival in ALL_TEAMS:
        if rival in schedule: schedule.remove(rival)
        schedule.append(rival)
    else:
        random.shuffle(schedule)
    return schedule

def engine_play_game(my_rating, opp_rating, staff, schemes, opp_schemes, game_plan, opp_coaches, is_home, is_rival, fac_lvl, my_roster):
    # 1. Roster Talent
    my_off = (my_roster["QB"] * 0.3) + (my_roster["OL"] * 0.25) + ((my_roster["RB"] + my_roster["WR"])/2 * 0.45)
    my_def = sum(my_roster[p] for p in ["DL","LB","DB"]) / 3
    
    talent_gap = (my_rating**2 - opp_rating**2) / 125.0
    
    # 2. Scheme
    scheme_bonus = 0
    if COUNTERS[opp_schemes['Def']] == schemes['Off']: scheme_bonus += 4
    elif COUNTERS[schemes['Off']] == opp_schemes['Def']: scheme_bonus -= 4
    
    # 3. Coaching Tier Logic (1.1x weight)
    my_oc = staff.get('OC', {'off':3})['off']
    my_dc = staff.get('DC', {'def':3})['def']
    opp_oc = opp_coaches.get('OC', 5)
    opp_dc = opp_coaches.get('DC', 5)
    
    def get_tier_bonus(rating):
        if rating >= 8: return 3
        elif rating <= 4: return -3
        return 0
    
    # Net Coaching Impact
    coaching_net = ((get_tier_bonus(my_oc) - get_tier_bonus(opp_dc)) * 1.1) + ((get_tier_bonus(my_dc) - get_tier_bonus(opp_oc)) * 1.1)
    
    # 4. Sim Variables
    home_bonus = 3 if is_home and fac_lvl > 8 else ( -3 if not is_home and random.random() < 0.3 else 0)
    var_mult = 2.0 if is_rival else 1.0
    if game_plan == "Aggressive": var_mult *= 1.5
    
    # 5. Monte Carlo Loop
    sims = []
    for _ in range(100):
        luck = random.gauss(0, 3.0 * var_mult)
        sims.append(talent_gap + scheme_bonus + coaching_net + home_bonus + luck)
    
    margin = sum(sims) / len(sims)
    my_score = int(28 + (margin/1.5)) if margin > 0 else int(24 + (margin/1.5))
    opp_score = int(my_score - margin)
    
    # Visual Stats
    visual_my_off = int(my_off + get_tier_bonus(my_oc))
    visual_my_def = int(my_def + get_tier_bonus(my_dc))
    
    return {
        "result": "W" if margin > 0 else "L", "score": f"{max(0,my_score)}-{max(0,opp_score)}",
        "stats": {
            "qb_duel": [int(my_roster["QB"]), int(opp_rating)], 
            "off_vs_def": [visual_my_off, int(opp_rating + get_tier_bonus(opp_dc))], 
            "def_vs_off": [visual_my_def, int(opp_rating + get_tier_bonus(opp_oc))], 
            "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"],
            "raw_roster": int((my_off + my_def)/2)
        }
    }

def engine_evolve_universe(opponents_db):
    for team, data in opponents_db.items():
        wins = int((data['OVR']/100)*12) + random.randint(-2, 2)
        wins = max(0, min(12, wins))
        
        change = 0
        if wins >= 10: change = 3
        elif wins <= 4: change = -3
        data['Prestige'] = max(20, min(99, data['Prestige'] + change))
        
        if data['Prestige'] > 80 and wins < 6: # Fire
            data['Coaches'] = {"OC": random.randint(7,9), "DC": random.randint(7,9)}
        elif data['Prestige'] < 70 and wins > 9: # Poach
            data['Coaches'] = {"OC": random.randint(3,6), "DC": random.randint(3,6)}
            
        base_ovr = int(data['Prestige'] * 0.9)
        data['OVR'] = base_ovr + random.randint(-3, 3)
    return opponents_db

def engine_generate_portal_players():
    players = []
    # High Tier
    for _ in range(3):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(90, 99), 
                        "cost": random.randint(3000000, 6000000), "trait": random.choice(TRAITS), "year": "Sr"})
    # Mid Tier
    for _ in range(3):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(80, 89), 
                        "cost": random.randint(1000000, 2500000), "trait": random.choice(TRAITS), "year": "Sr"})
    # Bargain Bin
    for _ in range(4):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(70, 78), 
                        "cost": random.randint(150000, 500000), "trait": "None", "year": "Jr"})
    return players

def process_recruiting(budget, allocations, staff, prestige, inflation):
    results = {"roster_updates": {}, "gems": [], "cost": sum(allocations.values()), "booster_bonus": 0}
    if results["cost"] > budget: return None
    
    scout_rate = staff.get('Scout', {'recruit':1})['recruit']
    
    # 1-4 Bad (Penalty), 5-7 Normal, 8-10 Elite (Discount)
    cost_mult = 1.2 
    if scout_rate >= 8: cost_mult = 0.8 
    elif scout_rate >= 5: cost_mult = 1.0 
    
    base_cost = 800000 * inflation * cost_mult
    
    home_region = st.session_state.home_region
    hot_positions = st.session_state.hotspots.get(home_region, []) 
    
    for pos, amount in allocations.items():
        if amount < base_cost * 0.5: change = -random.randint(2, 6)
        else:
            bonus = 1.15 if pos in hot_positions else 1.0
            change = (amount / base_cost) * bonus
            if amount > base_cost * 1.2 and random.random() < 0.15:
                change += 5
                new_star = generate_star_player(pos, 1)
                new_star['name'] += " (GEM)"
                results["gems"].append(new_star)
                results["booster_bonus"] += 250000
        results["roster_updates"][pos] = change
            
    return results

# ==============================================================================
# ZONE 4: STATE MANAGEMENT
# ==============================================================================

def initialize_game_state():
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'SETUP'
        st.session_state.year = 2026
        st.session_state.budget = 0
        st.session_state.prestige = 50
        st.session_state.job_security = 80
        st.session_state.expected_wins = 6
        st.session_state.tenure = 1
        st.session_state.roster = {p: 75 for p in POSITIONS}
        st.session_state.active_transfers = {p: False for p in POSITIONS}
        st.session_state.stars = []
        st.session_state.staff = {}
        st.session_state.facilities = {"Marketing": 1, "Training": 1, "Stadium": 1}
        st.session_state.history = []
        st.session_state.record = {"w":0, "l":0}
        st.session_state.opponents_db = {}
        st.session_state.my_schemes = {"Off": "Pro Style", "Def": "Man Coverage"}
        st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
        st.session_state.season_logs = []
        st.session_state.schedule = []
        st.session_state.season_simulated = False 
        st.session_state.hotspots = {}
        st.session_state.portal_players = []
        st.session_state.candidates = {}
        st.session_state.postseason_data = {}
        st.session_state.revenue_report = None
        st.session_state.inflation = 1.0 
    
    # SAFETY CHECK for Existing Saves (V7.2 CRASH FIX)
    if 'inflation' not in st.session_state: st.session_state.inflation = 1.0
    if 'revenue_report' not in st.session_state: st.session_state.revenue_report = None
    if 'postseason_data' not in st.session_state: st.session_state.postseason_data = {}

def generate_hotspots():
    hotspots = {}
    for reg in REGION_STRENGTH.keys(): hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

initialize_game_state()

# ==============================================================================
# ZONE 5: UI CONTROLLERS
# ==============================================================================

def run_setup():
    st.title("🏆 College Football Mogul V7.2")
    st.markdown("### Dynasty Mode (Jan 2026)")
    c1, c2 = st.columns(2)
    name = c1.text_input("AD Name", "Coach Prime")
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    sorted_teams = sorted(REAL_WORLD_INIT.keys()) + sorted([t for t in ALL_TEAMS if t not in REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)
    
    if team in REAL_WORLD_INIT:
        d = REAL_WORLD_INIT[team]
        tier = d['Tier']
        budget = 25000000 if tier == 1 else (15000000 if tier == 2 else 5000000)
        conf = "SEC" if team in CONFERENCES["SEC"] else ("Big Ten" if team in CONFERENCES["Big Ten"] else "G5")
        rival = d.get('Rival', 'Rival')
    else:
        tier, budget, conf, rival = 3, 5000000, "G5", "Rival"
        for c, t_list in CONFERENCES.items():
            if team in t_list: conf = c
            
    expect = 10 if tier == 1 else (8 if tier == 2 else (6 if tier == 3 else 4))
    st.info(f"**{team}** | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival}")
    st.caption(f"Expectation: {expect}+ Wins")
    
    if st.button("Start Dynasty", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = TEAMS_DB.get(team, {}).get('color', '#333333')
        st.session_state.team_conf = conf
        st.session_state.team_rival = rival
        st.session_state.home_region = "South"
        st.session_state.expected_wins = expect
        st.session_state.school_tier = tier
        st.session_state.budget = int(budget * (0.75 if diff == "Hard" else 1.25 if diff == "Easy" else 1.0))
        st.session_state.roster = engine_generate_roster(tier, REAL_WORLD_INIT.get(team, {}).get('Talent'))
        st.session_state.prestige = REAL_WORLD_INIT.get(team, {}).get('Prestige', 60)
        
        for r in ["HC","OC","DC","Scout"]: st.session_state.staff[r] = engine_generate_coach(r, tier)
        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}
        
        for opp in ALL_TEAMS:
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                st.session_state.opponents_db[opp] = {"Prestige": data['Prestige'], "OVR": data['Talent'], "Off": random.choice(list(SCHEMES["Offense"])), "Def": random.choice(list(SCHEMES["Defense"])), "Coaches": {"OC": random.randint(5,9), "DC": random.randint(5,9)}}
            else:
                pres = 85 if opp in CONFERENCES['SEC'] else 65
                ovr = 82 if opp in CONFERENCES['SEC'] else 70
                st.session_state.opponents_db[opp] = {"Prestige": pres, "OVR": ovr, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC":5,"DC":5}}
        
        st.session_state.hotspots = generate_hotspots()
        st.session_state.schedule = engine_generate_schedule(team, conf, rival)
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < thresh: st.session_state.game_state = "FIRED"; st.rerun()
    
    # Financial Report (V7.1 Fix)
    if st.session_state.revenue_report:
        st.markdown(f"<div class='finance-alert'>💰 FINANCIAL REPORT<br>{st.session_state.revenue_report}</div>", unsafe_allow_html=True)
    
    sec = st.session_state.job_security
    sec_cls = "security-safe" if sec > 75 else ("security-warm" if sec > 40 else "security-hot")
    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Security: <span class='{sec_cls}'>{sec}%</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 5px; color: white;'><h2>{st.session_state.team_name}</h2></div>", unsafe_allow_html=True)
    
    raw_roster_val = int(sum(st.session_state.roster.values()) / 7)
    curr_ovr = int((st.session_state.roster['QB']*0.3) + (st.session_state.roster['OL']*0.25) + ((st.session_state.roster['RB']+st.session_state.roster['WR'])/2 * 0.45) + (st.session_state.facilities['Training']*0.5))
    st.session_state.team_rating = curr_ovr
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("Team OVR", curr_ovr, f"Raw Talent: {raw_roster_val}")
    c3.metric("Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Strategy", "Staff", "Facilities", "Season"])
    
    with tab1:
        c1, c2 = st.columns(2)
        st.session_state.my_schemes["Off"] = c1.selectbox("Offense", SCHEMES["Offense"])
        st.session_state.my_schemes["Def"] = c2.selectbox("Defense", SCHEMES["Defense"])
        st.write("Unit Strength")
        for p, v in st.session_state.roster.items():
            lab = f"{p}: {int(v)}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.progress(min(1.0, v/100), lab)
            
    with tab2:
        st.markdown("### 🧢 Current Staff")
        cols = st.columns(4)
        roles = ["HC", "OC", "DC", "Scout"]
        for i, role in enumerate(roles):
            with cols[i]:
                if role in st.session_state.staff:
                    c = st.session_state.staff[role]
                    rtg = c['off'] if role in ['HC','OC'] else (c['def'] if role=='DC' else c['recruit'])
                    badge_cls = "badge-tier-s" if rtg >=8 else ("badge-tier-a" if rtg >=5 else "badge-tier-f")
                    st.markdown(f"""
                    <div class='staff-card'>
                        <div class='staff-role'>{role}</div>
                        <div class='staff-name'>{c['name']}</div>
                        <div><span class='badge {badge_cls}'>RATING: {rtg}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Fire", key=f"fire_{role}"): 
                        del st.session_state.staff[role]; st.rerun()
                else:
                    st.warning(f"{role} VACANT")
        st.divider()
        st.markdown("### 📋 Job Market")
        vacancies = [r for r in roles if r not in st.session_state.staff]
        if vacancies:
            for role in vacancies:
                if role not in st.session_state.candidates:
                    st.session_state.candidates[role] = [engine_generate_coach(role, random.randint(1,3)) for _ in range(3)]
                
                cols = st.columns(3)
                for i, cand in enumerate(st.session_state.candidates[role]):
                    with cols[i]:
                        vis_rate = f"{cand['off']}" if cand['scouted'] else f"{get_letter_grade(cand['off'])}"
                        vis_trait = cand['trait'] if cand['scouted'] else "???"
                        st.markdown(f"""
                        <div class='staff-card'>
                            <div class='staff-name'>{cand['name']}</div>
                            <div style='font-size:0.8em'>{cand['history']}</div>
                            <div style='margin:5px 0'><span class='badge badge-trait'>OVR: {vis_rate}</span></div>
                            <div style='font-weight:bold'>{helper_format_cash(cand['salary'])}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        b1, b2 = st.columns(2)
                        if b1.button("Hire", key=f"h_{role}_{i}"):
                            if st.session_state.budget >= cand['salary']:
                                st.session_state.budget -= cand['salary']
                                st.session_state.staff[role] = cand
                                del st.session_state.candidates[role]
                                st.rerun()
                        if not cand['scouted'] and b2.button("Scout ($25k)", key=f"sc_{role}_{i}"):
                            if st.session_state.budget >= 25000:
                                st.session_state.budget -= 25000
                                cand['scouted'] = True
                                st.rerun()
                if st.button(f"Promote GA (Free)", key=f"ga_{role}"):
                    st.session_state.staff[role] = generate_ga_coach(role); st.rerun()

    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.metric("Marketing", st.session_state.facilities['Marketing'], delta="Rev: +$2M/yr")
            if st.button("Upgrade ($1M)", key="um"): 
                if st.session_state.budget >= 1000000: st.session_state.budget -= 1000000; st.session_state.facilities['Marketing'] += 1; st.rerun()
        with c2:
            st.metric("Training", st.session_state.facilities['Training'], delta="OVR Boost")
            if st.button("Upgrade ($3M)", key="ut"): 
                if st.session_state.budget >= 3000000: st.session_state.budget -= 3000000; st.session_state.facilities['Training'] += 1; st.rerun()
        with c3:
            st.metric("Stadium", st.session_state.facilities['Stadium'], delta="Prestige")
            if st.button("Upgrade ($10M)", key="us"): 
                if st.session_state.budget >= 10000000: st.session_state.budget -= 10000000; st.session_state.facilities['Stadium'] += 1; st.rerun()

    with tab4:
        if len(st.session_state.staff) < 4: st.error("Fill Staff First!"); return
        
        if not st.session_state.season_simulated:
            if not st.session_state.schedule: st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
            c1, c2 = st.columns(2)
            with c1:
                st.caption("First Half")
                for i in range(6):
                    opp = st.session_state.schedule[i]
                    css = "game-card-rival" if opp == st.session_state.team_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)
            with c2:
                st.caption("Second Half")
                for i in range(6, 12):
                    opp = st.session_state.schedule[i]
                    css = "game-card-rival" if opp == st.session_state.team_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)
            if st.button("▶️ SIMULATE SEASON", type="primary"): run_season()
        else:
            st.write("### Season Results")
            for log in st.session_state.season_logs:
                res = "W" if "W" in log['Score'] else "L"
                css = "game-card-win" if res == "W" else "game-card-loss"
                s = log['Stats']
                st.markdown(f"""
                <div class='game-card {css}'>
                    <div class='card-header'><span class='card-score'>{log['Score']}</span><span>vs {log['Opponent']}</span></div>
                    <div class='stat-grid'>
                        <div class='stat-row'><span class='stat-label'>🔥 QB Duel</span><span>{s['qb_duel'][0]} vs {s['qb_duel'][1]}</span></div>
                        <div class='stat-row'><span class='stat-label'>⚔️ Off vs Def</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div>
                        <div class='stat-row'><span class='stat-label'>🛡️ Def vs Off</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div>
                        <div class='stat-row'><span class='stat-label'>🧠 Staff</span><span>{s['staff'][0]} vs {s['staff'][1]}</span></div>
                        <div class='stat-row'><span class='stat-label'>💪 Raw Talent</span><span>{s['raw_roster']}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            if st.button("Proceed to Postseason"): 
                wins = st.session_state.record['w']
                rank = 130 - (wins * 10)
                if rank < 1: rank = 1
                bowl = get_bowl_name(rank)
                candidates = [t for t in ALL_TEAMS if t != st.session_state.team_name]
                opp = random.choice(candidates)
                st.session_state.postseason_data = {"Bowl": bowl, "Rank": rank, "Opponent": opp, "OppData": st.session_state.opponents_db[opp]}
                st.session_state.game_state = "POSTSEASON"; st.rerun()

def run_season():
    wins = 0; losses = 0; logs = []
    bar = st.progress(0)
    for i, opp in enumerate(st.session_state.schedule):
        opp_data = st.session_state.opponents_db.get(opp)
        is_riv = (opp == st.session_state.team_rival)
        res = engine_play_game(st.session_state.team_rating, opp_data['OVR'], st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data['Off'], "Def": opp_data['Def']}, "Normal", opp_data['Coaches'], i%2==0, is_riv, st.session_state.facilities['Stadium'], st.session_state.roster)
        
        if res['result'] == "W": 
            wins += 1
            st.session_state.job_security = min(100, st.session_state.job_security + (5 if is_riv else 2))
        else:
            losses += 1
            pen = 2 if st.session_state.tenure <= 2 else 5
            st.session_state.job_security = max(0, st.session_state.job_security - pen)
            
        logs.append({"Week": i+1, "Opponent": opp, "Score": f"{res['result']} {res['score']}", "Stats": res['stats']})
        bar.progress((i+1)/12)
        
    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    st.session_state.season_simulated = True
    st.rerun()

def show_postseason():
    st.title("Postseason Hub")
    data = st.session_state.postseason_data
    
    c1, c2 = st.columns(2)
    c1.metric("Final Rank", f"#{data['Rank']}")
    c2.metric("Bowl Invite", data['Bowl'])
    
    st.markdown(f"<div class='bracket-box'><h3>{data['Bowl']}</h3><h1>VS {data['Opponent']}</h1></div>", unsafe_allow_html=True)
    
    c_strat, c_opp = st.columns(2)
    plan = c_strat.selectbox("Game Plan", ["Balanced", "Aggressive", "Conservative"])
    c_opp.markdown(f"<div class='scout-report'>Opponent: {data['Opponent']}<br>OVR: {data['OppData']['OVR']}</div>", unsafe_allow_html=True)
    
    if st.button("PLAY BOWL GAME 🏈"):
        res = engine_play_game(st.session_state.team_rating, data['OppData']['OVR'], st.session_state.staff, st.session_state.my_schemes, {"Off":data['OppData']['Off'], "Def":data['OppData']['Def']}, plan, data['OppData']['Coaches'], False, False, 10, st.session_state.roster)
        
        wins = st.session_state.record['w'] + (1 if res['result']=="W" else 0)
        delta = wins - st.session_state.expected_wins
        
        if res['result'] == "W":
            st.balloons()
            st.success(f"WON {res['score']}")
            st.session_state.career_stats['bowl_w'] += 1
            if data['Bowl'] == "CFP Playoff": 
                st.session_state.career_stats['titles'] += 1
                st.session_state.budget += 50000000
                st.toast("🏆 NATIONAL TITLE BONUS: $50M")
            else:
                st.session_state.budget += 2000000
                st.toast("🎳 BOWL WIN BONUS: $2M")
        else:
            st.error(f"LOST {res['score']}")
            st.session_state.career_stats['bowl_l'] += 1
            
        if delta > 0: 
            bonus = delta * 1000000
            st.session_state.budget += bonus
            st.success(f"💰 Booster Payout: {helper_format_cash(bonus)}")
        elif delta < 0:
            cut = abs(delta) * 500000
            st.session_state.budget -= cut
            st.error(f"📉 Booster Budget Cut: {helper_format_cash(cut)}")
            
        hist = {"Year": st.session_state.year, "Record": f"{wins}-{st.session_state.record['l'] + (1 if res['result']=='L' else 0)}", "Rank": f"#{data['Rank']}", "Bowl": data['Bowl']}
        st.session_state.history.append(hist)
        
        time.sleep(4)
        st.session_state.game_state = "SUMMARY"; st.rerun()

def show_year_summary():
    st.title(f"{st.session_state.year} Summary")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    
    # V7.2: Money Clarity
    st.markdown(f"<div class='nil-alert'>💰 WAR CHEST AVAILABLE FOR NIL: {helper_format_cash(st.session_state.budget)}</div>", unsafe_allow_html=True)
    
    if st.button("Enter Portal"):
        st.session_state.portal_players = engine_generate_portal_players()
        st.session_state.game_state = "PORTAL"; st.rerun()

def show_portal():
    st.title("Transfer Portal")
    st.write(f"Budget: {helper_format_cash(st.session_state.budget)}")
    
    for i, p in enumerate(st.session_state.portal_players):
        c1, c2 = st.columns([3, 1])
        c1.write(f"{p['pos']} {p['name']} ({p['rating']}) - {helper_format_cash(p['cost'])}")
        if c2.button("Sign", key=f"p_{i}"):
            if st.session_state.budget >= p['cost']:
                st.session_state.budget -= p['cost']
                st.session_state.roster[p['pos']] = p['rating']
                st.session_state.active_transfers[p['pos']] = True
                st.session_state.portal_players.pop(i)
                st.rerun()
                
    if st.button("Go to Recruiting"): st.session_state.game_state = "RECRUITING"; st.rerun()

def show_recruiting():
    st.title("High School Recruiting")
    st.write(f"Budget: {helper_format_cash(st.session_state.budget)}")
    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    st.markdown(f"<div class='recruiting-intel'>Pipeline Bonus ({st.session_state.home_region}): {', '.join(hot)}</div>", unsafe_allow_html=True)
    
    allocs = {}
    curr = 0
    for p in POSITIONS:
        allocs[p] = st.number_input(f"{p}", 0, 10000000, 0, step=100000)
        curr += allocs[p]
    
    st.metric("Remaining", helper_format_cash(st.session_state.budget - curr))
    
    if st.button("Finalize Class"):
        res = process_recruiting(st.session_state.budget, allocs, st.session_state.staff, st.session_state.prestige, st.session_state.inflation)
        if res:
            st.session_state.budget -= res['cost']
            
            if res['booster_bonus'] > 0:
                st.session_state.budget += res['booster_bonus']
                st.toast(f"💎 Gem Discovery Bonus: {helper_format_cash(res['booster_bonus'])}")
                
            for p, g in res['roster_updates'].items():
                loss = 12 if st.session_state.active_transfers[p] else random.randint(2, 5)
                st.session_state.active_transfers[p] = False
                st.session_state.roster[p] = max(40, min(99, st.session_state.roster[p] - loss + g))
            
            # Annual Revenue Payout
            rev = engine_calculate_revenue(st.session_state.school_tier, st.session_state.facilities['Marketing'], st.session_state.inflation)
            st.session_state.budget += rev
            st.session_state.revenue_report = f"Season Budget Injection: +{helper_format_cash(rev)}"
            
            st.session_state.opponents_db = engine_evolve_universe(st.session_state.opponents_db)
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.inflation *= 1.05
            st.session_state.season_simulated = False
            st.session_state.schedule = []
            st.session_state.hotspots = generate_hotspots()
            
            time.sleep(3)
            st.session_state.game_state = "DASHBOARD"
            st.rerun()
        else: st.error("Over Budget")

def show_fired():
    st.error("FIRED! Your tenure has ended.")
    if st.button("Restart Career"): st.session_state.clear(); st.rerun()

# --- 7. ROUTER ---
if st.session_state.game_state == 'SETUP': run_setup()
elif st.session_state.game_state == 'FIRED': show_fired()
elif st.session_state.game_state == 'DASHBOARD': show_dashboard()
elif st.session_state.game_state == 'POSTSEASON': show_postseason()
elif st.session_state.game_state == 'SUMMARY': show_year_summary()
elif st.session_state.game_state == 'PORTAL': show_portal()
elif st.session_state.game_state == 'RECRUITING': show_recruiting()
elif st.session_state.game_state == 'RETIREMENT': show_retirement()
