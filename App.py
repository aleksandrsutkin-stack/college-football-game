import streamlit as st
import random
import time
import pandas as pd

# --- 1. PAGE CONFIG (Must be first) ---
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

# --- 3. GAME DATA ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
POS_WEIGHTS = {"QB": 0.25, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.10}
REGIONS = ["South", "North", "West", "Texas"]

# Teams defined line-by-line to prevent errors
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

# --- 4. HELPER FUNCTIONS (Flattened) ---

def format_cash(amount):
    if amount >= 1000000: return f"${amount/1000000:.1f}M"
    elif amount >= 1000: return f"${amount/1000:.0f}K"
    return f"${int(amount)}"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers"]
    return f"{random.choice(first)} {random.choice(last)}"

def calculate_saban_score(career_stats, prestige):
    return int((career_stats['w'] * 1) + (career_stats['bowl_w'] * 5) + (career_stats['titles'] * 50) + (prestige * 0.5))

def get_bowl_name(rank):
    if rank <= 12: return "CFP Playoff"
    elif rank <= 18: return random.choice(BOWL_MAPPING["Elite"])
    elif rank <= 25: return random.choice(BOWL_MAPPING["High"])
    elif rank <= 40: return random.choice(BOWL_MAPPING["Mid"])
    else: return random.choice(BOWL_MAPPING["Low"])

def generate_initial_roster(tier):
    base = 90 if tier == 1 else (82 if tier == 2 else (74 if tier == 3 else 64))
    roster = {}
    for p in POSITIONS:
        roster[p] = min(99, max(40, base + random.randint(0, 6)))
    return roster

def generate_star_player(position, tier):
    base = 92 if tier == 1 else (86 if tier == 2 else 75)
    star = {}
    star["id"] = random.randint(10000, 99999)
    star["name"] = generate_name()
    star["pos"] = position
    star["rating"] = min(99, base + random.randint(2, 6))
    star["year"] = random.choice(["Fr", "So", "Jr", "Sr"])
    star["trait"] = random.choice(list(TRAITS.keys()))
    return star

def calculate_ovr(roster, stars, OC, DC):
    off_rating = sum(roster[p] for p in ["QB", "RB", "WR", "OL"]) / 4
    def_rating = sum(roster[p] for p in ["DL", "LB", "DB"]) / 3
    off_rating += (OC - 5) * 1.5 
    def_rating += (DC - 5) * 1.5 
    star_boost = 0
    for s in stars:
        if s['trait'] == "🧠 General": star_boost += 2
    return int((off_rating * 0.5) + (def_rating * 0.5) + star_boost)

def generate_schedule(my_team_name):
    pool = [t for t in OPPONENT_POOL if t != my_team_name]
    return random.sample(pool, 12)

def play_game(my_rating, opponent_name, coach_lvl, stars):
    opp_rating = random.randint(55, 65) if "FCS" in opponent_name else random.randint(70, 96)
    
    rating_diff = my_rating - opp_rating
    execution_bonus = (coach_lvl - 5) * 0.5 
    
    trait_impact = 0
    clutch = False
    for s in stars:
        if s['trait'] == "😤 Enforcer": trait_impact += 2 
        if s['trait'] == "❄️ Clutch" and abs(rating_diff) < 8: trait_impact += 5; clutch = True
    
    final_margin = rating_diff + execution_bonus + trait_impact + random.randint(-8, 8)
    
    if final_margin > 0:
        res = "W"
        my_score = int(28 + (final_margin / 1.5))
        opp_score = int(my_score - final_margin)
    else:
        res = "L"
        opp_score = int(30 + (abs(final_margin) / 1.5))
        my_score = int(opp_score - abs(final_margin))
        
    return {
        "result": res,
        "score": f"{max(0,my_score)}-{max(0,opp_score)}",
        "ovr": opp_rating,
        "clutch": clutch,
        "my_power": int(my_rating + execution_bonus + trait_impact)
    }

def process_recruiting(budget, allocations, scout_lvl, prestige, inflation):
    results = {"roster_updates": {}, "gems": [], "cost": 0, "booster_bonus": 0}
    total_cost = sum(allocations.values())
    
    if total_cost > budget: return None
    
    results["cost"] = total_cost
    scout_eff = 1.0 + (scout_lvl / 10.0)
    prestige_bonus = 1.0 + (prestige / 200.0)
    
    for pos, amount in allocations.items():
        if amount > 0:
            buying_power = amount / (800000 * inflation)
            rating_gain = buying_power * scout_eff * prestige_bonus
            
            gem_prob = (scout_lvl * 4) / 100.0
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
    st.session_state.staff["Coach"] = 5
    st.session_state.staff["Scout"] = 5
    st.session_state.staff["OC"] = 5
    st.session_state.staff["DC"] = 5
    st.session_state.rank = 0
    st.session_state.inflation = 1.0
    st.session_state.team_color = "#333333"
    st.session_state.current_headline = "Welcome to College Football!"
    st.session_state.home_region = "South" 
    st.session_state.talent_pool = {}
    st.session_state.last_season_summary = {} 
    st.session_state.postseason_result = {}

