import streamlit as st
import random
import time
import pandas as pd
import math

# ==============================================================================
# COLLEGE FOOTBALL MOGUL — V6 (Refactored + Realism Upgrades)
# Single-file Streamlit app
# ==============================================================================

# ----------------------------
# ZONE 1: CONFIG + UI THEME
# ----------------------------
try:
    st.set_page_config(page_title="College Football Mogul V6", page_icon="🏈", layout="wide")
except:
    pass

st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }

/* DASHBOARD WIDGETS */
.security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
.security-safe { color: #28a745; font-weight: bold; }
.security-warm { color: #fd7e14; font-weight: bold; }
.security-hot { color: #dc3545; font-weight: bold; }

/* FINANCIAL REPORT BOX */
.finance-alert { background-color: #d1e7dd; color: #0f5132; border: 1px solid #badbcc; padding: 15px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-weight: bold; }
.nil-alert { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; padding: 16px; border-radius: 8px; margin-bottom: 14px; text-align: center; font-size: 1.1em; font-weight: bold; }

/* GAME CARDS */
.game-card { padding: 10px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #ddd; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.game-card-win { border-left: 5px solid #28a745; }
.game-card-loss { border-left: 5px solid #dc3545; }
.game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
.game-card-rival { border: 2px solid #ffc107 !important; background-color: #fffbf0 !important; }

.card-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 5px;}
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.85em; }
.stat-row { display: flex; justify-content: space-between; }

/* STAFF CARDS */
.staff-card { background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
.staff-role { font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.staff-name { font-size: 1.1em; font-weight: 800; color: #333; }
.badge { padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; margin-right: 5px; display: inline-block;}
.badge-tier-s { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-tier-a { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-tier-f { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-trait { background: #e2e3e5; color: #383d41; }

/* RECRUITING */
.recruiting-intel { background-color: #e0f7fa; border-left: 5px solid #006064; padding: 12px; margin-bottom: 12px; border-radius: 4px; }
.bracket-box { background-color: #2c3e50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
.bracket-row { display: flex; justify-content: space-between; padding: 6px; border-bottom: 1px solid #444; }
.news-box { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.news-item { padding: 6px 0; border-bottom: 1px solid #f1f1f1; }
.news-item:last-child { border-bottom: none; }

.small-muted { color: #777; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# ZONE 2: STATIC DATA
# ----------------------------
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}

SCHEMES = {"Offense": ["Air Raid", "Smashmouth", "Pro Style"],
           "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]}

COUNTERS = {
    "Air Raid": "3-3-5 Cloud",
    "Smashmouth": "4-4 Heavy",
    "Pro Style": "Man Coverage",
    "3-3-5 Cloud": "Smashmouth",
    "4-4 Heavy": "Air Raid",
    "Man Coverage": "Pro Style"
}

TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {
    "None": "None",
    "Recruiter": "+10–15% Elite Recruiting",
    "Tactician": "+Gameplan + In-Game Edge",
    "Air Raid": "+Off Scheme Fit",
    "Smashmouth": "+Off Scheme Fit",
    "Pro Style": "+Off Scheme Fit"
}

BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"]
}

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

CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Texas A&M", "Ole Miss", "Vanderbilt", "Florida", "Mississippi St"],
    "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington", "Indiana", "Nebraska", "Purdue"],
    "ACC": ["Florida St", "Clemson", "Miami", "Stanford", "Cal", "Louisville", "UNC", "Virginia Tech", "SMU"],
    "Big 12": ["Utah", "TCU", "Baylor", "Texas Tech", "Arizona State", "Colorado", "Kansas State", "Oklahoma St", "BYU", "Arizona"],
    "G5": ["Boise State", "San Jose State", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St", "Fresno St", "Tulane", "Memphis", "Navy", "Army"]
}
ALL_TEAMS = [t for c in CONFERENCES.values() for t in c]

# ----------------------------
# ZONE 3: HELPERS (PURE / SAFE)
# ----------------------------
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def helper_format_cash(amount: int) -> str:
    if amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    return f"${int(amount/1_000)}K"

def generate_name() -> str:
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Arch", "Shedeur", "Quinn", "Travis", "Ashton"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck", "Jeanty", "Judkins"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name() -> str:
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan", "Kalen"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman", "Lanning", "DeBoer"]
    return f"{random.choice(first)} {random.choice(last)}"

def get_letter_grade(val: int) -> str:
    if val >= 9: return "A+"
    if val >= 8: return "A"
    if val >= 7: return "B"
    if val >= 5: return "C"
    if val >= 3: return "D"
    return "F"

def get_conference(team: str) -> str:
    for conf, teams in CONFERENCES.items():
        if team in teams:
            return conf
    return "G5"

def role_rating(cand: dict, role: str) -> int:
    if role in ["HC", "OC"]:
        return int(cand.get("off", 1))
    if role == "DC":
        return int(cand.get("def", 1))
    if role == "Scout":
        return int(cand.get("recruit", 1))
    return int(cand.get("off", 1))

def compute_team_needs(roster: dict, k: int = 3) -> list:
    sorted_pos = sorted(roster.items(), key=lambda x: x[1])
    return [p for p, _ in sorted_pos[:k]]

def add_news(text: str):
    if "news" not in st.session_state:
        st.session_state.news = []
    st.session_state.news.insert(0, f"{st.session_state.year}: {text}")
    st.session_state.news = st.session_state.news[:12]

def calculate_saban_score(career_stats, prestige):
    return int((career_stats['w'] * 1) + (career_stats['bowl_w'] * 5) + (career_stats['titles'] * 50) + (prestige * 0.5))

def get_bowl_name(rank):
    if rank <= 12: return "CFP Playoff"
    if rank <= 25: return random.choice(BOWL_MAPPING["Elite"])
    if rank <= 40: return random.choice(BOWL_MAPPING["High"])
    if rank <= 80: return random.choice(BOWL_MAPPING["Mid"])
    return random.choice(BOWL_MAPPING["Low"])

def generate_star_player(position, tier):
    # tier is currently unused but kept for future depth
    return {
        "id": random.randint(10000, 99999),
        "name": generate_name(),
        "pos": position,
        "rating": min(99, 85 + random.randint(0, 10)),
        "year": "Fr",
        "trait": random.choice(TRAITS)
    }

def generate_ga_coach(role):
    return {
        "name": f"GA {generate_name()}",
        "role": role,
        "off": random.randint(1, 3),
        "def": random.randint(1, 3),
        "recruit": random.randint(1, 2),
        "trait": "None",
        "salary": 50000,
        "history": "Former Player",
        "scouted": True
    }

# ----------------------------
# ZONE 4: ENGINE (PURE-ish)
# ----------------------------
def engine_calculate_revenue(tier, marketing_lvl, inflation):
    base = {1: 40_000_000, 2: 25_000_000, 3: 10_000_000, 4: 5_000_000}.get(int(tier or 3), 5_000_000)
    marketing_bonus = int(marketing_lvl) * 2_000_000
    return int((base + marketing_bonus) * float(inflation))

def engine_generate_coach(role, tier):
    tier = int(tier)
    cost = random.randint(4_000_000, 8_000_000) if tier == 1 else random.randint(500_000, 3_500_000)
    trait_pool = list(COACH_TRAITS.keys())
    if role == "OC":
        trait_pool = ["Air Raid", "Smashmouth", "Pro Style", "Recruiter", "Tactician"]
    base = 8 if tier == 1 else (5 if tier == 2 else 2)
    return {
        "name": generate_coach_name(),
        "role": role,
        "off": min(10, base + random.randint(0, 3)),
        "def": min(10, base + random.randint(0, 3)),
        "recruit": min(10, base + random.randint(0, 3)),
        "trait": random.choice(trait_pool),
        "salary": cost,
        "history": "External Hire",
        "scouted": False
    }

def engine_generate_roster(tier, base_ovr=None):
    base = int(base_ovr) if base_ovr else (90 if int(tier) == 1 else (80 if int(tier) == 2 else 74))
    roster = {}
    for p in POSITIONS:
        roster[p] = clamp(base + random.randint(-4, 4), 40, 99)
    return roster

def engine_team_rating(roster: dict, training_lvl: int) -> int:
    # Weighted to make roster management matter more
    qb = roster["QB"]
    line = roster["OL"]
    skill = (roster["RB"] + roster["WR"]) / 2
    front7 = (roster["DL"] + roster["LB"]) / 2
    db = roster["DB"]
    raw = (qb * 0.28) + (line * 0.20) + (skill * 0.22) + (front7 * 0.18) + (db * 0.12)
    boost = 0.6 * int(training_lvl)
    return int(clamp(raw + boost, 40, 99))

def engine_generate_schedule(my_team, my_conf, rival):
    conf_foes = [t for t in CONFERENCES.get(my_conf, CONFERENCES['G5']) if t != my_team]
    schedule = random.sample(conf_foes, min(8, len(conf_foes)))
    needed = 12 - len(schedule)
    non_conf = [t for t in ALL_TEAMS if t not in CONFERENCES.get(my_conf, []) and t != my_team]
    schedule += random.sample(non_conf, min(len(non_conf), needed))
    if rival in ALL_TEAMS:
        if rival in schedule:
            schedule.remove(rival)
        schedule.append(rival)
    random.shuffle(schedule)
    return schedule[:12]

def _tier_bonus(x):
    if x >= 9: return 3.0
    if x >= 7: return 2.0
    if x >= 5: return 1.0
    if x <= 2: return -2.0
    if x <= 4: return -1.0
    return 0.0

def engine_play_game(my_rating, opp_rating, staff, schemes, opp_schemes, game_plan,
                     opp_coaches, is_home, is_rival, stadium_lvl, my_roster, return_debug=True):
    """
    Realism upgrades:
    - Uses a more “spread-like” model based on rating delta, coaching, scheme, homefield.
    - Uses pace (scheme + gameplan) for total points.
    - Produces larger distribution of margins so management choices matter.
    """
    my_rating = float(my_rating)
    opp_rating = float(opp_rating)

    # roster unit visuals (for UI)
    my_off = (my_roster["QB"] * 0.32) + (my_roster["OL"] * 0.22) + (((my_roster["RB"] + my_roster["WR"]) / 2) * 0.46)
    my_def = (my_roster["DL"] * 0.38) + (my_roster["LB"] * 0.32) + (my_roster["DB"] * 0.30)

    # 1) Talent baseline
    rating_delta = (my_rating - opp_rating)
    base_spread = rating_delta * 0.75  # management impact: bigger rating differences matter

    # 2) Coaching
    my_oc = float(staff.get("OC", {}).get("off", 3))
    my_dc = float(staff.get("DC", {}).get("def", 3))
    my_hc = float(staff.get("HC", {}).get("off", 3))
    opp_oc = float(opp_coaches.get("OC", 5))
    opp_dc = float(opp_coaches.get("DC", 5))

    coach_edge = (_tier_bonus(my_oc) - _tier_bonus(opp_dc)) + (_tier_bonus(my_dc) - _tier_bonus(opp_oc))
    coach_edge *= 1.15

    # HC traits: tactician helps execution; recruiter doesn't help on-field much
    hc_trait = staff.get("HC", {}).get("trait", "None")
    if hc_trait == "Tactician":
        coach_edge += 1.3

    # 3) Scheme
    scheme_bonus = 0.0
    my_off_s = schemes.get("Off", "Pro Style")
    opp_def_s = opp_schemes.get("Def", "Man Coverage")
    if COUNTERS.get(opp_def_s, "Pro Style") == my_off_s:
        scheme_bonus += 2.5
    elif COUNTERS.get(my_off_s, "Man Coverage") == opp_def_s:
        scheme_bonus -= 2.5

    oc_trait = staff.get("OC", {}).get("trait", "None")
    if oc_trait in ["Air Raid", "Smashmouth", "Pro Style"] and oc_trait == my_off_s:
        scheme_bonus += 1.5  # clear identity boost

    # 4) Home field
    home_bonus = 0.0
    if is_home:
        home_bonus = clamp((stadium_lvl - 1) / 3.0, 0.0, 3.5)
    else:
        # hostile road effect sometimes
        if random.random() < 0.20:
            home_bonus = -clamp((stadium_lvl - 1) / 4.0, 0.0, 2.5)

    # 5) Gameplan
    plan_bonus = 0.0
    var_mult = 1.0
    if game_plan == "Aggressive":
        plan_bonus = 1.2
        var_mult = 1.25
    elif game_plan == "Conservative":
        plan_bonus = -0.8
        var_mult = 0.85

    if is_rival:
        var_mult *= 1.25

    # Final expected spread before randomness
    spread_mu = base_spread + coach_edge + scheme_bonus + home_bonus + plan_bonus

    # Variance tuned to avoid “all games are close”
    # Underdogs + rivalry + aggressive = more chaos
    sigma = 8.5 * var_mult
    # When teams are very different, outcomes are more stable
    sigma *= clamp(1.15 - (abs(rating_delta) / 35.0), 0.65, 1.15)

    margin = random.gauss(spread_mu, sigma)
    margin = clamp(margin, -35, 35)

    # Total points based on pace (scheme + plan)
    pace = 0.0
    if my_off_s == "Air Raid": pace += 3.5
    if my_off_s == "Smashmouth": pace -= 3.0
    if game_plan == "Aggressive": pace += 2.5
    if game_plan == "Conservative": pace -= 2.0

    total_points = random.gauss(56 + pace, 10.5)
    total_points = clamp(total_points, 28, 92)

    my_score = int(round((total_points / 2.0) + (margin / 2.0)))
    opp_score = int(round(total_points - my_score))

    my_score = clamp(my_score, 0, 75)
    opp_score = clamp(opp_score, 0, 75)

    # Visuals + stats
    visual_my_off = int(clamp(my_off + _tier_bonus(my_oc) * 1.0, 40, 99))
    visual_my_def = int(clamp(my_def + _tier_bonus(my_dc) * 1.0, 40, 99))

    debug = {
        "rating_delta": rating_delta,
        "base_spread": base_spread,
        "coach_edge": coach_edge,
        "scheme_bonus": scheme_bonus,
        "home_bonus": home_bonus,
        "plan_bonus": plan_bonus,
        "spread_mu": spread_mu,
        "sigma": sigma,
        "final_margin": margin,
        "total_points": total_points
    }

    out = {
        "result": "W" if margin > 0 else "L",
        "score": f"{my_score}-{opp_score}",
        "margin": float(margin),
        "stats": {
            "qb_duel": [int(my_roster["QB"]), int(opp_rating)],
            "off_vs_def": [visual_my_off, int(clamp(opp_rating + _tier_bonus(opp_dc), 40, 99))],
            "def_vs_off": [visual_my_def, int(clamp(opp_rating + _tier_bonus(opp_oc), 40, 99))],
            "staff": [f"{int(my_oc)}/{int(my_dc)}", f"{int(opp_oc)}/{int(opp_dc)}"],
            "raw_roster": int((my_off + my_def) / 2)
        }
    }
    if return_debug:
        out["debug"] = debug
    return out

def engine_evolve_universe(opponents_db):
    # Lightweight league evolution: wins shift prestige, prestige shifts OVR, coaching changes on extremes
    for team, data in opponents_db.items():
        wins = int((data['OVR'] / 100) * 12) + random.randint(-2, 2)
        wins = clamp(wins, 0, 12)

        change = 0
        if wins >= 10: change = 3
        elif wins <= 4: change = -3
        data['Prestige'] = clamp(data['Prestige'] + change, 20, 99)

        if data['Prestige'] > 80 and wins < 6:
            data['Coaches'] = {"OC": random.randint(7, 9), "DC": random.randint(7, 9)}
        elif data['Prestige'] < 70 and wins > 9:
            data['Coaches'] = {"OC": random.randint(3, 6), "DC": random.randint(3, 6)}

        base_ovr = int(data['Prestige'] * 0.90)
        data['OVR'] = clamp(base_ovr + random.randint(-3, 3), 55, 99)
    return opponents_db

def engine_generate_portal_players():
    players = []
    for _ in range(3):
        players.append({"name": generate_name(), "pos": random.choice(POSITIONS),
                        "rating": random.randint(90, 99), "cost": random.randint(3_000_000, 6_000_000),
                        "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(3):
        players.append({"name": generate_name(), "pos": random.choice(POSITIONS),
                        "rating": random.randint(80, 89), "cost": random.randint(1_000_000, 2_500_000),
                        "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(4):
        players.append({"name": generate_name(), "pos": random.choice(POSITIONS),
                        "rating": random.randint(70, 78), "cost": random.randint(150_000, 500_000),
                        "trait": "None", "year": "Jr"})
    return players

def generate_hotspots():
    return {reg: random.sample(POSITIONS, 2) for reg in REGION_STRENGTH.keys()}

# ----------------------------
# ZONE 5: POSTSEASON (BRACKET LOGIC)
# ----------------------------
def init_playoff_bracket(user_rank, user_team_name):
    sorted_ai = [(t, d) for t, d in st.session_state.opponents_db.items() if t != user_team_name]
    sorted_ai.sort(key=lambda x: x[1]['OVR'], reverse=True)

    top_12 = []
    ai_idx = 0
    for r in range(1, 13):
        if r == user_rank:
            top_12.append(user_team_name)
        else:
            top_12.append(sorted_ai[ai_idx][0])
            ai_idx += 1

    r1 = [
        {"t1": top_12[4], "t2": top_12[11], "winner": None, "score": None},  # 5/12
        {"t1": top_12[5], "t2": top_12[10], "winner": None, "score": None},  # 6/11
        {"t1": top_12[6], "t2": top_12[9],  "winner": None, "score": None},  # 7/10
        {"t1": top_12[7], "t2": top_12[8],  "winner": None, "score": None},  # 8/9
    ]
    qf_seeds = [top_12[0], top_12[1], top_12[2], top_12[3]]
    return {"Type": "CFP", "Round": 1, "Matches": r1, "Seeds": top_12, "QF_Seeds": qf_seeds, "UserAlive": True, "Rank": user_rank}

def _team_profile_for_ai(team_name: str):
    d = st.session_state.opponents_db.get(team_name, None)
    if not d:
        return {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Prestige": 70}
    return d

def sim_ai_match(t1: str, t2: str):
    a = _team_profile_for_ai(t1)
    b = _team_profile_for_ai(t2)

    # Create minimal roster proxies for AI using OVR (so engine works consistently)
    # This keeps AI results “in-family” with the same engine.
    def proxy_roster(ovr):
        base = int(ovr)
        return {p: clamp(base + random.randint(-3, 3), 40, 99) for p in POSITIONS}

    staff_a = {"OC": {"off": a["Coaches"].get("OC", 5)}, "DC": {"def": a["Coaches"].get("DC", 5)}, "HC": {"off": 6, "trait": "None"}}
    staff_b = {"OC": {"off": b["Coaches"].get("OC", 5)}, "DC": {"def": b["Coaches"].get("DC", 5)}, "HC": {"off": 6, "trait": "None"}}

    res = engine_play_game(
        my_rating=float(a["OVR"]),
        opp_rating=float(b["OVR"]),
        staff=staff_a,
        schemes={"Off": a.get("Off", "Pro Style"), "Def": a.get("Def", "Man Coverage")},
        opp_schemes={"Off": b.get("Off", "Pro Style"), "Def": b.get("Def", "Man Coverage")},
        game_plan="Normal",
        opp_coaches=b.get("Coaches", {"OC": 5, "DC": 5}),
        is_home=False,
        is_rival=False,
        stadium_lvl=8,
        my_roster=proxy_roster(a["OVR"]),
        return_debug=False
    )
    winner = t1 if res["result"] == "W" else t2
    return winner, res["score"]

def postseason_advance(current):
    """
    Returns (new_round, new_matches) after all winners decided in current['Matches'].
    """
    rnd = int(current["Round"])
    winners = [m["winner"] for m in current["Matches"] if m.get("winner")]
    if len(winners) != len(current["Matches"]):
        return None

    if rnd == 1:
        seeds = current["QF_Seeds"]  # 1-4
        # Pair 1-4 vs reversed winners list (simple bracket)
        new_matches = []
        for i in range(4):
            new_matches.append({"t1": seeds[i], "t2": winners[3 - i], "winner": None, "score": None})
        return 2, new_matches

    if rnd == 2:
        # Semis: 0 vs 3, 1 vs 2
        return 3, [
            {"t1": winners[0], "t2": winners[3], "winner": None, "score": None},
            {"t1": winners[1], "t2": winners[2], "winner": None, "score": None},
        ]

    if rnd == 3:
        # Title
        return 4, [{"t1": winners[0], "t2": winners[1], "winner": None, "score": None}]

    return None

# ----------------------------
# ZONE 6: OFFSEASON RECRUITING MODULE (3 STEPS)
# ----------------------------
def build_outreach_default_shares(needs: list, hot: list):
    # Start with a reasonable baseline; then tilt to needs + pipeline
    shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
    for p in POSITIONS:
        if p in needs:
            shares[p] += 4.0
        if p in hot:
            shares[p] += 2.0
    total = sum(shares.values())
    return {p: (shares[p] / total) * 100.0 for p in POSITIONS}

def normalize_shares(shares: dict):
    total = sum(max(0.0, float(v)) for v in shares.values())
    if total <= 0:
        return {p: 100.0 / len(POSITIONS) for p in POSITIONS}
    return {p: (max(0.0, float(v)) / total) * 100.0 for p in POSITIONS}

def outreach_points_from_spend(amount: float, inflation: float):
    """
    Converts money into a 'recruiting points' scale with diminishing returns.
    """
    # scale so ~ $1M produces a few points
    x = amount / (1_000_000 * inflation)
    return (x ** 0.85) * 10.0

def process_outreach_to_roster_updates(allocations: dict, staff: dict, prestige: int, inflation: float, hotspots: list, needs: list):
    """
    Overall HS outreach -> roster deltas + gems + booster bonus.
    This is your Step 2 “position investment” system.
    """
    results = {"roster_updates": {}, "gems": [], "booster_bonus": 0}

    scout = int(staff.get("Scout", {}).get("recruit", 3))
    hc_trait = staff.get("HC", {}).get("trait", "None")

    for pos, amt in allocations.items():
        pts = outreach_points_from_spend(float(amt), inflation)

        pipeline_bonus = 1.0 + (0.12 if pos in hotspots else 0.0)
        need_bonus = 1.0 + (0.18 if pos in needs else 0.0)
        scout_bonus = 1.0 + (0.04 * max(0, scout - 5))
        prestige_bonus = clamp((prestige / 75.0) ** 0.30, 0.88, 1.18)

        # change scale: baseline attrition handled elsewhere; this is “class impact”
        change = (pts / 8.0) * pipeline_bonus * need_bonus * scout_bonus * prestige_bonus
        change = clamp(change, 0.0, 12.0)

        # GEM chance: increases with need + pipeline + good staff
        gem_chance = 0.07
        if pos in needs: gem_chance += 0.06
        if pos in hotspots: gem_chance += 0.04
        if hc_trait == "Recruiter": gem_chance += 0.05
        gem_chance += clamp((scout - 5) * 0.02, 0.0, 0.08)

        if float(amt) >= (1_200_000 * inflation) and random.random() < gem_chance:
            new_star = generate_star_player(pos, 1)
            new_star["name"] += " (GEM)"
            results["gems"].append(new_star)
            results["booster_bonus"] += random.randint(200_000, 700_000)
            change = clamp(change + 4.0, 0.0, 16.0)

        results["roster_updates"][pos] = float(change)

    return results

def generate_top8_prospects(needs: list, hotspots: list):
    prospects = []
    for i in range(8):
        pos = random.choice(POSITIONS)
        # bias a bit toward needs/hotspots
        if random.random() < 0.45 and needs:
            pos = random.choice(needs)
        if random.random() < 0.25 and hotspots:
            pos = random.choice(hotspots)

        rating = random.randint(88, 99)
        base_ask = random.randint(750_000, 3_500_000)
        trait = random.choice(TRAITS)

        # pick AI contenders
        contenders = random.sample([t for t in ALL_TEAMS if t != st.session_state.team_name], 3)
        prospects.append({
            "id": 10_000 + i,
            "name": generate_name(),
            "pos": pos,
            "rating": rating,
            "trait": trait,
            "base_ask": base_ask,
            "contenders": contenders,
            "resolved": False,
            "signed": None,
            "user_offer": 0
        })
    return prospects

def ai_offers_for_prospect(prospect):
    offers = []
    for t in prospect["contenders"]:
        d = _team_profile_for_ai(t)
        prestige = d.get("Prestige", 70)
        ovr = d.get("OVR", 80)
        # AI willingness: prestige + ovr → higher offers
        factor = (prestige / 80.0) * 0.6 + (ovr / 90.0) * 0.4
        noise = random.uniform(0.85, 1.25)
        offer = int(prospect["base_ask"] * clamp(factor, 0.7, 1.35) * noise)
        offers.append((t, offer))
    offers.sort(key=lambda x: x[1], reverse=True)
    return offers

def win_prob_top8(prospect, user_offer, staff, prestige, outreach_allocations, inflation):
    scout = int(staff.get("Scout", {}).get("recruit", 3))
    hc_trait = staff.get("HC", {}).get("trait", "None")

    ai_offers = ai_offers_for_prospect(prospect)
    best_ai_offer = ai_offers[0][1] if ai_offers else prospect["base_ask"]

    # offer edge
    offer_edge = (user_offer - best_ai_offer) / 1_000_000.0  # scale in millions

    # outreach edge for that position
    spend = float(outreach_allocations.get(prospect["pos"], 0))
    pts = outreach_points_from_spend(spend, inflation)
    outreach_edge = (pts / 10.0)  # 0..maybe 3

    # staff + prestige
    staff_edge = (scout - 5) * 0.10
    if hc_trait == "Recruiter":
        staff_edge += 0.18

    prestige_edge = clamp((prestige - 70) / 50.0, -0.25, 0.35)

    # Base chance for top 8 is intentionally tough
    x = -0.35 + (0.65 * offer_edge) + (0.35 * outreach_edge) + staff_edge + prestige_edge
    p = 1.0 / (1.0 + math.exp(-x))
    return clamp(p, 0.05, 0.90), ai_offers

# ----------------------------
# ZONE 7: STATE MANAGEMENT
# ----------------------------
def initialize_game_state():
    if "game_state" not in st.session_state:
        st.session_state.game_state = "SETUP"
        st.session_state.year = 2026
        st.session_state.inflation = 1.0

        # Program
        st.session_state.team_name = None
        st.session_state.team_conf = None
        st.session_state.team_rival = None
        st.session_state.team_color = "#333333"
        st.session_state.home_region = "South"
        st.session_state.school_tier = 3

        # Economy
        st.session_state.budget = 0
        st.session_state.revenue_report = None

        # Program health
        st.session_state.prestige = 50
        st.session_state.job_security = 80
        st.session_state.expected_wins = 6
        st.session_state.tenure = 1

        # Roster & staff
        st.session_state.roster = {p: 75 for p in POSITIONS}
        st.session_state.active_transfers = {p: False for p in POSITIONS}
        st.session_state.staff = {}
        st.session_state.candidates = {}
        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)

        # Facilities
        st.session_state.facilities = {"Marketing": 1, "Training": 1, "Stadium": 1}

        # League
        st.session_state.opponents_db = {}
        st.session_state.hotspots = generate_hotspots()

        # Strategy
        st.session_state.my_schemes = {"Off": "Pro Style", "Def": "Man Coverage"}
        st.session_state.game_plan = "Normal"

        # Season
        st.session_state.schedule = []
        st.session_state.week_index = 0
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.season_complete = False  # regular season complete

        # Postseason
        st.session_state.postseason_data = {"Type": None}
        st.session_state.postseason_complete = False

        # Offseason
        st.session_state.offseason_step = 1  # 1 NIL, 2 Outreach, 3 Top8, 4 Finalize
        st.session_state.portal_players = []
        st.session_state.outreach_total = 0
        st.session_state.outreach_alloc = {p: 0 for p in POSITIONS}
        st.session_state.top8 = []
        st.session_state.top8_results = []
        st.session_state.prev_outreach_alloc = None

        # Career
        st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
        st.session_state.history = []
        st.session_state.news = []

    # safety for future edits
    for k, v in {
        "inflation": 1.0,
        "revenue_report": None,
        "postseason_data": {"Type": None},
        "news": [],
        "offseason_step": 1
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

initialize_game_state()

# ----------------------------
# ZONE 8: UI PAGES
# ----------------------------
def run_setup():
    st.title("🏆 College Football Mogul V6")
    st.markdown("### Dynasty Mode (Jan 2026)")

    c1, c2 = st.columns(2)
    ad_name = c1.text_input("AD Name", "Coach Prime")
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"])

    sorted_teams = sorted(REAL_WORLD_INIT.keys()) + sorted([t for t in ALL_TEAMS if t not in REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)

    if team in REAL_WORLD_INIT:
        d = REAL_WORLD_INIT[team]
        tier = d["Tier"]
        budget = 25_000_000 if tier == 1 else (15_000_000 if tier == 2 else 5_000_000)
        conf = get_conference(team)
        rival = d.get("Rival", "Rival")
        base_talent = d.get("Talent", 74)
        base_prestige = d.get("Prestige", 60)
    else:
        tier = 3
        budget = 5_000_000
        conf = get_conference(team)
        rival = "Rival"
        base_talent = 74
        base_prestige = 60

    expect = 10 if tier == 1 else (8 if tier == 2 else (6 if tier == 3 else 4))
    st.info(f"**{team}** | Conf: {conf} | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival}")
    st.caption(f"Expectation: {expect}+ Wins")

    if st.button("Start Dynasty", type="primary"):
        st.session_state.ad_name = ad_name
        st.session_state.team_name = team
        st.session_state.team_color = TEAMS_DB.get(team, {}).get("color", "#333333")
        st.session_state.team_conf = conf
        st.session_state.team_rival = rival
        st.session_state.school_tier = tier
        st.session_state.expected_wins = expect
        st.session_state.prestige = base_prestige
        st.session_state.home_region = "South"

        # budget difficulty
        diff_mult = 1.0
        if diff == "Hard": diff_mult = 0.75
        if diff == "Easy": diff_mult = 1.25
        st.session_state.budget = int(budget * diff_mult)

        st.session_state.roster = engine_generate_roster(tier, base_talent)
        st.session_state.active_transfers = {p: False for p in POSITIONS}
        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)

        # Staff
        st.session_state.staff = {}
        for r in ["HC", "OC", "DC", "Scout"]:
            st.session_state.staff[r] = engine_generate_coach(r, tier)

        # Facilities
        val = 10 if tier == 1 else 6
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}

        # League
        st.session_state.opponents_db = {}
        for opp in ALL_TEAMS:
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                st.session_state.opponents_db[opp] = {
                    "Prestige": data["Prestige"],
                    "OVR": data["Talent"],
                    "Off": random.choice(SCHEMES["Offense"]),
                    "Def": random.choice(SCHEMES["Defense"]),
                    "Coaches": {"OC": random.randint(5, 9), "DC": random.randint(5, 9)}
                }
            else:
                pres = 85 if opp in CONFERENCES["SEC"] else 65
                ovr = 82 if opp in CONFERENCES["SEC"] else 70
                st.session_state.opponents_db[opp] = {
                    "Prestige": pres, "OVR": ovr, "Off": "Pro Style", "Def": "Man Coverage",
                    "Coaches": {"OC": 5, "DC": 5}
                }

        st.session_state.hotspots = generate_hotspots()
        st.session_state.schedule = engine_generate_schedule(team, conf, rival)

        # Season reset
        st.session_state.week_index = 0
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.season_complete = False

        # Postseason / offseason reset
        st.session_state.postseason_data = {"Type": None}
        st.session_state.postseason_complete = False
        st.session_state.offseason_step = 1
        st.session_state.portal_players = []
        st.session_state.outreach_total = 0
        st.session_state.outreach_alloc = {p: 0 for p in POSITIONS}
        st.session_state.top8 = []
        st.session_state.top8_results = []

        add_news(f"{team} hires {st.session_state.staff['HC']['name']} as HC.")
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

def show_staff_tab():
    st.markdown("### 🧢 Current Staff")
    cols = st.columns(4)
    roles = ["HC", "OC", "DC", "Scout"]

    for i, role in enumerate(roles):
        with cols[i]:
            if role in st.session_state.staff:
                c = st.session_state.staff[role]
                rtg = role_rating(c, role)
                badge_cls = "badge-tier-s" if rtg >= 8 else ("badge-tier-a" if rtg >= 5 else "badge-tier-f")
                st.markdown(f"""
                <div class='staff-card'>
                    <div class='staff-role'>{role}</div>
                    <div class='staff-name'>{c['name']}</div>
                    <div><span class='badge {badge_cls}'>RATING: {rtg}</span>
                        <span class='badge badge-trait'>{c.get('trait','None')}</span></div>
                    <div class='small-muted'>{helper_format_cash(c.get('salary',0))}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Fire", key=f"fire_{role}"):
                    add_news(f"{st.session_state.team_name} parts ways with {c['name']} ({role}).")
                    del st.session_state.staff[role]
                    # IMPORTANT: clear market cache so role shows offers immediately
                    if role in st.session_state.candidates:
                        del st.session_state.candidates[role]
                    st.rerun()
            else:
                st.warning(f"{role} VACANT")

    st.divider()
    st.markdown("### 📋 Job Market")
    vacancies = [r for r in roles if r not in st.session_state.staff]
    if not vacancies:
        st.info("No vacancies. You're fully staffed.")
        return

    for role in vacancies:
        if role not in st.session_state.candidates:
            st.session_state.candidates[role] = [engine_generate_coach(role, random.randint(1, 3)) for _ in range(3)]

        cols = st.columns(3)
        for i, cand in enumerate(st.session_state.candidates[role]):
            with cols[i]:
                rr = role_rating(cand, role)
                vis_rate = f"{rr}" if cand["scouted"] else f"{get_letter_grade(rr)}"
                vis_trait = cand["trait"] if cand["scouted"] else "???"
                st.markdown(f"""
                <div class='staff-card'>
                    <div class='staff-name'>{cand['name']}</div>
                    <div class='small-muted'>{cand['history']}</div>
                    <div style='margin:6px 0'>
                        <span class='badge badge-trait'>{role} OVR: {vis_rate}</span>
                        <span class='badge badge-trait'>Trait: {vis_trait}</span>
                    </div>
                    <div style='font-weight:bold'>{helper_format_cash(cand['salary'])}</div>
                </div>
                """, unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                if b1.button("Hire", key=f"h_{role}_{i}"):
                    if st.session_state.budget >= cand["salary"]:
                        st.session_state.budget -= cand["salary"]
                        st.session_state.staff[role] = cand
                        add_news(f"{st.session_state.team_name} hires {cand['name']} as {role}.")
                        del st.session_state.candidates[role]
                        st.rerun()
                    else:
                        st.error("Not enough budget.")
                if (not cand["scouted"]) and b2.button("Scout ($25k)", key=f"sc_{role}_{i}"):
                    if st.session_state.budget >= 25_000:
                        st.session_state.budget -= 25_000
                        cand["scouted"] = True
                        st.rerun()
                    else:
                        st.error("Not enough budget.")

        if st.button("Promote GA (Free)", key=f"ga_{role}"):
            ga = generate_ga_coach(role)
            st.session_state.staff[role] = ga
            add_news(f"{st.session_state.team_name} promotes {ga['name']} to {role}.")
            if role in st.session_state.candidates:
                del st.session_state.candidates[role]
            st.rerun()

def show_facilities_tab():
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Marketing", st.session_state.facilities["Marketing"], delta="Revenue +$2M/yr")
        if st.button("Upgrade ($1M)", key="fac_m"):
            if st.session_state.budget >= 1_000_000:
                st.session_state.budget -= 1_000_000
                st.session_state.facilities["Marketing"] += 1
                add_news("Marketing upgraded. Boosters are pleased.")
                st.rerun()
            else:
                st.error("Not enough budget.")

    with c2:
        st.metric("Training", st.session_state.facilities["Training"], delta="Team OVR Boost")
        if st.button("Upgrade ($3M)", key="fac_t"):
            if st.session_state.budget >= 3_000_000:
                st.session_state.budget -= 3_000_000
                st.session_state.facilities["Training"] += 1
                add_news("Training upgraded. Player development accelerates.")
                st.rerun()
            else:
                st.error("Not enough budget.")

    with c3:
        st.metric("Stadium", st.session_state.facilities["Stadium"], delta="Home Field + Prestige")
        if st.button("Upgrade ($10M)", key="fac_s"):
            if st.session_state.budget >= 10_000_000:
                st.session_state.budget -= 10_000_000
                st.session_state.facilities["Stadium"] += 1
                st.session_state.prestige = clamp(st.session_state.prestige + 1, 20, 99)
                add_news("Stadium upgraded. Home advantage grows.")
                st.rerun()
            else:
                st.error("Not enough budget.")

def _render_schedule_cards():
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Weeks 1–6")
        for i in range(6):
            opp = st.session_state.schedule[i]
            played = next((x for x in st.session_state.season_logs if x["Week"] == i + 1), None)
            is_rival = opp == st.session_state.team_rival
            if played:
                res = "W" if played["Score"].startswith("W") else "L"
                css = "game-card-win" if res == "W" else "game-card-loss"
                st.markdown(f"<div class='game-card {css}'>Week {i+1}: {played['Score']} vs {opp}</div>", unsafe_allow_html=True)
            else:
                css = "game-card-rival" if is_rival else "game-card-pending"
                st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)

    with c2:
        st.caption("Weeks 7–12")
        for i in range(6, 12):
            opp = st.session_state.schedule[i]
            played = next((x for x in st.session_state.season_logs if x["Week"] == i + 1), None)
            is_rival = opp == st.session_state.team_rival
            if played:
                res = "W" if played["Score"].startswith("W") else "L"
                css = "game-card-win" if res == "W" else "game-card-loss"
                st.markdown(f"<div class='game-card {css}'>Week {i+1}: {played['Score']} vs {opp}</div>", unsafe_allow_html=True)
            else:
                css = "game-card-rival" if is_rival else "game-card-pending"
                st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)

def play_one_week(wk_index: int):
    opp = st.session_state.schedule[wk_index]
    opp_data = st.session_state.opponents_db.get(opp, {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}})
    is_rival = (opp == st.session_state.team_rival)

    team_rating = engine_team_rating(st.session_state.roster, st.session_state.facilities["Training"])

    res = engine_play_game(
        my_rating=team_rating,
        opp_rating=opp_data["OVR"],
        staff=st.session_state.staff,
        schemes=st.session_state.my_schemes,
        opp_schemes={"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
        game_plan=st.session_state.game_plan,
        opp_coaches=opp_data.get("Coaches", {"OC": 5, "DC": 5}),
        is_home=(wk_index % 2 == 0),
        is_rival=is_rival,
        stadium_lvl=st.session_state.facilities["Stadium"],
        my_roster=st.session_state.roster,
        return_debug=True
    )

    if res["result"] == "W":
        st.session_state.record["w"] += 1
        st.session_state.career_stats["w"] += 1
        st.session_state.job_security = clamp(st.session_state.job_security + (5 if is_rival else 2), 0, 100)
        add_news(f"{st.session_state.team_name} wins Week {wk_index+1} vs {opp} ({res['score']}).")
    else:
        st.session_state.record["l"] += 1
        st.session_state.career_stats["l"] += 1
        pen = 2 if st.session_state.tenure <= 2 else 5
        st.session_state.job_security = clamp(st.session_state.job_security - pen, 0, 100)
        add_news(f"{st.session_state.team_name} loses Week {wk_index+1} vs {opp} ({res['score']}).")

    st.session_state.season_logs.append({
        "Week": wk_index + 1,
        "Opponent": opp,
        "OppOVR": opp_data.get("OVR", 80),
        "OppSchemes": {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
        "OppCoaches": opp_data.get("Coaches", {"OC": 5, "DC": 5}),
        "Home": (wk_index % 2 == 0),
        "Rival": is_rival,
        "Score": f"{res['result']} {res['score']}",
        "Stats": res["stats"],
        "Debug": res.get("debug", {})
    })

def end_regular_season_if_needed():
    if st.session_state.week_index >= 12 and not st.session_state.season_complete:
        st.session_state.season_complete = True
        add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")

        # Annual revenue injection (moved here per your request)
        rev = engine_calculate_revenue(
            st.session_state.school_tier,
            st.session_state.facilities["Marketing"],
            st.session_state.inflation
        )
        st.session_state.budget += rev
        st.session_state.revenue_report = f"End-of-Season Revenue: +{helper_format_cash(rev)}"
        add_news(f"Boosters + TV money deliver {helper_format_cash(rev)} into the war chest.")

def show_season_weekly_tab():
    if len(st.session_state.staff) < 4:
        st.error("Fill Staff First (HC/OC/DC/Scout).")
        return

    if not st.session_state.schedule:
        st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)

    st.session_state.game_plan = st.selectbox(
        "Weekly Gameplan",
        ["Conservative", "Normal", "Aggressive"],
        index=["Conservative", "Normal", "Aggressive"].index(st.session_state.game_plan)
    )

    _render_schedule_cards()

    st.divider()

    st.markdown("### 🗞️ News Feed")
    with st.container():
        st.markdown("<div class='news-box'>", unsafe_allow_html=True)
        if st.session_state.news:
            for n in st.session_state.news[:8]:
                st.markdown(f"<div class='news-item'>• {n}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='news-item'>• No headlines yet.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Next game controls
    if not st.session_state.season_complete:
        wk = st.session_state.week_index
        opp = st.session_state.schedule[wk]
        opp_data = st.session_state.opponents_db.get(opp, {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}})
        is_riv = (opp == st.session_state.team_rival)
        team_rating = engine_team_rating(st.session_state.roster, st.session_state.facilities["Training"])

        st.subheader(f"Next Game: Week {wk+1} vs {opp} (Opp OVR: {opp_data.get('OVR',80)})")
        st.caption(f"Your Team OVR: {team_rating} | Opp Schemes: {opp_data.get('Off','Pro Style')} / {opp_data.get('Def','Man Coverage')}")

        if is_riv:
            st.warning("RIVALRY WEEK: more chaos + bigger stakes.")

        cA, cB = st.columns(2)
        if cA.button("🏈 PLAY WEEK", type="primary"):
            play_one_week(wk)
            st.session_state.week_index += 1
            end_regular_season_if_needed()
            st.rerun()

        if cB.button("⏩ SIM REST OF SEASON"):
            while not st.session_state.season_complete:
                wk2 = st.session_state.week_index
                if wk2 >= 12:
                    break
                play_one_week(wk2)
                st.session_state.week_index += 1
                end_regular_season_if_needed()
            st.rerun()

    # Recap + explainers
    if st.session_state.season_logs:
        st.write("### Played Games (Details)")
        for log in st.session_state.season_logs[::-1][:6]:
            res = "W" if log["Score"].startswith("W") else "L"
            css = "game-card-win" if res == "W" else "game-card-loss"
            s = log["Stats"]
            st.markdown(f"""
            <div class='game-card {css}'>
                <div class='card-header'>
                    <span>{log['Score']} vs {log['Opponent']}</span>
                    <span>Opp OVR: {log.get('OppOVR','?')}</span>
                </div>
                <div class='stat-grid'>
                    <div class='stat-row'><span>🔥 QB Duel</span><span>{s['qb_duel'][0]} vs {s['qb_duel'][1]}</span></div>
                    <div class='stat-row'><span>⚔️ Off vs Def</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div>
                    <div class='stat-row'><span>🛡️ Def vs Off</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div>
                    <div class='stat-row'><span>🧠 Staff</span><span>{s['staff'][0]} vs {s['staff'][1]}</span></div>
                    <div class='stat-row'><span>💪 Raw Talent</span><span>{s['raw_roster']}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            dbg = log.get("Debug", {})
            with st.expander("Why this result happened (engine breakdown)"):
                if not dbg:
                    st.write("No debug data.")
                else:
                    st.write(f"**Rating Delta:** {dbg.get('rating_delta',0):.1f} → Base Spread: {dbg.get('base_spread',0):.1f}")
                    st.write(f"**Coach Edge:** {dbg.get('coach_edge',0):.1f} | **Scheme Bonus:** {dbg.get('scheme_bonus',0):.1f} | **Home:** {dbg.get('home_bonus',0):.1f} | **Plan:** {dbg.get('plan_bonus',0):.1f}")
                    st.write(f"**Expected Spread (μ):** {dbg.get('spread_mu',0):.1f} | **Variance (σ):** {dbg.get('sigma',0):.1f}")
                    st.write(f"**Final Margin:** {dbg.get('final_margin',0):.1f} | **Total Points:** {dbg.get('total_points',0):.1f}")
                    st.caption("Tip: increase roster gaps and coaching edges to reduce “coin-flip” games; rivalry + aggressive increases chaos.")

    if st.session_state.season_complete:
        st.divider()
        st.success(f"Regular season complete: {st.session_state.record['w']}-{st.session_state.record['l']}")
        if st.session_state.revenue_report:
            st.markdown(f"<div class='finance-alert'>💰 {st.session_state.revenue_report}</div>", unsafe_allow_html=True)

        if st.button("Proceed to Postseason", type="primary"):
            wins = st.session_state.record["w"]
            rank = 130 - (wins * 10)
            rank = clamp(rank, 1, 130)

            if rank <= 12:
                st.session_state.postseason_data = init_playoff_bracket(rank, st.session_state.team_name)
            else:
                bowl = get_bowl_name(rank)
                opp = random.choice([t for t in ALL_TEAMS if t != st.session_state.team_name])
                st.session_state.postseason_data = {"Type": "BOWL", "Bowl": bowl, "Rank": rank, "Opponent": opp, "OppData": _team_profile_for_ai(opp)}

            st.session_state.postseason_complete = False
            st.session_state.game_state = "POSTSEASON"
            st.rerun()

def show_dashboard():
    thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < thresh:
        st.session_state.game_state = "FIRED"
        st.rerun()

    if st.session_state.revenue_report:
        st.markdown(f"<div class='finance-alert'>💰 {st.session_state.revenue_report}</div>", unsafe_allow_html=True)

    sec = st.session_state.job_security
    sec_cls = "security-safe" if sec > 75 else ("security-warm" if sec > 40 else "security-hot")

    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Security: <span class='{sec_cls}'>{sec}%</span></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 5px; color: white;'>"
        f"<h2 style='margin:0'>{st.session_state.team_name}</h2></div>",
        unsafe_allow_html=True
    )

    team_ovr = engine_team_rating(st.session_state.roster, st.session_state.facilities["Training"])
    raw = int(sum(st.session_state.roster.values()) / len(POSITIONS))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("Team OVR", team_ovr, f"Raw: {raw}")
    c3.metric("Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")
    c4.metric("Legacy Score", calculate_saban_score(st.session_state.career_stats, st.session_state.prestige))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Strategy", "Staff", "Facilities", "Season (Weekly)", "Legacy"])

    with tab1:
        c1, c2 = st.columns(2)
        st.session_state.my_schemes["Off"] = c1.selectbox("Offense", SCHEMES["Offense"], index=SCHEMES["Offense"].index(st.session_state.my_schemes.get("Off","Pro Style")))
        st.session_state.my_schemes["Def"] = c2.selectbox("Defense", SCHEMES["Defense"], index=SCHEMES["Defense"].index(st.session_state.my_schemes.get("Def","Man Coverage")))
        st.write("Unit Strength")
        for p, v in st.session_state.roster.items():
            lab = f"{p}: {int(v)}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.progress(min(1.0, float(v) / 100.0), lab)

    with tab2:
        show_staff_tab()

    with tab3:
        show_facilities_tab()

    with tab4:
        show_season_weekly_tab()

    with tab5:
        cs = st.session_state.career_stats
        st.subheader("🏛️ Trophy Case")
        st.write(f"**Titles:** {cs['titles']}  |  **Bowl W-L:** {cs['bowl_w']}-{cs['bowl_l']}  |  **Career W-L:** {cs['w']}-{cs['l']}")
        st.write(f"**Prestige:** {st.session_state.prestige}  |  **Legacy:** {calculate_saban_score(cs, st.session_state.prestige)}")
        st.divider()
        st.subheader("📚 Season History")
        if st.session_state.history:
            st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
        else:
            st.info("No completed seasons yet.")

def show_postseason():
    st.title("Postseason Hub")
    data = st.session_state.postseason_data

    if data.get("Type") == "BOWL":
        st.markdown(f"<div class='bracket-box'><h3>{data['Bowl']}</h3><h1>VS {data['Opponent']}</h1></div>", unsafe_allow_html=True)
        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            opp = data["Opponent"]
            opp_data = _team_profile_for_ai(opp)

            team_rating = engine_team_rating(st.session_state.roster, st.session_state.facilities["Training"])

            res = engine_play_game(
                my_rating=team_rating,
                opp_rating=opp_data["OVR"],
                staff=st.session_state.staff,
                schemes=st.session_state.my_schemes,
                opp_schemes={"Off": opp_data.get("Off","Pro Style"), "Def": opp_data.get("Def","Man Coverage")},
                game_plan=st.session_state.game_plan,
                opp_coaches=opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                is_home=False, is_rival=False, stadium_lvl=10,
                my_roster=st.session_state.roster,
                return_debug=False
            )

            wins = st.session_state.record["w"] + (1 if res["result"] == "W" else 0)
            losses = st.session_state.record["l"] + (1 if res["result"] == "L" else 0)

            if res["result"] == "W":
                st.session_state.budget += 2_000_000
                st.session_state.career_stats["bowl_w"] += 1
                st.toast("🎳 BOWL WIN BONUS: $2M")
                add_news(f"{st.session_state.team_name} wins the {data['Bowl']} ({res['score']}).")
            else:
                st.session_state.career_stats["bowl_l"] += 1
                add_news(f"{st.session_state.team_name} falls in the {data['Bowl']} ({res['score']}).")

            # expectation booster
            delta = wins - st.session_state.expected_wins
            if delta > 0:
                st.session_state.budget += delta * 1_000_000
            elif delta < 0:
                st.session_state.budget -= abs(delta) * 500_000

            st.session_state.history.append({
                "Year": st.session_state.year,
                "Record": f"{wins}-{losses}",
                "Rank": f"#{data['Rank']}",
                "Bowl": data["Bowl"]
            })

            st.session_state.postseason_complete = True
            st.session_state.game_state = "OFFSEASON"
            st.session_state.offseason_step = 1
            st.rerun()

    elif data.get("Type") == "CFP":
        round_names = {1: "Opening Round", 2: "Quarterfinals", 3: "Semifinals", 4: "Championship"}
        rnd = int(data.get("Round", 1))
        st.header(f"CFP Round: {round_names.get(rnd, 'CFP')} (Seed #{data.get('Rank','?')})")

        st.write("--- Bracket Status ---")
        for m in data["Matches"]:
            if m.get("winner"):
                st.markdown(f"<div class='bracket-row'>✅ {m['winner']} advances ({m.get('score','')})</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bracket-row'>{m['t1']} vs {m['t2']}</div>", unsafe_allow_html=True)

        # find user's game
        user_match = None
        for m in data["Matches"]:
            if m["t1"] == st.session_state.team_name or m["t2"] == st.session_state.team_name:
                user_match = m
                break

        def resolve_round(user_play: bool):
            # Resolve all matches in current round. If user_play, user match uses your roster engine.
            next_round_winners = []
            for m in data["Matches"]:
                if m.get("winner"):
                    next_round_winners.append(m["winner"])
                    continue

                t1, t2 = m["t1"], m["t2"]
                if user_play and user_match is not None and m is user_match:
                    opp = t2 if t1 == st.session_state.team_name else t1
                    opp_data = _team_profile_for_ai(opp)
                    team_rating = engine_team_rating(st.session_state.roster, st.session_state.facilities["Training"])
                    res = engine_play_game(
                        my_rating=team_rating,
                        opp_rating=opp_data["OVR"],
                        staff=st.session_state.staff,
                        schemes=st.session_state.my_schemes,
                        opp_schemes={"Off": opp_data.get("Off","Pro Style"), "Def": opp_data.get("Def","Man Coverage")},
                        game_plan=st.session_state.game_plan,
                        opp_coaches=opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                        is_home=False, is_rival=False, stadium_lvl=10,
                        my_roster=st.session_state.roster,
                        return_debug=False
                    )
                    if res["result"] == "W":
                        m["winner"] = st.session_state.team_name
                        m["score"] = res["score"]
                        next_round_winners.append(st.session_state.team_name)
                        st.toast("VICTORY! Advancing...")
                        add_news(f"{st.session_state.team_name} advances in the CFP ({res['score']}).")
                    else:
                        m["winner"] = opp
                        m["score"] = res["score"]
                        next_round_winners.append(opp)
                        data["UserAlive"] = False
                        st.error(f"Eliminated by {opp}")
                        add_news(f"{st.session_state.team_name} eliminated by {opp} ({res['score']}).")
                else:
                    winner, score = sim_ai_match(t1, t2)
                    m["winner"] = winner
                    m["score"] = score
                    next_round_winners.append(winner)

            # Advance if user alive and round resolved
            adv = postseason_advance(data)
            if adv is None:
                return

            new_round, new_matches = adv
            data["Round"] = new_round
            data["Matches"] = new_matches

        if data.get("UserAlive", True):
            if user_match:
                opp = user_match["t2"] if user_match["t1"] == st.session_state.team_name else user_match["t1"]
                opp_ovr = _team_profile_for_ai(opp).get("OVR", 88)
                st.info(f"Your Matchup: vs {opp} (OVR {opp_ovr})")

                if st.button("PLAY PLAYOFF GAME 🏈", type="primary"):
                    resolve_round(user_play=True)

                    # Title check
                    if data.get("Round") == 4 and data.get("Matches") and data["Matches"][0].get("winner"):
                        champ = data["Matches"][0]["winner"]
                        if champ == st.session_state.team_name:
                            st.session_state.budget += 50_000_000
                            st.session_state.career_stats["titles"] += 1
                            st.balloons()
                            st.success("🏆 NATIONAL CHAMPIONS!")
                            add_news(f"{st.session_state.team_name} wins the NATIONAL TITLE!")
                            st.session_state.history.append({"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Bowl": "National Title"})
                            st.session_state.postseason_complete = True
                            st.session_state.game_state = "OFFSEASON"
                            st.session_state.offseason_step = 1
                        else:
                            # if user somehow wasn't champ, they lost earlier
                            pass
                    st.rerun()

            else:
                st.success("You have a BYE week.")
                if st.button("Simulate Round", type="primary"):
                    resolve_round(user_play=False)
                    st.rerun()

        else:
            st.warning("Your CFP run is over.")
            st.session_state.history.append({"Year": st.session_state.year, "Record": "Playoff Loss", "Rank": f"#{data.get('Rank','?')}", "Bowl": "CFP"})
            st.session_state.postseason_complete = True
            st.session_state.game_state = "OFFSEASON"
            st.session_state.offseason_step = 1
            if st.button("Continue to Offseason", type="primary"):
                st.rerun()

def show_offseason():
    st.title("Offseason Hub")
    st.markdown(f"<div class='nil-alert'>💰 War Chest: {helper_format_cash(st.session_state.budget)} | Step {st.session_state.offseason_step}/4</div>", unsafe_allow_html=True)

    steps = {
        1: "1) NIL Prospects (Portal)",
        2: "2) HS Outreach (Position Investment)",
        3: "3) Top 8 Prospect Battles",
        4: "4) Finalize Class & Advance Year"
    }
    st.write("**Offseason Roadmap**")
    st.write(" → ".join([steps[i] for i in [1,2,3,4]]))
    st.divider()

    step = int(st.session_state.offseason_step)

    # ----------------
    # STEP 1: NIL / PORTAL
    # ----------------
    if step == 1:
        st.subheader("1) NIL Prospects — Transfer Portal")
        if not st.session_state.portal_players:
            st.session_state.portal_players = engine_generate_portal_players()

        st.write(f"Budget: {helper_format_cash(st.session_state.budget)}")
        for i, p in enumerate(list(st.session_state.portal_players)):
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{p['pos']} {p['name']}** ({p['rating']}) — {p['trait']}  |  NIL: {helper_format_cash(p['cost'])}")
            if c2.button("Sign", key=f"portal_sign_{i}"):
                if st.session_state.budget >= p["cost"]:
                    st.session_state.budget -= p["cost"]
                    st.session_state.roster[p["pos"]] = max(st.session_state.roster[p["pos"]], p["rating"])
                    st.session_state.active_transfers[p["pos"]] = True
                    st.session_state.portal_players.pop(i)
                    add_news(f"{st.session_state.team_name} signs portal {p['pos']} {p['name']} ({p['rating']}).")
                    st.rerun()
                else:
                    st.error("Not enough budget.")

        cA, cB = st.columns(2)
        if cA.button("Continue to HS Outreach", type="primary"):
            st.session_state.offseason_step = 2
            st.rerun()
        if cB.button("Skip Portal"):
            st.session_state.offseason_step = 2
            st.rerun()

    # ----------------
    # STEP 2: OUTREACH (FAST INPUT UI)
    # ----------------
    elif step == 2:
        st.subheader("2) HS Outreach — Position Investment")
        hot = st.session_state.hotspots.get(st.session_state.home_region, [])
        needs = st.session_state.team_needs

        st.markdown(f"<div class='recruiting-intel'>Pipeline Bonus ({st.session_state.home_region}): {', '.join(hot)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='recruiting-intel'>Team Needs: <b>{', '.join(needs)}</b></div>", unsafe_allow_html=True)

        # Total budget chooser (fast)
        default_total = int(min(st.session_state.budget * 0.25, 10_000_000))
        if st.session_state.outreach_total <= 0:
            st.session_state.outreach_total = default_total

        st.session_state.outreach_total = st.number_input(
            "Total HS Outreach Budget (faster than 7 separate sliders)",
            min_value=0,
            max_value=int(min(st.session_state.budget, 50_000_000)),
            value=int(st.session_state.outreach_total),
            step=250_000
        )

        # Build/edit % shares table
        if (not st.session_state.prev_outreach_alloc) and sum(st.session_state.outreach_alloc.values()) == 0:
            shares = build_outreach_default_shares(needs, hot)
        else:
            # derive shares from existing allocation
            total_amt = sum(st.session_state.outreach_alloc.values()) or 1
            shares = {p: (st.session_state.outreach_alloc[p] / total_amt) * 100.0 for p in POSITIONS}

        # Presets
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Preset: Balanced"):
            shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
        if c2.button("Preset: Needs Focus"):
            shares = build_outreach_default_shares(needs, [])
        if c3.button("Preset: Pipeline Focus"):
            shares = build_outreach_default_shares([], hot)
        if c4.button("Preset: Needs + Pipeline"):
            shares = build_outreach_default_shares(needs, hot)

        shares = normalize_shares(shares)
        df = pd.DataFrame({"Position": POSITIONS, "Share %": [round(shares[p], 2) for p in POSITIONS]})

        edited = st.data_editor(
            df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Share %": st.column_config.NumberColumn("Share %", min_value=0.0, max_value=100.0, step=0.5)
            }
        )

        # Normalize button
        if st.button("Auto-Normalize to 100%"):
            new_shares = {row["Position"]: float(row["Share %"]) for _, row in edited.iterrows()}
            new_shares = normalize_shares(new_shares)
            edited["Share %"] = [round(new_shares[p], 2) for p in POSITIONS]

        # Compute amounts
        shares_now = {row["Position"]: float(row["Share %"]) for _, row in edited.iterrows()}
        shares_now = normalize_shares(shares_now)
        alloc = {p: int(st.session_state.outreach_total * (shares_now[p] / 100.0)) for p in POSITIONS}

        st.write("### Allocations (computed)")
        st.dataframe(pd.DataFrame({"Position": POSITIONS, "Amount": [helper_format_cash(alloc[p]) for p in POSITIONS]}), hide_index=True, use_container_width=True)

        st.metric("Remaining Budget After Outreach", helper_format_cash(st.session_state.budget - st.session_state.outreach_total))

        cA, cB, cC = st.columns(3)
        if cA.button("Commit Outreach Spend", type="primary"):
            if st.session_state.outreach_total > st.session_state.budget:
                st.error("Outreach total exceeds available budget.")
            else:
                st.session_state.budget -= int(st.session_state.outreach_total)
                st.session_state.outreach_alloc = alloc
                st.session_state.prev_outreach_alloc = dict(alloc)
                add_news(f"{st.session_state.team_name} invests {helper_format_cash(int(st.session_state.outreach_total))} in HS outreach.")
                st.success("Outreach committed.")
        if cB.button("Continue to Top 8 Battles"):
            # Ensure allocation stored even if user didn't press commit (optional)
            if sum(st.session_state.outreach_alloc.values()) == 0 and st.session_state.outreach_total > 0:
                st.session_state.outreach_alloc = alloc
            st.session_state.offseason_step = 3
            st.rerun()
        if cC.button("Back to Portal"):
            st.session_state.offseason_step = 1
            st.rerun()

    # ----------------
    # STEP 3: TOP 8 BATTLES
    # ----------------
    elif step == 3:
        st.subheader("3) Top 8 Prospect Battles")
        hot = st.session_state.hotspots.get(st.session_state.home_region, [])
        needs = st.session_state.team_needs

        if not st.session_state.top8:
            st.session_state.top8 = generate_top8_prospects(needs, hot)
            st.session_state.top8_results = []

        st.markdown("<div class='recruiting-intel'>These are elite recruits. Winning depends on: offer size + staff/scout + prestige + your outreach spend at that position.</div>", unsafe_allow_html=True)

        # pick which prospects to pursue (reduces UI spam)
        options = [f"{p['pos']} {p['name']} ({p['rating']}) — Ask {helper_format_cash(p['base_ask'])}" for p in st.session_state.top8]
        pursue = st.multiselect("Select prospects to pursue (recommended 2–4)", options, default=options[:3])

        pursue_ids = set()
        for s in pursue:
            for p in st.session_state.top8:
                if s.startswith(f"{p['pos']} {p['name']}"):
                    pursue_ids.add(p["id"])

        for p in st.session_state.top8:
            if p["resolved"]:
                continue

            card = f"**{p['pos']} {p['name']}** ({p['rating']}) — {p['trait']} | NIL Ask: {helper_format_cash(p['base_ask'])}"
            st.write(card)
            st.caption(f"Contenders: {', '.join(p['contenders'])}")

            ai_offers = ai_offers_for_prospect(p)
            st.write(f"Top AI offer (today): **{ai_offers[0][0]} {helper_format_cash(ai_offers[0][1])}**")

            if p["id"] in pursue_ids:
                # Better input UI: slider anchored around ask + AI offer
                hi = int(max(p["base_ask"] * 2.0, ai_offers[0][1] * 1.5))
                lo = int(p["base_ask"] * 0.5)
                p["user_offer"] = st.slider(
                    f"Your offer for {p['name']} ({p['pos']})",
                    min_value=0,
                    max_value=hi,
                    value=int(max(p["base_ask"], ai_offers[0][1])),
                    step=50_000,
                    key=f"offer_{p['id']}"
                )
                st.write(f"Your Offer: **{helper_format_cash(int(p['user_offer']))}**")
            else:
                st.write("_Not pursuing._")
            st.divider()

        if st.button("Resolve Top 8 Battles", type="primary"):
            allocations = st.session_state.outreach_alloc or {p: 0 for p in POSITIONS}
            for p in st.session_state.top8:
                if p["resolved"]:
                    continue
                if p["id"] not in pursue_ids:
                    # AI signs them
                    ai = ai_offers_for_prospect(p)
                    p["resolved"] = True
                    p["signed"] = ai[0][0] if ai else random.choice(ALL_TEAMS)
                    continue

                offer = int(p.get("user_offer", 0))
                if offer <= 0 or offer > st.session_state.budget:
                    # can't afford -> treat as no pursuit
                    ai = ai_offers_for_prospect(p)
                    p["resolved"] = True
                    p["signed"] = ai[0][0] if ai else random.choice(ALL_TEAMS)
                    continue

                prob, ai = win_prob_top8(
                    p,
                    offer,
                    st.session_state.staff,
                    st.session_state.prestige,
                    allocations,
                    st.session_state.inflation
                )

                roll = random.random()
                if roll < prob:
                    # User wins
                    st.session_state.budget -= offer
                    st.session_state.roster[p["pos"]] = max(st.session_state.roster[p["pos"]], p["rating"])
                    st.session_state.active_transfers[p["pos"]] = False

                    booster = random.randint(500_000, 6_000_000)
                    # Recruiter HC + big stadium/marketing => bigger booster pop
                    if st.session_state.staff.get("HC", {}).get("trait") == "Recruiter":
                        booster = int(booster * 1.15)
                    booster = int(booster * (1.0 + (st.session_state.facilities["Marketing"] - 5) * 0.03))
                    booster = clamp(booster, 200_000, 10_000_000)
                    st.session_state.budget += booster

                    p["resolved"] = True
                    p["signed"] = st.session_state.team_name
                    add_news(f"⭐ {p['name']} ({p['pos']}, {p['rating']}) commits! Boosters donate {helper_format_cash(booster)}.")
                    st.session_state.top8_results.append((p["name"], p["pos"], "SIGNED", prob, offer, ai[0][0], ai[0][1]))
                else:
                    # AI wins
                    ai_winner = ai[0][0] if ai else random.choice(ALL_TEAMS)
                    p["resolved"] = True
                    p["signed"] = ai_winner
                    add_news(f"Missed on {p['name']} ({p['pos']}). He signs with {ai_winner}.")
                    st.session_state.top8_results.append((p["name"], p["pos"], "LOST", prob, offer, ai[0][0], ai[0][1]))

            st.success("Top 8 battles resolved.")
            st.session_state.offseason_step = 4
            st.rerun()

        cA, cB = st.columns(2)
        if cA.button("Back to Outreach"):
            st.session_state.offseason_step = 2
            st.rerun()
        if cB.button("Skip Top 8 and Finalize"):
            st.session_state.offseason_step = 4
            st.rerun()

    # ----------------
    # STEP 4: FINALIZE CLASS + ADVANCE YEAR
    # ----------------
    elif step == 4:
        st.subheader("4) Finalize Class & Advance Year")

        st.write("### Results Snapshot")
        if st.session_state.top8_results:
            df = pd.DataFrame(st.session_state.top8_results, columns=["Prospect", "Pos", "Result", "WinProb", "YourOffer", "TopAI", "TopAI_Offer"])
            df["WinProb"] = df["WinProb"].apply(lambda x: f"{x*100:.0f}%")
            df["YourOffer"] = df["YourOffer"].apply(lambda x: helper_format_cash(int(x)))
            df["TopAI_Offer"] = df["TopAI_Offer"].apply(lambda x: helper_format_cash(int(x)))
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No Top 8 results yet (maybe skipped).")

        st.divider()
        st.write("### Apply HS Outreach Class Impact")

        hot = st.session_state.hotspots.get(st.session_state.home_region, [])
        needs = st.session_state.team_needs
        allocations = st.session_state.outreach_alloc or {p: 0 for p in POSITIONS}

        # Attrition + class impact
        res = process_outreach_to_roster_updates(
            allocations=allocations,
            staff=st.session_state.staff,
            prestige=int(st.session_state.prestige),
            inflation=float(st.session_state.inflation),
            hotspots=hot,
            needs=needs
        )

        # Apply updates (attrition first)
        for p in POSITIONS:
            attrition = 12 if st.session_state.active_transfers.get(p) else random.randint(2, 5)
            st.session_state.active_transfers[p] = False
            gain = float(res["roster_updates"].get(p, 0.0))
            st.session_state.roster[p] = int(clamp(st.session_state.roster[p] - attrition + gain, 40, 99))

        # Gems & booster bonus
        if res["gems"]:
            st.success(f"GEMS found: {len(res['gems'])}")
            for g in res["gems"][:3]:
                st.write(f"💎 {g['pos']} {g['name']} ({g['rating']}) {g['trait']}")
        if res["booster_bonus"] > 0:
            st.session_state.budget += int(res["booster_bonus"])
            add_news(f"Boosters add {helper_format_cash(int(res['booster_bonus']))} after surprise gems.")

        # Update needs
        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)

        st.divider()
        if st.button("Advance to Next Season", type="primary"):
            # League evolves
            st.session_state.opponents_db = engine_evolve_universe(st.session_state.opponents_db)

            # Advance time
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.inflation *= 1.05
            st.session_state.hotspots = generate_hotspots()

            # Reset season
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
            st.session_state.week_index = 0
            st.session_state.record = {"w": 0, "l": 0}
            st.session_state.season_logs = []
            st.session_state.season_complete = False

            # Clear postseason/offseason
            st.session_state.postseason_data = {"Type": None}
            st.session_state.postseason_complete = False
            st.session_state.offseason_step = 1
            st.session_state.portal_players = []
            st.session_state.top8 = []
            st.session_state.top8_results = []
            st.session_state.outreach_total = 0
            st.session_state.outreach_alloc = {p: 0 for p in POSITIONS}

            add_news(f"New season begins. Needs: {', '.join(st.session_state.team_needs)}.")
            st.session_state.game_state = "DASHBOARD"
            st.rerun()

def show_fired():
    st.error("FIRED! Your tenure has ended.")
    st.write(f"Final Legacy Score: **{calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)}**")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()

def show_retirement():
    st.title("Retirement")
    st.write("Thanks for playing!")
    st.write(f"Final Legacy Score: **{calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)}**")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()

# ----------------------------
# ROUTER
# ----------------------------
if st.session_state.game_state == "SETUP":
    run_setup()
elif st.session_state.game_state == "DASHBOARD":
    show_dashboard()
elif st.session_state.game_state == "POSTSEASON":
    show_postseason()
elif st.session_state.game_state == "OFFSEASON":
    show_offseason()
elif st.session_state.game_state == "FIRED":
    show_fired()
elif st.session_state.game_state == "RETIREMENT":
    show_retirement()
else:
    st.session_state.game_state = "SETUP"
    st.rerun()
