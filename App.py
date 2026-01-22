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
    .gem-box {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #2196f3;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIG ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
POS_WEIGHTS = {"QB": 0.20, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.15}

TEAMS_DB = {
    "Georgia": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 8, "facilities": 10},
    "Ohio State": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10},
    "Texas": {"tier": 1, "budget": 25_000_000, "expect": 10, "coach": 9, "facilities": 10},
    "Alabama": {"tier": 1, "budget": 22_000_000, "expect": 10, "coach": 9, "facilities": 9},
    "Florida St": {"tier": 2, "budget": 15_000_000, "expect": 9, "coach": 7, "facilities": 8},
    "Penn State": {"tier": 2, "budget": 16_000_000, "expect": 9, "coach": 7, "facilities": 8},
    "Boise State": {"tier": 3, "budget": 7_000_000, "expect": 9, "coach": 6, "facilities": 5},
    "Vanderbilt": {"tier": 3, "budget": 8_000_000, "expect": 5, "coach": 5, "facilities": 4},
}

# --- HELPERS ---
def generate_roster(tier):
    base = 92 if tier == 1 else (84 if tier == 2 else 74)
    return {p: min(99, max(50, base + random.randint(-8, 8))) for p in POSITIONS}

def calculate_ovr(roster):
    return round(sum(roster[p] * w for p, w in POS_WEIGHTS.items()), 1)

def calculate_saban_score():
    # Nick Saban Score Algorithm
    # 1 Win = 1 Pt | Bowl Win = 5 Pts | Natty = 50 Pts | Prestige = 1 Pt
    w = st.session_state.career_stats['w']
    bw = st.session_state.career_stats['bowl_w']
    natty = st.session_state.career_stats['titles']
    prest = st.session_state.prestige
    
    raw_score = (w * 1) + (bw * 5) + (natty * 50) + (prest * 0.5)
    # Scale: Saban approx 500-600 pts
    return int(raw_score)

# --- STATE INIT ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP'
    st.session_state.year = 2026
    st.session_state.budget = 0
    st.session_state.prestige = 75
    st.session_state.job_security = 100
    st.session_state.roster = {}
    st.session_state.record = {"w": 0, "l": 0}
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
    st.session_state.facilities = {"Marketing": 1, "Training": 1}
    st.session_state.staff = {"Coach": 5, "Scout": 5, "Coach_Sal": 3000000, "Scout_Sal": 500000}
    st.session_state.latest_result_text = "No games played"
    st.session_state.rank = 0

# --- SCREENS ---

def run_setup():
    st.title("🏆 Gridiron CEO V2")
    st.write("Take the reins as Athletic Director.")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", "AD Smith")
    with col2:
        diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    team = st.selectbox("Select Team", list(TEAMS_DB.keys()))
    d = TEAMS_DB[team]
    st.info(f"**{team}** | Tier {d['tier']} | Budget: ${d['budget']:,}")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.budget = int(d['budget'] * (0.75 if diff == "Hard" else 1.0))
        st.session_state.win_expect = d['expect']
        st.session_state.roster = generate_roster(d['tier'])
        st.session_state.team_rating = calculate_ovr(st.session_state.roster)
        
        # Init Staff
        base = 8 if d['tier'] == 1 else 6
        st.session_state.staff = {
            "Coach": base, "Scout": base, 
            "Coach_Sal": base * 600000, "Scout_Sal": base * 200000
        }
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    # --- HEADER ---
    saban = calculate_saban_score()
    st.markdown(f"### {st.session_state.team_name} ({st.session_state.year})")
    
    # METRICS ROW
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", f"${st.session_state.budget/1000000:.1f}M")
    c2.metric("OVR Rating", st.session_state.team_rating)
    c3.metric("Prestige", st.session_state.prestige)
    c4.metric("Career Score", saban, help="Nick Saban = ~600")

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📋 Roster", "🏢 Staff & Facilities", "⚔️ Season"])
    
    with tab1:
        st.write(" **Offense**")
        oc = st.columns(4)
        for i, p in enumerate(["QB", "RB", "WR", "OL"]):
            oc[i].metric(p, st.session_state.roster[p])
        st.write(" **Defense**")
        dc = st.columns(3)
        for i, p in enumerate(["DL", "LB", "DB"]):
            dc[i].metric(p, st.session_state.roster[p])

    with tab2:
        # STAFF UPGRADE LOGIC FIX
        st.subheader("Staff Management")
        sc1, sc2 = st.columns(2)
        
        # COACH
        with sc1:
            st.write(f"**Head Coach** (Lvl {st.session_state.staff['Coach']})")
            if st.session_state.staff['Coach'] < 10:
                cost = 4000000
                if st.button(f"Upgrade Coach (${cost//1000000}M)", key="up_coach"):
                    if st.session_state.budget >= cost:
                        st.session_state.budget -= cost
                        st.session_state.staff['Coach'] += 1
                        st.session_state.staff['Coach_Sal'] += 500000
                        st.success("Coach Upgraded!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Insufficient Funds")
            else:
                st.write("Max Level Reached")

        # SCOUT
        with sc2:
            st.write(f"**Head Scout** (Lvl {st.session_state.staff['Scout']})")
            if st.session_state.staff['Scout'] < 10:
                cost = 2000000
                if st.button(f"Upgrade Scout (${cost//1000000}M)", key="up_scout"):
                    if st.session_state.budget >= cost:
                        st.session_state.budget -= cost
                        st.session_state.staff['Scout'] += 1
                        st.session_state.staff['Scout_Sal'] += 200000
                        st.success("Scout Upgraded!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Insufficient Funds")
            else:
                st.write("Max Level Reached")
                
        st.divider()
        st.subheader("Facilities")
        fc1, fc2 = st.columns(2)
        with fc1:
            m_cost = 1000000
            if st.button(f"Marketing Campaign (${m_cost//1000000}M)"):
                if st.session_state.budget >= m_cost:
                    st.session_state.budget -= m_cost
                    st.session_state.facilities['Marketing'] += 1
                    st.toast("Marketing Boosted! +Revenue next year.")
                    st.rerun()
        with fc2:
            t_cost = 3000000
            if st.button(f"Upgrade Training Center (${t_cost//1000000}M)"):
                if st.session_state.budget >= t_cost:
                    st.session_state.budget -= t_cost
                    st.session_state.facilities['Training'] += 1
                    st.toast("Facilities Upgraded! +Recruiting Boost.")
                    st.rerun()

    with tab3:
        st.markdown("### ready to play?")
        if st.button("▶️ SIMULATE REGULAR SEASON", type="primary"):
            run_season()

