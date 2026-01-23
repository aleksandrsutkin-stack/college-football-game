import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIG & CSS ---
try:
    st.set_page_config(page_title="College Football Mogul V6.7", page_icon="🏈", layout="wide")
except:
    pass

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    
    /* Security Meter */
    .security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    .security-safe { color: #28a745; font-weight: bold; }
    .security-warm { color: #fd7e14; font-weight: bold; }
    .security-hot { color: #dc3545; font-weight: bold; }
    
    /* Game Cards */
    .game-card { padding: 10px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.08); background: white; }
    .game-card-win { border-left: 5px solid #28a745; }
    .game-card-loss { border-left: 5px solid #dc3545; }
    .game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
    .game-card-rival { border: 2px solid #ffc107 !important; background-color: #fffbf0 !important; }
    
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
    .card-score { font-size: 1.1em; font-weight: 800; }
    .card-opp { font-weight: 600; color: #333; }
    
    .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.85em; }
    .stat-row { display: flex; justify-content: space-between; }
    .stat-label { color: #666; font-weight: 500; }
    .stat-val { font-weight: bold; color: #222; }
    
    .home-label { font-size: 0.7em; font-weight: bold; text-transform: uppercase; color: #888; letter-spacing: 1px; }
    .recruiting-intel { background-color: #e0f7fa; border-left: 5px solid #006064; padding: 15px; margin-bottom: 20px; border-radius: 4px; }
    .scout-report { background-color: #212529; color: #00ff00; font-family: monospace; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .bracket-box { background-color: #2c3e50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATABASE ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}

TEAMS_DB = {
    "Georgia": {"color": "#BA0C2F"}, "Alabama": {"color": "#9E1B32"},
    "Ohio State": {"color": "#BB0000"}, "Michigan": {"color": "#00274C"},
    "Texas": {"color": "#BF5700"}, "Oklahoma": {"color": "#841617"},
    "Oregon": {"color": "#154733"}, "Washington": {"color": "#4B2E83"},
    "Florida St": {"color": "#782F40"}, "Miami": {"color": "#005030"},
    "Penn State": {"color": "#041E42"}, "Notre Dame": {"color": "#0C2340"},
    "LSU": {"color": "#461D7C"}, "Ole Miss": {"color": "#CE1126"},
    "Tennessee": {"color": "#FF8200"}, "Auburn": {"color": "#0C2340"},
    "Indiana": {"color": "#990000"}, "Purdue": {"color": "#CEB888"},
    "Colorado": {"color": "#CFB87C"}, "USC": {"color": "#990000"},
    "Boise State": {"color": "#0033A0"}, "San Jose State": {"color": "#0055A2"}
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

SCHEMES = {"Offense": ["Air Raid", "Smashmouth", "Pro Style"], "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]}
COUNTERS = {"Air Raid": "3-3-5 Cloud", "Smashmouth": "4-4 Heavy", "Pro Style": "Man Coverage", "3-3-5 Cloud": "Smashmouth", "4-4 Heavy": "Air Raid", "Man Coverage": "Pro Style"}
TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {"None": "None", "Recruiter": "+10% Recruiting", "Tactician": "+3 Game Boost", "Air Raid": "+2 Scheme", "Smashmouth": "+2 Scheme", "Pro Style": "+2 Scheme"}

BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl", "ReliaQuest Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl", "Sun Bowl", "Pinstripe Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl", "Frisco Bowl", "Myrtle Beach Bowl"]
}

# --- 3. FUNCTIONS ---

def format_cash(amount):
    if amount >= 1000000: return f"${amount/1000000:.1f}M"
    return f"${int(amount/1000)}K"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Arch", "Shedeur", "Quinn"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name():
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach(role, tier):
    base = 8 if tier == 1 else (5 if tier == 2 else 1)
    cost = random.randint(4000000, 8000000) if tier == 1 else random.randint(500000, 3500000)
    trait_pool = list(COACH_TRAITS.keys())
    if role == "OC": trait_pool = ["Air Raid", "Smashmouth", "Pro Style", "Recruiter", "Tactician"]
    c = {
        "name": f"{generate_coach_name()}", "role": role, "off": min(10, base + random.randint(0, 2)), 
        "def": min(10, base + random.randint(0, 2)), "recruit": min(10, base + random.randint(0, 2)),
        "trait": random.choice(trait_pool), "salary": cost
    }
    if c["trait"] == "None": c["salary"] = int(c["salary"] * 0.7)
    return c

def generate_ga_coach(role):
    return {"name": f"GA {generate_name()}", "role": role, "off": random.randint(1, 3), 
            "def": random.randint(1, 3), "recruit": random.randint(1, 2), "trait": "None", "salary": 50000}

def generate_portal_players():
    players = []
    # Expensive Stars
    for _ in range(3):
        pos = random.choice(POSITIONS)
        players.append({"name": f"{generate_name()}", "pos": pos, "rating": random.randint(90, 99), "cost": random.randint(3000000, 6000000), "trait": random.choice(TRAITS), "year": "Sr"})
    # Mid Tier
    for _ in range(3):
        pos = random.choice(POSITIONS)
        players.append({"name": f"{generate_name()}", "pos": pos, "rating": random.randint(80, 89), "cost": random.randint(1000000, 2500000), "trait": random.choice(TRAITS), "year": "Sr"})
    # Bargain Bin (RESTORED)
    for _ in range(3):
        pos = random.choice(POSITIONS)
        players.append({"name": f"{generate_name()}", "pos": pos, "rating": random.randint(70, 79), "cost": random.randint(150000, 500000), "trait": "None", "year": "Jr"})
    return players

def calculate_saban_score(career_stats, prestige):
    return int((career_stats['w'] * 1) + (career_stats['bowl_w'] * 5) + (career_stats['titles'] * 50) + (prestige * 0.5))

def get_bowl_name(rank):
    if rank <= 12: return "CFP Playoff Game"
    elif rank <= 25: return random.choice(BOWL_MAPPING["Elite"])
    elif rank <= 40: return random.choice(BOWL_MAPPING["High"])
    elif rank <= 80: return random.choice(BOWL_MAPPING["Mid"])
    else: return random.choice(BOWL_MAPPING["Low"])

def generate_initial_roster(tier, base_ovr=None):
    base = base_ovr if base_ovr else (90 if tier == 1 else 74)
    roster = {}
    for p in POSITIONS: roster[p] = min(99, max(40, base + random.randint(-4, 4)))
    return roster

def generate_star_player(position, tier):
    base = 92 if tier == 1 else 75
    return {"id": random.randint(10000, 99999), "name": generate_name(), "pos": position, "rating": min(99, 85 + random.randint(0, 10)), "year": "Fr", "trait": random.choice(TRAITS)}

def generate_hotspots():
    hotspots = {}
    for reg in REGION_STRENGTH.keys(): hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

def calculate_ovr(roster, stars, staff, facilities):
    qb, ol = roster["QB"], roster["OL"]
    skill = (roster["RB"] + roster["WR"]) / 2
    off = (qb * 0.30) + (ol * 0.25) + (skill * 0.45)
    defs = sum(roster[p] for p in ["DL","LB","DB"]) / 3
    if "OC" in staff: off += (staff["OC"]["off"] - 5) * 1.5
    if "DC" in staff: defs += (staff["DC"]["def"] - 5) * 1.5
    train_lvl = facilities.get("Training", 1)
    return int((off * 0.5) + (defs * 0.5) + (train_lvl * 0.5))

def generate_schedule(my_team_name, my_conf):
    conf_foes = [t for t in CONFERENCES.get(my_conf, CONFERENCES['G5']) if t != my_team_name]
    if len(conf_foes) >= 8: schedule = random.sample(conf_foes, 8)
    else: schedule = conf_foes
    needed = 12 - len(schedule)
    non_conf = [t for t in ALL_TEAMS if t not in CONFERENCES.get(my_conf, []) and t != my_team_name]
    schedule += random.sample(non_conf, min(len(non_conf), needed))
    
    rival = st.session_state.get('team_rival', 'None')
    if rival in ALL_TEAMS:
        if rival in schedule: schedule.remove(rival)
        schedule.append(rival)
    else:
        random.shuffle(schedule)
    return schedule

# --- 4. SIMULATION ENGINE ---
def play_game(my_rating, opp_rating, staff, stars, my_schemes, opp_schemes, game_plan, opp_coaches, is_home, is_rival, facilities_lvl, my_roster):
    my_qb = my_roster["QB"]
    my_ol = my_roster["OL"]
    my_skill = (my_roster["RB"] + my_roster["WR"]) / 2
    my_off_val = (my_qb * 0.3) + (my_ol * 0.25) + (my_skill * 0.45)
    my_def_val = sum(my_roster[p] for p in ["DL","LB","DB"]) / 3
    
    talent_gap = (my_rating**2 - opp_rating**2) / 125.0
    
    scheme_bonus = 0
    if COUNTERS[opp_schemes['Def']] == my_schemes['Off']: scheme_bonus += 4
    elif COUNTERS[my_schemes['Off']] == opp_schemes['Def']: scheme_bonus -= 4
    
    my_oc = staff.get('OC', {'off':3})['off']
    my_dc = staff.get('DC', {'def':3})['def']
    opp_oc = opp_coaches.get('OC', 5)
    opp_dc = opp_coaches.get('DC', 5)
    coaching_delta = ((my_oc - opp_dc) * 1.2) + ((my_dc - opp_oc) * 1.2)
    
    home_bonus = 3 if is_home and facilities_lvl > 8 else 0
    if not is_home and random.random() < 0.3: home_bonus = -3
    
    plan_bonus = 3 if game_plan == "Aggressive" and my_rating < opp_rating else 0
    var_mult = 2.0 if is_rival else 1.0
    if game_plan == "Aggressive": var_mult *= 1.5
    elif game_plan == "Conservative": var_mult *= 0.7
    
    sim_scores = []
    for _ in range(100):
        luck = random.gauss(0, 3.0 * var_mult)
        margin = talent_gap + scheme_bonus + coaching_delta + plan_bonus + home_bonus + luck
        sim_scores.append(margin)
    avg_margin = sum(sim_scores) / len(sim_scores)
    
    my_score = int(28 + (avg_margin/1.5)) if avg_margin > 0 else int(24 + (avg_margin/1.5))
    opp_score = int(my_score - avg_margin)
    
    display_my_off = int(my_off_val + (my_oc - 5))
    display_my_def = int(my_def_val + (my_dc - 5))
    
    return {
        "result": "W" if avg_margin > 0 else "L", "score": f"{max(0,my_score)}-{max(0,opp_score)}",
        "stats": {
            "qb_duel": [int(my_qb), int(opp_rating + random.randint(-5,5))],
            "off_vs_def": [display_my_off, int(opp_rating)],
            "def_vs_off": [display_my_def, int(opp_rating)],
            "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"]
        }
    }

def process_recruiting(budget, allocations, staff, prestige, inflation):
    results = {"roster_updates": {}, "gems": [], "cost": sum(allocations.values()), "booster_bonus": 0}
    if results["cost"] > budget: return None
    
    scout_rating = staff.get('Scout', {'recruit':1})['recruit']
    base_cost = 800000 * inflation * (1.0 - (scout_rating * 0.02))
    
    for pos, amount in allocations.items():
        if amount < base_cost * 0.5: change = -random.randint(1, 4)
        else:
            bonus = 1.15 if pos in st.session_state.hotspots.get(st.session_state.home_region, []) else 1.0
            change = (amount / base_cost) * bonus
            if amount > base_cost * 1.2 and random.random() < 0.15:
                change += 5
                new_star = generate_star_player(pos, 1)
                new_star['name'] += " (GEM)"
                results["gems"].append(new_star)
                results["booster_bonus"] += 250000
        results["roster_updates"][pos] = change
    
    # RESTORED: LIVING WORLD AI UPDATE
    for opp_name, data in st.session_state.opponents_db.items():
        # 1. Sim record based on OVR
        wins = int((data['OVR']/100)*12) + random.randint(-2, 2)
        
        # 2. Update Prestige
        pres_change = 0
        if wins >= 10: pres_change = 3
        elif wins <= 4: pres_change = -3
        data['Prestige'] = max(20, min(99, data['Prestige'] + pres_change))
        
        # 3. Update OVR
        data['OVR'] = int((data['Prestige'] * 0.9) + random.randint(-3, 3))
        
        # 4. Coach Carousel
        if data['Prestige'] > 80 and wins < 6: # Fired
            data['Coaches'] = {"OC": random.randint(6,9), "DC": random.randint(6,9)}
        elif data['Prestige'] < 70 and wins > 9: # Poached
            data['Coaches'] = {"OC": random.randint(3,6), "DC": random.randint(3,6)}
            
    return results

# --- 5. INITIALIZATION ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP'
    st.session_state.year = 2026
    st.session_state.budget = 0
    st.session_state.prestige = 50
    st.session_state.job_security = 80
    st.session_state.expected_wins = 6
    st.session_state.school_tier = 3
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
    st.session_state.momentum = 0
    st.session_state.rank = 0
    st.session_state.current_headline = "Season Begins"
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0, "cfp_w": 0, "cfp_g": 0}
    st.session_state.team_rating = 0
    st.session_state.season_logs = []
    st.session_state.undefeated_streak = 0
    st.session_state.inflation = 1.0
    st.session_state.playoff_round = 0
    st.session_state.last_season_summary = {}
    st.session_state.match_history = []
    st.session_state.schedule = []
    st.session_state.season_simulated = False 
    st.session_state.hotspots = generate_hotspots()
    st.session_state.portal_players = []
    st.session_state.candidates = {}

# --- 6. SCREENS ---
def run_setup():
    st.title("🏆 College Football Mogul V6.7")
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
    st.info(f"**{team}** | Tier: {tier} | Budget: {format_cash(budget)} | Rival: {rival}")
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
        st.session_state.roster = generate_initial_roster(tier, REAL_WORLD_INIT.get(team, {}).get('Talent'))
        st.session_state.prestige = REAL_WORLD_INIT.get(team, {}).get('Prestige', 60)
        st.session_state.stars = [generate_star_player("QB", tier)]
        for r in ["HC","OC","DC","Scout"]: st.session_state.staff[r] = generate_coach(r, tier)
        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}
        
        # Init AI
        for opp in ALL_TEAMS:
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                st.session_state.opponents_db[opp] = {"Prestige": data['Prestige'], "OVR": data['Talent'], "Off": random.choice(SCHEMES["Offense"]), "Def": random.choice(SCHEMES["Defense"]), "Coaches": {"OC": random.randint(5,9), "DC": random.randint(5,9)}}
            else:
                pres = 80 if opp in CONFERENCES['SEC'] else 60
                st.session_state.opponents_db[opp] = {"Prestige": pres, "OVR": int(pres*0.9), "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC":5,"DC":5}}
        
        st.session_state.schedule = generate_schedule(team, conf)
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    fire_thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < fire_thresh: st.session_state.game_state = "FIRED"; st.rerun()
    
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    sec = st.session_state.job_security
    sec_cls = "security-safe" if sec > 75 else ("security-warm" if sec > 40 else "security-hot")
    
    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Job Security: <span class='{sec_cls}'>{sec}%</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 5px; color: white;'><h2>{st.session_state.team_name}</h2></div>", unsafe_allow_html=True)
    
    ovr = calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff, st.session_state.facilities)
    st.session_state.team_rating = ovr
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget", format_cash(st.session_state.budget))
    c2.metric("Team OVR", ovr)
    c3.metric("Legacy", saban)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Strategy", "Staff", "Facilities", "Season"])
    
    with tab1:
        c_off, c_def = st.columns(2)
        st.session_state.my_schemes["Off"] = c_off.selectbox("Offense", SCHEMES["Offense"])
        st.session_state.my_schemes["Def"] = c_def.selectbox("Defense", SCHEMES["Defense"])
        st.write("Roster Strength")
        for p, v in st.session_state.roster.items():
            lab = f"{p}: {int(v)}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.progress(min(1.0, v/100), lab)
            
    with tab2:
        for role in ["HC","OC","DC","Scout"]:
            if role in st.session_state.staff:
                c = st.session_state.staff[role]
                st.success(f"{role}: {c['name']} (Off:{c['off']} Def:{c['def']})")
                if st.button(f"Fire {role}", key=f"f_{role}"): del st.session_state.staff[role]; st.rerun()
            else:
                st.warning(f"{role} Vacant")
                c1, c2 = st.columns(2)
                if c1.button("Search ($500k)", key=f"s_{role}"): 
                    if st.session_state.budget >= 500000:
                        st.session_state.budget -= 500000
                        st.session_state.candidates[role] = [generate_coach(role, random.randint(1,3)) for _ in range(3)]
                        st.rerun()
                if c2.button("Promote GA (Free)", key=f"ga_{role}"):
                    st.session_state.staff[role] = generate_ga_coach(role); st.rerun()
                if role in st.session_state.candidates:
                    for i, cand in enumerate(st.session_state.candidates[role]):
                        if st.button(f"Hire {cand['name']} ({format_cash(cand['salary'])})", key=f"h_{i}"):
                            if st.session_state.budget >= cand['salary']:
                                st.session_state.budget -= cand['salary']
                                st.session_state.staff[role] = cand
                                del st.session_state.candidates[role]
                                st.rerun()

    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.metric("Marketing", st.session_state.facilities['Marketing'])
            st.caption("Inc. Revenue")
            if st.button("Upgr ($1M)", key="up_mkt"): 
                if st.session_state.budget >= 1000000: st.session_state.budget -= 1000000; st.session_state.facilities['Marketing'] += 1; st.rerun()
        with c2: 
            st.metric("Training", st.session_state.facilities['Training'])
            st.caption("Inc. OVR")
            if st.button("Upgr ($3M)", key="up_trn"): 
                if st.session_state.budget >= 3000000: st.session_state.budget -= 3000000; st.session_state.facilities['Training'] += 1; st.rerun()
        with c3: 
            st.metric("Stadium", st.session_state.facilities['Stadium'])
            st.caption("Inc. Prestige")
            if st.button("Upgr ($10M)", key="up_std"): 
                if st.session_state.budget >= 10000000: st.session_state.budget -= 10000000; st.session_state.facilities['Stadium'] += 1; st.rerun()

    with tab4:
        if len(st.session_state.staff) < 4: st.error("Fill Staff First!"); return
        
        if not st.session_state.season_simulated:
            if not st.session_state.schedule: st.session_state.schedule = generate_schedule(st.session_state.team_name, st.session_state.team_conf)
            c1, c2 = st.columns(2)
            with c1:
                st.caption("First Half")
                for i in range(6):
                    opp = st.session_state.schedule[i]
                    is_riv = (opp == st.session_state.team_rival)
                    css = "game-card-rival" if is_riv else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)
            with c2:
                st.caption("Second Half")
                for i in range(6, 12):
                    opp = st.session_state.schedule[i]
                    is_riv = (opp == st.session_state.team_rival)
                    css = "game-card-rival" if is_riv else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)
            if st.button("▶️ SIMULATE SEASON", type="primary"): run_season()
        else:
            st.write("### Season Results")
            logs = st.session_state.season_logs
            for log in logs:
                res = "W" if "W" in log['Score'] else "L"
                css = "game-card-win" if res == "W" else "game-card-loss"
                stats = log['Stats']
                st.markdown(f"""
                <div class='game-card {css}'>
                    <div class='card-header'><span class='card-score'>{log['Score']}</span> <span>vs {log['Opponent']}</span></div>
                    <div class='stat-grid'>
                        <div class='stat-row'><span>🔥 QB Duel</span><span>{stats['qb_duel'][0]} vs {stats['qb_duel'][1]}</span></div>
                        <div class='stat-row'><span>⚔️ Off vs Def</span><span>{stats['off_vs_def'][0]} vs {stats['off_vs_def'][1]}</span></div>
                        <div class='stat-row'><span>🛡️ Def vs Off</span><span>{stats['def_vs_off'][0]} vs {stats['def_vs_off'][1]}</span></div>
                        <div class='stat-row'><span>🧠 Staff</span><span>{stats['staff'][0]} vs {stats['staff'][1]}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("Proceed to Postseason"): st.session_state.game_state = "POSTSEASON"; st.rerun()

def run_season():
    wins = 0; losses = 0; logs = []
    bar = st.progress(0)
    for i, opp in enumerate(st.session_state.schedule):
        opp_data = st.session_state.opponents_db.get(opp)
        is_rival = (opp == st.session_state.team_rival)
        res = play_game(st.session_state.team_rating, opp_data['OVR'], st.session_state.staff, st.session_state.stars, st.session_state.my_schemes, {"Off": opp_data['Off'], "Def": opp_data['Def']}, "Normal", opp_data['Coaches'], i%2==0, is_rival, st.session_state.facilities['Stadium'], st.session_state.roster)
        if res['result'] == "W": 
            wins += 1
            st.session_state.job_security = min(100, st.session_state.job_security + (5 if is_rival else 2))
        else:
            losses += 1
            st.session_state.job_security = max(0, st.session_state.job_security - (2 if st.session_state.tenure <= 2 else 5))
        logs.append({"Week": i+1, "Opponent": opp, "Score": f"{res['result']} {res['score']}", "Stats": res['stats']})
        bar.progress((i+1)/12)
    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    st.session_state.season_simulated = True
    st.rerun()

def show_postseason():
    st.title("Postseason Hub")
    wins = st.session_state.record['w']
    rank = 130 - (wins * 10) 
    if rank < 1: rank = 1
    
    bowl_name = "None"
    if rank <= 12: bowl_name = "CFP Playoff"
    elif wins >= 6: bowl_name = get_bowl_name(rank)
    
    st.metric("Final Rank", f"#{rank}")
    st.metric("Bowl Invite", bowl_name)
    
    if st.button("Advance to Offseason"):
        delta = wins - st.session_state.expected_wins
        if delta > 0: 
            st.toast(f"Bonus: ${delta}M")
            st.session_state.budget += delta * 1000000
        elif delta < 0:
            st.toast("Budget Cut")
            st.session_state.budget -= abs(delta) * 500000
            
        history_entry = {"Year": st.session_state.year, "Record": f"{wins}-{st.session_state.record['l']}", "Rank": f"#{rank}", "Bowl": bowl_name}
        st.session_state.history.append(history_entry)
        st.session_state.game_state = "SUMMARY"; st.rerun()

def show_year_summary():
    st.title(f"{st.session_state.year} Summary")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
    if st.button("Enter Portal"): 
        st.session_state.portal_players = generate_portal_players()
        st.session_state.game_state = "PORTAL"; st.rerun()

def show_portal():
    st.title("Transfer Portal")
    st.write(f"Budget: {format_cash(st.session_state.budget)}")
    if not st.session_state.portal_players: st.write("No players.")
    for i, p in enumerate(st.session_state.portal_players):
        c1, c2 = st.columns([3,1])
        c1.write(f"{p['pos']} {p['name']} ({p['rating']}) - {format_cash(p['cost'])}")
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
    st.write(f"Budget: {format_cash(st.session_state.budget)}")
    
    # RESTORED INFO
    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    st.info(f"Hotspots ({st.session_state.home_region}): {', '.join(hot)}")
    
    allocs = {}
    current_spend = 0
    for p in POSITIONS:
        allocs[p] = st.number_input(f"{p}", 0, 10000000, 0, step=100000)
        current_spend += allocs[p]
    
    st.metric("Remaining", format_cash(st.session_state.budget - current_spend))
    
    if st.button("Finalize Class"):
        res = process_recruiting(st.session_state.budget, allocs, st.session_state.staff, st.session_state.prestige, st.session_state.inflation)
        if res:
            st.session_state.budget -= res['cost']
            for p, g in res['roster_updates'].items():
                loss = 12 if st.session_state.active_transfers[p] else 3
                st.session_state.active_transfers[p] = False
                st.session_state.roster[p] = max(40, min(99, st.session_state.roster[p] - loss + g))
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.season_simulated = False
            st.session_state.schedule = generate_schedule(st.session_state.team_name, st.session_state.team_conf)
            st.session_state.hotspots = generate_hotspots()
            st.session_state.game_state = "DASHBOARD"
            st.rerun()
        else: st.error("Over Budget")

def show_fired():
    st.error("YOU HAVE BEEN FIRED")
    if st.button("Restart"): 
        st.session_state.clear()
        st.rerun()

# --- 7. ROUTER ---
if st.session_state.game_state == 'SETUP': run_setup()
elif st.session_state.game_state == 'FIRED': show_fired()
elif st.session_state.game_state == 'DASHBOARD': show_dashboard()
elif st.session_state.game_state == 'POSTSEASON': show_postseason()
elif st.session_state.game_state == 'SUMMARY': show_year_summary()
elif st.session_state.game_state == 'PORTAL': show_portal()
elif st.session_state.game_state == 'RECRUITING': show_recruiting()
elif st.session_state.game_state == 'RETIREMENT': show_retirement()
