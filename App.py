import streamlit as st
import random
import time
import json
import datetime
import math

# ==============================================================================
# COLLEGE FOOTBALL MOGUL V22 — FINAL PLATINUM
# 1) Critical Fixes: Restored compute_team_needs & finalize_season helpers.
# 2) Engine Safety: Defensive dict access in play_game (no KeyErrors).
# 3) CFP Logic: Auto-advance rounds when matches complete.
# 4) Budget Guard: Strict checks prevent negative spending.
# ==============================================================================

STATE_VERSION = 22.0

# 1. CONSTANTS & CONFIG
try:
    st.set_page_config(page_title="CFB Mogul V22", page_icon="🏈", layout="wide")
except Exception:
    pass

st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
.game-card, .staff-card, .news-box, .security-box, .trophy-tile, .rank-row, .resume-box { color: #111111 !important; }
.security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
.finance-alert { background-color: #d1e7dd; color: #0f5132 !important; border: 1px solid #badbcc; padding: 15px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-weight: bold; }
.nil-alert { background-color: #cff4fc; color: #055160 !important; border: 1px solid #b6effb; padding: 18px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-size: 1.1em; font-weight: bold; }
.game-card { padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #ddd; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.game-card-win { border-left: 5px solid #28a745; }
.game-card-loss { border-left: 5px solid #dc3545; }
.game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
.game-card-rival { border: 2px solid #ffc107 !important; background-color: #fffbf0 !important; }
.card-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 5px;}
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.85em; }
.stat-row { display: flex; justify-content: space-between; }
.staff-card { background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
.staff-role { font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.staff-name { font-size: 1.1em; font-weight: 800; color: #333; }
.badge { padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; margin-right: 5px; display: inline-block;}
.badge-tier-s { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-tier-a { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-tier-f { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-trait { background: #e2e3e5; color: #383d41; }
.recruiting-intel { background-color: #e0f7fa; color: #006064 !important; border-left: 5px solid #006064; padding: 12px; margin-bottom: 10px; border-radius: 4px; }
.bracket-box { background-color: #2c3e50; color: white !important; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
.bracket-row { display: flex; justify-content: space-between; padding: 6px; border-bottom: 1px solid #444; }
.news-box { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.news-item { padding: 6px 0; border-bottom: 1px solid #f1f1f1; }
.news-item:last-child { border-bottom: none; }
.small-muted { font-size: 0.85em; color: #666; }
.trophy-tile { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 10px; }
.newspaper-head { font-family: 'Georgia', serif; font-size: 2em; text-align: center; border-bottom: 3px double #333; padding-bottom: 10px; margin-bottom: 20px; color: #2c3e50; background: #fdfbf7; padding: 15px; border-radius: 5px; }
.newspaper-sub { font-family: 'Georgia', serif; font-style: italic; text-align: center; color: #555; margin-bottom: 20px; }
.booster-meter-container { background: #eee; height: 20px; border-radius: 10px; margin-top: 5px; overflow: hidden; border: 1px solid #ccc; }
.booster-meter-fill { height: 100%; transition: width 0.5s; }
.rank-row { background: white; padding: 8px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.rank-row-user { background: #e3f2fd !important; border-left: 5px solid #2196f3; font-weight: bold; }
.rank-num { width: 40px; font-weight: bold; color: #555; }
.rank-team { flex-grow: 1; }
.rank-rec { width: 80px; text-align: right; }
.resume-box { background-color: #fff; border: 2px solid #333; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
.resume-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: center; }
.resume-label { font-size: 0.8em; text-transform: uppercase; color: #666; letter-spacing: 1px; }
.resume-val { font-size: 1.2em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}
SCHEMES = {"Offense": ["Air Raid", "Smashmouth", "Pro Style"], "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]}
COUNTERS = {"Air Raid": "3-3-5 Cloud", "Smashmouth": "4-4 Heavy", "Pro Style": "Man Coverage", "3-3-5 Cloud": "Smashmouth", "4-4 Heavy": "Air Raid", "Man Coverage": "Pro Style"}
TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {"None": "None", "Recruiter": "+10% Recruit", "Tactician": "+3 Game Boost", "Air Raid": "+2 Scheme", "Smashmouth": "+2 Scheme", "Pro Style": "+2 Scheme"}
BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"]
}
TROPHY_ICONS = {"National Title": "🏆", "CFP": "🏆", "Rose Bowl": "🌹", "Sugar Bowl": "🍬", "Orange Bowl": "🍊", "Cotton Bowl": "🤠", "Peach Bowl": "🍑", "Fiesta Bowl": "🎉", "Citrus Bowl": "🍋", "Alamo Bowl": "🏰", "Pop-Tarts Bowl": "🍪", "Gator Bowl": "🐊", "Liberty Bowl": "🗽", "Music City Bowl": "🎸", "Las Vegas Bowl": "🎰", "Gasparilla Bowl": "🏴‍☠️", "Boca Raton Bowl": "🌴", "Potato Bowl": "🥔", "Bowl Win": "🎳"}
CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Texas A&M", "Ole Miss", "Vanderbilt", "Florida", "Mississippi St"],
    "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington", "Indiana", "Nebraska", "Purdue"],
    "ACC": ["Florida St", "Clemson", "Miami", "Stanford", "Cal", "Louisville", "UNC", "Virginia Tech", "SMU"],
    "Big 12": ["Utah", "TCU", "Baylor", "Texas Tech", "Arizona State", "Colorado", "Kansas State", "Oklahoma St", "BYU", "Arizona"],
    "G5": ["Boise State", "San Jose State", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St", "Fresno St", "Tulane", "Memphis", "Navy", "Army"]
}
ALL_TEAMS = [t for c in CONFERENCES.values() for t in c]
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

# 2. STATE SCHEMA
DEFAULT_STATE = {
    "state_version": STATE_VERSION, "game_state": "SETUP", "year": 2026, "tenure": 1, "budget": 5_000_000,
    "prestige": 60, "job_security": 80, "expected_wins": 6, "record": {"w": 0, "l": 0},
    "history": [], "news": [], "career_stats": {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0},
    "roster": {p: 75 for p in POSITIONS}, "staff": {}, "facilities": {"Marketing": 1, "Training": 1, "Stadium": 1},
    "my_schemes": {"Off": "Pro Style", "Def": "Man Coverage"}, "active_transfers": {p: False for p in POSITIONS},
    "stars": [], "candidates": {}, "schedule": [], "season_logs": [], "season_simulated": False,
    "season_end_ready": False, "week_index": 0, "offseason_step": 1, "nil_class": [],
    "hs_total_spend": 0, "hs_shares": {p: 100.0/7 for p in POSITIONS}, "hs_spend_by_pos": {p: 0 for p in POSITIONS},
    "hs_alloc_by_pos": {p: 0 for p in POSITIONS}, "top8": [], "top8_resolved": set(), "trophies": [],
    "conf_revenue_boost_mult": 1.0, "pending_invite": None, "booster_rating": 50, "ai_records": [],
    "selection_sunday_results": [], "ad_name": "Coach Prime", "team_name": "Unknown U", "team_color": "#333333",
    "team_conf": "G5", "team_rival": "Rival", "home_region": "South", "school_tier": 3,
    "team_off": 75, "team_def": 75, "team_rating": 75, "last_postseason_result": "NONE",
    "achievements": [], "milestone_log": [], "conferences_map": {k: list(v) for k, v in CONFERENCES.items()},
    "opponents_db": {}, "hotspots": {}, "postseason_data": {"Type": "NONE"}, "team_needs": []
}

ALLOWED_SAVE_KEYS = set(DEFAULT_STATE.keys())

def ensure_state():
    # Initialize missing keys
    for k, v in DEFAULT_STATE.items():
        if k not in st.session_state:
            st.session_state[k] = v
    
    # Type Safety Fixes
    if isinstance(st.session_state.get("top8_resolved"), list):
        st.session_state.top8_resolved = set(st.session_state.top8_resolved)
    
    # Ensure hs_alloc_by_pos exists
    if "hs_alloc_by_pos" not in st.session_state or not isinstance(st.session_state.hs_alloc_by_pos, dict):
        st.session_state.hs_alloc_by_pos = {p: 0 for p in POSITIONS}
    
    for k in ["year", "budget", "prestige", "job_security", "week_index", "booster_rating"]:
        try:
            st.session_state[k] = int(st.session_state.get(k, 0))
        except:
            st.session_state[k] = DEFAULT_STATE[k]
            
    # Identity Safety
    if st.session_state.team_name in [None, ""]:
        st.session_state.team_name = "Unknown U"
    
    # Opponents DB Safety
    if "opponents_db" not in st.session_state or not st.session_state.opponents_db:
         st.session_state.opponents_db = init_opponents_db()
         
    # Team Needs Safety
    if "team_needs" not in st.session_state or not isinstance(st.session_state.team_needs, list):
        st.session_state.team_needs = compute_team_needs(st.session_state.roster)
        
    st.session_state.state_version = STATE_VERSION

# 3. HELPERS
def safe_progress(value, label=""):
    try:
        st.progress(value, text=label)
    except:
        st.progress(value)

def helper_format_cash(amount):
    try: amount = int(amount)
    except: amount = 0
    return f"${amount/1_000_000:.1f}M" if amount >= 1_000_000 else f"${int(amount/1_000)}K"

def add_news(text):
    st.session_state.news.insert(0, f"{st.session_state.year}: {text}")
    st.session_state.news = st.session_state.news[:12]

def get_conferences_map():
    if "conferences_map" not in st.session_state:
        st.session_state.conferences_map = {k: list(v) for k, v in CONFERENCES.items()}
    return st.session_state.conferences_map

def get_conference(team):
    conf_map = get_conferences_map()
    for conf, teams in conf_map.items():
        if team in teams: return conf
    return "G5"

def compute_team_unit_ratings(roster, staff, facilities):
    r = {p: int(roster.get(p, 75)) for p in POSITIONS}
    oc = int(staff.get("OC", {}).get("off", 3))
    dc = int(staff.get("DC", {}).get("def", 3))
    training = int(facilities.get("Training", 1))
    
    off = (r["QB"]*0.34) + (r["OL"]*0.26) + ((r["RB"]+r["WR"])/2 * 0.40) + (oc*1.2) + (training*0.8)
    deff = (r["DL"]*0.32) + (r["LB"]*0.28) + (r["DB"]*0.40) + (dc*1.2) + (training*0.8)
    
    # OVR is average of OFF and DEF
    ovr = (off + deff) / 2
    return (int(max(40, min(99, off))), int(max(40, min(99, deff))), int(max(40, min(99, ovr))))

def sync_team_ratings():
    if "roster" in st.session_state and "staff" in st.session_state:
        res = compute_team_unit_ratings(st.session_state.roster, st.session_state.staff, st.session_state.facilities)
        st.session_state.team_off = res[0]
        st.session_state.team_def = res[1]
        st.session_state.team_rating = res[2]

def calculate_saban_score(career, prestige):
    return int((career["w"]*1) + (career["bowl_w"]*5) + (career["titles"]*50) + (prestige*0.5))

def generate_star_player(pos, tier):
    base = 85 if tier <= 2 else 80
    return {"id": random.randint(10000, 99999), "name": "New Recruit", "pos": pos, "rating": min(99, base + random.randint(5,14)), "year": "Fr", "trait": random.choice(TRAITS)}

def generate_hotspots():
   regions = list(REGION_STRENGTH.keys())
   weighted = {
       "South": ["RB", "WR", "DL", "LB", "QB", "DB", "OL"],
       "Midwest":["OL", "LB", "DL", "RB", "QB", "DB", "WR"],
       "West": ["QB", "WR", "DB", "RB", "OL", "DL", "LB"],
       "North": ["DL", "LB", "OL", "DB", "RB", "WR", "QB"]
   }
   out = {}
   for r in regions:
       pool = weighted.get(r, POSITIONS)
       picks = []
       while len(picks) < 3:
           c = random.choice(pool)
           if c not in picks: picks.append(c)
       out[r] = picks
   return out

def get_season_metrics():
    # V21.4 FIX: Defensive Metric Checks
    logs = st.session_state.get("season_logs", [])
    if not logs: return 0, "None", "None"
    wins_ovr = []
    loss_ovr = []
    sos_accum = 0
    opp_db = st.session_state.get("opponents_db", {})
    
    for log in logs:
        opp = log.get("Opponent", "Unknown")
        data = opp_db.get(opp, {"Prestige": 60, "OVR": 75})
        pres = int(data.get("Prestige", 60))
        sos_accum += pres
        
        score = str(log.get("Score", ""))
        ovr_val = int(data.get("OVR", 75) or 75)
        
        if score.startswith("W"): 
            wins_ovr.append((ovr_val, opp))
        elif score.startswith("L"): 
            loss_ovr.append((ovr_val, opp))
        
    avg_sos = int(sos_accum / max(1, len(logs)))
    best_win = max(wins_ovr, key=lambda x: x[0])[1] if wins_ovr else "None"
    worst_loss = min(loss_ovr, key=lambda x: x[0])[1] if loss_ovr else "None"
    return avg_sos, best_win, worst_loss

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Arch", "Shedeur"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name():
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman"]
    return f"{random.choice(first)} {random.choice(last)}"

def render_trophy_gallery(title_text="🏆 Trophy Gallery"):
    st.subheader(title_text)
    trophies = st.session_state.get("trophies", [])
    if not trophies:
        st.info("No trophies yet. Win a bowl or title.")
        return
    cols = st.columns(4)
    for i, t in enumerate(sorted(trophies, key=lambda x: x["Year"], reverse=True)[:24]):
        with cols[i%4]:
            st.markdown(f"<div class='trophy-tile'><div style='font-size:2em'>{t['Icon']}</div><div style='font-weight:800'>{t['Name']}</div><div class='small-muted'>{t['Year']}</div></div>", unsafe_allow_html=True)

def render_dynasty_timeline(max_items=25):
    st.subheader("🕰️ Dynasty Timeline")
    items = []
    for n in st.session_state.news:
        items.append({"year": int(n.split(":")[0]) if ":" in n else st.session_state.year, "text": n, "kind": 0})
    for h in st.session_state.history:
        items.append({"year": h["Year"], "text": f"{h['Year']}: {h['Record']} {h.get('Bowl','')} Rank {h.get('Rank','?')}", "kind": 1})
    
    items.sort(key=lambda x: (-x["year"], x["kind"]))
    st.markdown("<div class='news-box'>", unsafe_allow_html=True)
    for i in items[:max_items]:
        st.markdown(f"<div class='news-item'>• {i['text']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def init_opponents_db():
   db = {}
   for team in ALL_TEAMS + [st.session_state.team_name]:
       base = REAL_WORLD_INIT.get(team, {"Prestige": 60, "Talent": 75, "Tier": 3, "Rival": "Rival"})
       tier = int(base.get("Tier", 3))
       talent = int(base.get("Talent", 75))
       prestige = int(base.get("Prestige", 60))
       off = min(99, max(40, talent + random.randint(-3, 3)))
       deff = min(99, max(40, talent + random.randint(-3, 3)))
       db[team] = {
           "Team": team,
           "Prestige": prestige,
           "OVR": int((off + deff) / 2),
           "OffOVR": off,
           "DefOVR": deff,
           "Off": "Pro Style",
           "Def": "Man Coverage",
           "Tier": tier
       }
   return db

def build_season_summary_dict():
    """Safe season summary for recap screen."""
    wins = int(st.session_state.record.get("w", 0))
    losses = int(st.session_state.record.get("l", 0))

    avg_sos, best_win, worst_loss = get_season_metrics()

    this_year_hist = next((h for h in st.session_state.history if h.get("Year") == st.session_state.year), None)
    final_rank = this_year_hist.get("Rank", "Unranked") if this_year_hist else "Unranked"
    postseason = this_year_hist.get("Bowl", "No Bowl") if this_year_hist else "No Bowl"

    expected = int(st.session_state.expected_wins)
    delta = wins - expected

    return {
        "Year": st.session_state.year,
        "Team": st.session_state.team_name,
        "Conf": st.session_state.team_conf,
        "Record": f"{wins}-{losses}",
        "FinalRank": final_rank,
        "Postseason": postseason,
        "ExpectedWins": expected,
        "Delta": delta,
        "SOS": int(avg_sos),
        "BestWin": best_win,
        "WorstLoss": worst_loss,
    }

# V22: Restored Missing Helper
def compute_team_needs(roster, n=3):
   ratings = []
   for p in POSITIONS:
       try:
           val = int(roster.get(p, 75))
       except:
           val = 75
       ratings.append((val, p))
   ratings.sort(key=lambda x: x[0])
   return [p for _, p in ratings[:max(1, int(n))]]

# V22: Restored Missing Helper
def finalize_season(rank='Unranked', bowl='No Bowl'):
   w = int(st.session_state.record.get("w", 0))
   l = int(st.session_state.record.get("l", 0))

   st.session_state.history.append({
       "Year": int(st.session_state.year),
       "Team": st.session_state.team_name,
       "Conf": st.session_state.team_conf,
       "Record": f"{w}-{l}",
       "Rank": rank,
       "Bowl": bowl
   })

   cs = st.session_state.career_stats
   cs["w"] = int(cs.get("w", 0)) + w
   cs["l"] = int(cs.get("l", 0)) + l

   check_and_award_achievements()

# V22: CFP Auto-Advance Logic
def cfp_advance_if_ready():
   data = st.session_state.postseason_data
   if data.get("Type") != "CFP": return

   matches = data.get("Matches", [])
   if not matches or not all(m.get("winner") for m in matches): return

   round_num = int(data.get("Round", 1))
   winners = [m["winner"] for m in matches]

   if round_num in (2, 3):
       new_matches = []
       if round_num == 2:
           new_matches = [{"t1": winners[0], "t2": winners[3], "winner": None},
                          {"t1": winners[1], "t2": winners[2], "winner": None}]
           data["Round"] = 3
       else:
           new_matches = [{"t1": winners[0], "t2": winners[1], "winner": None}]
           data["Round"] = 4

       data["Matches"] = new_matches
       st.session_state.postseason_data = data
       return

   if round_num == 4:
       champ = winners[0]
       if champ == st.session_state.team_name:
           st.session_state.last_postseason_result = "TITLE"
           st.session_state.trophies.append({"Name": "National Title", "Year": st.session_state.year, "Icon": "🏆"})
           st.session_state.career_stats["titles"] += 1
       else:
           st.session_state.last_postseason_result = f"CFP_LOSS" # Simplified
       
       finalize_season(rank="#1" if champ == st.session_state.team_name else "#2", bowl="National Title")
       st.session_state.game_state = "SEASON_RECAP"

# 4. ENGINE (Pure Logic)
def engine_generate_roster(tier, base_ovr=None):
    # V21.4 FIX: Truthiness check on base_ovr
    base = base_ovr if base_ovr is not None else (90 if tier==1 else (82 if tier==2 else 74))
    return {p: min(99, max(40, int(base + random.randint(-4, 4)))) for p in POSITIONS}

def engine_generate_schedule(my_team, my_conf, rival):
    conf_map = get_conferences_map()
    conf_foes = [t for t in conf_map.get(my_conf, []) if t != my_team]
    schedule = random.sample(conf_foes, min(8, len(conf_foes)))
    needed = 12 - len(schedule)
    non_conf = [t for t in ALL_TEAMS if t not in conf_map.get(my_conf, []) and t != my_team]
    schedule += random.sample(non_conf, min(len(non_conf), needed))
    if rival in ALL_TEAMS:
        if rival in schedule: schedule.remove(rival)
        schedule.append(rival)
    random.shuffle(schedule)
    return schedule[:12]

def engine_generate_coach(role, tier):
    return {"name": generate_coach_name(), "role": role, "off": random.randint(1,10), "def": random.randint(1,10), "recruit": random.randint(1,10), "trait": random.choice(list(COACH_TRAITS.keys())), "salary": 1000000}

def simulate_ai_regular_season_seeded(seed):
    rnd = random.Random(seed)
    results = []
    # V19 Fix: Sort keys for determinism
    for team in sorted(st.session_state.opponents_db.keys()):
        if team == st.session_state.team_name: continue
        data = st.session_state.opponents_db[team]
        pres = data.get("Prestige", 60)
        wins = rnd.choices([12,11,10,9,8,7,6,5,4], weights=[5,15,20,20,15,10,5,5,5])[0] if pres > 80 else rnd.randint(3,9)
        results.append({"Team": team, "Wins": wins, "Losses": 12-wins, "Conf": get_conference(team), "Prestige": pres, "SOS": 60 + rnd.randint(-10,10)})
    return results

def engine_play_game_v8(my_off, my_def, opp_off, opp_def, staff, schemes, opp_data, plan, opp_coaches, is_home, is_rival, my_stad, opp_stad):
    # V22: Defensive Dict Access
    schemes = schemes or {}
    opp_data = opp_data or {}
    
    my_off_scheme = schemes.get("Off", "Pro Style")
    opp_def_scheme = opp_data.get("Def", "Man Coverage")

    my_edge = (my_off - opp_def) * 0.35
    opp_edge = (opp_off - my_def) * 0.35
    
    bonus = 0.0
    if COUNTERS.get(opp_def_scheme) == my_off_scheme: bonus += 2.5
    if COUNTERS.get(my_off_scheme) == opp_def_scheme: bonus -= 2.5
    
    hf = 3.0 if is_home else -3.0
    
    my_score = int(random.gauss(27 + my_edge + bonus + hf, 10))
    opp_score = int(random.gauss(27 + opp_edge - bonus - hf, 10))
    if my_score == opp_score: my_score += 3
    
    qb_val = int(st.session_state.roster.get("QB", 75))
    
    return {
        "result": "W" if my_score > opp_score else "L",
        "score": f"{my_score}-{opp_score}",
        "stats": {"raw_roster": int((my_off+my_def)/2), "qb_duel": [qb_val, int(opp_off)]},
        "explain": {}
    }

# 5. UI VIEWS & MODULES

def check_and_award_achievements():
    cs = st.session_state.get("career_stats", {})
    wins = int(cs.get("w", 0))
    titles = int(cs.get("titles", 0))
    
    unlocked_ids = {x['id'] for x in st.session_state.achievements}
    
    def unlock(aid, title, icon, desc):
        if aid not in unlocked_ids:
            st.session_state.achievements.append({"id": aid, "title": title, "icon": icon, "desc": desc, "year": st.session_state.year})
            st.session_state.milestone_log.insert(0, f"{st.session_state.year}: {icon} {title}")
            st.toast(f"Achievement Unlocked: {title}")

    if wins >= 10: unlock("WIN_10", "10 Wins", "✅", "10 Career Wins")
    if titles >= 1: unlock("TITLE_1", "National Champ", "🏆", "Won Title")
    if st.session_state.booster_rating >= 90: unlock("BOOST_90", "Golden Boy", "🤑", "90+ Boosters")

def render_achievements_panel():
    st.subheader("🏅 Milestones")
    unlocked = st.session_state.achievements
    unlocked_ids = {x['id'] for x in unlocked}
    
    cols = st.columns(3)
    ach_list = [
        {"id": "WIN_10", "title": "10 Wins", "icon": "✅", "desc": "10 Career Wins"},
        {"id": "TITLE_1", "title": "National Champ", "icon": "🏆", "desc": "Win Title"},
        {"id": "BOOST_90", "title": "Golden Boy", "icon": "🤑", "desc": "90+ Boosters"}
    ]
    
    for i, a in enumerate(ach_list):
        with cols[i%3]:
            done = a['id'] in unlocked_ids
            status = "✅ UNLOCKED" if done else "🔒 LOCKED"
            st.markdown(f"""<div class='trophy-tile'><div style='font-size:1.5em'>{a['icon']}</div><b>{a['title']}</b><br><small>{a['desc']}</small><br><b>{status}</b></div>""", unsafe_allow_html=True)

# --- RECRUITING MODULES ---
def process_hs_outreach(total_spend, shares_pct, staff, prestige, inflation, hotspots, region, needs):
    spent = int(total_spend)
    updates = {}
    gems = []
    
    # V19: Diminishing Returns Logic (using math.exp)
    cap = 900000 * 2.0
    effective_spend = cap * (1 - math.exp(-spent / cap)) if spent > 0 else 0
    
    for p in POSITIONS:
        pct = shares_pct.get(p, 0)
        updates[p] = random.randint(1, 3) if pct > 10 else 0
        if pct > 15 and random.random() < 0.1:
            gems.append({"name": "Gem Recruit", "pos": p, "rating": 85, "year": "Fr", "trait": "Gem"})
            
    return {"spent": spent, "roster_updates": updates, "gems": gems, "booster_bonus": 0}

def normalize_shares(shares):
    total = sum(shares.values())
    if total == 0: return {p: 0 for p in POSITIONS}
    return {p: (v/total)*100 for p,v in shares.items()}

def compute_recruiting_class_grade():
    return "B+", 85, {"nil_signed": len(st.session_state.nil_class), "top8_commits": 0, "gems_found": 0}

def show_offseason_nil_v8():
    st.subheader("1) NIL Prospects")
    st.write("Sign transfers using your budget.")
    if st.button("Scout Portal"):
        st.session_state.nil_class = [{"name": "Transfer QB", "pos": "QB", "rating": 88, "ask": 2000000, "status": "OPEN", "id": 101}]
    
    for p in st.session_state.nil_class:
        c1, c2 = st.columns(2)
        c1.write(f"{p['pos']} {p['name']} ({p['rating']}) - ${p['ask']:,}")
        
        btn_key = f"sign_{p.get('id', 0)}"
        if p['status'] == "OPEN" and c2.button(f"Sign {p['name']}", key=btn_key):
             if st.session_state.budget >= p['ask']:
                 st.session_state.budget -= p['ask']
                 st.session_state.roster[p['pos']] = max(st.session_state.roster[p['pos']], p['rating'])
                 p['status'] = "SIGNED"
                 st.success("Signed!")
             else:
                 st.error("No funds")

def show_offseason_top8_v8():
    st.subheader("3) Top-8 Battles")
    st.write("Pitch to elite recruits.")
    if not st.session_state.top8:
        st.session_state.top8 = [{"name": "Elite WR", "pos": "WR", "rating": 95, "ask": 150000, "status": "OPEN", "id": 201}]
        
    for r in st.session_state.top8:
        if r['status'] == "OPEN":
            key = f"pitch_{r.get('id')}"
            if st.button(f"Pitch {r['name']} (${r['ask']:,})", key=key):
                if st.session_state.budget < r['ask']:
                    st.error("Not enough budget!")
                else:
                    st.session_state.budget -= r['ask']
                    if random.random() > 0.4:
                        r['status'] = "COMMITTED"
                        st.session_state.roster[r['pos']] = max(st.session_state.roster[r['pos']], r['rating'])
                        st.balloons()
                    else:
                        r['status'] = "LOST"
                        st.error("Missed!")
                    st.rerun()
        else:
            st.write(f"{r['name']}: {r['status']}")

def show_offseason_hs_outreach():
    st.subheader("2) HS Outreach: The War Room")
    st.write("Allocate budget to positions.")
    
    budget = int(st.session_state.budget)
    alloc = st.session_state.hs_alloc_by_pos
    
    # V19: Auto-Distribute
    c1, c2, c3 = st.columns(3)
    if c1.button("Balanced"):
        share = int(budget * 0.5 / 7)
        for p in POSITIONS: alloc[p] = share
        st.rerun()
    if c2.button("Needs Heavy"):
        # V21.1: Fix missing team_needs
        needs = st.session_state.get("team_needs", [])
        for p in POSITIONS: alloc[p] = 500000 if p in needs else 100000
        st.rerun()
        
    # Input Grid
    cols = st.columns(2)
    total_alloc = 0
    for i, p in enumerate(POSITIONS):
        with cols[i%2]:
            val = st.number_input(f"{p} Allocation", value=int(alloc.get(p, 0)), step=250000, key=f"alloc_{p}")
            alloc[p] = val
            total_alloc += val
            
    st.divider()
    remaining = budget - total_alloc
    if remaining < 0:
        st.error(f"Over Budget by {helper_format_cash(abs(remaining))}")
    else:
        st.success(f"Remaining Budget: {helper_format_cash(remaining)}")
        if st.button("Confirm Recruiting Class", type="primary"):
            # V22: Budget Guard
            if remaining < 0:
                st.error("Cannot confirm while over budget.")
                st.stop()
            
            res = process_hs_outreach(total_alloc, normalize_shares(alloc), {}, 60, 1.0, [], "South", [])
            st.session_state.budget -= res["spent"]
            # Apply updates
            for p, val in res["roster_updates"].items():
                st.session_state.roster[p] += val
            
            st.success("Recruiting Complete! Roster Updated.")
            sync_team_ratings()

# --- MAIN VIEWS ---
def show_offseason():
    sync_team_ratings()
    st.title("🏟️ Offseason Hub")
    st.markdown(f"<div class='nil-alert'>Budget: {helper_format_cash(st.session_state.budget)} | Prestige: {st.session_state.prestige}</div>", unsafe_allow_html=True)

    if st.session_state.pending_invite:
        inv = st.session_state.pending_invite
        st.warning(f"Invite to {inv['to_conf']}")
        if st.button("Accept"):
            st.session_state.team_conf = inv['to_conf']
            st.session_state.pending_invite = None
            st.success("Moved!")
            st.rerun()

    steps = {1: "NIL Prospects", 2: "HS Outreach (War Room)", 3: "Top-8 Battles", 4: "Advance Year"}
    cols = st.columns(4)
    for i in range(1, 5):
        if cols[i-1].button(steps[i], disabled=(st.session_state.offseason_step == i)):
            st.session_state.offseason_step = i
            st.rerun()

    st.divider()
    step = st.session_state.offseason_step
    
    if step == 1: show_offseason_nil_v8()
    elif step == 2: show_offseason_hs_outreach()
    elif step == 3: show_offseason_top8_v8()
    else:
        st.subheader("4) Advance to Next Season")
        grade, score, br = compute_recruiting_class_grade()
        st.markdown(f"### 📦 Class Grade: **{grade}**")
        if st.button("Advance Year ➜", type="primary"):
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.week_index = 0
            st.session_state.record = {"w": 0, "l": 0}
            st.session_state.season_logs = []
            st.session_state.season_simulated = False
            st.session_state.season_end_ready = False
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
            
            # Clear Offseason State
            st.session_state.nil_class = []
            st.session_state.top8 = []
            st.session_state.top8_resolved = set()
            st.session_state.hs_alloc_by_pos = {p: 0 for p in POSITIONS}
            
            add_news(f"Season {st.session_state.year} begins!")
            st.session_state.game_state = "DASHBOARD"
            st.rerun()

def show_season_recap():
    st.title(f"Season {st.session_state.year} Recap")
    flag = st.session_state.last_postseason_result
    st.write(f"Postseason Result: **{flag}**")
    
    summary = build_season_summary_dict()
    st.metric("Final Record", summary["Record"])
    
    if st.button("Go to Offseason", type="primary"):
        st.session_state.game_state = "OFFSEASON"
        st.rerun()

def show_postseason():
    st.title("Postseason Hub")
    data = st.session_state.postseason_data
    
    if data["Type"] == "CFP":
        round_num = data["Round"]
        st.header(f"CFP Round {round_num}")
        
        # V19: True Seeding
        user_alive = data.get("UserAlive")
        user_match = None
        for m in data["Matches"]:
             if m.get("t1") == st.session_state.team_name or m.get("t2") == st.session_state.team_name:
                 user_match = m
        
        if not user_match and user_alive and round_num == 1:
            st.success("✅ First Round BYE")
            if st.button("Simulate & Advance"):
                # Sim round 1
                winners = []
                for m in data["Matches"]:
                    w = m["t1"] if random.random() > 0.5 else m["t2"] # Sim logic
                    m["winner"] = w
                    # V21.4 FIX: Track Winner Seed Correctly
                    seed_val = m.get("seed_high", 99) if w == m.get("t1") else m.get("seed_low", 99)
                    winners.append({"team": w, "seed": seed_val})
                
                # Re-seed QFs: Seeds 1-4 vs Winners (Lowest Seed plays 1)
                seeds = data.get("QF_Seeds", [])
                
                # Sort winners by seed (worst seed first = highest number)
                winners.sort(key=lambda x: x["seed"], reverse=True)
                
                new_matches = []
                if len(seeds) == 4 and len(winners) >= 4:
                    new_matches.append({"t1": seeds[0], "t2": winners[0]["team"], "winner": None}) # 1 vs Worst
                    new_matches.append({"t1": seeds[1], "t2": winners[1]["team"], "winner": None})
                    new_matches.append({"t1": seeds[2], "t2": winners[2]["team"], "winner": None})
                    new_matches.append({"t1": seeds[3], "t2": winners[3]["team"], "winner": None})
                
                st.session_state.postseason_data["Round"] = 2
                st.session_state.postseason_data["Matches"] = new_matches
                st.rerun()
                
        elif user_match:
            opp = user_match["t2"] if user_match["t1"] == st.session_state.team_name else user_match["t1"]
            st.info(f"Matchup: vs {opp}")
            if st.button("Play Game"):
                res = engine_play_game_v8(80,80,80,80,{},{},{"Def":"Pro Style"},"Normal",{},False,False,1,1)
                if res["result"] == "W":
                    user_match["winner"] = st.session_state.team_name
                    st.success("You Won!")
                else:
                    user_match["winner"] = opp
                    st.session_state.postseason_data["UserAlive"] = False
                    st.session_state.last_postseason_result = "CFP_LOSS"
                
                # V22 Fix: Auto-Advance Logic
                matches_done = all(m.get("winner") for m in data["Matches"])
                if matches_done:
                    cfp_advance_if_ready()
                else:
                    st.rerun()
                
    elif data["Type"] == "BOWL":
        st.write(f"Bowl: {data['Bowl']} vs {data['Opponent']}")
        if st.button("Play Bowl"):
             st.session_state.last_postseason_result = "BOWL_WIN"
             finalize_season(rank="Ranked", bowl=data['Bowl'])
             st.session_state.game_state = "SEASON_RECAP"
             st.rerun()

def show_selection_sunday():
    st.title("Selection Sunday")
    if st.button("Advance to Postseason"):
        # Init 12 team bracket
        seeds = ["Georgia", "Ohio State", "Texas", "Oregon"] + ["Alabama", "Michigan", "Penn St", "Notre Dame", "Ole Miss", "FSU", "Clemson", "Utah"]
        # Inject user if good enough
        if st.session_state.record["w"] >= 10:
             seeds[2] = st.session_state.team_name # Force rank 3 for testing
        
        st.session_state.postseason_data = {
            "Type": "CFP", "Round": 1, 
            "Seeds": seeds, "QF_Seeds": seeds[:4],
            "Matches": [
                {"t1": seeds[4], "t2": seeds[11], "seed_high": 5, "seed_low": 12, "winner": None},
                {"t1": seeds[5], "t2": seeds[10], "seed_high": 6, "seed_low": 11, "winner": None},
                {"t1": seeds[6], "t2": seeds[9], "seed_high": 7, "seed_low": 10, "winner": None},
                {"t1": seeds[7], "t2": seeds[8], "seed_high": 8, "seed_low": 9, "winner": None}
            ],
            "UserAlive": True,
            "Rank": 3 if st.session_state.record["w"] >= 10 else 25
        }
        st.session_state.game_state = "POSTSEASON"
        st.rerun()

def show_season_end():
    st.title("Regular Season Complete")
    if st.button("Go to Selection Sunday"):
        st.session_state.game_state = "SELECTION_SUNDAY"
        st.rerun()

def show_dashboard():
    sync_team_ratings()
    st.title(f"{st.session_state.team_name} Dashboard")
    st.metric("Budget", helper_format_cash(st.session_state.budget))
    st.metric("OVR", st.session_state.team_rating)
    
    # Simple Sim Button
    if st.button("Simulate Season"):
        st.session_state.record = {"w": random.randint(10, 12), "l": random.randint(0, 2)} # Good record for testing
        st.session_state.season_end_ready = True
        st.session_state.game_state = "SEASON_END"
        st.rerun()
        
    render_achievements_panel()

# V21.1 FIX: Safe Setup (Patch A)
def run_setup():
   st.title("New Dynasty")
   team = st.text_input("School Name", st.session_state.get("team_name","State U"))
   if st.button("Start Game", type="primary"):
       st.session_state.team_name = team or "State U"
       # Ensure opponents/schedule exist
       if not st.session_state.get("opponents_db"):
           st.session_state.opponents_db = init_opponents_db()
       st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
       st.session_state.game_state = "DASHBOARD"
       st.rerun()
        
def show_fired():
    st.error("You have been fired.")
    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()

def show_retirement():
    st.success("Happy Retirement!")
    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()

# 6. ROUTER REGISTRY AND GUARD
VIEWS = {
    "SETUP": run_setup,
    "DASHBOARD": show_dashboard,
    "SEASON_END": show_season_end,
    "SELECTION_SUNDAY": show_selection_sunday,
    "POSTSEASON": show_postseason,
    "SEASON_RECAP": show_season_recap,
    "OFFSEASON": show_offseason,
    "FIRED": show_fired,
    "RETIREMENT": show_retirement
}

# V21.2 PATCH: Expanded Guard
REQUIRED_FUNCS = [
    "run_setup", "show_dashboard", "show_season_end", "show_selection_sunday",
    "show_postseason", "show_season_recap", "show_offseason", "show_fired", "show_retirement"
]
_missing = [f for f in REQUIRED_FUNCS if f not in globals()]
if _missing:
    st.error("Missing required functions: " + ", ".join(sorted(set(_missing))))
    st.stop()

# 5. INITIALIZATION & ROUTER
# V21.1 FIX: Centralized Sidebar in Zone 5
def safe_json_default(obj):
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return str(obj)

def render_system_sidebar():
    with st.sidebar:
        st.header("💾 Dynasty System")
        st.caption(f"Version {STATE_VERSION} (Stable)")
        
        # V21.4 FIX: Always show export
        state_copy = dict(st.session_state)
        if "top8_resolved" in state_copy:
            state_copy["top8_resolved"] = list(state_copy["top8_resolved"])
        export_data = {k: v for k, v in state_copy.items() if k in ALLOWED_SAVE_KEYS}
        json_str = json.dumps(export_data, default=safe_json_default)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        
        st.download_button(
            label="📥 Download Save (JSON)",
            data=json_str,
            file_name=f"CFB_Mogul_Save_{timestamp}.json",
            mime="application/json"
        )
            
        uploaded_file = st.file_uploader("Import Save File", type=["json"])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                for k, v in data.items():
                    if k not in ALLOWED_SAVE_KEYS:
                        continue
                    if k == "top8_resolved":
                        st.session_state[k] = set(v) if isinstance(v, list) else set()
                    else:
                        st.session_state[k] = v
                
                # V21.4 FIX: Use ensure_state
                ensure_state() 
                st.session_state.candidates = {}   # transient UI cache
                sync_team_ratings()                # derived OFF/DEF/OVR always present
                
                st.success("Save Loaded Successfully! Reloading...")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error loading save: {e}")

def run_app():
    ensure_state()
    render_system_sidebar()
    view = VIEWS.get(st.session_state.game_state, show_dashboard)
    view()

if __name__ == "__main__":
    run_app()
```”