def run_season():
    # SIMULATION
    wins = 0; losses = 0
    logs = []
    
    bar = st.progress(0, "Kickoff...")
    
    power = st.session_state.team_rating + st.session_state.staff['Coach'] + (st.session_state.facilities['Training']*0.5)
    
    for i in range(12):
        time.sleep(0.05)
        opp_rtg = random.randint(65, 95)
        opp_name = f"Opponent {i+1}"
        
        diff = (power + random.randint(-10, 10)) - opp_rtg
        if diff > 0:
            wins += 1
            res = "W"
            sc = f"{random.randint(24,45)}-{max(0, random.randint(24,45)-int(diff))}"
        else:
            losses += 1
            res = "L"
            sc = f"{min(20, 24-int(abs(diff)))}-{random.randint(24,45)}"
            
        logs.append({"Week": i+1, "Opponent": opp_name, "Ovr": opp_rtg, "Result": res, "Score": sc})
        bar.progress((i+1)/12, f"Week {i+1}: {res}")
        
    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    
    # Calculate Rank based on Wins + Rating
    rank_score = (wins * 100) + st.session_state.team_rating
    # Basic ranking simulation
    st.session_state.rank = max(1, 130 - int(rank_score/15))
    
    st.session_state.game_state = "POSTSEASON"
    st.rerun()

def show_postseason():
    st.header(f"Season Finale: {st.session_state.record['w']}-{st.session_state.record['l']}")
    
    # Game Logs
    df = pd.DataFrame(st.session_state.season_logs)
    st.dataframe(df, use_container_width=True)
    
    # BOWL LOGIC
    bowl_result = "No Bowl"
    bowl_payout = 0
    rank = st.session_state.rank
    
    if rank <= 12:
        st.success("🔥 COLLEGE FOOTBALL PLAYOFF!")
        st.write("Your team made the 12-team playoff.")
        bowl_payout = 5000000
        # Sim Playoff
        if random.random() < 0.5:
            st.balloons()
            st.success("🏆 NATIONAL CHAMPIONS!!")
            bowl_result = "Won National Title"
            st.session_state.career_stats['titles'] += 1
            st.session_state.career_stats['bowl_w'] += 1
            bowl_payout += 10000000
        else:
            st.warning("Lost in Playoffs.")
            bowl_result = "Lost Playoff Game"
            st.session_state.career_stats['bowl_l'] += 1
            
    elif st.session_state.record['w'] >= 6:
        bowl_name = "Citrus Bowl" if rank < 25 else "Myrtle Beach Bowl"
        st.info(f"🎳 Invite: {bowl_name}")
        bowl_payout = 2000000
        if random.random() < 0.6:
            st.success("Won Bowl Game!")
            bowl_result = "Won Bowl"
            st.session_state.career_stats['bowl_w'] += 1
        else:
            st.error("Lost Bowl Game.")
            bowl_result = "Lost Bowl"
            st.session_state.career_stats['bowl_l'] += 1
    
    st.session_state.latest_result_text = bowl_result
    st.session_state.bowl_payout = bowl_payout
    
    if st.button("Proceed to Season Recap"):
        st.session_state.budget += bowl_payout
        st.session_state.career_stats['w'] += st.session_state.record['w']
        st.session_state.career_stats['l'] += st.session_state.record['l']
        
        # Update Prestige based on result
        if st.session_state.record['w'] >= 10: st.session_state.prestige += 3
        elif st.session_state.record['w'] < 6: st.session_state.prestige -= 3
        
        st.session_state.game_state = "SUMMARY"
        st.rerun()

