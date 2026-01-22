import streamlit as st
import random
import time
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gridiron CEO", page_icon="🏈", layout="centered")

# --- CUSTOM CSS FOR IPHONE FEEL ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE & CONFIG ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
POS_WEIGHTS = {"QB": 0.20, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.15}

TEAMS_DB = {
    "Georgia": {"tier": 1, "conf": "SEC", "budget": 24_000_000, "expect": 11, "coach": 8, "facilities": 10},
    "Ohio State": {"tier": 1, "conf": "B1G", "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10},
    "Texas": {"tier": 1, "conf": "SEC", "budget": 25_000_000, "expect": 10, "coach": 9, "facilities": 10},
    "Alabama": {"tier": 1, "conf": "SEC", "budget": 22_000_000, "expect": 10, "coach": 9, "facilities": 9},
    "Michigan": {"tier": 1, "conf": "B1G", "budget": 20_000_000, "expect": 10, "coach": 8, "facilities": 9},
    "Florida St": {"tier": 2, "conf": "ACC", "budget": 15_000_000, "expect": 9, "coach": 7, "facilities": 8},
    "Clemson": {"tier": 2, "conf": "ACC", "budget": 15_000_000, "expect": 9, "coach": 8, "facilities": 8},
    "Penn State": {"tier": 2, "conf": "B1G", "budget": 16_000_000, "expect": 9, "coach": 7, "facilities": 8},
    "Utah": {"tier": 2, "conf": "B12", "budget": 13_000_000, "expect": 9, "coach": 6, "facilities": 10},
    "Boise State": {"tier": 3, "conf": "G5", "budget": 7_000_000, "expect": 9, "coach": 6, "facilities": 5},
    "Vanderbilt": {"tier": 3, "conf": "SEC", "budget": 8_000_000, "expect": 5, "coach": 5, "facilities": 4},
}

# --- HELPER FUNCTIONS ---
def generate_roster(tier):
    base = 92 if tier == 1 else (84 if tier == 2 else 74)
    roster = {p: min(99, max(50, base + random.randint(-8, 8))) for p in POSITIONS}
    return roster

def calculate_ovr(roster):
    return round(sum(roster[p] * w for p, w in POS_WEIGHTS.items()), 1)

# --- SESSION STATE INITIALIZATION ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP' # SETUP, DASHBOARD, SEASON, RECRUITING
    st.session_state.year = 2026
    st.session_state.team_name = ""
    st.session_state.budget = 0
    st.session_state.roster = {}
    st.session_state.record = {"w": 0, "l": 0}
    st.session_state.history = []
    st.session_state.job_security = 100
    st.session_state.prestige = 80
    st.session_state.facilities = {"Stadium": 1, "Marketing": 1, "Training": 1}
    st.session_state.staff = {"Coach_Off": 5, "Coach_Def": 5, "Scout": 5}
    st.session_state.logs = []

# --- GAME LOGIC ---

def run_setup():
    st.title("👔 Gridiron CEO Mobile")
    st.write("Select your franchise to begin your career as Athletic Director.")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("AD Name", "Coach Prime")
    with col2:
        diff = st.selectbox("Difficulty", ["Normal", "Hard (Less Budget)", "Easy (Rich)"])
    
    team_choice = st.selectbox("Choose Team", list(TEAMS_DB.keys()))
    
    # Preview Team
    d = TEAMS_DB[team_choice]
    st.info(f"**{team_choice}** | Tier {d['tier']} | Budget: ${d['budget']:,} | Goal: {d['expect']} Wins")
    
    if st.button("📝 Sign Contract", type="primary"):
        # Initialize Game Data
        st.session_state.ad_name = name
        st.session_state.team_name = team_choice
        
        # Apply Difficulty
        mult = 1.0 if diff == "Normal" else (0.75 if "Hard" in diff else 1.25)
        st.session_state.budget = int(d['budget'] * mult)
        st.session_state.win_expect = d['expect']
        st.session_state.roster = generate_roster(d['tier'])
        st.session_state.team_rating = calculate_ovr(st.session_state.roster)
        
        # Staff Init
        base_skill = 8 if d['tier'] == 1 else 6
        st.session_state.staff = {
            "Coach_Off": base_skill, 
            "Coach_Def": base_skill, 
            "Scout": base_skill,
            "Coach_Sal": base_skill * 500000,
            "Scout_Sal": base_skill * 200000
        }
        
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    # Header Stats
    st.markdown(f"### 🏈 {st.session_state.team_name} ({st.session_state.year})")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Budget", f"${st.session_state.budget/1000000:.1f}M")
    col2.metric("Rating", st.session_state.team_rating)
    col3.metric("Job Security", f"{st.session_state.job_security}%", delta_color="normal")
    
    # Roster Visualization
    with st.expander("📋 View Roster & Staff", expanded=False):
        r = st.session_state.roster
        st.write(" **Offense:**")
        cols = st.columns(4)
        cols[0].metric("QB", r['QB'])
        cols[1].metric("RB", r['RB'])
        cols[2].metric("WR", r['WR'])
        cols[3].metric("OL", r['OL'])
        
        st.write(" **Defense:**")
        cols = st.columns(3)
        cols[0].metric("DL", r['DL'])
        cols[1].metric("LB", r['LB'])
        cols[2].metric("DB", r['DB'])
        
        st.divider()
        s = st.session_state.staff
        st.caption(f"Head Coach: Off {s['Coach_Off']} | Def {s['Coach_Def']}")
        st.caption(f"Head Scout: {s['Scout']}/10")

    # Actions Menu
    st.subheader("Front Office")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏟️ Investments"):
            st.session_state.sub_state = "INVEST"
            st.rerun()
    with c2:
        if st.button("👥 Staff Mgmt"):
            st.session_state.sub_state = "STAFF"
            st.rerun()
            
    st.subheader("Season")
    if st.button("▶️ SIMULATE SEASON", type="primary"):
        run_season()

    # Handling Sub-Menus
    if 'sub_state' in st.session_state:
        if st.session_state.sub_state == "INVEST":
            st.warning("Investment Opportunity")
            inv_col1, inv_col2 = st.columns(2)
            if inv_col1.button("Marketing ($1M)"):
                if st.session_state.budget >= 1000000:
                    st.session_state.budget -= 1000000
                    st.session_state.facilities['Marketing'] += 1
                    st.success("Marketing Upgraded!")
                    time.sleep(0.5)
                    st.rerun()
            if inv_col2.button("Training ($3M)"):
                if st.session_state.budget >= 3000000:
                    st.session_state.budget -= 3000000
                    st.session_state.facilities['Training'] += 1
                    st.success("Facilities Upgraded!")
                    time.sleep(0.5)
                    st.rerun()
            if st.button("Close Menu"):
                st.session_state.sub_state = None
                st.rerun()

def run_season():
    # Simulate 12 Games
    wins = 0
    losses = 0
    log_data = []
    
    progress_text = "Simulating Season..."
    my_bar = st.progress(0, text=progress_text)
    
    # Calculate Power
    coach_bonus = (st.session_state.staff['Coach_Off'] + st.session_state.staff['Coach_Def'])
    fac_bonus = st.session_state.facilities['Training'] * 0.5
    my_power = st.session_state.team_rating + coach_bonus + fac_bonus
    
    for i in range(12):
        time.sleep(0.1) # UI Effect
        opp_rating = random.randint(65, 95)
        opp_name = f"Week {i+1} Opponent"
        
        score_diff = (my_power + random.randint(-10, 10)) - opp_rating
        
        if score_diff > 0:
            wins += 1
            res = "W"
            my_score = random.randint(24, 45)
            opp_score = max(0, my_score - int(score_diff/2))
        else:
            losses += 1
            res = "L"
            opp_score = random.randint(24, 45)
            my_score = max(0, opp_score - int(abs(score_diff)/2))
            
        log_data.append([opp_name, int(opp_rating), f"{my_score}-{opp_score}", res])
        my_bar.progress((i + 1) / 12, text=f"Week {i+1}: {res} ({wins}-{losses})")

    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.logs = log_data
    
    # Calculate Post Season
    rank = max(1, 130 - (wins * 10) - int(st.session_state.team_rating/5))
    st.session_state.rank = rank
    
    st.session_state.game_state = "POSTSEASON"
    st.rerun()

def show_postseason():
    st.header(f"Season Over: {st.session_state.record['w']}-{st.session_state.record['l']}")
    
    # Display Game Log Table
    df = pd.DataFrame(st.session_state.logs, columns=["Opponent", "Rating", "Score", "Result"])
    st.dataframe(df, use_container_width=True)
    
    # Bowl Logic
    if st.session_state.rank <= 12:
        st.success("🔥 PLAYOFF BOUND! ($5M Bonus)")
        bonus = 5000000
    elif st.session_state.record['w'] >= 6:
        st.info("🎳 BOWL INVITE! ($2M Bonus)")
        bonus = 2000000
    else:
        st.error("❌ No Bowl Game.")
        bonus = 0
        
    if st.button("Advance to Offseason"):
        st.session_state.budget += bonus
        
        # Pay Staff
        payroll = st.session_state.staff['Coach_Sal'] + st.session_state.staff['Scout_Sal']
        st.session_state.budget -= payroll
        
        # Board Review
        expect = st.session_state.win_expect
        if st.session_state.record['w'] >= expect:
            st.session_state.job_security = min(100, st.session_state.job_security + 10)
        else:
            st.session_state.job_security -= 15
            
        st.session_state.game_state = "RECRUITING"
        st.rerun()

def show_recruiting():
    st.header("🦅 Recruiting & Portal")
    st.write(f"Budget Available: **${st.session_state.budget:,}**")
    
    # 1. Retention Phase
    if 'retention_done' not in st.session_state:
        st.error("🚨 TRANSFER PORTAL ALERT")
        risk_pos = random.choice(POSITIONS)
        cost = 1500000
        st.write(f"Your starting **{risk_pos}** wants to transfer to Alabama.")
        st.write(f"Cost to keep: **${cost:,}**")
        
        col1, col2 = st.columns(2)
        if col1.button("💰 Pay to Keep"):
            if st.session_state.budget >= cost:
                st.session_state.budget -= cost
                st.toast("Player Retained!", icon="✅")
            else:
                st.toast("Not enough money!", icon="❌")
                st.session_state.roster[risk_pos] -= 5
            st.session_state.retention_done = True
            st.rerun()
            
        if col2.button("👋 Let him walk"):
            st.session_state.roster[risk_pos] -= 8
            st.toast("Player Left. Ratings dropped.", icon="📉")
            st.session_state.retention_done = True
            st.rerun()
            
    else:
        # 2. Investment Phase
        st.subheader("Invest in Positions")
        
        with st.form("recruiting_form"):
            investments = {}
            cols = st.columns(2)
            for i, pos in enumerate(POSITIONS):
                with cols[i % 2]:
                    current = int(st.session_state.roster[pos])
                    investments[pos] = st.number_input(f"{pos} (Rtg: {current})", min_value=0, step=100000, key=f"inv_{pos}")
            
            submitted = st.form_submit_button("Finalize Class ($)")
            
            if submitted:
                total_spend = sum(investments.values())
                if total_spend > st.session_state.budget:
                    st.error(f"Over Budget! You spent ${total_spend:,} but only have ${st.session_state.budget:,}")
                else:
                    # Process Results
                    st.session_state.budget -= total_spend
                    
                    scout_mult = 0.5 + (st.session_state.staff['Scout'] / 10.0)
                    
                    for pos, amt in investments.items():
                        if amt > 0:
                            gain = (amt / 800000) * scout_mult
                            # Gem Chance
                            if amt > 500000 and random.random() < 0.3:
                                gain += 3
                                st.toast(f"Found a GEM at {pos}!", icon="💎")
                            
                            st.session_state.roster[pos] = min(99, st.session_state.roster[pos] + gain)
                    
                    # Graduation Attrition
                    for pos in POSITIONS:
                        st.session_state.roster[pos] -= random.uniform(0.5, 2.0)
                        
                    # Recalculate and Advance
                    st.session_state.team_rating = calculate_ovr(st.session_state.roster)
                    st.session_state.year += 1
                    
                    # Revenue Reset
                    base_rev = 15000000 + (st.session_state.facilities['Marketing'] * 1000000)
                    st.session_state.budget += base_rev
                    
                    # Cleanup
                    del st.session_state.retention_done
                    st.session_state.game_state = "DASHBOARD"
                    st.rerun()

# --- MAIN CONTROLLER ---
if st.session_state.game_state == 'SETUP':
    run_setup()
elif st.session_state.game_state == 'DASHBOARD':
    show_dashboard()
elif st.session_state.game_state == 'SEASON':
    # We handle season inside the function to use progress bars
    pass 
elif st.session_state.game_state == 'POSTSEASON':
    show_postseason()
elif st.session_state.game_state == 'RECRUITING':
    show_recruiting()
