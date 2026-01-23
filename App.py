import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(page_title="College Football Mogul", page_icon="🏈", layout="centered")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    .news-ticker { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px; border: 1px solid #ffeeba; }
    .star-card { background: white; border: 1px solid #ddd; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 8px; }
    .staff-card { background: #f0f4c3; border: 1px solid #dce775; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 5px; }
    .gem-box { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 5px solid #2196f3; margin-bottom: 5px; }
    .scheme-box { background-color: #e8f5e9; border: 1px solid #c8e6c9; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .fired-card { background-color: #ffcccc; padding: 20px; border-radius: 10px; border: 2px solid #ff0000; text-align: center; }
    .bracket-box { background-color: #2c3e50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]

# TEAMS DATABASE (Fully Connected)
TEAMS_DB = {
    "Georgia": {"tier": 1, "budget": 24000000, "conf": "SEC", "rival": "Alabama", "color": "#BA0C2F", "facilities": 10},
    "Ohio State": {"tier": 1, "budget": 24000000, "conf": "Big Ten", "rival": "Michigan", "color": "#BB0000", "facilities": 10},
    "Texas": {"tier": 1, "budget": 25000000, "conf": "SEC", "rival": "Oklahoma", "color": "#BF5700", "facilities": 10},
    "Alabama": {"tier": 1, "budget": 22000000, "conf": "SEC", "rival": "Georgia", "color": "#9E1B32", "facilities": 9},
    "Oregon": {"tier": 1, "budget": 20000000, "conf": "Big Ten", "rival": "Washington", "color": "#154733", "facilities": 10},
    "Florida St": {"tier": 2, "budget": 15000000, "conf": "ACC", "rival": "Clemson", "color": "#782F40", "facilities": 8},
    "Penn State": {"tier": 2, "budget": 16000000, "conf": "Big Ten", "rival": "Ohio State", "color": "#041E42", "facilities": 8},
    "Boise State": {"tier": 3, "budget": 7000000, "conf": "G5", "rival": "Fresno St", "color": "#0033A0", "facilities": 5},
    "San Jose State": {"tier": 4, "budget": 4500000, "conf": "G5", "rival": "San Diego St", "color": "#0055A2", "facilities": 3}
}

CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Texas A&M"],
    "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington"],
    "ACC": ["Florida St", "Clemson", "Miami", "Stanford", "Cal", "Louisville", "UNC", "Virginia Tech"],
    "Big 12": ["Utah", "TCU", "Baylor", "Texas Tech", "Arizona State", "Colorado", "Kansas State", "Oklahoma St"],
    "G5": ["Boise State", "San Jose State", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St", "Fresno St"]
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

TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {"None": "None", "Recruiter": "+10% Recruiting", "Tactician": "+3 Game Boost", "Cheap": "Low Salary"}

BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl", "ReliaQuest Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl", "Sun Bowl", "Pinstripe Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl", "Frisco Bowl", "Myrtle Beach Bowl"]
}

HEADLINES = [
    "Rumor: Offensive Coordinator considering NFL jobs.",
    "Boosters reportedly 'furious' after rival loss.",
    "Analyst: 'This team recruits the South better than anyone.'",
    "Breaking: 5-Star QB spotted at campus steakhouse.",
    "Stadium renovations approved by the board.",
    "Polls: Voters skeptical of strength of schedule.",
    "Committee Chair: 'We are watching the strength of schedule closely.'"
]

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
    c = {
        "name": f"{generate_coach_name()}",
        "role": role,
        "off": min(10, base + random.randint(0, 2)),
        "def": min(10, base + random.randint(0, 2)),
        "recruit": min(10, base + random.randint(0, 2)),
        "trait": random.choice(list(COACH_TRAITS.keys())),
        "salary": cost
    }
    if c["trait"] == "Cheap": c["salary"] = int(c["salary"] * 0.5)
    return c

def generate_portal_players():
    players = []
    # Tier 1: Elite
    for _ in range(2):
        pos = random.choice(POSITIONS)
        players.append({
            "name": f"Elite {pos} {random.randint(1,99)}",
            "pos": pos,
            "rating": random.randint(90, 99),
            "cost": random.randint(4000000, 8000000),
            "trait": random.choice(TRAITS),
            "year": "Sr",
            "desc": "Day 1 Starter"
        })
    # Tier 2: Solid
    for _ in range(2):
        pos = random.choice(POSITIONS)
        players.append({
            "name": f"Solid {pos} {random.randint(1,99)}",
            "pos": pos,
            "rating": random.randint(80, 89),
            "cost": random.randint(1000000, 3000000),
            "trait": random.choice(TRAITS),
            "year": random.choice(["Jr", "Sr"]),
            "desc": "Good Depth"
        })
    # Tier 3: Budget
    for _ in range(3):
        pos = random.choice(POSITIONS)
        players.append({
            "name": f"Value {pos} {random.randint(1,99)}",
            "pos": pos,
            "rating": random.randint(70, 79),
            "cost": random.randint(250000, 800000),
            "trait": "None",
            "year": random.choice(["So", "Jr"]),
            "desc": "Immediate Help"
        })
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

def generate_initial_roster(tier):
    base = 64
    if tier == 1: base = 90
    elif tier == 2: base = 82
    elif tier == 3: base = 74
    roster = {}
    for p in POSITIONS: roster[p] = min(99, max(40, base + random.randint(0, 6)))
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
    star["trait"] = random.choice(list(TRAITS))
    return star

def calculate_ovr(roster, stars, staff, facilities):
    off = sum(roster[p] for p in ["QB","RB","WR","OL"]) / 4
    defs = sum(roster[p] for p in ["DL","LB","DB"]) / 3
    
    if "OC" in staff: off += (staff["OC"]["off"] - 5) * 1.5
    if "DC" in staff: defs += (staff["DC"]["def"] - 5) * 1.5
    if "HC" in staff: 
        off += (staff["HC"]["off"] - 5) * 0.5
        defs += (staff["HC"]["def"] - 5) * 0.5
    
    # Facility Bonus Check
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

def play_game(my_rating, opp_rating, staff, stars, my_schemes, opp_schemes, is_rival, momentum):
    margin = my_rating - opp_rating
    
    scheme_bonus = 0
    if COUNTERS[opp_schemes['Def']] == my_schemes['Off']: scheme_bonus += 8 
    elif COUNTERS[my_schemes['Off']] == opp_schemes['Def']: scheme_bonus -= 8 
    
    if COUNTERS[opp_schemes['Off']] == my_schemes['Def']: scheme_bonus += 8
    elif COUNTERS[my_schemes['Def']] == opp_schemes['Off']: scheme_bonus -= 8
    
    exec_bonus = 0
    if "HC" in staff:
        if staff["HC"]["trait"] == "Tactician": exec_bonus += 3
        exec_bonus += (staff["HC"]["off"] + staff["HC"]["def"] - 10) * 0.2

    mom_bonus = 3 if momentum >= 3 else 0
    rival_bonus = 0
    if is_rival: rival_bonus = random.randint(-5, 5)

    total_margin = margin + scheme_bonus + exec_bonus + mom_bonus + rival_bonus + random.randint(-10, 10)
    
    my_score = int(28 + (total_margin/1.5)) if total_margin > 0 else int(24 + (total_margin/1.5))
    opp_score = int(my_score - total_margin)
    
    return {
        "result": "W" if total_margin > 0 else "L", 
        "score": f"{max(0,my_score)}-{max(0,opp_score)}",
        "scheme_bonus": scheme_bonus
    }

def process_recruiting(budget, allocations, staff, prestige, inflation):
    results = {"roster_updates": {}, "gems": [], "cost": sum(allocations.values()), "booster_bonus": 0}
    if results["cost"] > budget: return None
    
    staff_rec = 0
    for role in ["HC", "OC", "DC", "Scout"]:
        if role in staff:
            val = staff[role]["recruit"]
            if staff[role]["trait"] == "Recruiter": val += 2
            staff_rec += val
            
    scout_eff = 1.0 + (staff_rec / 40.0) 
    prestige_bonus = 1.0 + (prestige / 200.0)
    
    for pos, amount in allocations.items():
        if amount > 0:
            buying_power = amount / (800000 * inflation)
            gain = buying_power * scout_eff * prestige_bonus
            
            gem_prob = (staff_rec * 0.5) / 100.0
            if amount > (250000 * inflation) and random.random() < gem_prob:
                gain += 5 
                new_star = generate_star_player(pos, 1)
                new_star['year'] = "Fr"
                new_star['name'] = f"{new_star['name']} (GEM)"
                results["gems"].append(new_star)
                # GEM BONUS
                results["booster_bonus"] += random.randint(2, 5) * 100000
            results["roster_updates"][pos] = gain
    return results

# --- 5. INITIALIZATION & STATE REPAIR ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP'
    st.session_state.year = 2026
    st.session_state.budget = 0
    st.session_state.prestige = 50
    st.session_state.booster_morale = 80
    st.session_state.roster = {p: 75 for p in POSITIONS}
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
    st.session_state.current_headline = "Season Begins"
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
    st.session_state.team_rating = 0
    st.session_state.season_logs = []
    st.session_state.postseason_result = {}
    st.session_state.undefeated_streak = 0
    st.session_state.inflation = 1.0
    st.session_state.playoff_round = 0
    st.session_state.last_season_summary = {}

# REPAIR STATE
if 'inflation' not in st.session_state: st.session_state.inflation = 1.0
if 'playoff_round' not in st.session_state: st.session_state.playoff_round = 0
if 'undefeated_streak' not in st.session_state: st.session_state.undefeated_streak = 0
if 'last_season_summary' not in st.session_state: st.session_state.last_season_summary = {}

# --- 6. SCREENS ---

def run_setup():
    st.title("🏆 College Football Mogul v2.1")
    st.markdown("### Dynasty Mode")
    col1, col2 = st.columns(2)
    with col1: name = st.text_input("AD Name", "Coach Prime")
    with col2: diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    team = st.selectbox("Select Team", sorted(TEAMS_DB.keys()))
    d = TEAMS_DB[team]
    st.info(f"**{team}** ({d['conf']}) | Rival: {d['rival']} | Budget: {format_cash(d['budget'])}")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = d.get('color', '#333333')
        st.session_state.team_conf = d.get('conf', 'SEC')
        st.session_state.team_rival = d.get('rival', 'None')
        
        mult = 1.0
        if diff == "Hard": mult = 0.75
        elif diff == "Easy": mult = 1.25
            
        st.session_state.budget = int(d['budget'] * mult)
        st.session_state.prestige = 95 - (d['tier'] * 12)
        
        st.session_state.roster = generate_initial_roster(d['tier'])
        st.session_state.stars = [generate_star_player("QB", d['tier'])]
        if d['tier'] < 4: st.session_state.stars.append(generate_star_player("LB", d['tier']))
        
        for r in ["HC","OC","DC","Scout"]: st.session_state.staff[r] = generate_coach(r, d['tier'])
        
        # FIXED: Explicit facility loading
        fac_val = d.get('facilities', 1)
        st.session_state.facilities = {"Marketing": fac_val, "Training": fac_val, "Stadium": fac_val}
        
        for opp in ALL_TEAMS:
            rtg = 75
            if opp in CONFERENCES["SEC"] or opp in CONFERENCES["Big Ten"]: rtg = 85
            st.session_state.opponents_db[opp] = {
                "OVR": rtg + random.randint(-5, 5),
                "Off": random.choice(SCHEMES["Offense"]),
                "Def": random.choice(SCHEMES["Defense"])
            }
            
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    # FIRE CHECK
    if st.session_state.booster_morale < 25:
        st.session_state.game_state = "FIRED"
        st.rerun()

    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.markdown(f"<div class='news-ticker'>📰 {st.session_state.current_headline}</div>", unsafe_allow_html=True)
    st.markdown(f"""<div style='background-color: {st.session_state.team_color}; padding: 15px; border-radius: 10px;'><h2 style='color: white; margin:0; text-align: center;'>{st.session_state.team_name} ({st.session_state.year})</h2></div>""", unsafe_allow_html=True)
    
    ovr = calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff, st.session_state.facilities)
    if st.session_state.momentum >= 3: ovr += 3
    st.session_state.team_rating = ovr
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget", format_cash(st.session_state.budget))
    c2.metric("Team OVR", ovr, f"{'🔥 Hot' if st.session_state.momentum >=3 else ''}")
    c3.metric("Legacy Score", saban)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Strategy", "Staff", "Facilities", "Season"])
    
    with tab1:
        st.subheader("Tactical War Room")
        c_off, c_def = st.columns(2)
        with c_off:
            new_off = st.selectbox("Offense", SCHEMES["Offense"], index=SCHEMES["Offense"].index(st.session_state.my_schemes["Off"]))
            st.session_state.my_schemes["Off"] = new_off
        with c_def:
            new_def = st.selectbox("Defense", SCHEMES["Defense"], index=SCHEMES["Defense"].index(st.session_state.my_schemes["Def"]))
            st.session_state.my_schemes["Def"] = new_def
            
        st.write("Roster Strength")
        for p, v in st.session_state.roster.items(): st.progress(min(1.0, v/100), f"{p}: {int(v)}")

    with tab2:
        for role in ["HC","OC","DC","Scout"]:
            if role in st.session_state.staff:
                c = st.session_state.staff[role]
                st.success(f"**{role}**: {c['name']} (Off:{c['off']} Def:{c['def']} Rec:{c['recruit']}) [{c['trait']}]")
                if st.button(f"Fire {role}", key=f"f_{role}"):
                    del st.session_state.staff[role]; st.rerun()
            else:
                st.warning(f"{role} Vacant")
                if st.button(f"Search ($500k)", key=f"s_{role}"):
                    if st.session_state.budget >= 500000:
                        st.session_state.budget -= 500000
                        st.session_state.candidates[role] = [generate_coach(role, i) for i in [1,2,3]]
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
        if st.button("▶️ SIMULATE SEASON", type="primary"):
            run_season()

def run_season():
    wins = 0; losses = 0; logs = []
    schedule = generate_schedule(st.session_state.team_name, st.session_state.team_conf)
    
    bar = st.progress(0, "Kickoff...")
    
    for i, opp_name in enumerate(schedule):
        opp_data = st.session_state.opponents_db.get(opp_name, {"OVR": 75, "Off": "Pro Style", "Def": "Man Coverage"})
        is_rival = (opp_name == st.session_state.team_rival)
        opp_schemes = {"Off": opp_data["Off"], "Def": opp_data["Def"]}
        
        res = play_game(
            st.session_state.team_rating, 
            opp_data["OVR"], 
            st.session_state.staff, 
            st.session_state.stars,
            st.session_state.my_schemes,
            opp_schemes,
            is_rival,
            st.session_state.momentum
        )
        
        if res['result'] == "W": 
            wins += 1
            st.session_state.momentum += 1
            if is_rival: st.session_state.booster_morale = min(100, st.session_state.booster_morale + 10)
        else: 
            losses += 1
            st.session_state.momentum = 0
            if is_rival: st.session_state.booster_morale = max(0, st.session_state.booster_morale - 15)
            
        logs.append({"Week": i+1, "Opp": opp_name, "Result": res['result'], "Score": res['score']})
        bar.progress((i+1)/12)

    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    
    if wins == 12: st.session_state.undefeated_streak += 1
    else: st.session_state.undefeated_streak = 0
    
    # RANKING LOGIC
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
    else: 
        st.session_state.rank = 130 - (wins*10)
    
    st.session_state.playoff_round = 0
    st.session_state.game_state = "POSTSEASON"
    st.rerun()

def show_postseason():
    rank = st.session_state.rank
    wins = st.session_state.record['w']
    
    st.title("Postseason Hub")
    st.info(f"Season Record: {wins}-{st.session_state.record['l']} | Final Rank: #{rank}")
    
    # --- LOGIC CONTROLLER ---
    if 'current_matchup' not in st.session_state:
        st.session_state.current_matchup = None
        st.session_state.ps_active = True
        
        if rank <= 12: # 12-Team Playoff
            st.session_state.ps_mode = "PLAYOFF"
            st.session_state.current_matchup = f"#{random.randint(1,12)} {random.choice(ALL_TEAMS)}"
            st.session_state.budget += 5000000
            st.toast("🏆 Playoff Qualifier Bonus: $5M")
        elif wins >= 6:
            st.session_state.ps_mode = "BOWL"
            bowl_name = get_bowl_name(rank)
            st.session_state.current_matchup = f"{random.choice(ALL_TEAMS)} in {bowl_name}"
            st.session_state.budget += 1000000
            st.toast("🎳 Bowl Invite Bonus: $1M")
        else:
            st.session_state.ps_active = False
            st.error("Season Over. No Bowl Invite.")

    # --- DISPLAY AREA ---
    if st.session_state.ps_active:
        st.markdown(f"""<div class='bracket-box'><h2>{st.session_state.ps_mode} GAME</h2>
        <h1>VS {st.session_state.current_matchup}</h1></div>""", unsafe_allow_html=True)
        
        opp_ovr = 85 + (st.session_state.playoff_round * 3) if st.session_state.ps_mode == "PLAYOFF" else 78
        st.caption(f"Opponent Scout: Rated {opp_ovr} OVR")
        
        if st.button("PLAY GAME 🏈"):
            res = play_game(st.session_state.team_rating, opp_ovr, st.session_state.staff, st.session_state.stars, st.session_state.my_schemes, {"Off":"Pro Style","Def":"Man Coverage"}, False, 0)
            
            if res['result'] == "W":
                st.balloons()
                bonus = 10000000 if st.session_state.ps_mode == "PLAYOFF" else 2000000
                st.session_state.budget += bonus
                st.success(f"VICTORY! {res['score']}")
                st.toast(f"💰 Booster Donation: {format_cash(bonus)}")
                
                if st.session_state.ps_mode == "PLAYOFF":
                    st.session_state.playoff_round += 1
                    if st.session_state.playoff_round >= 4:
                        st.session_state.ps_active = False
                        st.markdown("# 🏆 NATIONAL CHAMPIONS!")
                        st.session_state.career_stats['titles'] += 1
                        st.session_state.budget += 20000000
                    else:
                        st.session_state.current_matchup = f"#{random.randint(1,8)} {random.choice(ALL_TEAMS)}"
                        st.info("Advancing to next round...")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.session_state.ps_active = False 
                    st.session_state.career_stats['bowl_w'] += 1
            else:
                st.error(f"DEFEAT {res['score']}")
                st.session_state.ps_active = False
                if st.session_state.ps_mode == "BOWL": st.session_state.career_stats['bowl_l'] += 1
                
    else:
        rev = 15000000 + (st.session_state.facilities['Marketing'] * 1000000)
        st.success(f"Season Complete. Revenue Generated: {format_cash(rev)}")
        
        if st.session_state.team_conf == "G5" and rank <= 12:
            st.success("🌟 BIG 12 INVITE RECEIVED!")
            if st.button("Accept Big 12 Invite"):
                st.session_state.team_conf = "Big 12"; st.session_state.budget += 20000000; st.rerun()
                
        if st.button("View Season Recap"):
            st.session_state.budget += rev
            st.session_state.career_stats['w'] += wins
            del st.session_state['current_matchup'] 
            
            history_entry = {
                "Year": st.session_state.year,
                "Record": f"{st.session_state.record['w']}-{st.session_state.record['l']}",
                "Rank": f"#{st.session_state.rank}",
                "Bowl": st.session_state.ps_mode if wins >= 6 else "None"
            }
            st.session_state.history.append(history_entry)
            st.session_state.last_season_summary = history_entry
            
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
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Career Wins", st.session_state.career_stats['w'])
    c2.metric("Titles", st.session_state.career_stats['titles'])
    c3.metric("Bowl Wins", st.session_state.career_stats['bowl_w'])
    
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
                    # FIX: Add to Stars List
                    new_star = {
                        "id": random.randint(1000,9999),
                        "name": p['name'],
                        "pos": p['pos'],
                        "rating": p['rating'],
                        "year": p.get('year', 'Sr'),
                        "trait": p.get('trait', 'None')
                    }
                    st.session_state.stars.append(new_star)
                    # Update Unit Rating
                    st.session_state.roster[p['pos']] = max(st.session_state.roster[p['pos']], p['rating'])
                    
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
            st.session_state.roster[p] = min(99, st.session_state.roster[p] + g)
        
        # Add Gems
        if res['gems']: st.session_state.stars.extend(res['gems'])
        
        # RESTORED GEM BONUS CASH
        if res['booster_bonus'] > 0:
            st.session_state.budget += res['booster_bonus']
            st.toast(f"💎 Gem Bonus: {format_cash(res['booster_bonus'])}")
        
        # GRADUATION LOGIC FOR STARS
        active_stars = []
        for s in st.session_state.stars:
            if s['year'] == "Sr": st.toast(f"🎓 {s['name']} Graduated")
            else:
                if s['year'] == "Fr": s['year'] = "So"
                elif s['year'] == "So": s['year'] = "Jr"
                elif s['year'] == "Jr": s['year'] = "Sr"
                active_stars.append(s)
        st.session_state.stars = active_stars
        
        # Unit Decay
        for p in POSITIONS: st.session_state.roster[p] -= random.randint(2, 6)
        st.session_state.year += 1
        
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
