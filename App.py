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
    .star-card {
        background-color: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .star-name { font-size: 1.2em; font-weight: bold; color: #1e3a8a; }
    .star-trait { font-size: 0.9em; color: #d97706; font-weight: 600; }
    .star-rating { font-size: 1.5em; float: right; font-weight: bold; color: #10b981; }
    .legacy-card {
        background-color: #fff8e1;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffecb3;
        text-align: center;
        margin-bottom: 20px;
    }
    .gem-box {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #2196f3;
        margin-bottom: 5px;
    }
    .news-ticker {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffeeba;
        font-style: italic;
        margin-bottom: 15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIG & DATA ---
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
POS_WEIGHTS = {"QB": 0.20, "RB": 0.10, "WR": 0.15, "OL": 0.15, "DL": 0.15, "LB": 0.10, "DB": 0.15}

FIRST_NAMES = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Stone", "General", "Maverick"]
LAST_NAMES = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Downs", "Bond", "Nix", "Penix", "Bowers", "Sayin", "Manning"]

HEADLINES = [
    "BREAKING: Ohio State lands 5-star QB from Texas!",
    "RUMOR: Coach Prime considering NFL offers?",
    "ANALYSIS: SEC defenses looking softer this year.",
    "ALUMNI: Boosters demanding a National Title run.",
    "RECRUITING: Top WR decommits from Alabama.",
    "INJURY REPORT: Star players resting for playoffs.",
    "POLLS: Georgia unanimous #1 in preseason rankings.",
    "SCANDAL: NCAA investigating improper benefits at rival school."
]

TRAITS = {
    "None": {"desc": "No special ability", "effect": 0},
    "❄️ Clutch": {"desc": "+10 Rating in 4th Qtr/Close Games", "effect": 1},
    "🚀 Speedster": {"desc": "High Variance Scoring (Big Plays)", "effect": 2},
    "🧠 Field General": {"desc": "Boosts entire Offense +2", "effect": 3},
    "😤 Enforcer": {"desc": "Opponent scores less (Intimidation)", "effect": 4},
}

TEAMS_DB = {
    "Georgia": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BA0C2F"},
    "Ohio State": {"tier": 1, "budget": 24_000_000, "expect": 11, "coach": 9, "facilities": 10, "color": "#BB0000"},
    "Texas": {"tier": 1, "budget": 25_000_000, "expect": 10, "coach": 9, "facilities": 10, "color": "#BF5700"},
    "Alabama": {"tier": 1, "budget": 22_000_000, "expect": 10, "coach": 9, "facilities": 9, "color": "#9E1B32"},
    "Florida St": {"tier": 2, "budget": 15_000_000, "expect": 9, "coach": 7, "facilities": 8, "color": "#782F40"},
    "Penn State": {"tier": 2, "budget": 16_000_000, "expect": 9, "coach": 8, "facilities": 8, "color": "#041E42"},
    "Boise State": {"tier": 3, "budget": 7_000_000, "expect": 9, "coach": 6, "facilities": 5, "color": "#0033A0"},
    "Vanderbilt": {"tier": 3, "budget": 8_000_000, "expect": 5, "coach": 5, "facilities": 4, "color": "#866D4B"},
    "San Jose State": {"tier": 4, "budget": 4_500_000, "expect": 6, "coach": 5, "facilities": 3, "color": "#0055A2"},
}

OPPONENT_POOL = [
    "USC", "Michigan", "LSU", "Clemson", "Notre Dame", "Oklahoma", "Miami",
    "Tennessee", "Auburn", "Texas A&M", "Wisconsin", "UCLA", "Iowa",
    "Stanford", "Cal", "Arizona State", "Washington", "Utah", "TCU",
    "Baylor", "Texas Tech", "Okla State", "Kansas State", "North Carolina",
    "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St"
]

# --- HELPERS ---
def generate_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_star_player(position, tier):
    base = 94 if tier == 1 else (88 if tier == 2 else 80)
    rating = min(99, base + random.randint(0, 5))
    trait_name = random.choice(list(TRAITS.keys()))
    if tier == 4 and random.random() > 0.3: trait_name = "None"
        
    return {
        "id": random.randint(1000,9999),
        "name": generate_name(),
        "pos": position,
        "rating": rating,
        "year": random.choice(["Fr", "So", "Jr", "Sr"]),
        "trait": trait_name
    }

def calculate_ovr(roster, stars):
    base_ovr = sum(roster[p] * w for p, w in POS_WEIGHTS.items())
    star_bonus = 0
    for s in stars:
        diff = max(0, s['rating'] - roster[s['pos']])
        star_bonus += (diff * POS_WEIGHTS[s['pos']])
        if s['trait'] == "🧠 Field General": star_bonus += 2
    return int(round(base_ovr + star_bonus, 0))

def calculate_saban_score():
    w = st.session_state.career_stats['w']
    bw = st.session_state.career_stats['bowl_w']
    natty = st.session_state.career_stats['titles']
    prest = st.session_state.prestige
    return int((w * 1) + (bw * 5) + (natty * 50) + (prest * 0.5))

def format_cash(amount):
    if amount >= 1_000_000:
        return f"${int(amount/1_000_000)}M"
    elif amount >= 1_000:
        return f"${int(amount/1_000)}K"
    return f"${int(amount)}"

# --- STATE INIT ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'SETUP'
    st.session_state.year = 2026
    st.session_state.budget = 0
    st.session_state.prestige = 50
    st.session_state.job_security = 100
    st.session_state.start_prestige = 50 
    st.session_state.start_rating = 0    
    st.session_state.roster = {} 
    st.session_state.stars = []
    st.session_state.hall_of_fame = []
    st.session_state.record = {"w": 0, "l": 0}
    st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
    st.session_state.facilities = {"Marketing": 1, "Training": 1}
    st.session_state.staff = {"Coach": 5, "Scout": 5, "Coach_Sal": 3000000, "Scout_Sal": 500000}
    st.session_state.rank = 0
    st.session_state.inflation = 1.0
    st.session_state.team_color = "#333333"
    st.session_state.current_headline = random.choice(HEADLINES)

# --- SCREENS ---

def run_setup():
    st.title("🏆 Gridiron CEO V2.4")
    st.markdown("### Dynasty Mode")
    
    col1, col2 = st.columns(2)
    with col1: name = st.text_input("AD Name", "Coach Prime")
    with col2: diff = st.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    sorted_teams = sorted(TEAMS_DB.keys(), key=lambda x: (TEAMS_DB[x]['tier'], x))
    team = st.selectbox("Choose School", sorted_teams, format_func=lambda x: f"{x} (Tier {TEAMS_DB[x]['tier']})")
    d = TEAMS_DB[team]
    
    st.info(f"**{team}** | Tier {d['tier']} | Budget: ${d['budget']:,}")
    
    if st.button("Start Career", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = d.get('color', '#333333')
        
        mult = 1.0
        if "Hard" in diff: mult = 0.75
        elif "Easy" in diff: mult = 1.25
            
        st.session_state.budget = int(d['budget'] * mult)
        st.session_state.win_expect = d['expect']
        st.session_state.prestige = 95 - (d['tier'] * 12)
        st.session_state.start_prestige = st.session_state.prestige
        
        base_rtg = 92 if d['tier'] == 1 else (84 if d['tier'] == 2 else 74)
        if d['tier'] == 4: base_rtg = 65
        st.session_state.roster = {p: min(99, max(40, base_rtg + random.randint(-5, 5))) for p in POSITIONS}
        
        st.session_state.stars = []
        st.session_state.stars.append(generate_star_player("QB", d['tier']))
        if d['tier'] < 4:
            st.session_state.stars.append(generate_star_player("LB", d['tier']))
            
        st.session_state.team_rating = calculate_ovr(st.session_state.roster, st.session_state.stars)
        st.session_state.start_rating = st.session_state.team_rating
        st.session_state.facilities['Training'] = d['facilities']
        
        base = max(4, 9 - d['tier'])
        st.session_state.staff = {"Coach": base, "Scout": base, "Coach_Sal": base*400000, "Scout_Sal": base*150000}
        
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_dashboard():
    # HEADLINE TICKER
    st.markdown(f"<div class='news-ticker'>📰 {st.session_state.current_headline}</div>", unsafe_allow_html=True)
    
    # TEAM HEADER WITH COLOR
    st.markdown(f"""
        <div style='background-color: {st.session_state.team_color}; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h2 style='color: white; margin:0; text-align: center; text-shadow: 1px 1px 2px black;'>{st.session_state.team_name} ({st.session_state.year})</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # STATUS INDICATORS
    # Job Security
    sec = st.session_state.job_security
    sec_icon = "🛡️ Safe" if sec > 80 else ("⚠️ Shaky" if sec > 50 else "🔥 Hot Seat")
    
    # Prestige
    prest = int(st.session_state.prestige)
    prest_icon = "👑 Elite" if prest > 90 else ("📈 Rising" if prest > 70 else "📉 Rebuild")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", format_cash(st.session_state.budget))
    c2.metric("Security", f"{sec}%", sec_icon)
    c3.metric("Prestige", prest, prest_icon)
    c4.metric("Career Score", calculate_saban_score())

    # SABAN METER
    saban = calculate_saban_score()
    st.progress(min(1.0, saban/600), f"Saban Meter: {saban}/600")

    tab1, tab2, tab3 = st.tabs(["⭐ Roster", "🏢 Staff", "⚔️ Season"])
    
    with tab1:
        st.subheader("Franchise Captains")
        if not st.session_state.stars:
            st.info("No Franchise Players. Recruit some!")
        for s in st.session_state.stars:
            with st.container():
                st.markdown(f"""
                <div class="star-card">
                    <span class="star-rating">{int(s['rating'])}</span>
                    <div class="star-name">{s['pos']} {s['name']} <span style='font-size:0.8em;color:gray'>({s['year']})</span></div>
                    <div class="star-trait">{s['trait']}</div>
                    <div style='font-size:0.8em;color:gray'>{TRAITS[s['trait']]['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        st.write(f"**Team OVR: {int(st.session_state.team_rating)}**")
        col_off, col_def = st.columns(2)
        with col_off:
            for p in ["QB", "RB", "WR", "OL"]: 
                val = int(st.session_state.roster[p])
                st.progress(val/100, f"{p}: {val}")
        with col_def:
            for p in ["DL", "LB", "DB"]: 
                val = int(st.session_state.roster[p])
                st.progress(val/100, f"{p}: {val}")

    with tab2:
        st.subheader("Staff Management")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.write(f"**Head Coach** (Lvl {st.session_state.staff['Coach']})")
            if st.session_state.staff['Coach'] < 10:
                cost = int(3000000 * st.session_state.inflation)
                if st.button(f"Upgrade Coach ({format_cash(cost)})"):
                    if st.session_state.budget >= cost:
                        st.session_state.budget -= cost
                        st.session_state.staff['Coach'] += 1
                        st.session_state.staff['Coach_Sal'] += 500000
                        st.success("Upgraded!")
                        time.sleep(0.5); st.rerun()
                    else: st.error("Too poor.")
        with sc2:
            st.write(f"**Head Scout** (Lvl {st.session_state.staff['Scout']})")
            if st.session_state.staff['Scout'] < 10:
                cost = int(1500000 * st.session_state.inflation)
                if st.button(f"Upgrade Scout ({format_cash(cost)})"):
                    if st.session_state.budget >= cost:
                        st.session_state.budget -= cost
                        st.session_state.staff['Scout'] += 1
                        st.session_state.staff['Scout_Sal'] += 150000
                        st.success("Upgraded!")
                        time.sleep(0.5); st.rerun()
                    else: st.error("Too poor.")

    with tab3:
        st.markdown("### Ready for Kickoff?")
        if st.button("▶️ SIMULATE SEASON", type="primary"):
            st.session_state.current_headline = random.choice(HEADLINES) # Update ticker
            run_season()

def run_season():
    wins = 0; losses = 0
    logs = []
    
    schedule = random.sample([t for t in OPPONENT_POOL if t != st.session_state.team_name], 12)
    bar = st.progress(0, "Kickoff...")
    
    base_power = st.session_state.team_rating + st.session_state.staff['Coach'] + (st.session_state.facilities['Training']*0.5)
    
    trait_bonus_off = 0
    trait_bonus_def = 0
    for s in st.session_state.stars:
        if s['trait'] == "🧠 Field General": trait_bonus_off += 2
        if s['trait'] == "😤 Enforcer": trait_bonus_def += 3 
    
    for i, opp_name in enumerate(schedule):
        time.sleep(0.05)
        
        if "(FCS)" in opp_name: opp_rating = random.randint(55, 70)
        else: opp_rating = random.randint(70, 96)
            
        variance = random.randint(-10, 10)
        clutch_active = False
        for s in st.session_state.stars:
            if s['trait'] == "❄️ Clutch" and abs(base_power - opp_rating) < 7:
                variance += 8; clutch_active = True
            if s['trait'] == "🚀 Speedster": variance += random.randint(-5, 10)
        
        final_power = base_power + trait_bonus_off + variance
        score_diff = final_power - opp_rating
        
        if score_diff > 0:
            wins += 1; res = "W"
            my_score = random.randint(24, 48) + int(score_diff/2)
            opp_score = max(0, my_score - int(score_diff/1.5)) - trait_bonus_def
        else:
            losses += 1; res = "L"
            opp_score = random.randint(28, 52)
            my_score = max(0, opp_score - int(abs(score_diff)/1.5))
            
        note = "Clutch!" if clutch_active and wins > losses and abs(score_diff) < 10 else ""
        logs.append({"Week": i+1, "Opponent": opp_name, "Ovr": int(opp_rating), "Result": res, "Score": f"{int(my_score)}-{int(opp_score)}", "Note": note})
        bar.progress((i+1)/12, f"Week {i+1}: {res}")

    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    rank_score = (wins * 100) + st.session_state.team_rating
    st.session_state.rank = max(1, 130 - int(rank_score/12))
    
    # Job Security Logic
    if wins >= st.session_state.win_expect:
        st.session_state.job_security = min(100, st.session_state.job_security + 10)
    else:
        st.session_state.job_security -= 15
        
    st.session_state.game_state = "POSTSEASON"
    st.rerun()

def show_postseason():
    st.header(f"Season Finale: {st.session_state.record['w']}-{st.session_state.record['l']}")
    
    df = pd.DataFrame(st.session_state.season_logs)
    st.dataframe(df, use_container_width=True)
    
    bowl_result = "No Bowl"
    bowl_payout = 0
    rank = st.session_state.rank
    
    if rank <= 12:
        st.success(f"🔥 PLAYOFF BOUND! Ranked #{rank}")
        bowl_payout = 5000000
        if random.random() < 0.5:
            st.balloons(); st.success("🏆 NATIONAL CHAMPIONS!!")
            bowl_result = "Won National Title"; st.session_state.career_stats['titles'] += 1; st.session_state.career_stats['bowl_w'] += 1; bowl_payout += 10000000
        else:
            st.warning("Eliminated in Playoffs."); bowl_result = "Lost Playoff Game"; st.session_state.career_stats['bowl_l'] += 1
            
    elif st.session_state.record['w'] >= 6:
        bowl_name = "Citrus Bowl" if rank < 25 else "Potato Bowl"
        st.info(f"🎳 Invite: {bowl_name}")
        bowl_payout = 2000000
        if random.random() < 0.6:
            st.success(f"Won {bowl_name}!"); bowl_result = f"Won {bowl_name}"; st.session_state.career_stats['bowl_w'] += 1
        else:
            st.error(f"Lost {bowl_name}."); bowl_result = f"Lost {bowl_name}"; st.session_state.career_stats['bowl_l'] += 1
    
    st.session_state.latest_result_text = bowl_result
    
    if st.button("View Summary"):
        st.session_state.budget += bowl_payout
        st.session_state.career_stats['w'] += st.session_state.record['w']
        st.session_state.career_stats['l'] += st.session_state.record['l']
        if st.session_state.record['w'] >= 10: st.session_state.prestige = min(99, st.session_state.prestige + 3)
        elif st.session_state.record['w'] < 6: st.session_state.prestige = max(10, st.session_state.prestige - 4)
        st.session_state.game_state = "SUMMARY"
        st.rerun()

def show_year_summary():
    st.title(f"📊 {st.session_state.year} Recap")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")
    c2.metric("Rank", f"#{st.session_state.rank}")
    c3.metric("Result", st.session_state.latest_result_text)
    c4.metric("Prestige", int(st.session_state.prestige))
    
    st.divider()
    
    score = calculate_saban_score()
    st.write(f"**Career Legacy Score:** {score}")
    st.progress(min(1.0, score/600), f"Comparison to Nick Saban (600 pts)")
    
    # RETIREMENT OPTION
    if st.session_state.year >= 2030:
        st.warning(f"You have completed 5 Seasons (2026-{st.session_state.year}).")
        if st.button("🌴 RETIRE & VIEW LEGACY", type="primary"):
            st.session_state.game_state = "RETIREMENT"
            st.rerun()
    
    if st.button("Enter Offseason (Retention & Recruiting)"):
        payroll = st.session_state.staff['Coach_Sal'] + st.session_state.staff['Scout_Sal']
        st.session_state.budget -= payroll
        rev = 16000000 + (st.session_state.facilities['Marketing'] * 1000000)
        st.session_state.budget += rev
        st.session_state.inflation += 0.08
        if 'retention_done' in st.session_state: del st.session_state.retention_done
        st.session_state.game_state = "RECRUITING"
        st.rerun()

def show_retirement():
    st.balloons()
    st.title(f"🌴 Hall of Fame Induction: {st.session_state.ad_name}")
    
    start_p = st.session_state.start_prestige
    end_p = st.session_state.prestige
    start_r = st.session_state.start_rating
    end_r = st.session_state.team_rating
    
    score = calculate_saban_score()
    if score > 500: grade = "GOAT 🐐"
    elif score > 300: grade = "Legend 💎"
    elif score > 150: grade = "A-"
    elif score > 100: grade = "B"
    elif score > 50: grade = "C"
    else: grade = "D"
    
    st.markdown(f"""
    <div class="legacy-card">
        <h1>Final Grade: {grade}</h1>
        <h3>Saban Comparison Score: {score} / 600</h3>
        <p><i>Nick Saban retired with approx. 600 points based on our formula.</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Wins", st.session_state.career_stats['w'])
    c2.metric("National Titles", st.session_state.career_stats['titles'])
    c3.metric("Bowl Wins", st.session_state.career_stats['bowl_w'])
    
    st.subheader("Program Impact")
    col1, col2 = st.columns(2)
    col1.metric("Prestige Change", f"{int(end_p)}", f"{int(end_p - start_p)}")
    col2.metric("Rating Change", f"{int(end_r)}", f"{int(end_r - start_r)}")
    
    st.divider()
    st.subheader(f"🏛️ {st.session_state.team_name} Hall of Fame")
    if st.session_state.hall_of_fame:
        for p in st.session_state.hall_of_fame:
            st.markdown(f"🏆 **{p['pos']} {p['name']}** (Rtg: {int(p['rating'])}) - {p['trait']}")
    elif st.session_state.stars:
        st.write("Inducting current active stars:")
        for s in st.session_state.stars:
            st.markdown(f"⭐ **{s['pos']} {s['name']}** (Rtg: {int(s['rating'])})")
    else:
        st.write("No eligible Hall of Famers.")
        
    st.divider()
    if st.button("Start New Career"):
        st.session_state.clear()
        st.rerun()

def show_recruiting():
    st.header("🦅 Offseason War Room")
    st.write(f"Budget: **{format_cash(st.session_state.budget)}**")
    
    # --- PHASE 1: RETENTION ---
    if 'retention_done' not in st.session_state:
        st.error("🚨 TRANSFER PORTAL ALERT")
        if st.session_state.stars:
            threat = random.choice(st.session_state.stars)
            cost = int(threat['rating'] * 25000 * st.session_state.inflation)
            
            st.markdown(f"**{threat['pos']} {threat['name']}** is thinking of transferring.")
            st.write(f"Cost to match offer: **{format_cash(cost)}**")
            
            c1, c2 = st.columns(2)
            if c1.button("💰 Pay & Keep"):
                if st.session_state.budget >= cost:
                    st.session_state.budget -= cost
                    st.success("He stays!")
                    time.sleep(1); st.session_state.retention_done = True; st.rerun()
                else: st.error("Not enough funds!")
            
            if c2.button("👋 Let him walk"):
                st.session_state.stars.remove(threat)
                st.warning("He transferred.")
                time.sleep(1); st.session_state.retention_done = True; st.rerun()
        else:
            st.info("No major threats.")
            if st.button("Next"): st.session_state.retention_done = True; st.rerun()
        return

    # --- PHASE 2: RECRUITING ---
    with st.form("recruit_form"):
        allocations = {}
        cols = st.columns(2)
        for i, pos in enumerate(POSITIONS):
            with cols[i%2]:
                curr = int(st.session_state.roster[pos])
                allocations[pos] = st.number_input(f"{pos} (Rtg: {curr})", 0, 10000000, 0, step=100000, key=f"rec_{pos}")
        
        submitted = st.form_submit_button("Sign Class")
    
    if submitted:
        total = sum(allocations.values())
        if total > st.session_state.budget:
            st.error("Over Budget!")
        else:
            st.session_state.budget -= total
            gems = []
            scout_mult = 1.0 + (st.session_state.staff['Scout'] / 10.0)
            
            for pos, amt in allocations.items():
                if amt > 0:
                    gain = (amt / (800000 * st.session_state.inflation)) * scout_mult
                    star_chance = (amt / 500000) * 0.05 + (st.session_state.staff['Scout'] * 0.01)
                    if star_chance > 0.4: star_chance = 0.4
                    
                    if random.random() < star_chance:
                        new_star = generate_star_player(pos, 1)
                        new_star['year'] = "Fr"
                        st.session_state.stars.append(new_star)
                        gems.append(f"🌟 Signed 5-Star {pos} **{new_star['name']}**")
                        gain += 5
                    
                    st.session_state.roster[pos] = min(99, st.session_state.roster[pos] + gain)
            
            if gems:
                st.balloons()
                for g in gems: st.success(g)
            
            # Graduation
            seniors = [s for s in st.session_state.stars if s['year'] == "Sr"]
            st.session_state.hall_of_fame.extend(seniors)
            st.session_state.stars = [s for s in st.session_state.stars if s['year'] != "Sr"]
            
            for s in st.session_state.stars:
                if s['year'] == "Jr": s['year'] = "Sr"
                elif s['year'] == "So": s['year'] = "Jr"
                elif s['year'] == "Fr": s['year'] = "So"
                s['rating'] = min(99, s['rating'] + random.randint(1, 4))
            
            for p in POSITIONS: st.session_state.roster[p] -= random.uniform(0.5, 2.5)
            
            st.session_state.team_rating = calculate_ovr(st.session_state.roster, st.session_state.stars)
            st.session_state.year += 1
            st.session_state.game_state = "DASHBOARD"
            st.rerun()

# --- ROUTER ---
if st.session_state.game_state == 'SETUP': run_setup()
elif st.session_state.game_state == 'DASHBOARD': show_dashboard()
elif st.session_state.game_state == 'POSTSEASON': show_postseason()
elif st.session_state.game_state == 'SUMMARY': show_year_summary()
elif st.session_state.game_state == 'RETIREMENT': show_retirement()
elif st.session_state.game_state == 'RECRUITING': show_recruiting()
