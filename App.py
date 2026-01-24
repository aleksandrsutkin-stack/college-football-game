import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# COLLEGE FOOTBALL MOGUL V10 — SINGLE FILE APP
# NEW IN V10:
# 1) "THEME PROOF" CSS: Forces dark text on cards to prevent "Invisible Ink" in Dark Mode.
# 2) Includes all V9 features: Season Recap, Booster Meter, Resume Button.
# 3) Includes all V8 features: Scoring Engine, NIL Tiers, Realignment.
# ==============================================================================

# ==============================================================================
# ZONE 1: CONFIGURATION & STATIC DATA
# ==============================================================================
try:
    st.set_page_config(page_title="College Football Mogul V10", page_icon="🏈", layout="wide")
except Exception:
    pass

st.markdown("""
<style>
/* GLOBAL & BUTTONS */
.stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }

/* THEME-PROOFING: FORCE DARK TEXT ON LIGHT BACKGROUNDS */
.game-card, .staff-card, .news-box, .security-box, .trophy-tile {
    color: #111111 !important; /* Fixes White-on-White in Dark Mode */
}

/* CONTAINERS */
.security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
.security-safe { color: #28a745; font-weight: bold; }
.security-warm { color: #fd7e14; font-weight: bold; }
.security-hot { color: #dc3545; font-weight: bold; }

.finance-alert { background-color: #d1e7dd; color: #0f5132 !important; border: 1px solid #badbcc; padding: 15px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-weight: bold; }
.nil-alert { background-color: #cff4fc; color: #055160 !important; border: 1px solid #b6effb; padding: 18px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-size: 1.1em; font-weight: bold; }

/* GAME CARDS */
.game-card { padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #ddd; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.game-card-win { border-left: 5px solid #28a745; }
.game-card-loss { border-left: 5px solid #dc3545; }
.game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
.game-card-rival { border: 2px solid #ffc107 !important; background-color: #fffbf0 !important; }

.card-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 5px;}
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.85em; }
.stat-row { display: flex; justify-content: space-between; }

/* STAFF CARDS */
.staff-card { background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
.staff-role { font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.staff-name { font-size: 1.1em; font-weight: 800; color: #333; }

/* BADGES */
.badge { padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; margin-right: 5px; display: inline-block;}
.badge-tier-s { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-tier-a { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-tier-f { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-trait { background: #e2e3e5; color: #383d41; }

/* RECRUITING & NEWS */
.recruiting-intel { background-color: #e0f7fa; color: #006064 !important; border-left: 5px solid #006064; padding: 12px; margin-bottom: 10px; border-radius: 4px; }
.bracket-box { background-color: #2c3e50; color: white !important; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
.bracket-row { display: flex; justify-content: space-between; padding: 6px; border-bottom: 1px solid #444; }

.news-box { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.news-item { padding: 6px 0; border-bottom: 1px solid #f1f1f1; }
.news-item:last-child { border-bottom: none; }

.small-muted { font-size: 0.85em; color: #666; }

/* TROPHIES & NEWSPAPER */
.trophy-strip { font-size: 1.4em; line-height: 1.6em; }
.trophy-tile { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 10px; }

.newspaper-head { font-family: 'Georgia', serif; font-size: 2em; text-align: center; border-bottom: 3px double #333; padding-bottom: 10px; margin-bottom: 20px; color: #2c3e50; background: #fdfbf7; padding: 15px; border-radius: 5px; }
.newspaper-sub { font-family: 'Georgia', serif; font-style: italic; text-align: center; color: #555; margin-bottom: 20px; }

.booster-meter-container { background: #eee; height: 20px; border-radius: 10px; margin-top: 5px; overflow: hidden; border: 1px solid #ccc; }
.booster-meter-fill { height: 100%; transition: width 0.5s; }
</style>
""", unsafe_allow_html=True)

POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}
SCHEMES = {"Offense": ["Air Raid", "Smashmouth", "Pro Style"], "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]}
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
    "Recruiter": "+10% Recruiting",
    "Tactician": "+3 Game Boost",
    "Air Raid": "+2 Scheme",
    "Smashmouth": "+2 Scheme",
    "Pro Style": "+2 Scheme"
}
BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"]
}

# Trophy icons
TROPHY_ICONS = {
    "National Title": "🏆",
    "CFP": "🏆",
    "Rose Bowl": "🌹",
    "Sugar Bowl": "🍬",
    "Orange Bowl": "🍊",
    "Cotton Bowl": "🤠",
    "Peach Bowl": "🍑",
    "Fiesta Bowl": "🎉",
    "Citrus Bowl": "🍋",
    "Alamo Bowl": "🏰",
    "Pop-Tarts Bowl": "🍪",
    "Gator Bowl": "🐊",
    "Liberty Bowl": "🗽",
    "Music City Bowl": "🎸",
    "Las Vegas Bowl": "🎰",
    "Gasparilla Bowl": "🏴‍☠️",
    "Boca Raton Bowl": "🌴",
    "Potato Bowl": "🥔",
    "Bowl Win": "🎳"
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
CONF_POWER = {"SEC": 1.10, "Big Ten": 1.08, "ACC": 1.04, "Big 12": 1.03, "G5": 0.95}

# ==============================================================================
# ZONE 2: HELPERS
# ==============================================================================
def helper_format_cash(amount: int) -> str:
    try:
        amount = int(amount)
    except Exception:
        amount = 0
    return f"${amount/1_000_000:.1f}M" if amount >= 1_000_000 else f"${int(amount/1_000)}K"

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Arch", "Shedeur", "Quinn", "Travis", "Ashton"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck", "Jeanty", "Judkins"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name():
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan", "Kalen"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman", "Lanning", "DeBoer"]
    return f"{random.choice(first)} {random.choice(last)}"

def get_letter_grade(val):
    if val >= 9: return "A+"
    elif val >= 8: return "A"
    elif val >= 7: return "B"
    elif val >= 5: return "C"
    elif val >= 3: return "D"
    else: return "F"

def calculate_saban_score(career_stats, prestige):
    return int((career_stats["w"] * 1) + (career_stats["bowl_w"] * 5) + (career_stats["titles"] * 50) + (prestige * 0.5))

def get_bowl_name(rank):
    if rank <= 12: return "CFP Playoff"
    elif rank <= 25: return random.choice(BOWL_MAPPING["Elite"])
    elif rank <= 40: return random.choice(BOWL_MAPPING["High"])
    elif rank <= 80: return random.choice(BOWL_MAPPING["Mid"])
    else: return random.choice(BOWL_MAPPING["Low"])

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