# --- 6. SCREEN FUNCTIONS ---

def run_setup():
    st.title("🏆 Gridiron CEO V6.0")
    st.markdown("### Dynasty Mode")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("AD Name", "Coach Prime")
    with col2:
        diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    team = st.selectbox("Choose School", sorted(TEAMS_DB.keys()))
    d = TEAMS_DB[team]
    st.info(f"**{team}** ({d['region']}) | Tier {d['tier']} | Budget: {format_cash(d['budget'])}")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = d.get('color', '#333333')
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
        
        base = max(4, 9 - d['tier'])
        st.session_state.staff["Coach"] = base
        st.session_state.staff["OC"] = max(1, base - 1)
        st.session_state.staff["DC"] = max(1, base - 1)
        st.session_state.staff["Scout"] = base
        
        st.session_state.team_rating = calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff["OC"], st.session_state.staff["DC"])
        st.session_state.facilities['Training'] = d['facilities']
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.markdown(f"<div class='news-ticker'>📰 {st.session_state.current_headline}</div>", unsafe_allow_html=True)
    st.markdown(f"""<div style='background-color: {st.session_state.team_color}; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'><h2 style='color: white; margin:0; text-align: center; text-shadow: 1px 1px 2px black;'>{st.session_state.team_name} ({st.session_state.year})</h2></div>""", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", format_cash(st.session_state.budget))
    c2.metric("Team Power", int(st.session_state.team_rating))
    c3.metric("Booster Morale", f"{st.session_state.booster_morale}%")
    c4.metric("Legacy Score", saban)
    st.progress(min(1.0, saban/600), f"Legacy Meter ({saban}/600)")

    tab1, tab2, tab3 = st.tabs(["⭐ Team", "🏢 Staff & Ops", "⚔️ Season"])
    
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

    with tab2:
        st.subheader("Coaching Staff")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"<div class='staff-card'><b>Head Coach</b><br>Lvl {st.session_state.staff['Coach']}</div>", unsafe_allow_html=True)
            if st.button("Upgrade HC"): 
                cost = 3000000
                if st.session_state.budget >= cost and st.session_state.staff['Coach'] < 10:
                    st.session_state.budget -= cost
                    st.session_state.staff['Coach'] += 1
                    st.rerun()
        with sc2:
            st.markdown(f"<div class='staff-card'><b>Off Coord (OC)</b><br>Lvl {st.session_state.staff['OC']}</div>", unsafe_allow_html=True)
            if st.button("Hire Better OC"): 
                cost = 1500000
                if st.session_state.budget >= cost and st.session_state.staff['OC'] < 10:
                    st.session_state.budget -= cost
                    st.session_state.staff['OC'] += 1
                    st.rerun()
        with sc3:
            st.markdown(f"<div class='staff-card'><b>Def Coord (DC)</b><br>Lvl {st.session_state.staff['DC']}</div>", unsafe_allow_html=True)
            if st.button("Hire Better DC"): 
                cost = 1500000
                if st.session_state.budget >= cost and st.session_state.staff['DC'] < 10:
                    st.session_state.budget -= cost
                    st.session_state.staff['DC'] += 1
                    st.rerun()
        
        st.markdown("---")
        st.subheader("Scouting Department")
        scout_lvl = st.session_state.staff['Scout']
        st.markdown(f"<div class='staff-card'><b>Head Scout</b><br>Lvl {scout_lvl}<br><small>Recruiting Multiplier: {1.0 + (scout_lvl/10.0)}x</small></div>", unsafe_allow_html=True)
        if st.button(f"Upgrade Scout ($1.5M)"):
            cost = 1500000
            if st.session_state.budget >= cost and scout_lvl < 10:
                st.session_state.budget -= cost
                st.session_state.staff['Scout'] += 1
                st.toast("Scout Upgraded!")
                st.rerun()
        
        st.divider()
        st.subheader("Facilities")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            if st.button("Marketing ($1M)"):
                if st.session_state.budget >= 1000000:
                    st.session_state.budget -= 1000000
                    st.session_state.facilities['Marketing'] += 1
                    st.toast("Revenue +")
                    st.rerun()
        with fc2:
            if st.button("Training ($3M)"):
                if st.session_state.budget >= 3000000:
                    st.session_state.budget -= 3000000
                    st.session_state.facilities['Training'] += 1
                    st.toast("Development +")
                    st.rerun()
        with fc3:
            if st.button("Stadium ($10M)"):
                if st.session_state.budget >= 10000000:
                    st.session_state.budget -= 10000000
                    st.session_state.facilities['Stadium'] += 1
                    st.session_state.prestige += 5
                    st.rerun()

    with tab3:
        if st.button("▶️ SIMULATE SEASON", type="primary"):
            st.session_state.current_headline = random.choice(HEADLINES)
            run_season()

