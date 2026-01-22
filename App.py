import streamlit as st
import random
import time
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gridiron CEO", page_icon="🏈", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    .news-ticker { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px; border: 1px solid #ffeeba; }
    .star-card { background: white; border: 1px solid #ddd; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 8px; }
    .staff-card { background: #f0f4c3; border: 1px solid #dce775; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 5px; }
    .booster-alert { background: #e8f5e9; border-left: 5px solid #4caf50; padding: 10px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

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
    "🚀 Speedster": {"desc": "High Variance Scoring", "effect": 0},
    "🧠 General": {"desc": "Boosts Offense +2", "effect": 3},
    "😤 Enforcer": {"desc": "Lowers Opponent Score", "effect": 3},
}

HEADLINES = [
    "Rumor: Offensive Coordinator considering NFL jobs.",
    "Boosters reportedly 'furious' after rival loss.",
    "Analyst: 'This team recruits the South better than anyone.'",
    "Breaking: 5-Star QB spotted at campus steakhouse.",
    "Stadium renovations approved by the board.",
    "Polls: Voters skeptical of strength of schedule."
]

# ==============================================================================
# MODULE: UTILS & ENGINES
# ==============================================================================
class Utils:
    @staticmethod
    def format_cash(amount):
        if amount >= 1_000_000: return f"${int(amount/1_000_000)}M"
        elif amount >= 1_000: return f"${int(amount/1_000)}K"
        return f"${int(amount)}"

    @staticmethod
    def generate_name():
        first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank"]
        last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers"]
        return f"{random.choice(first)} {random.choice(last)}"

    @staticmethod
    def calculate_saban_score(career_stats, prestige):
        return int((career_stats['w'] * 1) + (career_stats['bowl_w'] * 5) + (career_stats['titles'] * 50) + (prestige * 0.5))

class TeamEngine:
    @staticmethod
    def generate_initial_roster(tier):
        base = 90 if tier == 1 else (82 if tier == 2 else (74 if tier == 3 else 64))
        return {p: min(99, max(40, base + random.randint(0, 6))) for p in POSITIONS}

    @staticmethod
    def generate_star_player(position, tier):
        base = 92 if tier == 1 else (86 if tier == 2 else 75)
        return {
            "id": random.randint(10000, 99999),
            "name": Utils.generate_name(), "pos": position,
            "rating": min(99, base + random.randint(2, 6)),
            "year": random.choice(["Fr", "So", "Jr", "Sr"]),
            "trait": random.choice(list(TRAITS.keys()))
        }

    @staticmethod
    def calculate_ovr(roster, stars, OC, DC):
        # Base Unit Ratings
        off_weight = 0.5; def_weight = 0.5
        off_rating = sum(roster[p] for p in ["QB", "RB", "WR", "OL"]) / 4
        def_rating = sum(roster[p] for p in ["DL", "LB", "DB"]) / 3
        
        # Coordinator Impact
        off_rating += (OC - 5) * 1.5 
        def_rating += (DC - 5) * 1.5 
        
        # Star Impact
        star_boost = 0
        for s in stars:
            if s['trait'] == "🧠 General": star_boost += 2
            
        return int((off_rating * off_weight) + (def_rating * def_weight) + star_boost)

class SimEngine:
    @staticmethod
    def generate_schedule(my_team_name):
        return random.sample([t for t in OPPONENT_POOL if t != my_team_name], 12)

    @staticmethod
    def play_game(my_rating, opponent_name, coach_lvl, stars):
        # Determine Opponent Strength
        if "FCS" in opponent_name: opp_rating = random.randint(55, 65)
        else: opp_rating = random.randint(70, 96) # Variance for D1
        
        rating_diff = my_rating - opp_rating
        execution_bonus = (coach_lvl - 5) * 0.5 
        
        # Traits
        trait_impact = 0; clutch = False
        for s in stars:
            if s['trait'] == "😤 Enforcer": trait_impact += 2 
            if s['trait'] == "❄️ Clutch" and abs(rating_diff) < 8: trait_impact += 5; clutch = True
        
        final_margin = rating_diff + execution_bonus + trait_impact + random.randint(-8, 8)
        
        if final_margin > 0:
            res = "W"; my_score = int(28 + (final_margin/1.5)); opp_score = int(my_score - final_margin)
        else:
            res = "L"; opp_score = int(30 + (abs(final_margin)/1.5)); my_score = int(opp_score - abs(final_margin))
            
        return {"result": res, "score": f"{max(0,my_score)}-{max(0,opp_score)}", "ovr": opp_rating, "clutch": clutch}

# ==============================================================================
# MAIN APP CONTROLLER
# ==============================================================================

if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP'
    st.session_state.year = 2026
    st.session_state.budget = 0
    st.session_state.prestige = 50
    st.session_state.job_security = 100
    st.session_state.booster_morale = 80 # New: Booster Happiness (0-100)
    st.session_state.roster = {}; st.session_state.stars = []; st.session_state.hall_of_fame = []
    st.session_state.record = {"w": 0, "l": 0}
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
    st.session_state.facilities = {"Marketing": 1, "Training": 1, "Stadium": 1}
    # NEW: Coordinators added to staff
    st.session_state.staff = {"Coach": 5, "Scout": 5, "OC": 5, "DC": 5, 
                              "Coach_Sal": 3000000, "Scout_Sal": 500000, "OC_Sal": 1000000, "DC_Sal": 1000000}
    st.session_state.rank = 0
    st.session_state.inflation = 1.0
    st.session_state.team_color = "#333333"
    st.session_state.current_headline = random.choice(HEADLINES)
    # NEW: Recruiting Pipeline
    st.session_state.home_region = "South" 
    st.session_state.talent_pool = {} # Will store region for each pos

# --- SETUP ---
def run_setup():
    st.title("🏆 Gridiron CEO V3.0")
    st.markdown("### Dynasty Mode")
    
    col1, col2 = st.columns(2)
    with col1: name = st.text_input("AD Name", "Coach Prime")
    with col2: diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    team = st.selectbox("Choose School", sorted(TEAMS_DB.keys()))
    d = TEAMS_DB[team]
    st.info(f"**{team}** ({d['region']}) | Tier {d['tier']} | Budget: {Utils.format_cash(d['budget'])}")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = d.get('color', '#333333')
        st.session_state.home_region = d.get('region', 'South')
        
        mult = 0.75 if diff == "Hard" else (1.25 if diff == "Easy" else 1.0)
        st.session_state.budget = int(d['budget'] * mult)
        st.session_state.win_expect = d['expect']
        st.session_state.prestige = 95 - (d['tier'] * 12)
        st.session_state.start_prestige = st.session_state.prestige
        st.session_state.start_rating = 0 # Will set below
        
        st.session_state.roster = TeamEngine.generate_initial_roster(d['tier'])
        st.session_state.stars = [TeamEngine.generate_star_player("QB", d['tier'])]
        if d['tier'] < 4: st.session_state.stars.append(TeamEngine.generate_star_player("LB", d['tier']))
        
        base = max(4, 9 - d['tier'])
        st.session_state.staff["Coach"] = base
        st.session_state.staff["OC"] = max(1, base - 1)
        st.session_state.staff["DC"] = max(1, base - 1)
        st.session_state.staff["Scout"] = base
        
        st.session_state.team_rating = TeamEngine.calculate_ovr(st.session_state.roster, st.session_state.stars, st.session_state.staff["OC"], st.session_state.staff["DC"])
        st.session_state.start_rating = st.session_state.team_rating
        st.session_state.facilities['Training'] = d['facilities']
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

# --- DASHBOARD ---
def show_dashboard():
    saban = Utils.calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.markdown(f"<div class='news-ticker'>📰 {st.session_state.current_headline}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background-color: {st.session_state.team_color}; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h2 style='color: white; margin:0; text-align: center; text-shadow: 1px 1px 2px black;'>{st.session_state.team_name} ({st.session_state.year})</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # BOOSTER ALERT
    morale = st.session_state.booster_morale
    morale_icon = "😡" if morale < 40 else ("😐" if morale < 75 else "🤑")
    if morale > 85: st.success("💰 Boosters are thrilled! NIL War Chest Unlocked.")
    elif morale < 40: st.error("📉 Boosters are angry. Budget constrained.")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", Utils.format_cash(st.session_state.budget))
    c2.metric("OVR Rating", int(st.session_state.team_rating))
    c3.metric("Booster Morale", f"{morale}%", morale_icon)
    c4.metric("Career Score", saban)
    st.progress(min(1.0, saban/600), f"Legacy Meter ({saban}/600)")

    tab1, tab2, tab3 = st.tabs(["⭐ Team", "🏢 Staff & Ops", "⚔️ Season"])
    
    with tab1:
        st.subheader("Franchise Captains")
        for s in st.session_state.stars:
            st.markdown(f"""<div class="star-card"><b>{s['pos']} {s['name']}</b> ({s['year']}) <span style='float:right;color:green'>{s['rating']}</span><br><small>{TRAITS[s['trait']]['desc']}</small></div>""", unsafe_allow_html=True)
        st.divider()
        st.write("Unit Strength")
        c_off, c_def = st.columns(2)
        with c_off:
            for p in ["QB", "RB", "WR", "OL"]: st.progress(st.session_state.roster[p]/100, f"{p}: {st.session_state.roster[p]}")
        with c_def:
            for p in ["DL", "LB", "DB"]: st.progress(st.session_state.roster[p]/100, f"{p}: {st.session_state.roster[p]}")

    with tab2:
        st.subheader("Coaching Staff (Carousel)")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"<div class='staff-card'><b>Head Coach</b><br>Lvl {st.session_state.staff['Coach']}</div>", unsafe_allow_html=True)
            if st.button("Upgrade HC"): 
                cost = 3000000
                if st.session_state.budget >= cost and st.session_state.staff['Coach'] < 10:
                    st.session_state.budget -= cost; st.session_state.staff['Coach'] += 1; st.rerun()
        with sc2:
            st.markdown(f"<div class='staff-card'><b>Off Coord (OC)</b><br>Lvl {st.session_state.staff['OC']}</div>", unsafe_allow_html=True)
            if st.button("Hire Better OC"): 
                cost = 1500000
                if st.session_state.budget >= cost and st.session_state.staff['OC'] < 10:
                    st.session_state.budget -= cost; st.session_state.staff['OC'] += 1; st.rerun()
        with sc3:
            st.markdown(f"<div class='staff-card'><b>Def Coord (DC)</b><br>Lvl {st.session_state.staff['DC']}</div>", unsafe_allow_html=True)
            if st.button("Hire Better DC"): 
                cost = 1500000
                if st.session_state.budget >= cost and st.session_state.staff['DC'] < 10:
                    st.session_state.budget -= cost; st.session_state.staff['DC'] += 1; st.rerun()
        
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

    with tab3:
        if st.button("▶️ SIMULATE SEASON", type="primary"):
            st.session_state.current_headline = random.choice(HEADLINES)
            run_season()

# --- SEASON SIM ---
def run_season():
    wins = 0; losses = 0; logs = []
    schedule = SimEngine.generate_schedule(st.session_state.team_name)
    bar = st.progress(0, "Kickoff...")
    
    # Calculate Power including Coordinators
    base_rating = st.session_state.team_rating
    
    for i, opp_name in enumerate(schedule):
        time.sleep(0.05)
        res = SimEngine.play_game(base_rating, opp_name, st.session_state.staff['Coach'], st.session_state.stars)
        
        if res['result'] == "W": wins += 1
        else: losses += 1
        
        # Booster Reaction (Micro)
        if res['result'] == "W" and res['ovr'] > 90: st.session_state.booster_morale = min(100, st.session_state.booster_morale + 2)
        if res['result'] == "L" and res['ovr'] < 75: st.session_state.booster_morale = max(0, st.session_state.booster_morale - 5)
            
        logs.append({"Week": i+1, "Opponent": opp_name, "Ovr": res['ovr'], "Result": res['result'], "Score": res['score']})
        bar.progress((i+1)/12, f"Week {i+1}: {res['result']}")

    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    
    # Calculate Rank
    rank_score = (wins * 100) + st.session_state.team_rating
    st.session_state.rank = max(1, 130 - int(rank_score/12))
    
    st.session_state.game_state = "POSTSEASON"
    st.rerun()

# --- POSTSEASON ---
def show_postseason():
    st.header(f"Season Finale: {st.session_state.record['w']}-{st.session_state.record['l']}")
    st.dataframe(pd.DataFrame(st.session_state.season_logs), use_container_width=True)
    
    bowl_payout = 0
    rank = st.session_state.rank
    
    if rank <= 12:
        st.success("🔥 PLAYOFF BOUND!"); bowl_payout = 5000000
        if random.random() < 0.5: st.balloons(); st.success("🏆 CHAMPIONS!"); st.session_state.career_stats['titles'] += 1; st.session_state.prestige += 5; st.session_state.booster_morale = 100
        else: st.warning("Lost in Playoffs")
    elif st.session_state.record['w'] >= 6:
        st.info("🎳 Bowl Game Invited"); bowl_payout = 2000000
        if random.random() < 0.6: st.success("Won Bowl!"); st.session_state.career_stats['bowl_w'] += 1; st.session_state.prestige += 2
        else: st.error("Lost Bowl")
    
    if st.button("Offseason"):
        st.session_state.budget += bowl_payout
        st.session_state.career_stats['w'] += st.session_state.record['w']
        st.session_state.career_stats['l'] += st.session_state.record['l']
        
        # COACH POACHING LOGIC
        if st.session_state.record['w'] >= 10:
            if random.random() < 0.3:
                st.warning("⚠️ Your Offensive Coordinator was hired as Head Coach elsewhere!")
                st.session_state.staff['OC'] = max(1, st.session_state.staff['OC'] - 3) # Replaced by worse coach
            if random.random() < 0.3:
                st.warning("⚠️ Your Defensive Coordinator left for the NFL!")
                st.session_state.staff['DC'] = max(1, st.session_state.staff['DC'] - 3)
        
        st.session_state.game_state = "RECRUITING"
        st.rerun()

# --- RECRUITING (PIPELINE EDITION) ---
def show_recruiting():
    st.header("🦅 Recruiting War Room")
    
    # 1. Pipeline Generation
    if not st.session_state.talent_pool:
        st.session_state.talent_pool = {pos: random.choice(REGIONS) for pos in POSITIONS}
    
    # Show Map
    home = st.session_state.home_region
    st.info(f"**Home Pipeline:** {home} Region | **Pipeline Bonus:** 1.5x Multiplier")
    
    cols = st.columns(4)
    for i, (pos, region) in enumerate(st.session_state.talent_pool.items()):
        match = "✅ Pipeline" if region == home else "❌ National"
        cols[i % 4].metric(f"{pos} Class", region, match)

    with st.form("recruit"):
        allocations = {}
        c1, c2 = st.columns(2)
        for i, pos in enumerate(POSITIONS):
            with c1 if i%2==0 else c2:
                allocations[pos] = st.number_input(f"{pos} Budget", 0, 10000000, 0, step=100000, key=pos)
        if st.form_submit_button("Sign Class"):
            cost = sum(allocations.values())
            if cost > st.session_state.budget: st.error("Over Budget")
            else:
                st.session_state.budget -= cost
                gems = []
                scout_eff = 1.0 + (st.session_state.staff['Scout']/10)
                
                for pos, amt in allocations.items():
                    if amt > 0:
                        # PIPELINE LOGIC
                        region_mult = 1.5 if st.session_state.talent_pool[pos] == home else 0.8
                        gain = (amt / 800000) * scout_eff * region_mult
                        
                        # Gem Logic
                        if amt > 500000 and random.random() < 0.2:
                            st.session_state.stars.append(TeamEngine.generate_star_player(pos, 1))
                            gems.append(f"💎 {pos} Gem Found!")
                            gain += 5
                        
                        st.session_state.roster[pos] = min(99, st.session_state.roster[pos] + gain)
                
                if gems: st.success(" ".join(gems))
                
                # Cleanup & Advance
                st.session_state.talent_pool = {} # Reset pool for next year
                st.session_state.year += 1
                
                # Revenue Reset based on Facilities & Booster Morale
                booster_mult = st.session_state.booster_morale / 100.0
                base_rev = 16000000 + (st.session_state.facilities['Marketing'] * 1000000)
                st.session_state.budget += int(base_rev * booster_mult)
                
                # Retire check
                if st.session_state.year >= 2031: st.session_state.game_state = "RETIREMENT"
                else: st.session_state.game_state = "DASHBOARD"
                st.rerun()

def show_retirement():
    st.balloons()
    st.title("Hall of Fame")
    st.write(f"Final Score: {Utils.calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)}")
    if st.button("New Game"): st.session_state.clear(); st.rerun()

# --- ROUTER ---
if st.session_state.game_state == 'SETUP': run_setup()
elif st.session_state.game_state == 'DASHBOARD': show_dashboard()
elif st.session_state.game_state == 'POSTSEASON': show_postseason()
elif st.session_state.game_state == 'RECRUITING': show_recruiting()
elif st.session_state.game_state == 'RETIREMENT': show_retirement()