def generate_star_player(position, tier):
    base = 85 if tier <= 2 else 80
    return {
        "id": random.randint(10000, 99999),
        "name": generate_name(),
        "pos": position,
        "rating": min(99, base + random.randint(5, 14)),
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

def add_news(text: str):
    if "news" not in st.session_state:
        st.session_state.news = []
    st.session_state.news.insert(0, f"{st.session_state.year}: {text}")
    st.session_state.news = st.session_state.news[:12]

def trophy_icon(name: str) -> str:
    return TROPHY_ICONS.get(name, TROPHY_ICONS.get("Bowl Win", "🎳"))

def award_trophy(trophy_name: str):
    if "trophies" not in st.session_state:
        st.session_state.trophies = []
    st.session_state.trophies.append({
        "Year": st.session_state.year,
        "Name": trophy_name,
        "Icon": trophy_icon(trophy_name)
    })

def normalize_shares(shares: dict):
    def _val(pos):
        try:
            return max(0.0, float(shares.get(pos, 0.0)))
        except Exception:
            return 0.0
    total = sum(_val(p) for p in POSITIONS)
    if total <= 0:
        return {p: 100.0 / len(POSITIONS) for p in POSITIONS}
    return {p: (_val(p) / total) * 100.0 for p in POSITIONS}

# ==============================================================================
# ZONE 3: ENGINE
# ==============================================================================
def engine_calculate_revenue(tier, marketing_lvl, inflation):
    if not tier:
        tier = 3
    base = {1: 40_000_000, 2: 25_000_000, 3: 10_000_000, 4: 5_000_000}.get(tier, 5_000_000)
    marketing_bonus = int(marketing_lvl) * 2_000_000
    total = (base + marketing_bonus) * float(inflation)
    conf_boost = float(st.session_state.get("conf_revenue_boost_mult", 1.0))
    total *= conf_boost
    return int(total)

def engine_generate_coach(role, tier):
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
    base = base_ovr if base_ovr is not None else (90 if tier == 1 else (82 if tier == 2 else 74))
    roster = {}
    for p in POSITIONS:
        roster[p] = min(99, max(40, int(base + random.randint(-4, 4))))
    return roster

def engine_generate_schedule(my_team, my_conf, rival):
    conf_foes = [t for t in CONFERENCES.get(my_conf, CONFERENCES["G5"]) if t != my_team]
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

def get_tier_bonus(rating):
    if rating >= 8:
        return 3
    if rating <= 4:
        return -3
    return 0

def home_field_points(stadium_level: int, is_home: bool) -> float:
    lvl = int(stadium_level)
    if is_home:
        if lvl <= 6: return 0.0
        if lvl <= 8: return 1.0
        if lvl <= 10: return 3.0
        return 4.0
    else:
        if lvl >= 11 and random.random() < 0.25: return -2.0
        if lvl >= 9 and random.random() < 0.25: return -1.5
        return 0.0

def compute_team_unit_ratings(roster: dict, staff: dict, facilities: dict):
    oc = staff.get("OC", {"off": 3}).get("off", 3)
    dc = staff.get("DC", {"def": 3}).get("def", 3)
    training = int(facilities.get("Training", 1))

    off = (roster["QB"] * 0.34) + (roster["OL"] * 0.26) + ((roster["RB"] + roster["WR"]) / 2 * 0.40)
    deff = (roster["DL"] * 0.34) + (roster["LB"] * 0.33) + (roster["DB"] * 0.33)

    off += get_tier_bonus(oc) * 1.0
    deff += get_tier_bonus(dc) * 1.0

    off += training * 0.40
    deff += training * 0.40

    overall = (off * 0.52) + (deff * 0.48)
    return int(off), int(deff), int(overall)

def ensure_opp_units(opp_data: dict):
    if "OffOVR" not in opp_data or "DefOVR" not in opp_data:
        base = int(opp_data.get("OVR", 80))
        opp_data["OffOVR"] = max(50, min(99, base + random.randint(-3, 3)))
        opp_data["DefOVR"] = max(50, min(99, base + random.randint(-3, 3)))
    return opp_data

def engine_play_game_v8(
    my_off, my_def,
    opp_off, opp_def,
    staff, schemes, opp_schemes,
    game_plan, opp_coaches,
    is_home, is_rival,
    my_stadium_level, opp_stadium_level
):
    my_edge = (my_off - opp_def) * 0.35
    opp_edge = (opp_off - my_def) * 0.35

    scheme_bonus_my = 0.0
    scheme_bonus_opp = 0.0
    my_off_s = schemes.get("Off", "Pro Style")
    opp_def_s = opp_schemes.get("Def", "Man Coverage")

    if COUNTERS.get(opp_def_s) == my_off_s:
        scheme_bonus_my += 2.5
        scheme_bonus_opp -= 1.0
    if COUNTERS.get(my_off_s) == opp_def_s:
        scheme_bonus_my -= 2.5
        scheme_bonus_opp += 1.0

    my_oc = staff.get("OC", {"off": 3}).get("off", 3)
    my_dc = staff.get("DC", {"def": 3}).get("def", 3)
    opp_oc = opp_coaches.get("OC", 5)
    opp_dc = opp_coaches.get("DC", 5)

    coaching_my = (get_tier_bonus(my_oc) - get_tier_bonus(opp_dc)) * 1.20
    coaching_opp = (get_tier_bonus(opp_oc) - get_tier_bonus(my_dc)) * 1.20

    hc_trait = staff.get("HC", {}).get("trait", "None")
    if hc_trait == "Tactician":
        coaching_my += 0.9
    elif hc_trait == "Recruiter":
        coaching_my += 0.25

    oc_trait = staff.get("OC", {}).get("trait", "None")
    if oc_trait in ["Air Raid", "Smashmouth", "Pro Style"] and oc_trait == my_off_s:
        scheme_bonus_my += 1.0

    hf = home_field_points(my_stadium_level, True) if is_home else home_field_points(opp_stadium_level, False)

    var_mult = 1.0
    if is_rival: var_mult *= 1.35
    if game_plan == "Aggressive": var_mult *= 1.25
    elif game_plan == "Conservative": var_mult *= 0.85

    base_pts = 27.5
    exp_my = base_pts + my_edge + scheme_bonus_my + coaching_my + (hf if is_home else 0.0)
    exp_opp = base_pts + opp_edge + scheme_bonus_opp + coaching_opp + (0.0 if is_home else (-hf if hf < 0 else 0.0))

    exp_my = max(10, min(50, exp_my))
    exp_opp = max(10, min(50, exp_opp))

    my_score = int(round(random.gauss(exp_my, 7.0 * var_mult)))
    opp_score = int(round(random.gauss(exp_opp, 7.0 * var_mult)))

    if my_score == opp_score:
        my_score += random.choice([0, 3, 7])
        opp_score += random.choice([0, 0, 3])

    my_score = max(0, min(70, my_score))
    opp_score = max(0, min(70, opp_score))

    explain = {
        "my_off": my_off, "my_def": my_def,
        "opp_off": opp_off, "opp_def": opp_def,
        "my_edge": float(my_edge), "opp_edge": float(opp_edge),
        "scheme_my": float(scheme_bonus_my), "scheme_opp": float(scheme_bonus_opp),
        "coach_my": float(coaching_my), "coach_opp": float(coaching_opp),
        "home_field": float(hf),
        "plan": game_plan
    }

    stats = {
        "qb_duel": [int(st.session_state.roster["QB"]), int(max(60, min(99, opp_off)))],
        "off_vs_def": [int(my_off), int(opp_def)],
        "def_vs_off": [int(my_def), int(opp_off)],
        "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"],
        "raw_roster": int((my_off + my_def) / 2)
    }

    return {
        "result": "W" if my_score > opp_score else "L",
        "score": f"{my_score}-{opp_score}",
        "stats": stats,
        "explain": explain
    }

def engine_evolve_universe(opponents_db):
    for team, data in opponents_db.items():
        wins = int((data.get("OVR", 75) / 100) * 12) + random.randint(-2, 2)
        wins = max(0, min(12, wins))

        change = 0
        if wins >= 10: change = 3
        elif wins <= 4: change = -3
        data["Prestige"] = max(20, min(99, data.get("Prestige", 60) + change))

        if data["Prestige"] > 80 and wins < 6:
            data["Coaches"] = {"OC": random.randint(7, 9), "DC": random.randint(7, 9)}
        elif data["Prestige"] < 70 and wins > 9:
            data["Coaches"] = {"OC": random.randint(3, 6), "DC": random.randint(3, 6)}

        base_ovr = int(data["Prestige"] * 0.9)
        data["OVR"] = base_ovr + random.randint(-3, 3)

        if random.random() < 0.35:
            data.pop("OffOVR", None)
            data.pop("DefOVR", None)
    return opponents_db

# HS outreach - V8 Gems logic PRESERVED (unaltered)
def process_hs_outreach(total_spend: int, shares_pct: dict, staff: dict, prestige: int, inflation: float, hotspots: dict, home_region: str, team_needs: list):
    results = {"roster_updates": {}, "gems": [], "booster_bonus": 0, "spent": int(total_spend)}
    total_spend = max(0, int(total_spend))
    scout = staff.get("Scout", {"recruit": 1}).get("recruit", 1)
    hc_trait = staff.get("HC", {}).get("trait", "None")

    efficiency = 0.85 if scout >= 8 else (1.0 if scout >= 5 else 1.15)
    base_cost = 900_000 * float(inflation) * float(efficiency)
    hot_positions = hotspots.get(home_region, [])

    for pos in POSITIONS:
        pct = float(shares_pct.get(pos, 0.0))
        amt = total_spend * (pct / 100.0)

        if amt <= 0:
            results["roster_updates"][pos] = -random.randint(1, 3)
            continue

        pipeline_bonus = 1.15 if pos in hot_positions else 1.0
        need_bonus = 1.25 if pos in team_needs else 1.0
        prestige_factor = max(0.85, min(1.20, (prestige / 75) ** 0.35))

        spend_ratio = amt / max(1.0, base_cost)
        dim = (spend_ratio ** 0.85)

        change = dim * pipeline_bonus * need_bonus * prestige_factor
        change = max(-4, min(12, change))

        if hc_trait == "Recruiter":
            change *= 1.08

        gem_chance = 0.08
        if pos in team_needs: gem_chance += 0.07
        if pos in hot_positions: gem_chance += 0.05
        if scout >= 8: gem_chance += 0.03
        if hc_trait == "Recruiter": gem_chance += 0.02

        if amt > base_cost * 1.25 and random.random() < gem_chance:
            star = generate_star_player(pos, tier=1)
            star["name"] += " (GEM)"
            results["gems"].append(star)
            change += 5
            results["booster_bonus"] += 250_000 + random.randint(0, 250_000)

        results["roster_updates"][pos] = change

    return results

