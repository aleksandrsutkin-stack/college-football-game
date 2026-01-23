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
    .fired-card { background-color: #ffcccc; padding: 20px; border-radius: 10px; border: 2px solid #ff0000; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA: TEAMS & CONFERENCES ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]

TEAMS_DB = {}
TEAMS_DB["Georgia"] = {"tier": 1, "budget": 24000000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BA0C2F", "conf": "SEC"}
TEAMS_DB["Ohio State"] = {"tier": 1, "budget": 24000000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BB0000", "conf": "Big Ten"}
TEAMS_DB["Texas"] = {"tier": 1, "budget": 25000000, "expect": 10, "coach": 9, "facilities": 10, "color": "#BF5700", "conf": "SEC"}
TEAMS_DB["Alabama"] = {"tier": 1, "budget": 22000000, "expect": 10, "coach": 9, "facilities": 9, "color": "#9E1B32", "conf": "SEC"}
TEAMS_DB["Oregon"] = {"tier": 1, "budget": 20000000, "expect": 10, "coach": 9, "facilities": 10, "color": "#154733", "conf": "Big Ten"}
TEAMS_DB["Florida St"] = {"tier": 2, "budget": 15000000, "expect": 9, "coach": 7, "facilities": 8, "color": "#782F40", "conf": "ACC"}
TEAMS_DB["Penn State"] = {"tier": 2, "budget": 16000000, "expect": 9, "coach": 8, "facilities": 8, "color": "#041E42", "conf": "Big Ten"}
TEAMS_DB["Boise State"] = {"tier": 3, "budget": 7000000, "expect": 9, "coach": 6, "facilities": 5, "color": "#0033A0", "conf": "G5 (Group of 5)"}
TEAMS_DB["San Jose State"] = {"tier": 4, "budget": 4500000, "expect": 6, "coach": 5, "facilities": 3, "color": "#0055A2", "conf": "G5 (Group of 5)"}

CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Texas A&M"],
    "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington"],
    "ACC": ["Florida St", "Clemson", "Miami", "Stanford", "Cal", "Louisville", "UNC", "Virginia Tech"],
    "Big 12": ["Utah", "TCU", "Baylor", "Texas Tech", "Arizona State", "Colorado", "Kansas State", "Oklahoma St"],
    "G5 (Group of 5)": ["Boise State", "San Jose State", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St", "Fresno St"]
}

# Create flat list of all teams for scheduling
ALL_TEAMS = []
for conf_list in CONFERENCES.values():
    ALL_TEAMS.extend(conf_list)

OPPONENT_POOL = ALL_TEAMS

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

# Added missing COACH_TRAITS to prevent crash
COACH_TRAITS = {
    "None": "No bonus",
    "Recruiter": "+10% Recruiting Bonus",
    "Tactician": "+3 Game Rating",
    "Cheap": "Half Salary Cost"
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
    elif amount >= 1000: return f"${amount/1000:.0f}K"
    return f"${int(amount)}"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Arch", "Shedeur"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name():
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach(role, tier):
    if tier == 1:
        base = 8; cost = random.randint(4000000, 8000000)
    elif tier == 2:
        base = 5; cost = random.randint(1500000, 3500000)
    else:
        base = 1; cost = random.randint(500000, 1200000)
    
    coach = {}
    coach["name"] = generate_coach_name()
    coach["role"] = role
    coach["off"] = min(10, base + random.randint(0, 2))
    coach["def"] = min(10, base + random.randint(0, 2))
    coach["recruit"] = min(10, base + random.randint(0, 2))
    coach["trait"] = random.choice(list(COACH_TRAITS.keys()))
    coach["salary"] = cost
    
    if coach["trait"] == "Cheap": coach["salary"] = int(coach["salary"] * 0.5)
    return coach

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
    star["trait"] = random.choice(list(TRAITS.keys()))
    return star

def calculate_ovr(roster, stars, staff):
    off_rating = sum(roster[p] for p in ["QB", "RB", "WR", "OL"]) / 4
    def_rating = sum(roster[p] for p in ["DL", "LB", "DB"]) / 3
    
    if "OC" in staff: off_rating += (staff["OC"]["off"] - 5) * 1.5
    if "DC" in staff: def_rating += (staff["DC"]["def"] - 5) * 1.5
    
    if "HC" in staff:
        off_rating += (staff["HC"]["off"] - 5) * 0.5
        def_rating += (staff["HC"]["def"] - 5) * 0.5
    
    star_boost = 0
    for s in stars:
        if s['trait'] == "🧠 General": star_boost += 2
    return int((off_rating * 0.5) + (def_rating * 0.5) + star_boost)

def generate_schedule(my_team_name, my_conf):
    conf_foes = [t for t in CONFERENCES[my_conf] if t != my_team_name]
    
    if len(conf_foes) >= 8:
        schedule = random.sample(conf_foes, 8)
    else:
        schedule = conf_foes
        
    needed = 12 - len(schedule)
    non_conf_pool = [t for t in ALL_TEAMS if t not in CONFERENCES[my_conf] and t != my_team_name]
    schedule += random.sample(non_conf_pool, needed)
    random.shuffle(schedule)
    return schedule

def play_game(my_rating, opponent_name, staff, stars, opponents_db):
    if "FCS" in opponent_name:
        opp_rating = random.randint(55, 65)
    else:
        opp_rating = opponents_db.get(opponent_name, 75)
        opp_rating += random.randint(-3, 3)
    
    rating_diff = my_rating - opp_rating
    
    execution_bonus = 0
    if "HC" in staff and staff["HC"]["trait"] == "Tactician": execution_bonus += 3
    if "HC" in staff: execution_bonus += (staff["HC"]["off"] + staff["HC"]["def"] - 10) * 0.2
    
    trait_impact = 0
    clutch = False
    
    for s in stars:
        if s['trait'] == "😤 Enforcer": trait_impact += 2 
        if s['trait'] == "❄️ Clutch" and abs(rating_diff) < 8: trait_impact += 5; clutch = True
    
    final_margin = rating_diff + execution_bonus + trait_impact + random.randint(-8, 8)
    
    my_score = 0; opp_score = 0; res = ""
    if final_margin > 0:
        res = "W"; my_score = int(28 + (final_margin / 1.5)); opp_score = int(my_score - final_margin)
    else:
        res = "L"; opp_score = int(30 + (abs(final_margin) / 1.5)); my_score = int(opp_score - abs(final_margin))
        
    result = {}
    result["result"] = res
    result["score"] = f"{max(0,my_score)}-{max(0,opp_score)}"
    result["ovr"] = opp_rating
    result["clutch"] = clutch
    result["my_power"] = int(my_rating + execution_bonus + trait_impact)
    return result

def process_recruiting(budget, allocations, staff, prestige, inflation):
    results = {"roster_updates": {}, "gems": [], "cost": 0, "booster_bonus": 0}
    total_cost = sum(allocations.values())
    if total_cost > budget: return None
    
    results["cost"] = total_cost
    
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
            rating_gain = buying_power * scout_eff * prestige_bonus
            
            gem_prob = (staff_rec * 0.5) / 100.0
            if amount > (250000 * inflation) and random.random() < gem_prob:
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
    st.session_state.hall_of_fame = []
    st.session_state.history = []
    st.session_state.record = {"w": 0, "l": 0}
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
    st.session_state.facilities = {"Marketing": 1, "Training": 1, "Stadium": 1}
    st.session_state.staff = {}
    st.session_state.rank = 0
    st.session_state.inflation = 1.0
    st.session_state.team_color = "#333333"
    st.session_state.team_name = "Team"
    st.session_state.team_conf = "SEC"
    st.session_state.current_headline = "Welcome to College Football!"
    st.session_state.home_region = "South" 
    st.session_state.talent_pool = {}
    st.session_state.last_season_summary = {} 
    st.session_state.postseason_result = {}
    st.session_state.opponents = {} 
    st.session_state.season_logs = []
    st.session_state.team_rating = 0
    st.session_state.candidates = {}

# --- 6. SCREEN FUNCTIONS ---

def run_setup():
    st.title("🏆 Gridiron CEO Draft 1.23")
    st.markdown("### Dynasty Mode")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("AD Name", "Coach Prime")
    with col2:
        diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    team = st.selectbox("Choose School", sorted(TEAMS_DB.keys()))
    d = TEAMS_DB[team]
    st.info(f"**{team}** ({d['conf']}) | Tier {d['tier']} | Budget: {format_cash(d['budget'])}")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = d.get('color', '#333333')
        st.session_state.team_conf = d.get('conf', 'SEC')
        st.session_state.home_region = d.get('region', 'South')
        
        mult = 1.0
        if diff == "Hard": mult = 0.75
        elif diff == "Easy": mult = 1.25
            
        st.session_state.budget = int(d['budget'] * mult)
        st.session_state.win_expect = d['expect']
        st.session_state.prestige = 95 - (d['tier'] * 12)
        
        st.session_state.roster = generate_initial_roster(d['tier'])
        st.session_state.stars = [generate_star_player("QB", d['tier'])]
        if d['tier'] < 4:
            st.session_state.stars.append(generate_star_player("LB", d['tier']))
        
        # Init Staff
        st.session_state.staff["HC"] = generate_coach("Head Coach", d['tier'])
        st.session_state.staff["OC"] = generate_coach("Off Coord", d['tier'])
        st.session_state.staff["DC"] = generate_coach("Def Coord", d['tier'])
        st.session_state.staff["Scout"] = generate_coach("Head Scout", d['tier'])
        
        st.session_state.team_rating = calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff)
        st.session_state.facilities['Training'] = d['facilities']
        
        for opp in ALL_TEAMS:
            rtg = 75
            if opp in CONFERENCES["SEC"] or opp in CONFERENCES["Big Ten"]: rtg = 85
            if opp in ["Georgia", "Ohio State", "Alabama", "Texas", "Oregon", "Michigan"]: rtg = 92
            if opp in CONFERENCES["G5 (Group of 5)"]: rtg = 68
            st.session_state.opponents[opp] = rtg + random.randint(-4, 4)
            
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    # FIRE CHECK
    if st.session_state.booster_morale < 25:
        st.session_state.game_state = "FIRED"
        st.rerun()

    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.markdown(f"<div class='news-ticker'>📰 {st.session_state.current_headline}</div>", unsafe_allow_html=True)
    st.markdown(f"""<div style='background-color: {st.session_state.team_color}; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'><h2 style='color: white; margin:0; text-align: center; text-shadow: 1px 1px 2px black;'>{st.session_state.team_name} ({st.session_state.year})</h2></div>""", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", format_cash(st.session_state.budget))
    c2.metric("Team Power", int(st.session_state.team_rating))
    c3.metric("Booster Morale", f"{st.session_state.booster_morale}%")
    c4.metric("Legacy Score", saban)
    st.progress(min(1.0, saban/600), f"Legacy Meter ({saban}/600)")

    tab1, tab2, tab3 = st.tabs(["⭐ Team", "👔 Staff", "⚔️ Season"])
    
    with tab1:
        st.subheader("Franchise Captains")
        for s in st.session_state.stars:
            st.markdown(f"""<div class="star-card"><b>{s['pos']} {s['name']}</b> ({s['year']}) <span style='float:right;color:green'>{s['rating']}</span><br><small>{TRAITS[s['trait']]['desc']}</small></div>""", unsafe_allow_html=True)
        st.write("Unit Strength")
        c_off, c_def = st.columns(2)
        with c_off:
            for p in ["QB", "RB", "WR", "OL"]:
                val = int(st.session_state.roster[p])
                st.progress(val/100, f"{p}: {val}")
        with c_def:
            for p in ["DL", "LB", "DB"]:
                val = int(st.session_state.roster[p])
                st.progress(val/100, f"{p}: {val}")
        
        st.divider()
        st.subheader("Facilities")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            if st.button("Marketing ($1M)"):
                if st.session_state.budget >= 1000000:
                    st.session_state.budget -= 1000000; st.session_state.facilities['Marketing'] += 1; st.toast("Revenue +"); st.rerun()
        with fc2:
            if st.button("Training ($3M)"):
                if st.session_state.budget >= 3000000:
                    st.session_state.budget -= 3000000; st.session_state.facilities['Training'] += 1; st.toast("Development +"); st.rerun()
        with fc3:
            if st.button("Stadium ($10M)"):
                if st.session_state.budget >= 10000000:
                    st.session_state.budget -= 10000000; st.session_state.facilities['Stadium'] += 1; st.session_state.prestige += 5; st.rerun()

    with tab2:
        st.subheader("Coaching Carousel")
        
        roles = ["HC", "OC", "DC", "Scout"]
        cols = st.columns(2)
        
        for i, role in enumerate(roles):
            with cols[i % 2]:
                if role in st.session_state.staff:
                    c = st.session_state.staff[role]
                    st.markdown(f"""
                    <div class='staff-card'>
                        <b>{role}: {c['name']}</b><br>
                        Off: {c['off']} | Def: {c['def']} | Rec: {c['recruit']}<br>
                        Trait: {c['trait']}
                    </div>
                    """, unsafe_allow_html=True)
                    buyout = int(c['salary'] * 0.5)
                    if st.button(f"Fire {role} (Buyout: {format_cash(buyout)})", key=f"fire_{role}"):
                        if st.session_state.budget >= buyout:
                            st.session_state.budget -= buyout
                            del st.session_state.staff[role]
                            st.rerun()
                        else:
                            st.error("Budget too low for buyout.")
                else:
                    st.warning(f"⚠️ {role} VACANT")
                    
                    if f"cand_{role}" not in st.session_state.candidates:
                        if st.button(f"🔍 Search Candidates ($500k)", key=f"search_{role}"):
                            if st.session_state.budget >= 500000:
                                st.session_state.budget -= 500000
                                cands = []
                                cands.append(generate_coach(role, 1))
                                cands.append(generate_coach(role, 2))
                                cands.append(generate_coach(role, 3))
                                st.session_state.candidates[f"cand_{role}"] = cands
                                st.rerun()
                            else: st.error("Need $500k to search.")
                    else:
                        cands = st.session_state.candidates[f"cand_{role}"]
                        for idx, cand in enumerate(cands):
                            cost = cand['salary']
                            st.markdown(f"**{cand['name']}** ({cand['trait']}) | Bonus: {format_cash(cost)}")
                            if st.button(f"Hire {cand['name']}", key=f"hire_{role}_{idx}"):
                                if st.session_state.budget >= cost:
                                    st.session_state.budget -= cost
                                    st.session_state.staff[role] = cand
                                    del st.session_state.candidates[f"cand_{role}"]
                                    st.rerun()
                                else: st.error("Cannot afford signing bonus.")
                        if st.button("Clear Search", key=f"clear_{role}"):
                            del st.session_state.candidates[f"cand_{role}"]
                            st.rerun()

    with tab3:
        st.info(f"Conference: {st.session_state.team_conf}")
        
        if len(st.session_state.staff) < 4:
            st.error("⚠️ You must fill all Staff vacancies before playing!")
        else:
            if st.button("▶️ SIMULATE SEASON", type="primary"):
                st.session_state.current_headline = random.choice(HEADLINES)
                run_season()

def run_season():
    wins = 0
    losses = 0
    logs = []
    schedule = generate_schedule(st.session_state.team_name, st.session_state.team_conf)
    
    bar = st.progress(0, "Kickoff...")
    st.session_state.team_rating = calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff)
    base_rating = st.session_state.team_rating
    
    for i, opp_name in enumerate(schedule):
        res = play_game(
            base_rating, 
            opp_name, 
            st.session_state.staff,
            st.session_state.stars, 
            st.session_state.opponents
        )
        
        if res['result'] == "W": wins += 1
        else: losses += 1
        
        if res['result'] == "W" and res['ovr'] > 90: st.session_state.booster_morale = min(100, st.session_state.booster_morale + 2)
        if res['result'] == "L" and res['ovr'] < 75: st.session_state.booster_morale = max(0, st.session_state.booster_morale - 5)
        
        entry = {}
        entry["Week"] = i+1
        entry["Opponent"] = opp_name
        entry["My Power"] = res['my_power']
        entry["Opp Power"] = res['ovr']
        entry["Result"] = res['result']
        entry["Score"] = res['score']
        logs.append(entry)
        bar.progress((i+1)/12, f"Week {i+1}: {res['result']}")

    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    
    score_val = (wins * 1000) + st.session_state.team_rating
    if wins == 12: score_val += 500
    
    if wins == 12: st.session_state.rank = random.randint(1, 4)
    elif wins == 11: st.session_state.rank = random.randint(5, 12)
    elif wins == 10: st.session_state.rank = random.randint(10, 20)
    elif wins == 9: st.session_state.rank = random.randint(18, 30)
    else: st.session_state.rank = 130 - (wins * 10)
    
    rank = st.session_state.rank
    outcome = {}
    outcome["type"] = "None"; outcome["name"] = "None"; outcome["result"] = "None"
    outcome["payout"] = 0; outcome["titles"] = 0; outcome["bowl_w"] = 0; outcome["bowl_l"] = 0
    
    if rank <= 16:
        outcome["type"] = "Playoff"; outcome["name"] = "CFP Playoff"; outcome["payout"] = 5000000
        if random.random() < 0.5:
            outcome["result"] = "Won National Title"; outcome["titles"] = 1; outcome["bowl_w"] = 1; outcome["payout"] += 10000000
        else:
            outcome["result"] = "Lost in Playoffs"; outcome["bowl_l"] = 1
    elif wins >= 6:
        outcome["type"] = "Bowl"; outcome["name"] = get_bowl_name(rank); outcome["payout"] = 2000000
        if random.random() < 0.6:
            outcome["result"] = "Won Bowl"; outcome["bowl_w"] = 1; outcome["payout"] += 2000000
        else:
            outcome["result"] = "Lost Bowl"; outcome["bowl_l"] = 1
            
    st.session_state.postseason_result = outcome
    st.session_state.game_state = "POSTSEASON"
    st.rerun()

def show_postseason():
    st.header(f"Season Finale: {st.session_state.record['w']}-{st.session_state.record['l']}")
    st.dataframe(pd.DataFrame(st.session_state.season_logs), use_container_width=True)
    
    outcome = st.session_state.postseason_result
    
    if outcome["type"] == "Playoff":
        if outcome["titles"] == 1:
            st.balloons(); st.success(f"🏆 NATIONAL CHAMPIONS! ({outcome['name']})")
            st.success(f"Boosters Donated {format_cash(outcome['payout'])}")
        else:
            st.warning(f"Eliminated in {outcome['name']}")
    elif outcome["type"] == "Bowl":
        if outcome["bowl_w"] == 1:
            st.success(f"🏆 Won the {outcome['name']}!")
            st.success(f"Boosters Donated {format_cash(outcome['payout'])}")
        else:
            st.error(f"Lost the {outcome['name']}")
    else:
        st.info("No Bowl Game Invited.")
    
    if st.button("View Year-End Summary"):
        st.session_state.budget += outcome["payout"]
        st.session_state.career_stats['w'] += st.session_state.record['w']
        st.session_state.career_stats['l'] += st.session_state.record['l']
        st.session_state.career_stats['titles'] += outcome["titles"]
        st.session_state.career_stats['bowl_w'] += outcome["bowl_w"]
        st.session_state.career_stats['bowl_l'] += outcome["bowl_l"]
        
        history_entry = {}
        history_entry["Year"] = st.session_state.year
        history_entry["Record"] = f"{st.session_state.record['w']}-{st.session_state.record['l']}"
        history_entry["Rank"] = f"#{st.session_state.rank}"
        history_entry["Result"] = outcome["result"]
        
        st.session_state.history.append(history_entry)
        st.session_state.last_season_summary = history_entry 
        st.session_state.game_state = "SUMMARY"
        st.rerun()

def show_year_summary():
    st.title(f"📊 {st.session_state.year} Year-End Review")
    if st.session_state.last_season_summary:
        entry = st.session_state.last_season_summary
        st.markdown(f"""<div class="summary-card"><h3>Season Performance</h3><p><b>Record:</b> {entry.get('Record')} | <b>Final Rank:</b> {entry.get('Rank')}</p><p><b>Postseason:</b> {entry.get('Result')}</p></div>""", unsafe_allow_html=True)
    
    st.subheader("Program History")
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist, use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Career Wins", st.session_state.career_stats['w'])
    c2.metric("Titles", st.session_state.career_stats['titles'])
    c3.metric("Bowl Wins", st.session_state.career_stats['bowl_w'])
    
    st.divider()
    col_next, col_retire = st.columns(2)
    with col_next:
        if st.button("➡️ Begin Offseason (Recruiting)", type="primary"):
            st.session_state.game_state = "RECRUITING"; st.rerun()
    with col_retire:
        if st.session_state.year >= 2030:
            if st.button("🌴 Retire & Hall of Fame"):
                st.session_state.game_state = "RETIREMENT"; st.rerun()

def show_recruiting():
    st.header("🦅 Recruiting War Room")
    if not st.session_state.talent_pool:
        st.session_state.talent_pool = {pos: random.choice(REGIONS) for pos in POSITIONS}
    
    home = st.session_state.home_region
    st.info(f"**Home Pipeline:** {home} Region | **Pipeline Bonus:** 1.5x Multiplier")
    cols = st.columns(4)
    for i, (pos, region) in enumerate(st.session_state.talent_pool.items()):
        match = "✅" if region == home else "❌"
        cols[i % 4].metric(f"{pos} Class", region, match)

    current_spend = 0
    for pos in POSITIONS:
        if f"recruit_{pos}" in st.session_state: current_spend += st.session_state[f"recruit_{pos}"]
    remaining = st.session_state.budget - current_spend
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Total Budget", format_cash(st.session_state.budget))
    c2.metric("Remaining", format_cash(remaining), delta_color="normal" if remaining >= 0 else "inverse")
    st.markdown("---")

    c1, c2 = st.columns(2)
    allocations = {}
    for i, pos in enumerate(POSITIONS):
        with c1 if i%2==0 else c2:
            allocations[pos] = st.number_input(f"{pos} Investment", 0, 10000000, 0, step=100000, key=f"recruit_{pos}")

    st.markdown("###")
    if st.button("✍️ Sign Class & Finalize", type="primary"):
        if current_spend > st.session_state.budget: 
            st.error("Over Budget!")
        else:
            result = process_recruiting(st.session_state.budget, allocations, st.session_state.staff, st.session_state.prestige, st.session_state.inflation)
            st.session_state.budget -= result['cost']
            
            for pos, gain in result['roster_updates'].items():
                st.session_state.roster[pos] = min(99, st.session_state.roster[pos] + gain)
            
            for pos in POSITIONS:
                loss = random.randint(3, 8)
                st.session_state.roster[pos] = max(40, st.session_state.roster[pos] - loss)
            
            for opp_team in st.session_state.opponents:
                decay = random.randint(4, 8)
                base_recruit = random.randint(2, 7)
                if opp_team in ["Michigan", "LSU", "Clemson", "Oklahoma", "Notre Dame"]: base_recruit += 2
                net_change = base_recruit - decay
                st.session_state.opponents[opp_team] = max(60, min(99, st.session_state.opponents[opp_team] + net_change))

            active_stars = []
            for s in st.session_state.stars:
                if s['year'] == "Sr":
                    st.toast(f"⭐ {s['name']} Graduated!")
                else:
                    if s['year'] == "Fr": s['year'] = "So"
                    elif s['year'] == "So": s['year'] = "Jr"
                    elif s['year'] == "Jr": s['year'] = "Sr"
                    active_stars.append(s)
            
            if result['gems']:
                st.balloons()
                active_stars.extend(result['gems'])
                for g in result['gems']:
                    st.markdown(f"<div class='gem-box'>💎 <b>GEM FOUND:</b> {g['name']} ({g['pos']})</div>", unsafe_allow_html=True)
            
            st.session_state.stars = active_stars

            if result['booster_bonus'] > 0:
                st.session_state.budget += result['booster_bonus']
                amt = result['booster_bonus']
                amt_str = format_cash(amt)
                msg = f"💰 Boosters donated {amt_str} for finding gems!"
                st.success(msg)
            
            st.success("Recruiting Complete! Seniors Graduated.")
            st.session_state.talent_pool = {} 
            st.session_state.year += 1
            
            st.session_state.team_rating = calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff)
            
            booster_mult = st.session_state.booster_morale / 100.0
            base_rev = 16000000 + (st.session_state.facilities['Marketing'] * 1000000)
            st.session_state.budget += int(base_rev * booster_mult)
            
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
        st.session_state.clear()
        st.rerun()

def show_fired():
    st.error("🚫 YOU HAVE BEEN FIRED!")
    st.markdown("""
        <div class="fired-card">
            <h2>Terminated</h2>
            <p>The Board of Regents has voted to terminate your contract effective immediately.</p>
            <p><b>Reason:</b> Booster Morale dropped below acceptable levels.</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.subheader("Final Stats")
    c1, c2 = st.columns(2)
    c1.metric("Years Coached", st.session_state.year - 2026)
    c2.metric("Total Wins", st.session_state.career_stats['w'])
    
    if st.button("Start New Career"):
        st.session_state.clear()
        st.rerun()

# --- 7. MAIN CONTROLLER ---
def main():
    if st.session_state.game_state == 'SETUP':
        run_setup()
    elif st.session_state.game_state == 'FIRED':
        show_fired()
    elif st.session_state.game_state == 'DASHBOARD':
        show_dashboard()
    elif st.session_state.game_state == 'POSTSEASON':
        show_postseason()
    elif st.session_state.game_state == 'SUMMARY':
        show_year_summary()
    elif st.session_state.game_state == 'RECRUITING':
        show_recruiting()
    elif st.session_state.game_state == 'RETIREMENT':
        show_retirement()

if __name__ == "__main__":
    main()