def show_year_summary():
    st.title(f"📊 {st.session_state.year} Year-End Recap")
    
    # 1. Season Stats
    st.subheader("Season Performance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Final Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")
    c2.metric("Nat'l Rank", f"#{st.session_state.rank}")
    c3.metric("Postseason", st.session_state.latest_result_text)
    c4.metric("Prestige", st.session_state.prestige, delta_color="normal")
    
    st.divider()
    
    # 2. Career Stats
    st.subheader(f"📜 {st.session_state.ad_name} Career File")
    cs = st.session_state.career_stats
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Lifetime Record", f"{cs['w']}-{cs['l']}")
    cc2.metric("Bowl Record", f"{cs['bowl_w']}-{cs['bowl_l']}")
    cc3.metric("National Titles", cs['titles'])
    
    # Saban Score
    score = calculate_saban_score()
    st.progress(min(1.0, score/600), f"Saban Score: {score}/600")
    
    st.divider()
    
    if st.button("Start Offseason (Recruiting)"):
        # Pay Staff
        payroll = st.session_state.staff['Coach_Sal'] + st.session_state.staff['Scout_Sal']
        st.session_state.budget -= payroll
        # Add Revenue
        rev = 15000000 + (st.session_state.facilities['Marketing'] * 1000000)
        st.session_state.budget += rev
        
        st.session_state.game_state = "RECRUITING"
        st.rerun()

def show_recruiting():
    st.header("🦅 Recruiting War Room")
    st.info("Allocate funds to position groups. Your Scout and Prestige affect results!")
    
    st.write(f"**Available Budget:** ${st.session_state.budget:,}")
    
    with st.form("recruit_form"):
        allocations = {}
        cols = st.columns(2)
        for i, pos in enumerate(POSITIONS):
            with cols[i%2]:
                curr = int(st.session_state.roster[pos])
                allocations[pos] = st.number_input(f"{pos} (Cur: {curr})", 0, 5000000, 0, step=100000, key=f"rec_{pos}")
        
        submitted = st.form_submit_button("Sign Class ($)")
    
    if submitted:
        total = sum(allocations.values())
        if total > st.session_state.budget:
            st.error("Over Budget!")
        else:
            st.session_state.budget -= total
            results = []
            
            # --- RECRUITING ENGINE ---
            scout_mult = 0.5 + (st.session_state.staff['Scout'] / 10.0)
            prestige_mult = 1.0 + (st.session_state.prestige / 200.0)
            
            for pos, amt in allocations.items():
                if amt > 0:
                    # 1. Base Gain
                    gain = (amt / 800000) * scout_mult * prestige_mult
                    
                    # 2. Hidden Gem Logic
                    gem = False
                    # Higher scout skill = better chance
                    gem_chance = (st.session_state.staff['Scout'] * 3) / 100.0 
                    if amt > 250000 and random.random() < gem_chance:
                        gem = True
                        gain += 4 # Big boost
                        # Booster Bonus
                        booster_money = random.randint(1, 5) * 100000
                        st.session_state.budget += booster_money
                        results.append(f"💎 GEM found at {pos}! (+4 Rtg) Boosters donated ${booster_money:,}")
                    
                    # 3. Update Roster
                    st.session_state.roster[pos] = min(99, st.session_state.roster[pos] + gain)
            
            # Show Results Report
            if results:
                st.success("Recruiting Success!")
                for r in results:
                    st.markdown(f"<div class='gem-box'>{r}</div>", unsafe_allow_html=True)
            else:
                st.info("Recruiting complete. No major gems found.")
            
            # Attrition
            for p in POSITIONS: st.session_state.roster[p] -= random.uniform(0.5, 2.0)
            
            # Finalize
            st.session_state.team_rating = calculate_ovr(st.session_state.roster)
            st.session_state.year += 1
            time.sleep(3)
            st.session_state.game_state = "DASHBOARD"
            st.rerun()

# --- MAIN ROUTER ---
if st.session_state.game_state == 'SETUP':
    run_setup()
elif st.session_state.game_state == 'DASHBOARD':
    show_dashboard()
elif st.session_state.game_state == 'POSTSEASON':
    show_postseason()
elif st.session_state.game_state == 'SUMMARY':
    show_year_summary()
elif st.session_state.game_state == 'RECRUITING':
    show_recruiting()