def generate_nil_class_15(team_needs: list):
    def mk(tier: int, pos: str):
        if tier == 1:
            rating = random.randint(90, 99)
            ask = int(random.randint(2_500_000, 9_000_000) * (1.0 + (rating - 90) / 25))
            badge = "Tier 1"
        elif tier == 2:
            rating = random.randint(84, 89)
            ask = int(random.randint(900_000, 3_500_000) * (1.0 + (rating - 84) / 35))
            badge = "Tier 2"
        else:
            rating = random.randint(76, 83)
            ask = int(random.randint(200_000, 1_200_000) * (1.0 + (rating - 76) / 40))
            badge = "Tier 3"
        return {
            "id": random.randint(10_000, 99_999),
            "tier": tier,
            "tier_label": badge,
            "name": generate_name(),
            "pos": pos,
            "rating": rating,
            "ask": ask,
            "trait": random.choice(TRAITS),
            "status": "AVAILABLE"
        }

    needs = team_needs[:] if team_needs else POSITIONS[:]
    pool = []
    for _ in range(5):
        pos = random.choice(needs if random.random() < 0.70 else POSITIONS)
        pool.append(mk(1, pos))
    for _ in range(5):
        pos = random.choice(needs if random.random() < 0.60 else POSITIONS)
        pool.append(mk(2, pos))
    for _ in range(5):
        pos = random.choice(needs if random.random() < 0.50 else POSITIONS)
        pool.append(mk(3, pos))
    pool.sort(key=lambda x: (x["tier"], -x["rating"]))
    return pool

def generate_top8_prospects(team_needs: list):
    recruits = []
    for _ in range(8):
        pos = random.choice(team_needs if team_needs and random.random() < 0.65 else POSITIONS)
        rating = random.randint(90, 99)
        ask = int(random.randint(2_000_000, 8_000_000) * (1.0 + (rating - 90) / 35))
        recruits.append({
            "id": random.randint(10_000, 99_999),
            "name": generate_name(),
            "pos": pos,
            "rating": rating,
            "ask": ask,
            "trait": random.choice(TRAITS),
            "status": "OPEN",
            "note": ""
        })
    recruits.sort(key=lambda x: x["rating"], reverse=True)
    return recruits

def top8_commit_chance(recruit: dict, spend_by_pos: dict, staff: dict, prestige: int) -> float:
    scout = staff.get("Scout", {"recruit": 1}).get("recruit", 1)
    hc_trait = staff.get("HC", {}).get("trait", "None")

    chance = 0.18
    chance += (max(40, min(99, prestige)) - 60) * 0.004
    chance += (scout - 5) * 0.02
    if hc_trait == "Recruiter":
        chance += 0.05

    pos = recruit["pos"]
    spend = float(spend_by_pos.get(pos, 0.0))
    chance += min(0.20, spend / 10_000_000)

    return max(0.05, min(0.80, chance))