def run_season():
    wins = 0
    losses = 0
    logs = []
    schedule = generate_schedule(st.session_state.team_name)
    bar = st.progress(0, "Kickoff...")
    base_rating = st.session_state.team_rating
    
    for i, opp_name in enumerate(schedule):
        time.sleep(0.05)
        res = play_game(base_rating, opp_name, st.session_state.staff['Coach'], st.session_state.stars)
        if res['result'] == "W":
            wins += 1
        else:
            losses += 1
        
        if res['result'] == "W" and res['ovr'] > 90:
            st.session_state.booster_morale = min(100, st.session_state.booster_morale + 2)
        if res['result'] == "L" and res['ovr'] < 75:
            st.session_state.booster_morale = max(0, st.session_state.booster_morale - 5)
        
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
    score_val = (wins * 100) + st.session_state.team_rating
    st.session_state.rank = max(1, 130 - int(score_val/12))
    
    rank = st.session_state.rank
    wins = st.session_state.record['w']
    outcome = {}
    outcome["type"] = "None"
    outcome["name"] = "None"
    outcome["result"] = "None"
    outcome["payout"] = 0
    outcome["titles"] = 0
    outcome["bowl_w"] = 0
    outcome["bowl_l"] = 0
    
    if rank <= 12:
        outcome["type"] = "Playoff"
        outcome["name"] = "CFP Playoff"
        outcome["payout"] = 5000000
        if random.random() < 0.5:
            outcome["result"] = "Won National Title"
            outcome["titles"] = 1
            outcome["bowl_w"] = 1
            outcome["payout"] += 10000000
        else:
            outcome["result"] = "Lost in Playoffs"
            outcome["bowl_l"] = 1
    elif wins >= 6:
        outcome["type"] = "Bowl"
        outcome["name"] = get_bowl_name(rank)
        outcome["payout"] = 2000000
        if random.random() < 0.6:
            outcome["result"] = "Won Bowl"
            outcome["bowl_w"] = 1
            outcome["payout"] += 2000000
        else:
            outcome["result"] = "Lost Bowl"
            outcome["bowl_l"] = 1
            
    st.session_state.postseason_result = outcome
    st.session_state.game_state = "POSTSEASON"
    st.rerun()

def show_postseason():
    st.header(f"Season Finale: {st.session_state.record['w']}-{st.session_state.record['l']}")
    st.dataframe(pd.DataFrame(st.session_state.season_logs), use_container_width=True)
    
    outcome = st.session_state.postseason_result
    
    if outcome["type"] == "Playoff":
        if outcome["titles"] == 1:
            st.balloons()
            st.success(f"🏆 NATIONAL CHAMPIONS! ({outcome['name']})")
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
        
        if st.session_state.record['w'] >= 10:
            if random.random() < 0.3:
                st.session_state.staff['OC'] = max(1, st.session_state.staff['OC'] - 3)
            if random.random() < 0.3:
                st.session_state.staff['DC'] = max(1, st.session_state.staff['DC'] - 3)
            
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
            st.session_state.game_state = "RECRUITING"
            st.rerun()
    with col_retire:
        if st.session_state.year >= 2030:
            if st.button("🌴 Retire & Hall of Fame"):
                st.session_state.game_state = "RETIREMENT"
                st.rerun()

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
        if f"recruit_{pos}" in st.session_state:
            current_spend += st.session_state[f"recruit_{pos}"]
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
            result = process_recruiting(st.session_state.budget, allocations, st.session_state.staff['Scout'], st.session_state.prestige, st.session_state.inflation)
            st.session_state.budget -= result['cost']
            
            for pos, gain in result['roster_updates'].items():
                st.session_state.roster[pos] = min(99, st.session_state.roster[pos] + gain)
            
            if result['gems']:
                st.balloons()
                st.session_state.stars.extend(result['gems'])
                for g in result['gems']:
                    st.markdown(f"<div class='gem-box'>💎 <b>GEM FOUND:</b> {g['name']} ({g['pos']})</div>", unsafe_allow_html=True)
            
            if result['booster_bonus'] > 0:
                st.session_state.budget += result['booster_bonus']
                st.success(f"💰 Boosters donated {format_cash(result['booster_bonus
