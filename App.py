import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIG ---
try:
    st.set_page_config(page_title="College Football Mogul V6.3", page_icon="🏈", layout="wide")
except:
    pass

# --- 2. CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    .news-ticker { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px; border: 1px solid #ffeeba; }
    
    .security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    .security-safe { color: #28a745; font-weight: bold; }
    .security-warm { color: #fd7e14; font-weight: bold; }
    .security-hot { color: #dc3545; font-weight: bold; }
    
    .game-card { padding: 10px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.08); background: white; }
    .game-card-win { border-left: 5px solid #28a745; }
    .game-card-loss { border-left: 5px solid #dc3545; }
    .game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
    
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
    .card-score { font-size: 1.1em; font-weight: 800; }
    .card-opp { font-weight: 600; color: #333; }
    
    .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.85em; }
    .stat-row { display: flex; justify-content: space-between; }
    .stat-label { color: #666; font-weight: 500; }
    .stat-val { font-weight: bold; color: #222; }
    
    .home-label { font-size: 0.7em; font-weight: bold; text-transform: uppercase; color: #888; letter-spacing: 1px; }
    
    .scout-report { background-color: #212529; color: #00ff00; font-family: monospace; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .bracket-box { background-color: #2c3e50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
    
    .recruiting-intel { background-color: #e0f7fa; border-left: 5px solid #006064; padding: 15px; margin-bottom: 20px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA & REAL WORLD MAPPINGS ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]

REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}

# Real World 2026 Starting State (Rankings + Talent Composite)
REAL_WORLD_INIT = {
    "Indiana": {"Prestige": 99, "Talent": 86, "Tier": 1},
    "Ohio State": {"Prestige": 95, "Talent": 94, "Tier": 1},
    "Miami": {"Prestige": 94, "Talent": 89, "Tier": 1},
    "Oregon": {"Prestige": 93, "Talent": 92, "Tier": 1},
    "Georgia": {"Prestige": 92, "Talent": 96, "Tier": 1},
    "Ole Miss": {"Prestige": 91, "Talent": 88, "Tier": 1},
    "Texas Tech": {"Prestige": 90, "Talent": 84, "Tier": 2},
    "Texas A&M": {"Prestige": 89, "Talent": 91, "Tier": 2},
    "Alabama": {"Prestige": 85, "Talent": 95, "Tier": 1},
    "Notre Dame": {"Prestige": 87, "Talent": 90, "Tier": 1},
    "BYU": {"Prestige": 86, "Talent": 82, "Tier": 2},
    "Texas": {"Prestige": 84, "Talent": 97, "Tier": 1},
    "Oklahoma": {"Prestige": 83, "Talent": 90, "Tier": 2},
    "Utah": {"Prestige": 82, "Talent": 85, "Tier": 2},
    "Vanderbilt": {"Prestige": 80, "Talent": 78, "Tier": 3},
    "USC": {"Prestige": 79, "Talent": 89, "Tier": 2},
    "Michigan": {"Prestige": 78, "Talent": 91, "Tier": 2},
    "Penn State": {"Prestige": 77, "Talent": 88, "Tier": 2},
    "LSU": {"Prestige": 76, "Talent": 92, "Tier": 2},
    "Florida St": {"Prestige": 70, "Talent": 87, "Tier": 3},
    "Colorado": {"Prestige": 75, "Talent": 85, "Tier": 2},
    "Boise State": {"Prestige": 72, "Talent": 79, "Tier": 3},
    "Tulane": {"Prestige": 74, "Talent": 77, "Tier": 3}
}

CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Texas A&M", "Ole Miss", "Vanderbilt", "Florida"],
    "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington", "Indiana", "Nebraska"],
    "ACC": ["Florida St", "Clemson", "Miami", "Stanford", "Cal", "Louisville", "UNC", "Virginia Tech", "SMU"],
    "Big 12": ["Utah", "TCU", "Baylor", "Texas Tech", "Arizona State", "Colorado", "Kansas State", "Oklahoma St", "BYU", "Arizona"],
    "G5": ["Boise State", "San Jose State", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St", "Fresno St", "Tulane", "Memphis", "Navy", "Army"]
}
ALL_TEAMS = [t for c in CONFERENCES.values() for t in c]

SCHEMES = {
    "Offense": ["Air Raid", "Smashmouth", "Pro Style"],
    "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]
}
COUNTERS = {
    "Air Raid": "3-3-5 Cloud", "Smashmouth": "4-4 Heavy", "Pro Style": "Man Coverage",
    "3-3-5 Cloud": "Smashmouth", "4-4 Heavy": "Air Raid", "Man Coverage": "Pro Style"
}

SCHEME_DESC = {
    "Air Raid": "Pass Heavy. Needs Air Raid OC.",
    "Smashmouth": "Run Heavy. Needs Smashmouth OC.",
    "Pro Style": "Balanced. Needs Pro Style OC.",
    "3-3-5 Cloud": "Anti-Pass.",
    "4-4 Heavy": "Anti-Run.",
    "Man Coverage": "Balanced."
}

TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {
    "None": "None",
    "Recruiter": "+10% Recruiting", 
    "Tactician": "+3 Game Boost", 
    "Air Raid": "+2 Scheme Fit (Air Raid)",
    "Smashmouth": "+2 Scheme Fit (Smashmouth)",
    "Pro Style": "+2 Scheme Fit (Pro Style)"
}

BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl", "ReliaQuest Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl", "Sun Bowl", "Pinstripe Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl", "Frisco Bowl", "Myrtle Beach Bowl"]
}

# --- 4. LOGIC FUNCTIONS ---

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
        "name": f"{generate_coach_name()}",
        "role": role,
        "off": min(10, base + random.randint(0, 2)),
        "def": min(10, base + random.randint(0, 2)),
        "recruit": min(10, base + random.randint(0, 2)),
        "trait": random.choice(trait_pool),
        "salary": cost
    }
    if c["trait"] == "None": c["salary"] = int(c["salary"] * 0.7)
    return c

# NEW: GA Generator for Low Budget
def generate_ga_coach(role):
    return {
        "name": f"GA {generate_name()}",
        "role": role,
        "off": random.randint(1, 3),
        "def": random.randint(1, 3),
        "recruit": random.randint(1, 2),
        "trait": "None",
        "salary": 50000
    }

def generate_portal_players():
    players = []
    for _ in range(2):
        pos = random.choice(POSITIONS)
        players.append({"name": f"{generate_name()}", "pos": pos, "rating": random.randint(90, 99), "cost": random.randint(4000000, 8000000), "trait": random.choice(TRAITS), "year": "Sr", "desc": "Day 1 Starter (1 Yr)"})
    for _ in range(2):
        pos = random.choice(POSITIONS)
        players.append({"name": f"{generate_name()}", "pos": pos, "rating": random.randint(80, 89), "cost": random.randint(1000000, 3000000), "trait": random.choice(TRAITS), "year": "Sr", "desc": "Good Depth (1 Yr)"})
    for _ in range(3):
        pos = random.choice(POSITIONS)
        players.append({"name": f"{generate_name()}", "pos": pos, "rating": random.randint(70, 79), "cost": random.randint(250000, 800000), "trait": "None", "year": "Jr", "desc": "Immediate Help (2 Yrs)"})
    return players

def calculate_saban_score(career_stats, prestige):
    wins = career_stats['w'] * 1
    bowls = career_stats['bowl_w'] * 5
    titles = career_stats['titles'] * 50
    prest = prestige * 0.5
    return int(wins + bowls + titles + prest)

def get_bowl_name(rank):
    if rank <= 16: return "CFP Playoff Game"
    elif rank <= 20: return random.choice(BOWL_MAPPING["Elite"])
    elif rank <= 30: return random.choice(BOWL_MAPPING["High"])
    elif rank <= 50: return random.choice(BOWL_MAPPING["Mid"])
    else: return random.choice(BOWL_MAPPING["Low"])

def generate_initial_roster(tier, base_ovr=None):
    if base_ovr:
        base = base_ovr
    else:
        base = 90 if tier == 1 else (82 if tier == 2 else 74)
        
    roster = {}
    for p in POSITIONS: roster[p] = min(99, max(40, base + random.randint(-4, 4)))
    return roster

def generate_star_player(position, tier):
    base = 92 if tier == 1 else 75
    star = {"id": random.randint(10000, 99999), "name": generate_name(), "pos": position, "rating": min(99, base + random.randint(2, 6)), "year": "Fr", "trait": random.choice(TRAITS)}
    return star

def generate_hotspots():
    hotspots = {}
    for reg in ["South", "Midwest", "West", "North"]:
        hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

def calculate_ovr(roster, stars, staff, facilities):
    qb = roster["QB"]
    ol = roster["OL"]
    skill = (roster["RB"] + roster["WR"]) / 2
    off = (qb * 0.30) + (ol * 0.25) + (skill * 0.45)
    
    defs = sum(roster[p] for p in ["DL","LB","DB"]) / 3
    
    if "OC" in staff: off += (staff["OC"]["off"] - 5) * 1.5
    if "DC" in staff: defs += (staff["DC"]["def"] - 5) * 1.5
    if "HC" in staff: 
        off += (staff["HC"]["off"]-5)*0.5
        defs += (staff["HC"]["def"]-5)*0.5
    
    train_lvl = facilities.get("Training", 1)
    fac_bonus = (train_lvl - 1) * 0.5 
    star_boost = sum(2 for s in stars if s['trait'] == "🧠 General")
    return int((off * 0.5) + (defs * 0.5) + star_boost + fac_bonus)

def generate_schedule(my_team_name, my_conf):
    conf_foes = [t for t in CONFERENCES[my_conf] if t != my_team_name]
    if len(conf_foes) >= 8: schedule = random.sample(conf_foes, 8)
    else: schedule = conf_foes
    needed = 12 - len(schedule)
    non_conf_pool = [t for t in ALL_TEAMS if t not in CONFERENCES[my_conf] and t != my_team_name]
    schedule += random.sample(non_conf_pool, needed)
    random.shuffle(schedule)
    return schedule

# --- 4. SIMULATION ENGINE ---

def play_game(my_rating, opp_rating, staff, stars, my_schemes, opp_schemes, game_plan="Normal", opp_coaches={}, is_home=False, is_rival=False, facilities_lvl=1, my_roster={}):
    
    # Visual Stats
    qb_rtg = my_roster["QB"]
    opp_qb_rtg = int(opp_rating + random.randint(-5, 5)) 
    
    # Weighted Offense Logic
    my_qb = my_roster["QB"]
    my_ol = my_roster["OL"]
    my_skill = (my_roster["RB"] + my_roster["WR"]) / 2
    my_off_talent = (my_qb * 0.30) + (my_ol * 0.25) + (my_skill * 0.45)
    my_def_talent = sum(my_roster[p] for p in ["DL","LB","DB"]) / 3
    
    opp_off_talent = opp_rating
    opp_def_talent = opp_rating
    
    # 1. Talent Gap (Blue Chip Curve)
    talent_gap = (my_rating**2 - opp_rating**2) / 125.0
    
    # 2. Scheme
    scheme_bonus = 0
    if COUNTERS[opp_schemes['Def']] == my_schemes['Off']: scheme_bonus += 4 
    elif COUNTERS[my_schemes['Off']] == opp_schemes['Def']: scheme_bonus -= 4 
    
    # 3. Staff
    my_oc = staff['OC']['off'] if 'OC' in staff else 3
    my_dc = staff['DC']['def'] if 'DC' in staff else 3
    opp_oc = opp_coaches.get('OC', 5)
    opp_dc = opp_coaches.get('DC', 5)
    
    off_adv = (my_oc - opp_dc) * 1.2
    def_adv = (my_dc - opp_oc) * 1.2
    coaching_delta = off_adv + def_adv
    
    # 4. Synergy
    synergy = 0
    if 'OC' in staff and staff['OC']['trait'] == my_schemes['Off']: synergy += 2
    
    # 5. Game Plan
    plan_bonus = 0
    variance_mult = 1.0
    if game_plan == "Aggressive":
        variance_mult = 1.5; 
        if my_rating < opp_rating: plan_bonus = 3 
    elif game_plan == "Conservative":
        variance_mult = 0.7 
        if my_rating > opp_rating: plan_bonus = 3 
        
    # 6. Home Field
    home_bonus = 0
    if is_home and facilities_lvl > 8: home_bonus = 3
    elif not is_home: 
        if random.random() < 0.30: home_bonus = -3
    
    if is_rival: variance_mult *= 2.0

    # 7. Monte Carlo
    sim_scores = []
    for _ in range(100):
        luck = random.gauss(0, 3.0 * variance_mult) 
        margin = talent_gap + scheme_bonus + coaching_delta + synergy + plan_bonus + home_bonus + luck
        sim_scores.append(margin)
    
    avg_margin = sum(sim_scores) / len(sim_scores)
    
    my_score = int(28 + (avg_margin/1.5)) if avg_margin > 0 else int(24 + (avg_margin/1.5))
    opp_score = int(my_score - avg_margin)
    
    display_my_off = int(my_off_talent + (my_oc - 5))
    display_my_def = int(my_def_talent + (my_dc - 5))
    display_opp_off = int(opp_off_talent + (opp_oc - 5))
    display_opp_def = int(opp_def_talent + (opp_dc - 5))
    
    return {
        "result": "W" if avg_margin > 0 else "L", 
        "score": f"{max(0,my_score)}-{max(0,opp_score)}",
        "stats": {
            "qb_duel": [qb_rtg, opp_qb_rtg],
            "off_vs_def": [display_my_off, display_opp_def],
            "def_vs_off": [display_my_def, display_opp_off],
            "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"]
        }
    }

def process_recruiting(budget, allocations, staff, prestige, inflation):
    results = {"roster_updates": {}, "gems": [], "cost": sum(allocations.values()), "booster_bonus": 0}
    if results["cost"] > budget: return None
    
    staff_rec = 0
    scout_rating = staff['Scout']['recruit'] if 'Scout' in staff else 1
    scout_discount = 1.0 - (scout_rating * 0.02)
    base_cost = 800000 * inflation * scout_discount
    
    home_region = st.session_state.home_region
    base_region_mult = REGION_STRENGTH.get(home_region, 1.02)
    hot_positions = st.session_state.hotspots.get(home_region, []) 
    
    for pos, amount in allocations.items():
        if amount < (base_cost * 0.5):
            rating_change = -random.randint(1, 4) 
        else:
            pos_bonus = 1.15 if pos in hot_positions else 1.0
            buying_power = amount / base_cost
            rating_change = buying_power * base_region_mult * pos_bonus
            
            if amount > (base_cost * 1.2) and random.random() < 0.15:
                rating_change += 5 
                new_star = generate_star_player(pos, 1)
                new_star['year'] = "Fr"
                new_star['name'] = f"{new_star['name']} (GEM)"
                results["gems"].append(new_star)
                results["booster_bonus"] += random.randint(2, 5) * 100000
        results["roster_updates"][pos] = rating_change
            
    # AI Dynamic Evolution (Year to Year)
    for opp_name in st.session_state.opponents_db:
        curr = st.session_state.opponents_db[opp_name]['Prestige']
        flux = random.randint(-2, 2)
        st.session_state.opponents_db[opp_name]['Prestige'] = max(40, min(99, curr + flux))
        
        # Re-calc OVR from new Prestige
        new_pres = st.session_state.opponents_db[opp_name]['Prestige']
        st.session_state.opponents_db[opp_name]['OVR'] = int((new_pres * 0.90) + random.randint(-3, 3))
            
    return results

# --- 5. INITIALIZATION & STATE ---
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
    st.session_state.candidates = {}
    st.session_state.portal_players = []
    st.session_state.history = []
    st.session_state.record = {"w":0, "l":0}
    st.session_state.opponents_db = {}
    st.session_state.my_schemes = {"Off": "Pro Style", "Def": "Man Coverage"}
    st.session_state.momentum = 0
    st.session_state.rank = 0
    st.session_state.team_name = "Team"
    st.session_state.team_color = "#333"
    st.session_state.team_conf = "SEC"
    st.session_state.team_rival = "None"
    st.session_state.home_region = "South"
    st.session_state.current_headline = "Season Begins"
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0, "cfp_w": 0, "cfp_g": 0}
    st.session_state.team_rating = 0
    st.session_state.season_logs = []
    st.session_state.postseason_result = {}
    st.session_state.undefeated_streak = 0
    st.session_state.inflation = 1.0
    st.session_state.playoff_round = 0
    st.session_state.last_season_summary = {}
    st.session_state.match_history = []
    st.session_state.schedule = []
    st.session_state.season_simulated = False 
    st.session_state.hotspots = {}

if 'active_transfers' not in st.session_state: st.session_state.active_transfers = {p: False for p in POSITIONS}
if 'job_security' not in st.session_state: st.session_state.job_security = 80
if 'expected_wins' not in st.session_state: st.session_state.expected_wins = 6
if 'inflation' not in st.session_state: st.session_state.inflation = 1.0
if 'hotspots' not in st.session_state: st.session_state.hotspots = generate_hotspots()

# --- 6. SCREENS ---

def run_setup():
    st.title("🏆 College Football Mogul V6.3")
    st.markdown("### Dynasty Mode (Jan 2026 Start)")
    col1, col2 = st.columns(2)
    with col1: name = st.text_input("AD Name", "Coach Prime")
    with col2: diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    sorted_teams = sorted(REAL_WORLD_INIT.keys()) + sorted([t for t in ALL_TEAMS if t not in REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)
    
    if team in REAL_WORLD_INIT:
        d = REAL_WORLD_INIT[team]
        tier = d['Tier']
        budget = 25000000 if tier == 1 else (15000000 if tier == 2 else 5000000)
        conf = "SEC" if team in CONFERENCES["SEC"] else ("Big Ten" if team in CONFERENCES["Big Ten"] else "G5")
    else:
        tier = 3
        budget = 5000000
        conf = "G5"
    
    st.info(f"**{team}** | Tier: {tier} | Budget: {format_cash(budget)}")
    
    expect = 6
    if tier == 1: expect = 10
    elif tier == 2: expect = 8
    elif tier == 3: expect = 6
    else: expect = 4
    st.caption(f"Booster Expectation: {expect}+ Wins")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = "#333333"
        if team in TEAMS_DB: st.session_state.team_color = TEAMS_DB[team]['color']
        
        st.session_state.team_conf = conf
        st.session_state.team_rival = "Rival"
        st.session_state.home_region = "South"
        st.session_state.expected_wins = expect
        st.session_state.school_tier = tier
        
        mult = 1.0
        if diff == "Hard": mult = 0.75
        elif diff == "Easy": mult = 1.25
            
        st.session_state.budget = int(budget * mult)
        st.session_state.job_security = 80
        st.session_state.tenure = 1
        st.session_state.active_transfers = {p: False for p in POSITIONS}
        
        start_ovr = None
        if team in REAL_WORLD_INIT:
            start_ovr = REAL_WORLD_INIT[team]['Talent']
            st.session_state.prestige = REAL_WORLD_INIT[team]['Prestige']
        else:
            st.session_state.prestige = 60
            
        st.session_state.roster = generate_initial_roster(tier, start_ovr)
        st.session_state.stars = [generate_star_player("QB", tier)]
        if tier < 4: st.session_state.stars.append(generate_star_player("LB", tier))
        
        for r in ["HC","OC","DC","Scout"]: st.session_state.staff[r] = generate_coach(r, tier)
        
        fac_val = 10 if tier == 1 else (7 if tier == 2 else 3)
        st.session_state.facilities = {"Marketing": fac_val, "Training": fac_val, "Stadium": fac_val}
        
        for opp in ALL_TEAMS:
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                pres = data['Prestige']
                ovr = data['Talent']
            else:
                pres = 60
                if opp in CONFERENCES["SEC"] or opp in CONFERENCES["Big Ten"]: pres = 80
                elif opp in CONFERENCES["ACC"] or opp in CONFERENCES["Big 12"]: pres = 72
                pres += random.randint(-5, 5)
                ovr = int((pres * 0.9) + random.randint(-3, 3))
            
            oc_rtg = int(pres / 10) + random.randint(-1, 1)
            dc_rtg = int(pres / 10) + random.randint(-1, 1)
            
            st.session_state.opponents_db[opp] = {
                "Prestige": pres,
                "OVR": ovr,
                "Off": random.choice(SCHEMES["Offense"]),
                "Def": random.choice(SCHEMES["Defense"]),
                "Coaches": {"OC": min(10, max(1, oc_rtg)), "DC": min(10, max(1, dc_rtg))}
            }
        
        st.session_state.schedule = generate_schedule(st.session_state.team_name, st.session_state.team_conf)
        st.session_state.hotspots = generate_hotspots()
            
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    fire_threshold = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < fire_threshold:
        st.session_state.game_state = "FIRED"
        st.rerun()

    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    sec = st.session_state.job_security
    sec_class = "security-safe" if sec >= 75 else ("security-warm" if sec >= 40 else "security-hot")
    sec_text = "🛡️ Safe" if sec >= 75 else ("🔥 Warm" if sec >= 40 else "🚨 HOT SEAT")
    if st.session_state.tenure <= 2: sec_text += " (Honeymoon)"
    
    st.markdown(f"""
    <div class='security-box'>
        <span>Year {st.session_state.tenure} | Expectation: <b>{st.session_state.expected_wins}+ Wins</b></span> | 
        <span>Job Security: <span class='{sec_class}'>{sec}% ({sec_text})</span></span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""<div style='background-color: {st.session_state.team_color}; padding: 15px; border-radius: 10px;'><h2 style='color: white; margin:0; text-align: center;'>{st.session_state.team_name} ({st.session_state.year})</h2></div>""", unsafe_allow_html=True)
    
    qb = st.session_state.roster["QB"]
    ol = st.session_state.roster["OL"]
    skill = (st.session_state.roster["RB"] + st.session_state.roster["WR"]) / 2
    raw_talent = int((qb*0.3)+(ol*0.25)+(skill*0.45))
    
    ovr = calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff, st.session_state.facilities)
    if st.session_state.momentum >= 3: ovr += 3
    st.session_state.team_rating = ovr
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget", format_cash(st.session_state.budget))
    c2.metric("Team OVR", ovr, f"Off. Talent: {raw_talent}")
    c3.metric("Legacy Score", saban)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Strategy", "Staff", "Facilities", "Season"])
    
    with tab1:
        st.subheader("Tactical War Room")
        c_off, c_def = st.columns(2)
        with c_off:
            new_off = st.selectbox("Offense", SCHEMES["Offense"], index=SCHEMES["Offense"].index(st.session_state.my_schemes["Off"]))
            st.session_state.my_schemes["Off"] = new_off
            st.caption(SCHEME_DESC[new_off])
        with c_def:
            new_def = st.selectbox("Defense", SCHEMES["Defense"], index=SCHEMES["Defense"].index(st.session_state.my_schemes["Def"]))
            st.session_state.my_schemes["Def"] = new_def
            st.caption(SCHEME_DESC[new_def])
        st.write("Roster Strength")
        for p, v in st.session_state.roster.items(): 
            label = f"{p}: {int(v)}"
            if st.session_state.active_transfers.get(p): label += " (TRANSFER BOOSTED)"
            st.progress(min(1.0, v/100), label)

    with tab2:
        for role in ["HC","OC","DC","Scout"]:
            if role in st.session_state.staff:
                c = st.session_state.staff[role]
                st.success(f"**{role}**: {c['name']} (Off:{c['off']} Def:{c['def']} Rec:{c['recruit']}) [{c['trait']}]")
                if st.button(f"Fire {role}", key=f"f_{role}"):
                    del st.session_state.staff[role]; st.rerun()
            else:
                st.warning(f"{role} Vacant")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"Search ($500k)", key=f"s_{role}"):
                        if st.session_state.budget >= 500000:
                            st.session_state.budget -= 500000
                            st.session_state.candidates[role] = [generate_coach(role, i) for i in [1,2,3]]
                            st.rerun()
                with c2:
                    if st.button(f"Promote GA (Free)", key=f"ga_{role}"):
                        st.session_state.staff[role] = generate_ga_coach(role)
                        st.rerun()
                        
                if role in st.session_state.candidates:
                    for i, cand in enumerate(st.session_state.candidates[role]):
                        if st.button(f"Hire {cand['name']} ({format_cash(cand['salary'])})", key=f"h_{role}_{i}"):
                            if st.session_state.budget >= cand['salary']:
                                st.session_state.budget -= cand['salary']
                                st.session_state.staff[role] = cand
                                del st.session_state.candidates[role]
                                st.rerun()

    with tab3:
        f1, f2, f3 = st.columns(3)
        with f1:
            lvl = st.session_state.facilities['Marketing']
            st.metric("Marketing", f"Lvl {lvl}", f"Rev: +${lvl}M")
            if st.button(f"Upgrade ($1M)", key="up_mkt"):
                if st.session_state.budget >= 1000000:
                    st.session_state.budget -= 1000000; st.session_state.facilities['Marketing'] += 1; st.rerun()
        with f2:
            lvl = st.session_state.facilities['Training']
            st.metric("Training", f"Lvl {lvl}", f"OVR: +{int((lvl-1)*0.5)}")
            if st.button(f"Upgrade ($3M)", key="up_trn"):
                if st.session_state.budget >= 3000000:
                    st.session_state.budget -= 3000000; st.session_state.facilities['Training'] += 1; st.rerun()
        with f3:
            lvl = st.session_state.facilities['Stadium']
            st.metric("Stadium", f"Lvl {lvl}", "Prestige++")
            if st.button(f"Upgrade ($10M)", key="up_std"):
                if st.session_state.budget >= 10000000:
                    st.session_state.budget -= 10000000; st.session_state.facilities['Stadium'] += 1; st.rerun()

    with tab4:
        st.info(f"Conference: {st.session_state.team_conf}")
        if len(st.session_state.staff) < 4: st.error("Fill Staff first!"); return
        
        # --- ENHANCED GAME CARDS ---
        if not st.session_state.season_simulated:
            st.write("### 📅 Upcoming Schedule")
            if not st.session_state.schedule:
                st.session_state.schedule = generate_schedule(st.session_state.team_name, st.session_state.team_conf)
                
            c1, c2 = st.columns(2)
            with c1:
                st.caption("First Half")
                for i in range(6):
                    opp = st.session_state.schedule[i]
                    opp_ovr = st.session_state.opponents_db.get(opp, {}).get('OVR', 75)
                    loc = "HOME" if i%2==0 else "AWAY"
                    st.markdown(f"""
                    <div class="game-card game-card-pending">
                        <div class="card-header">
                            <span class="home-label">{loc}</span>
                            <span class="card-opp">Week {i+1} vs {opp}</span>
                        </div>
                        <span class="stat-line">OVR: {opp_ovr}</span>
                    </div>
                    """, unsafe_allow_html=True)
            with c2:
                st.caption("Second Half")
                for i in range(6, 12):
                    opp = st.session_state.schedule[i]
                    opp_ovr = st.session_state.opponents_db.get(opp, {}).get('OVR', 75)
                    loc = "HOME" if i%2==0 else "AWAY"
                    st.markdown(f"""
                    <div class="game-card game-card-pending">
                        <div class="card-header">
                            <span class="home-label">{loc}</span>
                            <span class="card-opp">Week {i+1} vs {opp}</span>
                        </div>
                        <span class="stat-line">OVR: {opp_ovr}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.button("▶️ SIMULATE SEASON", type="primary"):
                run_season()
        else:
            st.write("### 📊 Season Results")
            logs = st.session_state.season_logs
            c1, c2 = st.columns(2)
            
            for col_idx, col in enumerate([c1, c2]):
                with col:
                    start = 0 if col_idx == 0 else 6
                    end = 6 if col_idx == 0 else 12
                    st.caption("First Half" if col_idx == 0 else "Second Half")
                    
                    for i in range(start, end):
                        log = logs[i]
                        stats = log['Stats']
                        is_win = "W" in log['Score']
                        css = "game-card-win" if is_win else "game-card-loss"
                        
                        st.markdown(f"""
                        <div class="game-card {css}">
                            <div class="card-header">
                                <span class="card-score">{log['Score']}</span>
                                <span class="card-opp">vs {log['Opponent']}</span>
                            </div>
                            <div class="stat-grid">
                                <div class="stat-row"><span class="stat-label">🔥 QB Duel:</span> <span class="stat-val">{stats['qb_duel'][0]} vs {stats['qb_duel'][1]}</span></div>
                                <div class="stat-row"><span class="stat-label">⚔️ Off vs Def:</span> <span class="stat-val">{stats['off_vs_def'][0]} vs {stats['off_vs_def'][1]}</span></div>
                                <div class="stat-row"><span class="stat-label">🛡️ Def vs Off:</span> <span class="stat-val">{stats['def_vs_off'][0]} vs {stats['def_vs_off'][1]}</span></div>
                                <div class="stat-row"><span class="stat-label">🧠 Staff:</span> <span class="stat-val">{stats['staff'][0]} vs {stats['staff'][1]}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.success(f"Regular Season Complete! Record: {st.session_state.record['w']}-{st.session_state.record['l']}")
            if st.button("➡️ Proceed to Postseason", type="primary"):
                st.session_state.game_state = "POSTSEASON"
                st.rerun()

def run_season():
    wins = 0; losses = 0; logs = []
    schedule = st.session_state.schedule
    my_oc = st.session_state.staff['OC']['off'] if 'OC' in st.session_state.staff else 3
    my_dc = st.session_state.staff['DC']['def'] if 'DC' in st.session_state.staff else 3
    
    patience = 1.0
    if st.session_state.tenure <= 2: patience = 0.5 
    elif st.session_state.school_tier == 4: patience = 0.5 
    elif st.session_state.school_tier == 1: patience = 1.5 
    
    bar = st.progress(0, "Simulating Games...")
    for i, opp_name in enumerate(schedule):
        opp_data = st.session_state.opponents_db.get(opp_name)
        is_rival = (opp_name == st.session_state.team_rival)
        opp_schemes = {"Off": opp_data["Off"], "Def": opp_data["Def"]}
        is_home = (i % 2 == 0)
        my_facilities = st.session_state.facilities.get("Stadium", 1)
        
        res = play_game(st.session_state.team_rating, opp_data["OVR"], st.session_state.staff, st.session_state.stars, st.session_state.my_schemes, opp_schemes, "Normal", opp_data["Coaches"], is_home, is_rival, my_facilities, st.session_state.roster)
        
        if res['result'] == "W": 
            wins += 1
            st.session_state.momentum += 1
            st.session_state.job_security = min(100, st.session_state.job_security + 2)
            if is_rival: st.session_state.job_security = min(100, st.session_state.job_security + 5)
        else: 
            losses += 1
            st.session_state.momentum = 0
            loss_hit = 3 * patience
            st.session_state.job_security = max(0, int(st.session_state.job_security - loss_hit))
            
        logs.append({
            "Week": i+1, "Opponent": opp_name, 
            "Score": f"{res['result']} {res['score']}", 
            "Stats": res['stats']
        })
        bar.progress((i+1)/12)

    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    if wins == 12: st.session_state.undefeated_streak += 1
    else: st.session_state.undefeated_streak = 0
    
    is_power4 = st.session_state.team_conf in ["SEC", "Big Ten", "Big 12", "ACC"]
    if wins == 12:
        if is_power4: st.session_state.rank = random.randint(1, 4)
        elif st.session_state.undefeated_streak >= 2: st.session_state.rank = random.randint(4, 8)
        else: st.session_state.rank = random.randint(10, 14)
    elif wins == 11:
        if is_power4: st.session_state.rank = random.randint(5, 11)
        else: st.session_state.rank = random.randint(12, 18)
    elif wins == 10:
        if is_power4: st.session_state.rank = random.randint(10, 18)
        else: st.session_state.rank = random.randint(18, 25)
    else: st.session_state.rank = 130 - (wins*10)
    
    st.session_state.playoff_round = 0
    st.session_state.match_history = []
    st.session_state.season_simulated = True 
    st.rerun()

def show_postseason():
    rank = st.session_state.rank
    wins = st.session_state.record['w']
    st.title("Postseason Hub")
    st.info(f"Season Record: {wins}-{st.session_state.record['l']} | Final Rank: #{rank}")
    
    if 'current_matchup' not in st.session_state:
        st.session_state.current_matchup = None
        st.session_state.ps_active = True
        sorted_opps = sorted(st.session_state.opponents_db.items(), key=lambda x: x[1]['OVR'], reverse=True)
        if rank <= 12: 
            st.session_state.ps_mode = "PLAYOFF"
            opp_name, opp_data = sorted_opps[random.randint(0, 11)]
            st.session_state.current_matchup_name = f"#{random.randint(1,12)} {opp_name}"
            st.session_state.current_matchup_data = opp_data
            st.session_state.budget += 5000000
            st.toast("🏆 Playoff Qualifier Bonus: $5M")
        elif wins >= 6:
            st.session_state.ps_mode = "BOWL"
            bowl_name = get_bowl_name(rank)
            opp_name, opp_data = sorted_opps[random.randint(20, 40)]
            st.session_state.current_matchup_name = f"{opp_name} in {bowl_name}"
            st.session_state.current_matchup_data = opp_data
            st.session_state.budget += 1000000
            st.toast("🎳 Bowl Invite Bonus: $1M")
        else:
            st.session_state.ps_active = False
            st.error("Season Over. No Bowl Invite.")

    if st.session_state.ps_active:
        opp_data = st.session_state.current_matchup_data
        st.markdown(f"""<div class='bracket-box'><h2>{st.session_state.ps_mode} GAME</h2><h1>VS {st.session_state.current_matchup_name}</h1></div>""", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.markdown(f"""<div class='scout-report'><b>OPPONENT SCOUT</b><br>OVR: {opp_data['OVR']}<br>Staff: OC {opp_data['Coaches']['OC']} / DC {opp_data['Coaches']['DC']}<br>Offense: {opp_data['Off']}<br>Defense: {opp_data['Def']}</div>""", unsafe_allow_html=True)
        with c2:
            my_oc = st.session_state.staff['OC']['off'] if 'OC' in st.session_state.staff else 3
            my_dc = st.session_state.staff['DC']['def'] if 'DC' in st.session_state.staff else 3
            st.markdown(f"""<div class='scout-report'><b>MY TEAM</b><br>OVR: {st.session_state.team_rating}<br>Staff: OC {my_oc} / DC {my_dc}<br>Offense: {st.session_state.my_schemes['Off']}<br>Defense: {st.session_state.my_schemes['Def']}</div>""", unsafe_allow_html=True)
        game_plan = st.selectbox("Game Plan", ["Balanced", "Aggressive", "Conservative"], help="Aggressive: High Risk/Reward. Conservative: Play safe.")
        if st.button("PLAY GAME 🏈"):
            res = play_game(st.session_state.team_rating, opp_data['OVR'], st.session_state.staff, st.session_state.stars, st.session_state.my_schemes, {"Off":opp_data['Off'],"Def":opp_data['Def']}, game_plan, opp_data['Coaches'], False, False, 10, st.session_state.roster)
            st.session_state.match_history.append(f"{st.session_state.ps_mode}: {res['result']} {res['score']} vs {st.session_state.current_matchup_name}")
            if res['result'] == "W":
                st.balloons()
                bonus = 10000000 if st.session_state.ps_mode == "PLAYOFF" else 2000000
                st.session_state.budget += bonus
                st.success(f"VICTORY! {res['score']}")
                st.toast(f"💰 Booster Donation: {format_cash(bonus)}")
                if st.session_state.ps_mode == "PLAYOFF":
                    st.session_state.career_stats['cfp_w'] += 1
                    st.session_state.career_stats['cfp_g'] += 1
                    st.session_state.playoff_round += 1
                    if st.session_state.playoff_round >= 4:
                        st.session_state.ps_active = False
                        st.markdown("# 🏆 NATIONAL CHAMPIONS!")
                        st.session_state.career_stats['titles'] += 1
                        st.session_state.budget += 20000000
                    else:
                        sorted_opps = sorted(st.session_state.opponents_db.items(), key=lambda x: x[1]['OVR'], reverse=True)
                        opp_name, opp_data = sorted_opps[st.session_state.playoff_round]
                        st.session_state.current_matchup_name = f"#{random.randint(1,4)} {opp_name}"
                        st.session_state.current_matchup_data = opp_data
                        st.info("Advancing to next round...")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.session_state.ps_active = False 
                    st.session_state.career_stats['bowl_w'] += 1
            else:
                st.error(f"DEFEAT {res['score']}")
                if st.session_state.ps_mode == "PLAYOFF": st.session_state.career_stats['cfp_g'] += 1
                st.session_state.ps_active = False
                if st.session_state.ps_mode == "BOWL": st.session_state.career_stats['bowl_l'] += 1
    else:
        if st.session_state.match_history:
            st.write("Postseason Results:")
            for m in st.session_state.match_history: st.write(m)
        rev = 15000000 + (st.session_state.facilities['Marketing'] * 1000000)
        st.success(f"Season Complete. Revenue Generated: {format_cash(rev)}")
        
        delta = wins - st.session_state.expected_wins
        if delta > 0:
            bonus = delta * 1000000
            st.success(f"📈 EXCEEDED EXPECTATIONS! Boosters donate {format_cash(bonus)}")
            st.session_state.budget += bonus
            st.session_state.job_security = min(100, st.session_state.job_security + 10)
        elif delta < 0:
            cut = abs(delta) * 500000
            st.error(f"📉 MISSED EXPECTATIONS. Budget cut by {format_cash(cut)}")
            st.session_state.budget -= cut
            if st.session_state.tenure <= 2:
                st.info("🔰 Rebuild Protection: Job Security hit reduced.")
                st.session_state.job_security = max(0, st.session_state.job_security - 5)
            else:
                st.session_state.job_security = max(0, st.session_state.job_security - 15)
        
        if st.session_state.team_conf == "G5" and rank <= 12:
            st.success("🌟 BIG 12 INVITE RECEIVED!")
            if st.button("Accept Big 12 Invite"):
                st.session_state.team_conf = "Big 12"; st.session_state.budget += 20000000; st.rerun()
        if st.button("Advance to Offseason"):
            st.session_state.budget += rev
            st.session_state.career_stats['w'] += wins
            del st.session_state['current_matchup'] 
            history_entry = {"Year": st.session_state.year, "Record": f"{st.session_state.record['w']}-{st.session_state.record['l']}", "Rank": f"#{st.session_state.rank}", "Bowl": st.session_state.ps_mode if wins >= 6 else "None"}
            st.session_state.history.append(history_entry)
            st.session_state.last_season_summary = history_entry
            st.session_state.season_simulated = False 
            st.session_state.game_state = "SUMMARY"
            st.rerun()

def show_year_summary():
    st.title(f"📊 {st.session_state.year} Season Recap")
    if st.session_state.last_season_summary:
        entry = st.session_state.last_season_summary
        st.markdown(f"""<div class="summary-card"><h3>Season Performance</h3><p><b>Record:</b> {entry.get('Record')} | <b>Final Rank:</b> {entry.get('Rank')}</p></div>""", unsafe_allow_html=True)
    st.subheader("Program History")
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist, use_container_width=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Wins", st.session_state.career_stats['w'])
    c2.metric("Nat'l Titles", st.session_state.career_stats['titles'])
    c3.metric("Bowl Wins", st.session_state.career_stats['bowl_w'])
    cfp_pct = 0
    if st.session_state.career_stats['cfp_g'] > 0: cfp_pct = int((st.session_state.career_stats['cfp_w'] / st.session_state.career_stats['cfp_g']) * 100)
    c4.metric("CFP Win %", f"{cfp_pct}%")
    st.divider()
    if st.button("Enter Transfer Portal", type="primary"):
        st.session_state.portal_players = generate_portal_players()
        st.session_state.game_state = "PORTAL"
        st.rerun()

def show_portal():
    st.header("🔄 Transfer Portal")
    st.info("Bid on players to fill holes immediately.")
    st.write(f"Budget: {format_cash(st.session_state.budget)}")
    if not st.session_state.portal_players: st.write("No players interested.")
    for i, p in enumerate(st.session_state.portal_players):
        c1, c2 = st.columns([3, 1])
        with c1: 
            st.markdown(f"**{p['pos']} {p['name']}** (OVR: {p['rating']})")
            st.caption(f"{p['desc']} | Cost: {format_cash(p['cost'])}")
        with c2:
            if st.button("Sign", key=f"sign_p_{i}"):
                if st.session_state.budget >= p['cost']:
                    st.session_state.budget -= p['cost']
                    new_star = {"id": random.randint(1000,9999), "name": p['name'], "pos": p['pos'], "rating": p['rating'], "year": p.get('year', 'Sr'), "trait": p.get('trait', 'None')}
                    st.session_state.stars.append(new_star)
                    st.session_state.roster[p['pos']] = max(st.session_state.roster[p['pos']], p['rating'])
                    st.session_state.active_transfers[p['pos']] = True 
                    st.session_state.portal_players.pop(i)
                    st.toast("Signed!")
                    st.rerun()
                else: st.error("Too expensive")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Advance to HS Recruiting"):
            st.session_state.game_state = "RECRUITING"
            st.rerun()
    with c2:
        if st.button("Retire & View Legacy"):
            st.session_state.game_state = "RETIREMENT"
            st.rerun()

def show_recruiting():
    st.header("High School Recruiting")
    st.info(f"Budget: {format_cash(st.session_state.budget)}")
    st.caption(f"Home Region: {st.session_state.home_region} (Base Boost: {int((REGION_STRENGTH.get(st.session_state.home_region, 1.0) - 1)*100)}%)")
    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    st.markdown(f"""<div class="recruiting-intel"><b>📍 Scouting Report ({st.session_state.home_region})</b><br>Top talent spotted this year at: <b>{', '.join(hot)}</b> (+15% Bonus)</div>""", unsafe_allow_html=True)
    current_spend = 0
    allocs = {}
    c1, c2 = st.columns(2)
    for i, p in enumerate(POSITIONS):
        with c1 if i%2==0 else c2:
            val = st.number_input(f"{p} Spend", 0, 10000000, 0, step=100000, key=f"rec_{p}")
            allocs[p] = val
            current_spend += val
    remaining = st.session_state.budget - current_spend
    if remaining < 0: st.error(f"Over Budget by {format_cash(abs(remaining))}")
    else: st.success(f"Remaining: {format_cash(remaining)}")
    if st.button("Finalize Class"):
        res = process_recruiting(st.session_state.budget, allocs, st.session_state.staff, st.session_state.prestige, st.session_state.inflation)
        if not res: st.error("Over Budget!"); return
        st.session_state.budget -= res['cost']
        for p, g in res['roster_updates'].items():
            base_loss = random.randint(2, 5)
            if st.session_state.active_transfers.get(p):
                base_loss = 12
                st.session_state.active_transfers[p] = False
            st.session_state.roster[p] = max(40, min(99, st.session_state.roster[p] - base_loss + g))
        if res['gems']: st.session_state.stars.extend(res['gems'])
        if res['booster_bonus'] > 0:
            st.session_state.budget += res['booster_bonus']
            st.toast(f"💎 Gem Bonus: {format_cash(res['booster_bonus'])}")
        active_stars = []
        for s in st.session_state.stars:
            if s['year'] == "Sr": st.toast(f"🎓 {s['name']} Graduated")
            else:
                if s['year'] == "Fr": s['year'] = "So"
                elif s['year'] == "So": s['year'] = "Jr"
                elif s['year'] == "Jr": s['year'] = "Sr"
                active_stars.append(s)
        st.session_state.stars = active_stars
        st.session_state.year += 1
        st.session_state.tenure += 1
        st.session_state.inflation *= 1.05 
        st.session_state.schedule = generate_schedule(st.session_state.team_name, st.session_state.team_conf)
        st.session_state.hotspots = generate_hotspots()
        time.sleep(2) 
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

def show_retirement():
    st.balloons()
    st.title(f"🏛️ Hall of Fame: {st.session_state.ad_name}")
    score = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.metric("Final Legacy Score", score, help="Saban = 600")
    st.divider()
    st.subheader("Career Timeline")
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist, use_container_width=True)
    st.subheader("Trophy Case")
    c1, c2, c3 = st.columns(3)
    c1.metric("Titles", st.session_state.career_stats['titles'])
    c2.metric("Bowl Wins", st.session_state.career_stats['bowl_w'])
    c3.metric("Total Wins", st.session_state.career_stats['w'])
    if st.button("Start New Career"):
        st.session_state.clear(); st.rerun()

def show_fired():
    st.error("🚫 FIRED! Booster morale dropped below 25%.")
    if st.button("Restart"): st.session_state.clear(); st.rerun()

# --- 7. ROUTER ---
if st.session_state.game_state == 'SETUP': run_setup()
elif st.session_state.game_state == 'FIRED': show_fired()
elif st.session_state.game_state == 'DASHBOARD': show_dashboard()
elif st.session_state.game_state == 'POSTSEASON': show_postseason()
elif st.session_state.game_state == 'SUMMARY': show_year_summary()
elif st.session_state.game_state == 'PORTAL': show_portal()
elif st.session_state.game_state == 'RECRUITING': show_recruiting()
elif st.session_state.game_state == 'RETIREMENT': show_retirement()