# ==============================================================================
# ZONE 4: STATE + CFP BRACKET + CONFERENCE REALIGNMENT
# ==============================================================================
def initialize_game_state():
    if "game_state" not in st.session_state:
        st.session_state.game_state = "SETUP"
        st.session_state.year = 2026
        st.session_state.budget = 0
        st.session_state.prestige = 50
        st.session_state.job_security = 80
        st.session_state.expected_wins = 6
        st.session_state.tenure = 1
        st.session_state.roster = {p: 75 for p in POSITIONS}
        st.session_state.active_transfers = {p: False for p in POSITIONS}
        st.session_state.stars = []
        st.session_state.staff = {}
        st.session_state.facilities = {"Marketing": 1, "Training": 1, "Stadium": 1}
        st.session_state.history = []
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.opponents_db = {}
        st.session_state.my_schemes = {"Off": "Pro Style", "Def": "Man Coverage"}
        st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}
        st.session_state.season_logs = []
        st.session_state.schedule = []
        st.session_state.season_simulated = False
        st.session_state.hotspots = {}
        st.session_state.candidates = {}
        st.session_state.postseason_data = {"Type": None, "Rank": 0, "Round": 0, "Matches": []}
        st.session_state.revenue_report = None
        st.session_state.inflation = 1.0
        st.session_state.team_needs = []
        st.session_state.game_plan = "Normal"
        st.session_state.week_index = 0
        st.session_state.news = []

        # Offseason modules
        st.session_state.offseason_step = 1
        st.session_state.nil_class = []
        st.session_state.hs_total_spend = 0
        st.session_state.hs_shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
        st.session_state.hs_spend_by_pos = {p: 0 for p in POSITIONS}
        st.session_state.top8 = []
        st.session_state.top8_resolved = set()

        # Trophies
        st.session_state.trophies = []

        # Conference invites / boost
        st.session_state.conf_revenue_boost_mult = 1.0
        st.session_state.pending_invite = None

        # UX: season end screen
        st.session_state.season_end_ready = False

        # V9: Booster Rating
        st.session_state.booster_rating = 50

    # safety defaults
    defaults = {
        "inflation": 1.0,
        "revenue_report": None,
        "postseason_data": {"Type": None, "Rank": 0, "Round": 0, "Matches": []},
        "team_needs": [],
        "game_plan": "Normal",
        "week_index": 0,
        "news": [],
        "offseason_step": 1,
        "nil_class": [],
        "hs_total_spend": 0,
        "hs_shares": {p: 100.0 / len(POSITIONS) for p in POSITIONS},
        "hs_spend_by_pos": {p: 0 for p in POSITIONS},
        "top8": [],
        "top8_resolved": set(),
        "trophies": [],
        "conf_revenue_boost_mult": 1.0,
        "pending_invite": None,
        "season_end_ready": False,
        "booster_rating": 50
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def generate_hotspots():
    hotspots = {}
    for reg in REGION_STRENGTH.keys():
        hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

def init_playoff_bracket(user_rank, user_team_name):
    sorted_ai = [(t, d) for t, d in st.session_state.opponents_db.items() if t != user_team_name]
    sorted_ai = sorted(sorted_ai, key=lambda x: x[1].get("OVR", 80), reverse=True)

    top_12 = []
    ai_idx = 0
    for r in range(1, 13):
        if r == user_rank:
            top_12.append(user_team_name)
        else:
            top_12.append(sorted_ai[ai_idx][0])
            ai_idx += 1

    r1_matches = [
        {"high": 5, "low": 12, "t1": top_12[4], "t2": top_12[11], "winner": None},
        {"high": 6, "low": 11, "t1": top_12[5], "t2": top_12[10], "winner": None},
        {"high": 7, "low": 10, "t1": top_12[6], "t2": top_12[9], "winner": None},
        {"high": 8, "low": 9,  "t1": top_12[7], "t2": top_12[8], "winner": None}
    ]
    qf_seeds = [top_12[0], top_12[1], top_12[2], top_12[3]]
    return {"Type": "CFP", "Round": 1, "Matches": r1_matches, "Seeds": top_12, "QF_Seeds": qf_seeds, "UserAlive": True, "Rank": user_rank}

def maybe_generate_conference_invite():
    if st.session_state.tenure % 5 != 0:
        return
    curr_conf = st.session_state.team_conf
    prestige = int(st.session_state.prestige)
    titles = int(st.session_state.career_stats.get("titles", 0))

    invite = None
    if curr_conf == "G5" and (prestige >= 82 or titles >= 1):
        invite = {"to_conf": "Big 12", "boost_mult": 1.25, "note": "Major TV deal + recruiting bump, tougher schedules."}
    elif curr_conf == "Big 12" and (prestige >= 88 or titles >= 2):
        invite = random.choice([
            {"to_conf": "Big Ten", "boost_mult": 1.35, "note": "National brand exposure. Expect tougher weekly opponents."},
            {"to_conf": "SEC", "boost_mult": 1.38, "note": "Biggest stage. Massive revenue. Weekly knife fights."}
        ])
    elif curr_conf == "ACC" and (prestige >= 90 or titles >= 2):
        invite = random.choice([
            {"to_conf": "Big Ten", "boost_mult": 1.30, "note": "Stability + strong brand. Tougher schedule."},
            {"to_conf": "SEC", "boost_mult": 1.34, "note": "Huge money. Brutal competition."}
        ])

    if curr_conf in ["SEC", "Big Ten"] and prestige <= 58 and titles == 0:
        add_news(f"Rumors: {st.session_state.team_name} could face conference pressure if results don't improve.")

    if invite:
        st.session_state.pending_invite = invite
        add_news(f"{st.session_state.team_name} receives a conference invite to the {invite['to_conf']}!")

def apply_conference_move(to_conf: str, boost_mult: float):
    team = st.session_state.team_name
    from_conf = st.session_state.team_conf
    for conf, teams in CONFERENCES.items():
        if team in teams:
            teams.remove(team)
    CONFERENCES.setdefault(to_conf, [])
    if team not in CONFERENCES[to_conf]:
        CONFERENCES[to_conf].append(team)
    st.session_state.team_conf = to_conf
    st.session_state.conf_revenue_boost_mult = max(st.session_state.conf_revenue_boost_mult, float(boost_mult))
    st.session_state.prestige = min(99, st.session_state.prestige + 3)
    add_news(f"{team} officially joins the {to_conf}! Revenue permanently increases.")
    st.toast(f"Conference Move: {from_conf} -> {to_conf}")

def ai_conference_swap_lightweight():
    if st.session_state.tenure % 5 != 0: return
    g5_teams = CONFERENCES.get("G5", [])[:]
    b12_teams = CONFERENCES.get("Big 12", [])[:]
    if not g5_teams or not b12_teams: return

    def pres(team):
        if team == st.session_state.team_name:
            return st.session_state.prestige
        return st.session_state.opponents_db.get(team, {}).get("Prestige", 60)

    g5_sorted = sorted(g5_teams, key=pres, reverse=True)
    b12_sorted = sorted(b12_teams, key=pres)

    promote = g5_sorted[0]
    relegate = b12_sorted[0]
    if promote == st.session_state.team_name or relegate == st.session_state.team_name: return

    CONFERENCES["G5"].remove(promote)
    CONFERENCES["Big 12"].append(promote)
    CONFERENCES["Big 12"].remove(relegate)
    CONFERENCES["G5"].append(relegate)
    add_news(f"Conference realignment: {promote} promoted to Big 12; {relegate} relegated to G5.")

initialize_game_state()

# ==============================================================================
# ZONE 5: FLOW HELPERS (Season end, etc.)
# ==============================================================================
def end_regular_season_and_stay_on_results():
    st.session_state.season_simulated = True
    st.session_state.season_end_ready = True
    rev = engine_calculate_revenue(st.session_state.school_tier, st.session_state.facilities["Marketing"], st.session_state.inflation)
    st.session_state.budget += rev
    st.session_state.revenue_report = f"End of Regular Season Payout: +{helper_format_cash(rev)}"
    add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")
    st.session_state.game_state = "SEASON_END"

def render_news_box():
    st.markdown("### 🗞️ News Feed")
    st.markdown("<div class='news-box'>", unsafe_allow_html=True)
    if st.session_state.news:
        for n in st.session_state.news[:10]:
            st.markdown(f"<div class='news-item'>• {n}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='news-item'>• No headlines yet.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_trophy_gallery(title="🏛️ Trophy Case Gallery"):
    st.subheader(title)
    trophies = st.session_state.get("trophies", [])
    if not trophies:
        st.info("No trophies yet. Win bowls and titles to build your gallery.")
        return
    icons = " ".join([t["Icon"] for t in trophies[-25:]])
    st.markdown(f"<div class='trophy-strip'>{icons}</div>", unsafe_allow_html=True)
    with st.expander("See trophy details"):
        df = pd.DataFrame(trophies)
        st.dataframe(df, use_container_width=True)

# ==============================================================================
# ZONE 6: UI / ROUTES
# ==============================================================================
def run_setup():
    st.title("🏆 College Football Mogul V10")
    st.markdown("### Dynasty Mode (Jan 2026)")

    c1, c2 = st.columns(2)
    name = c1.text_input("AD Name", "Coach Prime")
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"])

    sorted_teams = sorted(REAL_WORLD_INIT.keys()) + sorted([t for t in ALL_TEAMS if t not in REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)

    if team in REAL_WORLD_INIT:
        d = REAL_WORLD_INIT[team]
        tier = d["Tier"]
        budget = 25_000_000 if tier == 1 else (15_000_000 if tier == 2 else 5_000_000)
        conf = get_conference(team)
        rival = d.get("Rival", "Rival")
    else:
        tier, budget, conf, rival = 3, 5_000_000, get_conference(team), "Rival"

    expect = 10 if tier == 1 else (8 if tier == 2 else (6 if tier == 3 else 4))
    st.info(f"**{team}** | Conf: {conf} | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival}")
    st.caption(f"Expectation: {expect}+ Wins")

    if st.button("Start Dynasty", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = TEAMS_DB.get(team, {}).get("color", "#333333")
        st.session_state.team_conf = conf
        st.session_state.team_rival = rival
        st.session_state.home_region = "South"

        st.session_state.expected_wins = expect
        st.session_state.school_tier = tier
        st.session_state.budget = int(budget * (0.75 if diff == "Hard" else 1.25 if diff == "Easy" else 1.0))

        st.session_state.roster = engine_generate_roster(tier, REAL_WORLD_INIT.get(team, {}).get("Talent"))
        st.session_state.prestige = REAL_WORLD_INIT.get(team, {}).get("Prestige", 60)
        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)

        st.session_state.staff = {}
        for r in ["HC", "OC", "DC", "Scout"]:
            st.session_state.staff[r] = engine_generate_coach(r, tier)

        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}

        st.session_state.opponents_db = {}
        for opp in ALL_TEAMS:
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                st.session_state.opponents_db[opp] = {
                    "Prestige": data["Prestige"],
                    "OVR": data["Talent"],
                    "Off": random.choice(SCHEMES["Offense"]),
                    "Def": random.choice(SCHEMES["Defense"]),
                    "Coaches": {"OC": random.randint(5, 9), "DC": random.randint(5, 9)},
                    "Stadium": random.randint(5, 11)
                }
            else:
                pres = 85 if opp in CONFERENCES["SEC"] else 65
                ovr = 82 if opp in CONFERENCES["SEC"] else 70
                st.session_state.opponents_db[opp] = {
                    "Prestige": pres, "OVR": ovr,
                    "Off": "Pro Style", "Def": "Man Coverage",
                    "Coaches": {"OC": 5, "DC": 5},
                    "Stadium": random.randint(4, 10)
                }

        st.session_state.hotspots = generate_hotspots()
        st.session_state.schedule = engine_generate_schedule(team, conf, rival)

        st.session_state.week_index = 0
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.season_simulated = False
        st.session_state.season_end_ready = False

        st.session_state.offseason_step = 1
        st.session_state.nil_class = []
        st.session_state.hs_total_spend = 0
        st.session_state.hs_shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
        st.session_state.hs_spend_by_pos = {p: 0 for p in POSITIONS}
        st.session_state.top8 = []
        st.session_state.top8_resolved = set()

        st.session_state.trophies = []
        st.session_state.conf_revenue_boost_mult = 1.0
        st.session_state.pending_invite = None
        st.session_state.booster_rating = 50

        add_news(f"{team} hires {st.session_state.staff['HC']['name']} as HC.")
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

def show_dashboard():
    thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < thresh:
        st.session_state.game_state = "FIRED"
        st.rerun()

    # V9 Navigation Fix: Resume button
    if st.session_state.season_end_ready:
        st.markdown("""
        <div style="background:#ffcccb; padding:10px; border-radius:5px; text-align:center; border:2px solid #e00; color: #333;">
            <h3>🚨 SEASON COMPLETE</h3>
            <p>The regular season is over. Go to results/postseason.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Resume Postseason / Season End", type="primary"):
            st.session_state.game_state = "SEASON_END"
            st.rerun()

    if st.session_state.revenue_report:
        st.markdown(f"<div class='finance-alert'>💰 FINANCIAL REPORT<br>{st.session_state.revenue_report}</div>", unsafe_allow_html=True)

    sec = st.session_state.job_security
    sec_cls = "security-safe" if sec > 75 else ("security-warm" if sec > 40 else "security-hot")
    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Security: <span class='{sec_cls}'>{sec}%</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 5px; color: white;'><h2>{st.session_state.team_name}</h2></div>", unsafe_allow_html=True)

    my_off, my_def, my_ovr = compute_team_unit_ratings(st.session_state.roster, st.session_state.staff, st.session_state.facilities)
    st.session_state.team_off = my_off
    st.session_state.team_def = my_def
    st.session_state.team_rating = my_ovr

    raw_roster_val = int(sum(st.session_state.roster.values()) / len(POSITIONS))

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("OVR", my_ovr, f"Raw Talent: {raw_roster_val}")
    c3.metric("OFF", my_off)
    c4.metric("DEF", my_def)
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    c5.metric("Legacy", saban, f"Titles: {st.session_state.career_stats['titles']}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Strategy", "Staff", "Facilities", "Season (Weekly)", "Legacy"])

    with tab1:
        c1, c2 = st.columns(2)
        st.session_state.my_schemes["Off"] = c1.selectbox("Offense", SCHEMES["Offense"], index=SCHEMES["Offense"].index(st.session_state.my_schemes.get("Off", "Pro Style")))
        st.session_state.my_schemes["Def"] = c2.selectbox("Defense", SCHEMES["Defense"], index=SCHEMES["Defense"].index(st.session_state.my_schemes.get("Def", "Man Coverage")))

        st.write("Unit Strength")
        for p, v in st.session_state.roster.items():
            lab = f"{p}: {int(v)}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.progress(min(1.0, v / 100.0), lab)
        st.caption("V8 engine uses OFF vs DEF matchups + coaching + scheme + home-field tiers.")

    with tab2:
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
                             <span class='badge badge-trait'>Trait: {c.get('trait','None')}</span></div>
                        <div class='small-muted'>{helper_format_cash(c.get('salary',0))}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Fire", key=f"fire_{role}"):
                        add_news(f"{st.session_state.team_name} parts ways with {c['name']} ({role}).")
                        del st.session_state.staff[role]
                        st.rerun()
                else:
                    st.warning(f"{role} VACANT")

        st.divider()
        st.markdown("### 📋 Job Market")
        vacancies = [r for r in roles if r not in st.session_state.staff]
        if vacancies:
            for role in vacancies:
                if role not in st.session_state.candidates:
                    st.session_state.candidates[role] = [engine_generate_coach(role, random.randint(1, 3)) for _ in range(3)]
                cols = st.columns(3)
                for j, cand in enumerate(st.session_state.candidates[role]):
                    with cols[j]:
                        rr = role_rating(cand, role)
                        vis_rate = f"{rr}" if cand.get("scouted") else f"{get_letter_grade(rr)}"
                        vis_trait = cand.get("trait") if cand.get("scouted") else "???"
                        st.markdown(f"""
                        <div class='staff-card'>
                            <div class='staff-name'>{cand['name']}</div>
                            <div class='small-muted'>{cand.get('history','')}</div>
                            <div style='margin:5px 0'>
                                <span class='badge badge-trait'>{role} OVR: {vis_rate}</span>
                                <span class='badge badge-trait'>Trait: {vis_trait}</span>
                            </div>
                            <div style='font-weight:bold'>{helper_format_cash(cand['salary'])}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        b1, b2 = st.columns(2)
                        if b1.button("Hire", key=f"h_{role}_{j}"):
                            if st.session_state.budget >= cand["salary"]:
                                st.session_state.budget -= cand["salary"]
                                st.session_state.staff[role] = cand
                                add_news(f"{st.session_state.team_name} hires {cand['name']} as {role}.")
                                if role in st.session_state.candidates:
                                    del st.session_state.candidates[role]
                                st.rerun()
                            else:
                                st.error("Not enough budget.")
                        if not cand.get("scouted") and b2.button("Scout ($25k)", key=f"sc_{role}_{j}"):
                            if st.session_state.budget >= 25_000:
                                st.session_state.budget -= 25_000
                                cand["scouted"] = True
                                st.rerun()
                            else:
                                st.error("Not enough budget.")
                if st.button(f"Promote GA (Free)", key=f"ga_{role}"):
                    ga = generate_ga_coach(role)
                    st.session_state.staff[role] = ga
                    add_news(f"{st.session_state.team_name} promotes {ga['name']} to {role}.")
                    if role in st.session_state.candidates:
                        del st.session_state.candidates[role]
                    st.rerun()
        else:
            st.info("No vacancies. Fire someone to shop the market.")

    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Marketing", st.session_state.facilities["Marketing"], delta="Rev: +$2M/yr")
            if st.button("Upgrade ($1M)", key="um"):
                if st.session_state.budget >= 1_000_000:
                    st.session_state.budget -= 1_000_000
                    st.session_state.facilities["Marketing"] += 1
                    add_news("Marketing upgraded. Boosters are pleased.")
                    st.rerun()
        with c2:
            st.metric("Training", st.session_state.facilities["Training"], delta="OFF/DEF Boost")
            if st.button("Upgrade ($3M)", key="ut"):
                if st.session_state.budget >= 3_000_000:
                    st.session_state.budget -= 3_000_000
                    st.session_state.facilities["Training"] += 1
                    add_news("Training upgraded. Player development improves.")
                    st.rerun()
        with c3:
            st.metric("Stadium", st.session_state.facilities["Stadium"], delta="Home Field (Tiered)")
            st.caption("Tier: <7 none, 7–8 small, 9+ big.")
            if st.button("Upgrade ($10M)", key="us"):
                if st.session_state.budget >= 10_000_000:
                    st.session_state.budget -= 10_000_000
                    st.session_state.facilities["Stadium"] += 1
                    st.session_state.prestige = min(99, st.session_state.prestige + 1)
                    add_news("Stadium upgraded. Home field advantage grows.")
                    st.rerun()

    with tab4:
        if len(st.session_state.staff) < 4:
            st.error("Fill Staff First!")
            return

        if not st.session_state.schedule:
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)

        st.session_state.game_plan = st.selectbox(
            "Weekly Gameplan",
            ["Conservative", "Normal", "Aggressive"],
            index=["Conservative", "Normal", "Aggressive"].index(st.session_state.game_plan)
        )

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

        st.divider()
        render_news_box()
        st.divider()

        if not st.session_state.season_simulated:
            wk = st.session_state.week_index
            if wk < 12:
                opp = st.session_state.schedule[wk]
                opp_data = ensure_opp_units(st.session_state.opponents_db.get(opp, {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 7}))
                is_riv = (opp == st.session_state.team_rival)
                opp_off = int(opp_data["OffOVR"])
                opp_def = int(opp_data["DefOVR"])

                st.subheader(f"Next Game: Week {wk+1} vs {opp}")
                st.caption(f"Matchup: Your OFF {st.session_state.team_off} vs Opp DEF {opp_def} | Your DEF {st.session_state.team_def} vs Opp OFF {opp_off}")
                st.caption(f"Stadiums: Yours {st.session_state.facilities['Stadium']} | Opp {opp_data.get('Stadium',7)}")

                if is_riv:
                    st.warning("RIVALRY WEEK: More chaos, bigger stakes!")

                colA, colB = st.columns(2)

                def play_one_week():
                    res = engine_play_game_v8(
                        st.session_state.team_off, st.session_state.team_def,
                        opp_off, opp_def,
                        st.session_state.staff, st.session_state.my_schemes,
                        {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                        st.session_state.game_plan,
                        opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                        is_home=(wk % 2 == 0), is_rival=is_riv,
                        my_stadium_level=st.session_state.facilities["Stadium"],
                        opp_stadium_level=opp_data.get("Stadium", 7)
                    )
                    st.session_state.season_logs.append({
                        "Week": wk + 1, "Opponent": opp, "Score": f"{res['result']} {res['score']}",
                        "Stats": res["stats"], "Explain": res["explain"], "OppOVR": int(opp_data.get("OVR", 80))
                    })
                    if res["result"] == "W":
                        st.session_state.record["w"] += 1
                        st.session_state.career_stats["w"] += 1
                        st.session_state.job_security = min(100, st.session_state.job_security + (5 if is_riv else 2))
                        add_news(f"{st.session_state.team_name} wins Week {wk+1} vs {opp} ({res['score']}).")
                    else:
                        st.session_state.record["l"] += 1
                        st.session_state.career_stats["l"] += 1
                        pen = 2 if st.session_state.tenure <= 2 else 5
                        st.session_state.job_security = max(0, st.session_state.job_security - pen)
                        add_news(f"{st.session_state.team_name} loses Week {wk+1} vs {opp} ({res['score']}).")

                    st.session_state.week_index += 1
                    if st.session_state.week_index >= 12:
                        end_regular_season_and_stay_on_results()

                if colA.button("🏈 PLAY WEEK", type="primary"):
                    play_one_week()
                    st.rerun()

                if colB.button("⏩ SIM REST OF SEASON"):
                    while not st.session_state.season_simulated:
                        wk2 = st.session_state.week_index
                        if wk2 >= 12: break
                        opp2 = st.session_state.schedule[wk2]
                        opp_data2 = ensure_opp_units(st.session_state.opponents_db.get(opp2, {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 7}))
                        res2 = engine_play_game_v8(
                            st.session_state.team_off, st.session_state.team_def,
                            int(opp_data2["OffOVR"]), int(opp_data2["DefOVR"]),
                            st.session_state.staff, st.session_state.my_schemes,
                            {"Off": opp_data2.get("Off", "Pro Style"), "Def": opp_data2.get("Def", "Man Coverage")},
                            st.session_state.game_plan,
                            opp_data2.get("Coaches", {"OC": 5, "DC": 5}),
                            is_home=(wk2 % 2 == 0), is_rival=(opp2 == st.session_state.team_rival),
                            my_stadium_level=st.session_state.facilities["Stadium"],
                            opp_stadium_level=opp_data2.get("Stadium", 7)
                        )
                        st.session_state.season_logs.append({
                            "Week": wk2 + 1, "Opponent": opp2, "Score": f"{res2['result']} {res2['score']}",
                            "Stats": res2["stats"], "Explain": res2["explain"], "OppOVR": int(opp_data2.get("OVR", 80))
                        })
                        if res2["result"] == "W":
                            st.session_state.record["w"] += 1
                            st.session_state.career_stats["w"] += 1
                            st.session_state.job_security = min(100, st.session_state.job_security + (5 if is_riv2 else 2))
                        else:
                            st.session_state.record["l"] += 1
                            st.session_state.career_stats["l"] += 1
                            pen = 2 if st.session_state.tenure <= 2 else 5
                            st.session_state.job_security = max(0, st.session_state.job_security - pen)

                        st.session_state.week_index += 1
                        if st.session_state.week_index >= 12: break

                    end_regular_season_and_stay_on_results()
                    st.rerun()

    with tab5:
        st.subheader("🏛️ Trophy Case (Quick View)")
        cs = st.session_state.career_stats
        st.write(f"**Titles:** {cs['titles']}  |  **Bowl W-L:** {cs['bowl_w']}-{cs['bowl_l']}  |  **Career W-L:** {cs['w']}-{cs['l']}")
        st.write(f"**Current Prestige:** {st.session_state.prestige}")
        st.write(f"**Legacy (Saban) Score:** {calculate_saban_score(cs, st.session_state.prestige)}")
        st.divider()
        render_trophy_gallery("🏆 Trophy Case Gallery")
        st.divider()
        st.subheader("📚 Season History")
        if st.session_state.history:
            st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
        else:
            st.info("No completed seasons yet. Win some hardware!")

def show_season_end():
    st.title("📊 Season End — Results Hub")
    st.markdown(f"<div class='nil-alert'>Regular season complete. Record: <b>{st.session_state.record['w']}-{st.session_state.record['l']}</b> | Budget: <b>{helper_format_cash(st.session_state.budget)}</b></div>", unsafe_allow_html=True)

    render_news_box()
    st.divider()

    st.subheader("Game-by-game recap")
    for log in st.session_state.season_logs:
        res = "W" if log["Score"].startswith("W") else "L"
        css = "game-card-win" if res == "W" else "game-card-loss"
        s = log["Stats"]
        st.markdown(f"""
        <div class='game-card {css}'>
            <div class='card-header'><span>{log['Score']}</span><span>vs {log['Opponent']} (OVR {log.get('OppOVR','?')})</span></div>
            <div class='stat-grid'>
                <div class='stat-row'><span>🔥 QB Duel</span><span>{s['qb_duel'][0]} vs {s['qb_duel'][1]}</span></div>
                <div class='stat-row'><span>⚔️ OFF vs DEF</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div>
                <div class='stat-row'><span>🛡️ DEF vs OFF</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div>
                <div class='stat-row'><span>🧠 Staff</span><span>{s['staff'][0]} vs {s['staff'][1]}</span></div>
                <div class='stat-row'><span>💪 Raw</span><span>{s['raw_roster']}</span></div>
            </div>
        </div>""", unsafe_allow_html=True)
        with st.expander(f"Why this result? Week {log['Week']} vs {log['Opponent']}"):
            e = log.get("Explain", {})
            st.write(f"Your OFF/DEF: **{e.get('my_off','?')} / {e.get('my_def','?')}**")
            st.write(f"Opp OFF/DEF: **{e.get('opp_off','?')} / {e.get('opp_def','?')}**")
            st.write(f"OFF-DEF edge (you): **{e.get('my_edge',0):.2f}**")
            st.write(f"OFF-DEF edge (opp): **{e.get('opp_edge',0):.2f}**")
            st.write(f"Scheme (you/opp): **{e.get('scheme_my',0):.2f} / {e.get('scheme_opp',0):.2f}**")
            st.write(f"Coaching (you/opp): **{e.get('coach_my',0):.2f} / {e.get('coach_opp',0):.2f}**")
            st.write(f"Home field factor: **{e.get('home_field',0):.2f}**")
            st.write(f"Gameplan: **{e.get('plan','Normal')}**")

    st.divider()
    c1, c2 = st.columns(2)

    if c1.button("Proceed to Postseason 🏁", type="primary"):
        wins = st.session_state.record["w"]
        rank = max(1, 130 - (wins * 10))
        if rank <= 12:
            st.session_state.postseason_data = init_playoff_bracket(rank, st.session_state.team_name)
        else:
            bowl = get_bowl_name(rank)
            candidates = [t for t in ALL_TEAMS if t != st.session_state.team_name]
            opp = random.choice(candidates)
            st.session_state.postseason_data = {
                "Type": "BOWL", "Bowl": bowl, "Rank": rank, "Opponent": opp,
                "OppData": ensure_opp_units(st.session_state.opponents_db.get(opp, {"OVR": 85, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 8}))
            }
        st.session_state.game_state = "POSTSEASON"
        st.rerun()

    if c2.button("Back to Dashboard"):
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

def show_postseason():
    st.title("Postseason Hub")
    data = st.session_state.postseason_data

    if data.get("Type") == "BOWL":
        bowl_name = data["Bowl"]
        st.markdown(f"<div class='bracket-box'><h3>{bowl_name}</h3><h1>VS {data['Opponent']}</h1></div>", unsafe_allow_html=True)
        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            opp_data = ensure_opp_units(data["OppData"])
            res = engine_play_game_v8(
                st.session_state.team_off, st.session_state.team_def,
                int(opp_data["OffOVR"]), int(opp_data["DefOVR"]),
                st.session_state.staff, st.session_state.my_schemes,
                {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                st.session_state.game_plan,
                opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                is_home=False, is_rival=False,
                my_stadium_level=st.session_state.facilities["Stadium"],
                opp_stadium_level=opp_data.get("Stadium", 8)
            )
            wins = st.session_state.record["w"] + (1 if res["result"] == "W" else 0)
            losses = st.session_state.record["l"] + (1 if res["result"] == "L" else 0)

            if res["result"] == "W":
                st.session_state.budget += 2_000_000
                st.session_state.career_stats["bowl_w"] += 1
                add_news(f"{st.session_state.team_name} wins {bowl_name}! ({res['score']})")
                award_trophy(bowl_name if bowl_name in TROPHY_ICONS else "Bowl Win")
                st.toast("🎳 BOWL WIN BONUS: $2M")
            else:
                st.session_state.career_stats["bowl_l"] += 1
                add_news(f"{st.session_state.team_name} falls in {bowl_name} ({res['score']})")

            delta = wins - st.session_state.expected_wins
            if delta > 0: st.session_state.budget += delta * 1_000_000
            elif delta < 0: st.session_state.budget -= abs(delta) * 500_000

            hist = {"Year": st.session_state.year, "Record": f"{wins}-{losses}", "Rank": f"#{data['Rank']}", "Bowl": bowl_name}
            st.session_state.history.append(hist)

            st.session_state.game_state = "SEASON_RECAP"
            st.session_state.offseason_step = 1
            st.rerun()

    elif data.get("Type") == "CFP":
        st.header(f"CFP Round: {['Opening Rd', 'Quarterfinals', 'Semifinals', 'Championship'][data['Round'] - 1]}")
        st.write("--- Bracket Status ---")
        for m in data["Matches"]:
            if m.get("winner"):
                st.markdown(f"<div class='bracket-row'>✅ {m['winner']} advances</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bracket-row'>{m['t1']} vs {m['t2']}</div>", unsafe_allow_html=True)

        user_match = None
        for m in data["Matches"]:
            if m["t1"] == st.session_state.team_name or m["t2"] == st.session_state.team_name:
                user_match = m
                break

        if data.get("UserAlive") and user_match:
            opp = user_match["t2"] if user_match["t1"] == st.session_state.team_name else user_match["t1"]
            opp_data = ensure_opp_units(st.session_state.opponents_db.get(opp, {"OVR": 88, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 9}))
            st.info(f"Your Matchup: vs {opp} (OVR: {opp_data.get('OVR',88)})")
            if st.button("PLAY PLAYOFF GAME 🏈", type="primary"):
                res = engine_play_game_v8(
                    st.session_state.team_off, st.session_state.team_def,
                    int(opp_data["OffOVR"]), int(opp_data["DefOVR"]),
                    st.session_state.staff, st.session_state.my_schemes,
                    {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                    st.session_state.game_plan,
                    opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                    is_home=False, is_rival=False,
                    my_stadium_level=st.session_state.facilities["Stadium"],
                    opp_stadium_level=opp_data.get("Stadium", 9)
                )
                next_round_teams = []
                for m in data["Matches"]:
                    if m is user_match:
                        if res["result"] == "W":
                            m["winner"] = st.session_state.team_name
                            next_round_teams.append(st.session_state.team_name)
                            add_news(f"{st.session_state.team_name} advances in the CFP!")
                        else:
                            m["winner"] = opp
                            next_round_teams.append(opp)
                            st.session_state.postseason_data["UserAlive"] = False
                            add_news(f"{st.session_state.team_name} is eliminated by {opp}.")
                    else:
                        t1, t2 = m["t1"], m["t2"]
                        o1 = st.session_state.opponents_db.get(t1, {"OVR": 82}).get("OVR", 82)
                        o2 = st.session_state.opponents_db.get(t2, {"OVR": 82}).get("OVR", 82)
                        p = o1 / max(1.0, (o1 + o2))
                        winner = t1 if random.random() < p else t2
                        m["winner"] = winner
                        next_round_teams.append(winner)

                time.sleep(0.6)
                if st.session_state.postseason_data["UserAlive"]:
                    if data["Round"] == 4:
                        st.session_state.budget += 50_000_000
                        st.session_state.career_stats["titles"] += 1
                        st.balloons()
                        st.success("NATIONAL CHAMPIONS!")
                        add_news(f"{st.session_state.team_name} wins the NATIONAL TITLE!")
                        award_trophy("National Title")
                        hist = {"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Bowl": "National Title"}
                        st.session_state.history.append(hist)
                        st.session_state.game_state = "SEASON_RECAP"
                        st.rerun()
                    else:
                        new_matches = []
                        if data["Round"] == 1:
                            seeds = data["QF_Seeds"]
                            for i in range(4): new_matches.append({"t1": seeds[i], "t2": next_round_teams[3 - i], "winner": None})
                        elif data["Round"] == 2:
                            new_matches.append({"t1": next_round_teams[0], "t2": next_round_teams[3], "winner": None})
                            new_matches.append({"t1": next_round_teams[1], "t2": next_round_teams[2], "winner": None})
                        elif data["Round"] == 3:
                            new_matches.append({"t1": next_round_teams[0], "t2": next_round_teams[1], "winner": None})
                        st.session_state.postseason_data["Round"] += 1
                        st.session_state.postseason_data["Matches"] = new_matches
                        st.rerun()
                else:
                    hist = {"Year": st.session_state.year, "Record": "Playoff Loss", "Rank": f"#{data.get('Rank','?')}", "Bowl": "CFP"}
                    st.session_state.history.append(hist)
                    st.session_state.game_state = "SEASON_RECAP"
                    st.rerun()
        else:
            st.info("You are no longer alive in the bracket (or you had a BYE).")
            if st.button("Continue to Summary", type="primary"):
                st.session_state.game_state = "SEASON_RECAP"
                st.rerun()

def show_season_recap():
    st.title(f"SEASON RECAP: {st.session_state.year}")
    
    wins = st.session_state.record['w']
    losses = st.session_state.record['l']
    
    this_year_hist = next((h for h in st.session_state.history if h["Year"] == st.session_state.year), None)
    
    final_rank = this_year_hist["Rank"] if this_year_hist else "Unranked"
    bowl_res = this_year_hist["Bowl"] if this_year_hist else "No Bowl"
    
    expect = st.session_state.expected_wins
    delta = wins - expect
    
    booster_change = delta * 5
    if "National Title" in bowl_res: booster_change += 20
    elif "Bowl Win" in bowl_res: booster_change += 5
    elif "Playoff Loss" in bowl_res: booster_change += 10
    
    current_boost = max(0, min(100, st.session_state.booster_rating + booster_change))
    
    if "National Title" in bowl_res:
        headline = "DYNASTY! NATIONAL CHAMPIONS!"
        subhead = f"{st.session_state.team_name} shocks the world and takes the crown!"
    elif delta >= 3:
        headline = "Exceeding All Expectations!"
        subhead = f"Fans are ecstatic as {st.session_state.team_name} dominates the competition."
    elif delta <= -3:
        headline = "Disaster in the Making?"
        subhead = f"Boosters grow restless as {st.session_state.team_name} underperforms."
    elif wins > losses:
        headline = "Solid Season in the Books"
        subhead = f"The {st.session_state.team_name} finish with a record of {wins}-{losses}."
    else:
        headline = "Rebuilding Year Concludes"
        subhead = f"The {st.session_state.team_name} finish with a record of {wins}-{losses}."

    st.markdown(f"<div class='newspaper-head'>{headline}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='newspaper-sub'>{subhead}</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📊 Final Report Card")
        st.markdown(f"**Final Rank:** {final_rank}")
        st.markdown(f"**Record:** {wins}-{losses}")
        st.markdown(f"**Postseason:** {bowl_res}")
        st.markdown(f"**Expectation:** {expect} Wins")
        
        if delta > 0:
            st.success(f"Result: {delta} wins ABOVE expectation.")
        elif delta < 0:
            st.error(f"Result: {abs(delta)} wins BELOW expectation.")
        else:
            st.info("Result: Met expectations.")

    with c2:
        st.subheader("💰 Booster Confidence")
        st.write("Confidence determines offseason donations and job security pressure.")
        
        st.markdown(f"""
        <div class="booster-meter-container">
            <div class="booster-meter-fill" style="width: {current_boost}%; background-color: {'#28a745' if current_boost > 60 else ('#dc3545' if current_boost < 40 else '#ffc107')};"></div>
        </div>
        <div style="text-align:center; font-weight:bold; margin-top:5px;">{current_boost}/100</div>
        """, unsafe_allow_html=True)
        
        if current_boost > 80:
            st.success("Boosters are opening their checkbooks! Expect a budget bonus.")
        elif current_boost < 30:
            st.error("Boosters are angry. Job security is critical.")
        else:
            st.info("Boosters are satisfied, but want more next year.")

    st.divider()
    st.subheader("🏆 Legacy Growth (This Season)")
    
    bowl_w_add = 1 if "Win" in bowl_res or "National" in bowl_res else 0
    title_add = 1 if "National" in bowl_res else 0
    
    colA, colB, colC = st.columns(3)
    colA.metric("Wins Added", f"+{wins}")
    colB.metric("Bowl Wins", f"+{bowl_w_add}")
    colC.metric("Titles", f"+{title_add}")
    
    st.divider()
    
    if st.button("Close the Book on " + str(st.session_state.year) + " -> Go to Offseason", type="primary"):
        st.session_state.booster_rating = current_boost
        
        if current_boost >= 80:
            bonus = 3_000_000
            st.session_state.budget += bonus
            st.toast(f"Booster Donation: +{helper_format_cash(bonus)}")
        elif current_boost <= 20:
            st.session_state.job_security -= 10
            st.toast("Boosters pressure administration: Security -10")
            
        st.session_state.game_state = "OFFSEASON"
        st.session_state.offseason_step = 1
        st.rerun()

def show_offseason():
    st.title("Offseason Hub")
    st.markdown(f"<div class='nil-alert'>💰 Offseason Budget: {helper_format_cash(st.session_state.budget)}</div>", unsafe_allow_html=True)

    if st.session_state.pending_invite:
        inv = st.session_state.pending_invite
        st.warning(f"📨 Conference Invite: Join the **{inv['to_conf']}** (Revenue boost x{inv['boost_mult']:.2f}). {inv['note']}")
        c1, c2 = st.columns(2)
        if c1.button("Accept Invite ✅", type="primary"):
            apply_conference_move(inv["to_conf"], inv["boost_mult"])
            st.session_state.pending_invite = None
            st.rerun()
        if c2.button("Decline ❌"):
            add_news(f"{st.session_state.team_name} declines the {inv['to_conf']} invite.")
            st.session_state.pending_invite = None
            st.rerun()

    steps = ["1) NIL Prospects (15)", "2) HS Outreach", "3) Top-8 Battles", "Finish Offseason"]
    st.session_state.offseason_step = st.radio(
        "Offseason Steps",
        [1, 2, 3, 4],
        format_func=lambda x: steps[x-1],
        index=max(0, min(3, int(st.session_state.offseason_step)-1))
    )

    if st.session_state.offseason_step == 1:
        show_offseason_nil_v8()
    elif st.session_state.offseason_step == 2:
        show_offseason_hs_outreach()
    elif st.session_state.offseason_step == 3:
        show_offseason_top8_v8()
    else:
        st.subheader("✅ Wrap Up Offseason")
        st.write("This will advance the year, evolve the universe, reset the schedule, and return to Dashboard.")

        if st.button("Advance to Next Season", type="primary"):
            for p in POSITIONS:
                st.session_state.active_transfers[p] = False

            st.session_state.opponents_db = engine_evolve_universe(st.session_state.opponents_db)
            maybe_generate_conference_invite()
            ai_conference_swap_lightweight()

            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.inflation *= 1.05

            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
            st.session_state.hotspots = generate_hotspots()
            st.session_state.week_index = 0
            st.session_state.record = {"w": 0, "l": 0}
            st.session_state.season_logs = []
            st.session_state.season_simulated = False
            st.session_state.season_end_ready = False
            st.session_state.revenue_report = None

            st.session_state.nil_class = []
            st.session_state.hs_total_spend = 0
            st.session_state.hs_shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
            st.session_state.hs_spend_by_pos = {p: 0 for p in POSITIONS}
            st.session_state.top8 = []
            st.session_state.top8_resolved = set()

            add_news(f"New season begins. Needs: {', '.join(st.session_state.team_needs)}.")
            st.session_state.game_state = "DASHBOARD"
            st.rerun()

def show_offseason_nil_v8():
    st.subheader("1) NIL Prospects (Class of 15)")
    needs = st.session_state.get("team_needs", [])

    if not st.session_state.nil_class:
        st.session_state.nil_class = generate_nil_class_15(needs)
        add_news("NIL board posted: 15 prospects (Tier 1/2/3).")

    st.markdown(f"<div class='recruiting-intel'>Team Needs: <b>{', '.join(needs) if needs else 'Balanced'}</b></div>", unsafe_allow_html=True)
    st.write("You can sign any of these 15. When they’re gone, they’re gone (no infinite respawn).")

    signed = sum(1 for p in st.session_state.nil_class if p["status"] == "SIGNED")
    available = 15 - signed
    st.caption(f"Signed: {signed} | Remaining available: {available}")

    for p in st.session_state.nil_class:
        tier_badge = "badge-tier-s" if p["tier"] == 1 else ("badge-tier-a" if p["tier"] == 2 else "badge-tier-f")
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        c1.markdown(f"⭐ <b>{p['tier_label']}</b> — {p['pos']} {p['name']} ({p['rating']}) — {p['trait']}", unsafe_allow_html=True)
        c2.markdown(f"<span class='badge {tier_badge}'>{p['tier_label']}</span>", unsafe_allow_html=True)
        c3.write(f"Ask: {helper_format_cash(p['ask'])}")
        if p["status"] == "SIGNED":
            c4.write("✅ SIGNED")
        else:
            if c4.button("Sign", key=f"nil_sign_{p['id']}"):
                if st.session_state.budget >= p["ask"]:
                    st.session_state.budget -= p["ask"]
                    st.session_state.roster[p["pos"]] = max(st.session_state.roster[p["pos"]], p["rating"])
                    p["status"] = "SIGNED"
                    add_news(f"{st.session_state.team_name} signs NIL {p['tier_label']} {p['pos']} {p['name']} ({p['rating']}).")
                    st.toast("Signed ✔️")
                    st.rerun()
                else:
                    st.error("Not enough budget.")

def show_offseason_hs_outreach():
    st.subheader("2) HS Outreach (Fast Input)")
    st.write("Pick a **total HS outreach spend** once, then allocate by position using % sliders (auto-normalized).")
    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    needs = st.session_state.get("team_needs", [])
    st.markdown(f"<div class='recruiting-intel'>Pipeline Bonus ({st.session_state.home_region}): {', '.join(hot)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='recruiting-intel'>Team Needs: <b>{', '.join(needs)}</b></div>", unsafe_allow_html=True)

    max_spend = max(0, int(st.session_state.budget))
    st.session_state.hs_total_spend = st.slider("Total HS Outreach Spend", 0, max_spend, min(int(st.session_state.hs_total_spend), max_spend), 100_000)

    shares = dict(st.session_state.hs_shares)
    st.write("### Allocate % by Position (auto-normalized to 100%)")
    cols = st.columns(2)
    for idx, pos in enumerate(POSITIONS):
        with cols[idx % 2]:
            default = float(shares.get(pos, 100.0 / len(POSITIONS)))
            shares[pos] = st.slider(f"{pos} %{' (NEED)' if pos in needs else ''}", 0.0, 60.0, float(max(0.0, min(60.0, default))), 1.0, key=f"hs_pct_{pos}")

    shares = normalize_shares(shares)
    st.session_state.hs_shares = shares
    spend_by_pos = {p: int(st.session_state.hs_total_spend * (shares[p] / 100.0)) for p in POSITIONS}
    st.session_state.hs_spend_by_pos = spend_by_pos

    st.write("### Preview Spend by Position")
    df = pd.DataFrame([{"Pos": p, "Pct": round(shares[p], 1), "Spend": spend_by_pos[p]} for p in POSITIONS])
    df["Spend_fmt"] = df["Spend"].apply(helper_format_cash)
    st.dataframe(df[["Pos", "Pct", "Spend_fmt"]], use_container_width=True)
    st.divider()

    if st.button("Run HS Outreach", type="primary"):
        if st.session_state.hs_total_spend > st.session_state.budget:
            st.error("You can't spend more than your budget.")
            return

        res = process_hs_outreach(st.session_state.hs_total_spend, shares, st.session_state.staff, st.session_state.prestige, st.session_state.inflation, st.session_state.hotspots, st.session_state.home_region, needs)
        st.session_state.budget -= res["spent"]
        if res["booster_bonus"] > 0:
            st.session_state.budget += res["booster_bonus"]
            st.toast(f"💎 Booster bonus: {helper_format_cash(res['booster_bonus'])}")
            add_news("Boosters celebrate a surprise GEM discovery!")

        for p, g in res["roster_updates"].items():
            loss = random.randint(1, 4)
            st.session_state.roster[p] = max(40, min(99, int(st.session_state.roster[p] - loss + g)))

        if res["gems"]:
            st.session_state.stars.extend(res["gems"])
            add_news(f"Recruiting staff finds {len(res['gems'])} GEM(s)!")

        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
        add_news("HS outreach completed. Rankings buzz increases.")
        st.success("HS Outreach complete! Your roster has been updated.")
        st.rerun()

def show_offseason_top8_v8():
    st.subheader("3) Top-8 Prospect Battles (Clear Status UX)")
    st.write("Each recruit is **OPEN → COMMITTED / LOST** after you pitch. You’ll always know what happened.")
    needs = st.session_state.get("team_needs", [])
    if not st.session_state.top8:
        st.session_state.top8 = generate_top8_prospects(needs)
        st.session_state.top8_resolved = set()
        add_news("Top-8 battles are live. Elite prospects are being recruited nationwide.")

    spend_by_pos = st.session_state.get("hs_spend_by_pos", {p: 0 for p in POSITIONS})
    committed = sum(1 for r in st.session_state.top8 if r["status"] == "COMMITTED")
    lost = sum(1 for r in st.session_state.top8 if r["status"] == "LOST")
    remaining = 8 - (committed + lost)
    st.caption(f"Committed: {committed} | Lost: {lost} | Remaining: {remaining}")

    for r in st.session_state.top8:
        rid = r["id"]
        status = r.get("status", "OPEN")
        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
        c1.write(f"🏅 {r['pos']} {r['name']} ({r['rating']}) — {r['trait']}")
        c2.write(f"Ask: {helper_format_cash(r['ask'])}")
        chance = top8_commit_chance(r, spend_by_pos, st.session_state.staff, st.session_state.prestige)
        c3.write(f"Chance: {int(chance*100)}%")

        if status == "COMMITTED":
            c4.write("✅ COMMIT")
            c5.write(r.get("note", ""))
            continue
        if status == "LOST":
            c4.write("❌ LOST")
            c5.write(r.get("note", ""))
            continue

        pitch_cost = int(max(250_000, r["ask"] * 0.10))
        c4.write(f"Pitch: {helper_format_cash(pitch_cost)}")
        if c5.button("Pitch", key=f"pitch_{rid}"):
            if st.session_state.budget < pitch_cost:
                st.error("Not enough budget to pitch this recruit.")
                return
            st.session_state.budget -= pitch_cost
            if random.random() < chance:
                st.session_state.roster[r["pos"]] = max(st.session_state.roster[r["pos"]], r["rating"])
                st.session_state.stars.append({"id": rid, "name": r["name"], "pos": r["pos"], "rating": r["rating"], "year": "Fr", "trait": r["trait"]})
                booster = int(random.randint(500_000, 3_500_000) * (1.0 + (r["rating"] - 90) / 25))
                st.session_state.budget += booster
                r["status"] = "COMMITTED"
                r["note"] = f"Boosters +{helper_format_cash(booster)}"
                add_news(f"{st.session_state.team_name} lands TOP-8 recruit {r['pos']} {r['name']} ({r['rating']})! Boosters donate {helper_format_cash(booster)}.")
                st.success(f"COMMIT! Booster donation {helper_format_cash(booster)}.")
                st.toast("Top-8 Commit ✅")
            else:
                r["status"] = "LOST"
                r["note"] = "Picked another school"
                add_news(f"{st.session_state.team_name} loses a Top-8 battle for {r['pos']} {r['name']}.")
                st.warning("Missed! Another school won this battle.")
                st.toast("Top-8 Lost ❌")
            st.session_state.top8_resolved.add(rid)
            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
            st.rerun()

    st.divider()
    if remaining == 0:
        st.success("Top-8 battles completed. You can finish the offseason now.")

def show_fired():
    st.error("FIRED! Your tenure has ended.")
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.write(f"Final Legacy (Saban) Score: **{saban}**")
    render_trophy_gallery("🏛️ Your Trophy Gallery (Career)")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()

def show_retirement():
    st.title("Retirement")
    st.write("Thanks for playing!")
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.write(f"Final Legacy (Saban) Score: **{saban}**")
    render_trophy_gallery("🏛️ Your Trophy Gallery (Career)")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()

# ==============================================================================
# ROUTER
# ==============================================================================
if st.session_state.game_state == "SETUP":
    run_setup()
elif st.session_state.game_state == "FIRED":
    show_fired()
elif st.session_state.game_state == "DASHBOARD":
    show_dashboard()
elif st.session_state.game_state == "SEASON_END":
    show_season_end()
elif st.session_state.game_state == "POSTSEASON":
    show_postseason()
elif st.session_state.game_state == "SEASON_RECAP":
    show_season_recap()
elif st.session_state.game_state == "OFFSEASON":
    show_offseason()
elif st.session_state.game_state == "RETIREMENT":
    show_retirement()
else:
    st.session_state.game_state = "DASHBOARD"
    st.rerun()
