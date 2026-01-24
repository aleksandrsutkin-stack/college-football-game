import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# College Football V3.1 (Streamlit)
# ==============================================================================

try:
    st.set_page_config(page_title="College Football V3.1", page_icon="🏈", layout="wide")
except Exception:
    pass

st.markdown(
    """
<style>
.stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: 800; }

.kpi { background: #f8f9fa; border: 1px solid #e6e6e6; padding: 12px; border-radius: 10px; margin-bottom: 10px;}
.box { background: white; border: 1px solid #eee; padding: 12px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
.small { font-size: 0.9em; color: #666; }
.badge { padding: 2px 8px; border-radius: 8px; border: 1px solid #ddd; font-weight: 800; font-size: 0.8em; display: inline-block; margin-right: 6px; margin-top: 4px;}
.badge-green { background: #eaf7ea; border-color: #cfe9cf; color: #1f6c1f; }
.badge-yellow { background: #fff6db; border-color: #ffe6a6; color: #7a5b00; }
.badge-red { background: #fdecec; border-color: #f7caca; color: #8a1a1a; }
.badge-gray { background: #f3f4f6; border-color: #e5e7eb; color: #374151; }

.card { border: 1px solid #eee; border-left: 6px solid #ddd; border-radius: 12px; padding: 12px; margin-bottom: 10px; background: white; }
.win { border-left-color: #2e7d32; }
.loss { border-left-color: #c62828; }
.pending { border-left-color: #6c757d; background: #f8f9fa; }
.rival { border: 2px solid #ffc107; background: #fffaf0; }

.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.row { display: flex; justify-content: space-between; }
.hr { border-top: 1px solid #eee; margin: 10px 0; }

.bracket { background:#111827; color:#fff; border-radius:14px; padding:14px; margin: 10px 0; }
.brrow { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.08); }
.brrow:last-child { border-bottom:none; }
.brseed { opacity:0.85; font-weight:900; margin-right:8px; }
.brtxt { font-weight:800; }
.hi { color:#fde68a; font-weight:900; }
</style>
""",
    unsafe_allow_html=True
)

# ==============================================================================
# STATIC DATA
# ==============================================================================
POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}
SCHEMES = {"Offense": ["Air Raid", "Smashmouth", "Pro Style"], "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]}
COUNTERS = {
    "Air Raid": "3-3-5 Cloud",
    "Smashmouth": "4-4 Heavy",
    "Pro Style": "Man Coverage",
    "3-3-5 Cloud": "Smashmouth",
    "4-4 Heavy": "Air Raid",
    "Man Coverage": "Pro Style",
}
TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
COACH_TRAITS = {
    "None": "None",
    "Recruiter": "+10% Recruiting",
    "Tactician": "+3 Game Boost",
    "Air Raid": "+2 Scheme",
    "Smashmouth": "+2 Scheme",
    "Pro Style": "+2 Scheme",
}
BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"],
}

TEAMS_DB = {
    "Georgia": {"color": "#BA0C2F"},
    "Alabama": {"color": "#9E1B32"},
    "Ohio State": {"color": "#BB0000"},
    "Michigan": {"color": "#00274C"},
    "Texas": {"color": "#BF5700"},
    "Oklahoma": {"color": "#841617"},
    "Oregon": {"color": "#154733"},
    "Washington": {"color": "#4B2E83"},
    "Florida St": {"color": "#782F40"},
    "Miami": {"color": "#005030"},
    "Penn State": {"color": "#041E42"},
    "Notre Dame": {"color": "#0C2340"},
    "LSU": {"color": "#461D7C"},
    "Ole Miss": {"color": "#CE1126"},
    "Tennessee": {"color": "#FF8200"},
    "Auburn": {"color": "#0C2340"},
    "Indiana": {"color": "#990000"},
    "Purdue": {"color": "#CEB888"},
    "Colorado": {"color": "#CFB87C"},
    "USC": {"color": "#990000"},
    "Boise State": {"color": "#0033A0"},
    "San Jose State": {"color": "#0055A2"},
    "Texas A&M": {"color": "#500000"},
    "Texas Tech": {"color": "#CC0000"},
    "BYU": {"color": "#002E5D"},
    "Tulane": {"color": "#006747"},
}

REAL_WORLD_INIT = {
    "Indiana": {"Prestige": 70, "Talent": 86, "Tier": 2, "Rival": "Purdue"},
    "Ohio State": {"Prestige": 95, "Talent": 94, "Tier": 1, "Rival": "Michigan"},
    "Miami": {"Prestige": 88, "Talent": 89, "Tier": 2, "Rival": "Florida St"},
    "Oregon": {"Prestige": 93, "Talent": 92, "Tier": 1, "Rival": "Washington"},
    "Georgia": {"Prestige": 92, "Talent": 96, "Tier": 1, "Rival": "Florida"},
    "Ole Miss": {"Prestige": 86, "Talent": 88, "Tier": 2, "Rival": "Mississippi St"},
    "Texas Tech": {"Prestige": 78, "Talent": 84, "Tier": 3, "Rival": "Baylor"},
    "Texas A&M": {"Prestige": 86, "Talent": 91, "Tier": 2, "Rival": "Texas"},
    "Alabama": {"Prestige": 90, "Talent": 95, "Tier": 1, "Rival": "Auburn"},
    "Notre Dame": {"Prestige": 88, "Talent": 90, "Tier": 2, "Rival": "USC"},
    "BYU": {"Prestige": 75, "Talent": 82, "Tier": 3, "Rival": "Utah"},
    "Texas": {"Prestige": 90, "Talent": 97, "Tier": 1, "Rival": "Oklahoma"},
    "Oklahoma": {"Prestige": 86, "Talent": 90, "Tier": 2, "Rival": "Texas"},
    "Utah": {"Prestige": 78, "Talent": 85, "Tier": 3, "Rival": "BYU"},
    "Vanderbilt": {"Prestige": 72, "Talent": 78, "Tier": 4, "Rival": "Tennessee"},
    "USC": {"Prestige": 85, "Talent": 89, "Tier": 2, "Rival": "Notre Dame"},
    "Michigan": {"Prestige": 90, "Talent": 91, "Tier": 1, "Rival": "Ohio State"},
    "Penn State": {"Prestige": 86, "Talent": 88, "Tier": 2, "Rival": "Ohio State"},
    "LSU": {"Prestige": 88, "Talent": 92, "Tier": 2, "Rival": "Alabama"},
    "Florida St": {"Prestige": 82, "Talent": 87, "Tier": 3, "Rival": "Miami"},
    "Colorado": {"Prestige": 76, "Talent": 85, "Tier": 3, "Rival": "Nebraska"},
    "Boise State": {"Prestige": 74, "Talent": 79, "Tier": 3, "Rival": "Fresno St"},
    "Tulane": {"Prestige": 73, "Talent": 77, "Tier": 3, "Rival": "LSU"},
}

CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Texas A&M", "Ole Miss", "Vanderbilt", "Florida", "Mississippi St"],
    "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington", "Indiana", "Nebraska", "Purdue"],
    "ACC": ["Florida St", "Clemson", "Miami", "Stanford", "Cal", "Louisville", "UNC", "Virginia Tech", "SMU"],
    "Big 12": ["Utah", "TCU", "Baylor", "Texas Tech", "Arizona State", "Colorado", "Kansas State", "Oklahoma St", "BYU", "Arizona"],
    "G5": ["Boise State", "San Jose State", "San Diego St", "Nevada", "Wyoming", "Air Force", "Colorado St", "Fresno St", "Tulane", "Memphis", "Navy", "Army"],
}
ALL_TEAMS = [t for c in CONFERENCES.values() for t in c]

# ==============================================================================
# HELPERS
# ==============================================================================
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def helper_format_cash(amount: int) -> str:
    if amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    return f"${int(amount/1_000)}K"

def generate_name() -> str:
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Tank", "Arch", "Shedeur", "Quinn", "Travis", "Ashton", "Malik", "Jayden"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck", "Jeanty", "Judkins", "McCarthy", "Henderson"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name() -> str:
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan", "Kalen", "Mike", "James"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman", "Lanning", "DeBoer", "Norvell", "Franklin"]
    return f"{random.choice(first)} {random.choice(last)}"

def compute_team_needs(roster: dict, n: int = 3):
    items = sorted(roster.items(), key=lambda kv: kv[1])
    return [p for p, _ in items[:n]]

def add_news(msg: str):
    if "news" not in st.session_state:
        st.session_state.news = []
    st.session_state.news.insert(0, f"• {msg}")
    st.session_state.news = st.session_state.news[:40]

def generate_hotspots():
    return {reg: random.sample(POSITIONS, 2) for reg in REGION_STRENGTH.keys()}

def get_letter_grade(val):
    if val >= 9:
        return "A+"
    if val >= 8:
        return "A"
    if val >= 7:
        return "B"
    if val >= 5:
        return "C"
    if val >= 3:
        return "D"
    return "F"

def generate_star_player(position, tier):
    return {
        "id": random.randint(10000, 99999),
        "name": generate_name(),
        "pos": position,
        "rating": min(99, 85 + random.randint(0, 10)),
        "year": "Fr",
        "trait": random.choice(TRAITS),
    }

def generate_ga_coach(role):
    return {
        "name": f"GA {generate_name()}",
        "role": role,
        "off": random.randint(1, 3),
        "def": random.randint(1, 3),
        "recruit": random.randint(1, 2),
        "trait": "None",
        "salary": 0,
        "history": "Former Player",
        "scouted": True,
    }

def get_bowl_name(rank: int) -> str:
    if rank <= 25:
        return random.choice(BOWL_MAPPING["Elite"])
    if rank <= 45:
        return random.choice(BOWL_MAPPING["High"])
    if rank <= 80:
        return random.choice(BOWL_MAPPING["Mid"])
    return random.choice(BOWL_MAPPING["Low"])

# ==============================================================================
# PROGRAM / FACILITY EFFECTS
# ==============================================================================
def training_unit_boost(training_lvl: int) -> float:
    return 0.8 + training_lvl * 0.55

def stadium_home_field(stadium_lvl: int) -> float:
    return clamp(0.6 * stadium_lvl - 1.0, 0.0, 8.0)

def stadium_night_game_aura(stadium_lvl: int, site: str) -> float:
    if site != "HOME":
        return 0.0
    if stadium_lvl >= 8 and random.random() < 0.22:
        return random.uniform(0.8, 2.2)
    return 0.0

# ==============================================================================
# ECONOMY / GENERATION
# ==============================================================================
def engine_calculate_revenue(tier, marketing_lvl, inflation):
    base = {1: 40_000_000, 2: 25_000_000, 3: 10_000_000, 4: 5_000_000}.get(tier, 5_000_000)
    marketing_bonus = marketing_lvl * 2_000_000
    total = (base + marketing_bonus) * inflation
    return int(total)

def engine_generate_coach(role, tier):
    cost = random.randint(4_000_000, 8_000_000) if tier == 1 else random.randint(500_000, 3_500_000)
    trait_pool = list(COACH_TRAITS.keys())
    if role == "OC":
        trait_pool = ["Air Raid", "Smashmouth", "Pro Style", "Recruiter", "Tactician", "None"]
    elif role == "Scout":
        trait_pool = ["Recruiter", "None"]
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
        "scouted": False,
    }

def engine_generate_roster(tier, base_ovr=None):
    base = base_ovr if base_ovr else (90 if tier == 1 else 74)
    roster = {}
    for p in POSITIONS:
        roster[p] = min(99, max(40, base + random.randint(-4, 4)))
    return roster

def engine_generate_schedule(my_team, my_conf, rival):
    conf_foes = [t for t in CONFERENCES.get(my_conf, CONFERENCES["G5"]) if t != my_team]
    schedule = random.sample(conf_foes, min(8, len(conf_foes)))
    needed = 12 - len(schedule)
    non_conf = [t for t in ALL_TEAMS if t not in CONFERENCES.get(my_conf, []) and t != my_team]
    if needed > 0 and non_conf:
        schedule += random.sample(non_conf, min(needed, len(non_conf)))
    if rival in ALL_TEAMS:
        if rival in schedule:
            schedule.remove(rival)
        schedule.append(rival)
    random.shuffle(schedule)
    return schedule[:12]

def split_ovr_into_units(ovr: int):
    skew = random.randint(-5, 5)
    off = clamp(ovr + skew, 40, 99)
    deff = clamp(ovr - skew, 40, 99)
    return off, deff

# ==============================================================================
# GAME SIM (with breakdown for "why")
# ==============================================================================
def engine_play_game(
    my_off, my_def,
    opp_off, opp_def,
    staff, schemes, opp_schemes,
    game_plan,
    opp_coaches,
    site,              # "HOME" | "AWAY" | "NEUTRAL"
    is_rival,
    my_stadium_lvl, opp_stadium_lvl,
    force_luck=None, force_total_points=None
):
    style = st.session_state.get("sim_style", "Management")
    if style == "Management":
        base_sd = 6.0
        talent_w1 = 0.95
        talent_w2 = 0.85
        coach_w = 1.35
        scheme_w = 1.15
    elif style == "Chaos":
        base_sd = 12.0
        talent_w1 = 0.75
        talent_w2 = 0.65
        coach_w = 1.00
        scheme_w = 1.00
    else:
        base_sd = 9.0
        talent_w1 = 0.85
        talent_w2 = 0.75
        coach_w = 1.15
        scheme_w = 1.05

    my_oc = staff.get("OC", {}).get("off", 5)
    my_dc = staff.get("DC", {}).get("def", 5)
    my_hc = staff.get("HC", {}).get("recruit", 5)
    hc_trait = staff.get("HC", {}).get("trait", "None")
    oc_trait = staff.get("OC", {}).get("trait", "None")

    opp_oc = opp_coaches.get("OC", 5)
    opp_dc = opp_coaches.get("DC", 5)

    def tier_bonus(r):
        if r >= 8:
            return 3.0
        if r <= 4:
            return -3.0
        return 0.0

    coaching_net = ((tier_bonus(my_oc) - tier_bonus(opp_dc)) + (tier_bonus(my_dc) - tier_bonus(opp_oc))) * coach_w
    if hc_trait == "Tactician":
        coaching_net += 1.2
    if hc_trait == "Recruiter":
        coaching_net += 0.3
    if oc_trait in ["Air Raid", "Smashmouth", "Pro Style"] and oc_trait == schemes.get("Off"):
        coaching_net += 0.8

    talent_gap = ((my_off - opp_def) * talent_w1) + ((my_def - opp_off) * talent_w2)

    scheme_bonus = 0.0
    opp_def_scheme = opp_schemes.get("Def", "Man Coverage")
    my_off_scheme = schemes.get("Off", "Pro Style")
    if COUNTERS.get(opp_def_scheme, "Pro Style") == my_off_scheme:
        scheme_bonus += 3.0 * scheme_w
    elif COUNTERS.get(my_off_scheme, "Man Coverage") == opp_def_scheme:
        scheme_bonus -= 3.0 * scheme_w

    if site == "HOME":
        home_bonus = stadium_home_field(my_stadium_lvl)
    elif site == "AWAY":
        home_bonus = -stadium_home_field(opp_stadium_lvl)
    else:
        home_bonus = 0.0
    home_bonus += stadium_night_game_aura(my_stadium_lvl, site)

    var_mult = 1.0
    if is_rival:
        var_mult *= 1.20
    if game_plan == "Aggressive":
        var_mult *= 1.12
    if game_plan == "Conservative":
        var_mult *= 0.85

    coach_consistency = clamp((my_hc - 5) * 0.06 + (my_oc - 5) * 0.04 + (my_dc - 5) * 0.04, -0.20, 0.25)
    sd = base_sd * var_mult * (1.0 - coach_consistency)

    luck = force_luck if force_luck is not None else random.gauss(0, sd)
    margin = talent_gap + scheme_bonus + coaching_net + home_bonus + luck

    if force_total_points is not None:
        total_points = int(force_total_points)
    else:
        total_points = int(clamp(random.gauss(56, 12), 24, 92))

    spread = clamp(margin, -42, 42)

    my_score = int(round((total_points / 2) + (spread / 2)))
    opp_score = int(total_points - my_score)
    my_score = int(clamp(my_score, 0, 70))
    opp_score = int(clamp(opp_score, 0, 70))

    return {
        "result": "W" if margin > 0 else "L",
        "score": f"{my_score}-{opp_score}",
        "margin": round(margin, 1),
        "factors": {
            "talent_gap": round(talent_gap, 1),
            "coaching_net": round(coaching_net, 1),
            "scheme_bonus": round(scheme_bonus, 1),
            "home_bonus": round(home_bonus, 1),
            "luck": round(luck, 1),
            "sd": round(sd, 1),
        },
    }

def project_margin_only(my_off, my_def, opp_off, opp_def, staff, schemes, opp_schemes, game_plan, opp_coaches, site, is_rival, my_std, opp_std):
    res = engine_play_game(
        my_off, my_def, opp_off, opp_def,
        staff, schemes, opp_schemes,
        game_plan, opp_coaches,
        site, is_rival,
        my_std, opp_std,
        force_luck=0.0, force_total_points=56
    )
    return res["margin"], res["factors"]

# ==============================================================================
# AI UNIVERSE EVOLUTION + AI RECRUITING (Proposal G)
# ==============================================================================
def ai_recruiting_spend_adjust(opponents_db: dict, inflation: float):
    for _, d in opponents_db.items():
        tier = d.get("Tier", 3)
        pres = d.get("Prestige", 70)
        marketing = d.get("Marketing", 6)
        scout = d.get("Coaches", {}).get("Scout", 5) if isinstance(d.get("Coaches"), dict) else 5

        base = {1: 9_000_000, 2: 6_000_000, 3: 3_500_000, 4: 2_000_000}.get(tier, 3_000_000)
        pres_mult = 1.0 + (pres - 70) * 0.012
        mkt_mult = 1.0 + (marketing - 6) * 0.03
        budget = int(base * pres_mult * mkt_mult * inflation)

        eff = clamp(1.0 + (scout - 5) * 0.05, 0.75, 1.25)
        unit_delta = (budget / (6_500_000 * inflation)) * 2.2 * eff
        unit_delta = unit_delta ** 0.85
        unit_delta += random.uniform(-0.6, 1.0)

        gem_chance = clamp(0.04 + (budget / (10_000_000 * inflation)) * 0.06 + (pres - 75) * 0.004, 0.03, 0.18)
        if random.random() < gem_chance:
            unit_delta += random.uniform(1.8, 3.6)

        d["OffOVR"] = int(clamp(d.get("OffOVR", d["OVR"]) + unit_delta + random.uniform(-0.6, 0.8), 40, 99))
        d["DefOVR"] = int(clamp(d.get("DefOVR", d["OVR"]) + unit_delta + random.uniform(-0.8, 0.6), 40, 99))
        d["OVR"] = int(clamp((d["OffOVR"] + d["DefOVR"]) / 2 + random.randint(-1, 1), 40, 99))
    return opponents_db

def engine_evolve_universe(opponents_db: dict, inflation: float):
    for _, d in opponents_db.items():
        ovr = d.get("OVR", 70)
        wins = int((ovr / 100) * 12) + random.randint(-2, 2)
        wins = int(clamp(wins, 0, 12))
        d["LastWins"] = wins

        change = 0
        if wins >= 10:
            change = 3
        elif wins <= 4:
            change = -3
        d["Prestige"] = int(clamp(d.get("Prestige", 70) + change, 20, 99))

        if "Coaches" not in d:
            d["Coaches"] = {"OC": random.randint(4, 8), "DC": random.randint(4, 8), "Scout": random.randint(4, 8)}

        if d["Prestige"] > 84 and wins < 7:
            d["Coaches"]["OC"] = random.randint(7, 9)
            d["Coaches"]["DC"] = random.randint(7, 9)
            d["Coaches"]["Scout"] = random.randint(6, 9)
        elif d["Prestige"] < 70 and wins > 9:
            d["Coaches"]["OC"] = random.randint(3, 6)
            d["Coaches"]["DC"] = random.randint(3, 6)
            d["Coaches"]["Scout"] = random.randint(3, 6)

        base_ovr = int(d["Prestige"] * 0.90) + random.randint(-2, 2)
        base_ovr = int(clamp(base_ovr, 45, 99))

        if "OffOVR" not in d or "DefOVR" not in d:
            off, deff = split_ovr_into_units(base_ovr)
            d["OffOVR"], d["DefOVR"] = off, deff
        else:
            d["OffOVR"] = int(clamp(d["OffOVR"] * 0.70 + base_ovr * 0.30 + random.uniform(-1.0, 1.0), 40, 99))
            d["DefOVR"] = int(clamp(d["DefOVR"] * 0.70 + base_ovr * 0.30 + random.uniform(-1.0, 1.0), 40, 99))

        d["OVR"] = int(clamp((d["OffOVR"] + d["DefOVR"]) / 2, 40, 99))
        d["Stadium"] = int(clamp(d.get("Stadium", 6) + (1 if wins >= 10 and random.random() < 0.25 else 0), 1, 12))
        d["Marketing"] = int(clamp(d.get("Marketing", 6) + (1 if wins >= 10 and random.random() < 0.18 else 0), 1, 12))

    return ai_recruiting_spend_adjust(opponents_db, inflation)

# ==============================================================================
# OFFSEASON PIPELINE (NIL -> Outreach -> Top 8)
# ==============================================================================
def management_recruit_strength():
    hc = st.session_state.staff.get("HC", {})
    scout = st.session_state.staff.get("Scout", {})
    oc = st.session_state.staff.get("OC", {})
    dc = st.session_state.staff.get("DC", {})

    hc_r = hc.get("recruit", 5)
    scout_r = scout.get("recruit", 5)
    prestige = st.session_state.prestige
    marketing = st.session_state.facilities["Marketing"]
    stadium = st.session_state.facilities["Stadium"]

    staff_pull = 1.0 + (hc_r - 5) * 0.05 + (scout_r - 5) * 0.06
    brand_pull = 1.0 + (marketing - 5) * 0.015
    stadium_pull = 1.0 + (stadium - 5) * 0.010
    prestige_pull = 1.0 + (prestige - 70) * 0.004

    if hc.get("trait") == "Recruiter":
        staff_pull *= 1.08
    if scout.get("trait") == "Recruiter":
        staff_pull *= 1.05

    tact = 0.0
    if hc.get("trait") == "Tactician":
        tact += 0.02
    if oc.get("trait") in ["Air Raid", "Smashmouth", "Pro Style"]:
        tact += 0.01
    if dc.get("trait") == "Tactician":
        tact += 0.01

    overall = staff_pull * brand_pull * stadium_pull * prestige_pull * (1.0 + tact)
    overall = clamp(overall, 0.75, 1.40)
    return {"overall": overall, "hc_r": hc_r, "scout_r": scout_r, "marketing": marketing}

def generate_nil_prospects():
    picks = []
    for _ in range(3):
        picks.append({"name": generate_name(), "pos": random.choice(POSITIONS), "rating": random.randint(90, 99),
                      "ask": random.randint(2_500_000, 6_500_000), "trait": random.choice(TRAITS), "type": "Elite NIL"})
    for _ in range(4):
        picks.append({"name": generate_name(), "pos": random.choice(POSITIONS), "rating": random.randint(82, 89),
                      "ask": random.randint(900_000, 2_400_000), "trait": random.choice(TRAITS), "type": "Starter NIL"})
    for _ in range(3):
        picks.append({"name": generate_name(), "pos": random.choice(POSITIONS), "rating": random.randint(74, 81),
                      "ask": random.randint(150_000, 700_000), "trait": "None", "type": "Depth NIL"})
    random.shuffle(picks)
    return picks

def sign_nil_prospect(i: int):
    p = st.session_state.nil_board[i]
    if st.session_state.budget < p["ask"]:
        st.toast("Not enough budget.")
        return
    st.session_state.budget -= p["ask"]
    old = st.session_state.roster[p["pos"]]
    st.session_state.roster[p["pos"]] = max(old, p["rating"])
    add_news(f"NIL signing: {p['pos']} {p['name']} ({p['rating']}) for {helper_format_cash(p['ask'])}")
    st.session_state.nil_board.pop(i)

def run_outreach_investment(allocs: dict):
    strength = management_recruit_strength()
    scout_r = strength["scout_r"]
    mult = strength["overall"]

    total_spend = sum(allocs.values())
    if total_spend > st.session_state.budget:
        return None

    base_cost = int(700_000 * st.session_state.inflation)
    eff = clamp(1.0 + (scout_r - 5) * 0.06, 0.75, 1.40)

    results = {"roster_delta": {p: 0.0 for p in POSITIONS}, "gems": [], "booster": 0, "spent": total_spend}

    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    for pos, amt in allocs.items():
        if amt <= 0:
            continue

        impact = (amt / base_cost) * 1.6
        impact *= eff * mult

        if pos in hot:
            impact *= 1.10

        impact = impact ** 0.82
        impact += random.uniform(-0.7, 1.2)

        gem_chance = clamp(0.06 + (amt / (base_cost * 4)) * 0.06 + (scout_r - 5) * 0.02, 0.04, 0.22)
        if random.random() < gem_chance:
            gem_boost = random.uniform(3.5, 7.5) * (1.0 + (scout_r - 5) * 0.06)
            impact += gem_boost
            gem = generate_star_player(pos, 1)
            gem["name"] += " (GEM)"
            results["gems"].append(gem)
            b = int(random.randint(150_000, 650_000) * (1.0 + (strength["marketing"] - 5) * 0.04))
            results["booster"] += b

        results["roster_delta"][pos] += impact

    if total_spend >= 6_000_000 and random.random() < 0.35:
        results["booster"] += random.randint(250_000, 1_200_000)

    return results

def generate_top8_prospects():
    needs = compute_team_needs(st.session_state.roster, 3)
    regions = list(REGION_STRENGTH.keys())

    board = []
    stars_list = [5, 5, 4, 4, 4, 3, 3, 3]
    for stars in stars_list:
        pos = random.choice(POSITIONS)
        region = random.choice(regions)
        nil_ask = {5: random.randint(2_000_000, 4_500_000),
                   4: random.randint(800_000, 1_900_000),
                   3: random.randint(250_000, 900_000)}[stars]

        base_interest = random.randint(18, 40)
        if pos in needs:
            base_interest += 10
        if region == st.session_state.home_region:
            base_interest += 8

        board.append({
            "id": random.randint(10000, 99999),
            "name": generate_name(),
            "pos": pos,
            "stars": stars,
            "region": region,
            "my_interest": clamp(base_interest, 0, 100),
            "my_nil_offer": 0,
            "visited": False,
            "pitch": 0,
            "nil_ask": nil_ask,
            "visit_cost": {5: 400_000, 4: 280_000, 3: 180_000}[stars],
            "pitch_cost": 120_000,
            "schools": [
                {"name": random.choice(ALL_TEAMS), "interest": random.randint(35, 75)},
                {"name": random.choice(ALL_TEAMS), "interest": random.randint(35, 75)},
            ],
            "committed": None,
        })
    return board

def top8_ai_tick(r):
    for sc in r["schools"]:
        pres = st.session_state.opponents_db.get(sc["name"], {}).get("Prestige", 70)
        bump = (pres - 65) * 0.10 + random.randint(-2, 5)
        sc["interest"] = clamp(sc["interest"] + bump, 0, 100)

def top8_apply_action(r, action: str):
    strength = management_recruit_strength()
    scout_r = strength["scout_r"]
    hc_r = strength["hc_r"]
    mult = strength["overall"]

    needs = st.session_state.team_needs
    need_bonus = 1.18 if r["pos"] in needs else 1.0
    pipeline_bonus = 1.15 if r["region"] == st.session_state.home_region else 1.0

    if action == "VISIT":
        if r["visited"]:
            return 0, 0
        cost = r["visit_cost"]
        base = random.uniform(6, 11) if r["stars"] >= 4 else random.uniform(4, 8)
        base *= (1.0 + (hc_r - 5) * 0.05)
        delta = base * need_bonus * pipeline_bonus * mult
        r["visited"] = True
        return int(round(delta)), cost

    if action == "PITCH":
        cost = r["pitch_cost"]
        base = random.uniform(3.0, 6.0)
        base *= (1.0 + (hc_r - 5) * 0.05 + (scout_r - 5) * 0.03)
        delta = base * need_bonus * mult
        r["pitch"] += 1
        return int(round(delta)), cost

    return 0, 0

def top8_submit_nil(r, offer: int):
    delta_cost = offer - r["my_nil_offer"]
    if delta_cost > 0 and st.session_state.budget < delta_cost:
        return False, 0

    if delta_cost > 0:
        st.session_state.budget -= delta_cost
    r["my_nil_offer"] = offer

    ratio = offer / max(1, r["nil_ask"])
    bump = int(round(2 + 6 * (ratio ** 0.55)))
    bump = int(clamp(bump, 0, 10))
    r["my_interest"] = clamp(r["my_interest"] + bump, 0, 100)
    return True, bump

def resolve_top8_signing_day():
    strength = management_recruit_strength()
    hc_r = strength["hc_r"]
    scout_r = strength["scout_r"]
    mult = strength["overall"]

    signed, missed = [], []
    booster = 0
    roster_add = {p: 0.0 for p in POSITIONS}

    for r in st.session_state.top8_board:
        top8_ai_tick(r)

        ratio = clamp(r["my_nil_offer"] / max(1, r["nil_ask"]), 0.0, 2.0)
        nil_power = 9.5 * (ratio ** 0.75)

        staff_edge = (hc_r - 5) * 2.0 + (scout_r - 5) * 2.4
        staff_edge *= mult

        if r["pos"] in st.session_state.team_needs:
            staff_edge += 2.2
        if r["region"] == st.session_state.home_region:
            staff_edge += 1.6

        my_final = clamp(r["my_interest"] + nil_power + staff_edge, 0, 140)

        ai_vals = []
        for sc in r["schools"]:
            pres = st.session_state.opponents_db.get(sc["name"], {}).get("Prestige", 70)
            ai_vals.append(clamp(sc["interest"] + (pres - 70) * 0.35 + random.randint(-4, 6), 0, 140))

        candidates = [("YOU", my_final), (r["schools"][0]["name"], ai_vals[0]), (r["schools"][1]["name"], ai_vals[1])]
        weights = [max(1.0, c[1] ** 1.18) for c in candidates]
        pick = random.choices([c[0] for c in candidates], weights=weights, k=1)[0]
        r["committed"] = pick

        if pick == "YOU":
            signed.append(r)
            if r["stars"] == 5:
                pts = random.uniform(10, 15)
            elif r["stars"] == 4:
                pts = random.uniform(6, 10)
            else:
                pts = random.uniform(4, 7)

            if r["pos"] in st.session_state.team_needs:
                pts *= 1.15

            roster_add[r["pos"]] += pts

            if r["stars"] == 5:
                booster += random.randint(1_200_000, 3_500_000)
            elif r["stars"] == 4:
                booster += random.randint(300_000, 1_200_000)
            else:
                booster += random.randint(120_000, 450_000)
        else:
            missed.append(r)

    return signed, missed, roster_add, booster

def start_offseason():
    st.session_state.offseason_stage = "NIL"
    st.session_state.offseason_ready = True
    st.session_state.booster_bank = st.session_state.get("booster_bank", 0)

    st.session_state.nil_board = generate_nil_prospects()
    st.session_state.outreach_allocs = {p: 0 for p in POSITIONS}
    st.session_state.outreach_result = None
    st.session_state.team_needs = compute_team_needs(st.session_state.roster, 3)
    st.session_state.top8_board = generate_top8_prospects()
    add_news("Offseason begins: NIL Prospects board opens.")

# ==============================================================================
# POSTSEASON (Bowls + 12-team CFP)
# ==============================================================================
def estimate_ai_wins_for_ranking(team_data: dict) -> int:
    ovr = team_data.get("OVR", 70)
    pres = team_data.get("Prestige", 70)
    base = (ovr - 60) / 6.0 + (pres - 70) / 20.0
    wins = int(round(6 + base + random.uniform(-2.2, 2.2)))
    return int(clamp(wins, 0, 12))

def playoff_score(wins: int, avg_opp_ovr: float, prestige: int, conf: str, ovr: int) -> float:
    conf_bonus = 0
    if conf == "SEC":
        conf_bonus = 6
    elif conf == "Big Ten":
        conf_bonus = 5
    elif conf in ["ACC", "Big 12"]:
        conf_bonus = 3
    else:
        conf_bonus = 0
    return (wins * 100) + (avg_opp_ovr * 2.0) + (prestige * 1.2) + (ovr * 1.0) + conf_bonus

def build_rankings_for_postseason():
    # User
    wins = st.session_state.record["w"]
    opp_ovrs = []
    for opp in st.session_state.schedule:
        d = st.session_state.opponents_db.get(opp, {})
        opp_ovrs.append(d.get("OVR", 70))
    avg_opp = sum(opp_ovrs) / max(1, len(opp_ovrs))
    my_off, my_def, my_ovr = calc_my_units()
    my_score = playoff_score(wins, avg_opp, st.session_state.prestige, st.session_state.team_conf, my_ovr)

    entries = [{
        "team": st.session_state.team_name,
        "is_user": True,
        "wins": wins,
        "avg_opp": avg_opp,
        "prestige": st.session_state.prestige,
        "conf": st.session_state.team_conf,
        "ovr": my_ovr,
        "score": my_score
    }]

    # AI teams (estimate their season)
    ai_season = {}
    for team, d in st.session_state.opponents_db.items():
        conf = next((c for c, lst in CONFERENCES.items() if team in lst), "G5")
        wins_ai = estimate_ai_wins_for_ranking(d)
        avg_opp_ai = d.get("OVR", 70) - random.uniform(1, 6)
        s = playoff_score(wins_ai, avg_opp_ai, d.get("Prestige", 70), conf, d.get("OVR", 70))
        entries.append({
            "team": team,
            "is_user": False,
            "wins": wins_ai,
            "avg_opp": avg_opp_ai,
            "prestige": d.get("Prestige", 70),
            "conf": conf,
            "ovr": d.get("OVR", 70),
            "score": s
        })
        ai_season[team] = {"wins": wins_ai, "score": s, "conf": conf}

    entries.sort(key=lambda x: x["score"], reverse=True)
    for i, e in enumerate(entries):
        e["rank"] = i + 1

    st.session_state.ai_season_rankings = ai_season
    st.session_state.season_rankings = entries
    user_rank = next(e["rank"] for e in entries if e["is_user"])
    return user_rank, entries

def init_cfp_bracket(rankings: list):
    # Take top 12 teams
    top12 = rankings[:12]
    seeds = [{"seed": i+1, "team": top12[i]["team"]} for i in range(12)]

    # Round 1: 5v12, 6v11, 7v10, 8v9 (higher seed hosts)
    r1 = [
        {"seed1": 5, "team1": seeds[4]["team"], "seed2": 12, "team2": seeds[11]["team"], "winner": None, "score": None, "host": seeds[4]["team"]},
        {"seed1": 6, "team1": seeds[5]["team"], "seed2": 11, "team2": seeds[10]["team"], "winner": None, "score": None, "host": seeds[5]["team"]},
        {"seed1": 7, "team1": seeds[6]["team"], "seed2": 10, "team2": seeds[9]["team"], "winner": None, "score": None, "host": seeds[6]["team"]},
        {"seed1": 8, "team1": seeds[7]["team"], "seed2": 9,  "team2": seeds[8]["team"], "winner": None, "score": None, "host": seeds[7]["team"]},
    ]

    return {"Type": "CFP", "Round": 1, "Seeds": seeds, "Matches": r1, "UserAlive": True}

def pick_bowl_opponent(user_rank: int, rankings: list):
    # pick a team near user rank (±10), excluding user
    idx = user_rank - 1
    lo = max(0, idx - 10)
    hi = min(len(rankings) - 1, idx + 10)
    pool = [r["team"] for r in rankings[lo:hi+1] if r["team"] != st.session_state.team_name]
    if not pool:
        pool = [r["team"] for r in rankings if r["team"] != st.session_state.team_name]
    return random.choice(pool)

def start_postseason():
    user_rank, rankings = build_rankings_for_postseason()

    if user_rank <= 12:
        st.session_state.postseason_data = init_cfp_bracket(rankings)
        st.session_state.postseason_data["UserSeed"] = user_rank
        add_news(f"CFP berth! You are ranked #{user_rank}.")
    else:
        bowl = get_bowl_name(user_rank)
        opp = pick_bowl_opponent(user_rank, rankings)
        opp_data = st.session_state.opponents_db.get(opp, {})
        st.session_state.postseason_data = {
            "Type": "BOWL",
            "Rank": user_rank,
            "Bowl": bowl,
            "Opponent": opp,
            "OppData": opp_data
        }
        add_news(f"Bowl invite: {bowl} vs {opp} (Rank #{user_rank}).")

def ai_staff_from_team(team: str) -> dict:
    if team == st.session_state.team_name:
        return st.session_state.staff
    d = st.session_state.opponents_db.get(team, {})
    coaches = d.get("Coaches", {"OC": 5, "DC": 5, "Scout": 5})
    pres = d.get("Prestige", 70)
    hc_r = int(clamp(5 + (pres - 70) / 10.0, 3, 9))
    return {
        "HC": {"recruit": hc_r, "trait": "None"},
        "OC": {"off": coaches.get("OC", 5), "trait": "None"},
        "DC": {"def": coaches.get("DC", 5), "trait": "None"},
        "Scout": {"recruit": coaches.get("Scout", 5), "trait": "None"},
    }

def get_team_units(team: str):
    if team == st.session_state.team_name:
        my_off, my_def, my_ovr = calc_my_units()
        return my_off, my_def, my_ovr, st.session_state.facilities["Stadium"]
    d = st.session_state.opponents_db.get(team, {})
    off = int(d.get("OffOVR", d.get("OVR", 70)))
    deff = int(d.get("DefOVR", d.get("OVR", 70)))
    ovr = int(d.get("OVR", (off + deff)/2))
    std = int(d.get("Stadium", 6))
    return off, deff, ovr, std

def get_team_schemes(team: str):
    if team == st.session_state.team_name:
        return st.session_state.my_schemes
    d = st.session_state.opponents_db.get(team, {})
    return {"Off": d.get("OffScheme", "Pro Style"), "Def": d.get("DefScheme", "Man Coverage")}

def simulate_ai_vs_ai(teamA: str, teamB: str, host: str | None):
    a_off, a_def, _, a_std = get_team_units(teamA)
    b_off, b_def, _, b_std = get_team_units(teamB)

    a_staff = ai_staff_from_team(teamA)
    b_coaches = st.session_state.opponents_db.get(teamB, {}).get("Coaches", {"OC": 5, "DC": 5})

    a_schemes = get_team_schemes(teamA)
    b_schemes = get_team_schemes(teamB)

    if host is None:
        site = "NEUTRAL"
        my_std = a_std
        opp_std = b_std
        is_rival = False
    else:
        # host is the home team
        if host == teamA:
            site = "HOME"
            my_std = a_std
            opp_std = b_std
        else:
            site = "AWAY"
            my_std = a_std
            opp_std = b_std
        is_rival = False

    res = engine_play_game(
        a_off, a_def,
        b_off, b_def,
        a_staff, a_schemes, b_schemes,
        "Normal", b_coaches,
        site, is_rival,
        my_std, opp_std
    )
    winner = teamA if res["result"] == "W" else teamB
    return winner, res["score"]

def cfp_advance_round(data: dict):
    # Round 1 -> QF
    if data["Round"] == 1:
        # Need winners for the 4 games; if any missing, stop
        if any(m["winner"] is None for m in data["Matches"]):
            return
        # Map:
        # QF1: 1 vs winner(8/9) -> match index 3
        # QF2: 2 vs winner(7/10)-> match index 2
        # QF3: 3 vs winner(6/11)-> match index 1
        # QF4: 4 vs winner(5/12)-> match index 0
        s = {x["seed"]: x["team"] for x in data["Seeds"]}
        winners = [m["winner"] for m in data["Matches"]]
        qf = [
            {"seed1": 1, "team1": s[1], "seed2": None, "team2": winners[3], "winner": None, "score": None, "host": None},
            {"seed1": 2, "team1": s[2], "seed2": None, "team2": winners[2], "winner": None, "score": None, "host": None},
            {"seed1": 3, "team1": s[3], "seed2": None, "team2": winners[1], "winner": None, "score": None, "host": None},
            {"seed1": 4, "team1": s[4], "seed2": None, "team2": winners[0], "winner": None, "score": None, "host": None},
        ]
        data["Round"] = 2
        data["Matches"] = qf
        return

    # QF -> Semi
    if data["Round"] == 2:
        if any(m["winner"] is None for m in data["Matches"]):
            return
        w = [m["winner"] for m in data["Matches"]]
        semi = [
            {"seed1": None, "team1": w[0], "seed2": None, "team2": w[3], "winner": None, "score": None, "host": None},
            {"seed1": None, "team1": w[1], "seed2": None, "team2": w[2], "winner": None, "score": None, "host": None},
        ]
        data["Round"] = 3
        data["Matches"] = semi
        return

    # Semi -> Championship
    if data["Round"] == 3:
        if any(m["winner"] is None for m in data["Matches"]):
            return
        w = [m["winner"] for m in data["Matches"]]
        champ = [{"seed1": None, "team1": w[0], "seed2": None, "team2": w[1], "winner": None, "score": None, "host": None}]
        data["Round"] = 4
        data["Matches"] = champ
        return

# ==============================================================================
# STATE INIT
# ==============================================================================
def initialize_game_state():
    if "game_state" not in st.session_state:
        st.session_state.game_state = "SETUP"
        st.session_state.year = 2026
        st.session_state.tenure = 1

        st.session_state.budget = 0
        st.session_state.prestige = 60
        st.session_state.job_security = 80
        st.session_state.expected_wins = 6

        st.session_state.roster = {p: 75 for p in POSITIONS}
        st.session_state.staff = {}
        st.session_state.candidates = {}
        st.session_state.facilities = {"Marketing": 5, "Training": 5, "Stadium": 5}

        st.session_state.team_conf = "G5"
        st.session_state.team_rival = "Rival"
        st.session_state.team_name = "My Team"
        st.session_state.team_color = "#333333"
        st.session_state.home_region = "South"
        st.session_state.hotspots = generate_hotspots()

        st.session_state.opponents_db = {}
        st.session_state.my_schemes = {"Off": "Pro Style", "Def": "Man Coverage"}
        st.session_state.sim_style = "Management"

        st.session_state.schedule = []
        st.session_state.season_week = 0
        st.session_state.season_complete = False
        st.session_state.season_plan = "Normal"
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.history = []
        st.session_state.inflation = 1.0
        st.session_state.revenue_report = None
        st.session_state.revenue_paid_this_year = False
        st.session_state.news = []

        st.session_state.team_needs = compute_team_needs(st.session_state.roster, 3)

        st.session_state.offseason_stage = "NIL"
        st.session_state.offseason_ready = False
        st.session_state.nil_board = []
        st.session_state.outreach_allocs = {p: 0 for p in POSITIONS}
        st.session_state.outreach_result = None
        st.session_state.top8_board = []
        st.session_state.booster_bank = 0

        # Postseason & rankings
        st.session_state.postseason_data = None
        st.session_state.season_rankings = []
        st.session_state.ai_season_rankings = {}
        st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}

initialize_game_state()

# ==============================================================================
# STAFF MARKET / HELPERS
# ==============================================================================
def ensure_candidates_for_role(role: str):
    if role not in st.session_state.candidates:
        tier_roll = random.randint(1, 3)
        st.session_state.candidates[role] = [engine_generate_coach(role, tier_roll) for _ in range(3)]

def refresh_candidates(role: str):
    tier_roll = random.randint(1, 3)
    st.session_state.candidates[role] = [engine_generate_coach(role, tier_roll) for _ in range(3)]

def role_display_rating(cand: dict, role: str):
    if role in ["HC", "Scout"]:
        return cand.get("recruit", 5)
    if role == "OC":
        return cand.get("off", 5)
    if role == "DC":
        return cand.get("def", 5)
    return 5

# ==============================================================================
# UI: SETUP
# ==============================================================================
def run_setup():
    st.title("🏆 College Football V3.1")
    st.caption("Management-driven dynasty • Season Hub (week-by-week) • Postseason restored • Offseason pipeline")

    c1, c2, c3 = st.columns(3)
    ad_name = c1.text_input("AD Name", "Coach Prime")
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"], index=0)
    sim_style = c3.selectbox("Sim Style", ["Management", "Balanced", "Chaos"], index=0)

    sorted_teams = sorted(REAL_WORLD_INIT.keys()) + sorted([t for t in ALL_TEAMS if t not in REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)

    if team in REAL_WORLD_INIT:
        d = REAL_WORLD_INIT[team]
        tier = d["Tier"]
        budget = 25_000_000 if tier == 1 else (15_000_000 if tier == 2 else (7_000_000 if tier == 3 else 4_500_000))
        conf = next((c for c, teams in CONFERENCES.items() if team in teams), "G5")
        rival = d.get("Rival", "Rival")
        prestige = d.get("Prestige", 60)
        base_talent = d.get("Talent", 75)
    else:
        tier, budget, conf, rival, prestige, base_talent = 3, 7_000_000, "G5", "Rival", 60, 72
        conf = next((c for c, teams in CONFERENCES.items() if team in teams), conf)

    expect = 10 if tier == 1 else (8 if tier == 2 else (6 if tier == 3 else 4))
    st.info(f"**{team}** | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival} | Expect: {expect}+ wins")

    if st.button("Start Dynasty", type="primary"):
        st.session_state.ad_name = ad_name
        st.session_state.team_name = team
        st.session_state.team_color = TEAMS_DB.get(team, {}).get("color", "#333333")
        st.session_state.team_conf = conf
        st.session_state.team_rival = rival
        st.session_state.home_region = "South"
        st.session_state.sim_style = sim_style

        mult = 1.0
        if diff == "Hard":
            mult = 0.75
        elif diff == "Easy":
            mult = 1.25

        st.session_state.school_tier = tier
        st.session_state.budget = int(budget * mult)
        st.session_state.expected_wins = expect
        st.session_state.prestige = prestige

        st.session_state.roster = engine_generate_roster(tier, base_talent)

        st.session_state.staff = {}
        for r in ["HC", "OC", "DC", "Scout"]:
            st.session_state.staff[r] = engine_generate_coach(r, tier)

        st.session_state.candidates = {}

        val = 8 if tier == 1 else (6 if tier == 2 else 5)
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}

        st.session_state.opponents_db = {}
        for opp in ALL_TEAMS:
            if opp == team:
                continue
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                ovr = data["Talent"]
                off, deff = split_ovr_into_units(ovr)
                st.session_state.opponents_db[opp] = {
                    "Prestige": data["Prestige"],
                    "Tier": data["Tier"],
                    "OVR": ovr,
                    "OffOVR": off,
                    "DefOVR": deff,
                    "OffScheme": random.choice(SCHEMES["Offense"]),
                    "DefScheme": random.choice(SCHEMES["Defense"]),
                    "Coaches": {"OC": random.randint(5, 9), "DC": random.randint(5, 9), "Scout": random.randint(4, 9)},
                    "Stadium": random.randint(5, 10),
                    "Marketing": random.randint(5, 10),
                }
            else:
                pres = 78 if opp in CONFERENCES.get("SEC", []) else 65
                tier2 = 2 if opp in CONFERENCES.get("SEC", []) else 3
                ovr = 82 if tier2 == 2 else 70
                off, deff = split_ovr_into_units(ovr)
                st.session_state.opponents_db[opp] = {
                    "Prestige": pres,
                    "Tier": tier2,
                    "OVR": ovr,
                    "OffOVR": off,
                    "DefOVR": deff,
                    "OffScheme": "Pro Style",
                    "DefScheme": "Man Coverage",
                    "Coaches": {"OC": 5, "DC": 5, "Scout": 5},
                    "Stadium": 6,
                    "Marketing": 6,
                }

        st.session_state.hotspots = generate_hotspots()

        st.session_state.schedule = engine_generate_schedule(team, conf, rival)
        st.session_state.season_week = 0
        st.session_state.season_complete = False
        st.session_state.season_plan = "Normal"
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.history = []
        st.session_state.revenue_report = None
        st.session_state.revenue_paid_this_year = False

        st.session_state.postseason_data = None
        st.session_state.season_rankings = []
        st.session_state.ai_season_rankings = {}
        st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}

        st.session_state.news = []
        add_news(f"Career begins at {team}. Sim style: {sim_style}. Difficulty: {diff}.")
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

# ==============================================================================
# UI: DASHBOARD CORE
# ==============================================================================
def calc_my_units():
    r = st.session_state.roster
    my_off_raw = (r["QB"] * 0.35) + (r["OL"] * 0.30) + (((r["RB"] + r["WR"]) / 2) * 0.35)
    my_def_raw = (r["DL"] * 0.34) + (r["LB"] * 0.33) + (r["DB"] * 0.33)
    boost = training_unit_boost(st.session_state.facilities["Training"])
    my_off = my_off_raw + boost
    my_def = my_def_raw + boost
    team_ovr = (my_off * 0.52) + (my_def * 0.48)
    return int(clamp(my_off, 40, 99)), int(clamp(my_def, 40, 99)), int(clamp(team_ovr, 40, 99))

def staff_missing_roles():
    roles = ["HC", "OC", "DC", "Scout"]
    return [r for r in roles if r not in st.session_state.staff]

def show_staff_hq():
    st.subheader("Staff HQ")

    missing = staff_missing_roles()
    if missing:
        st.error("Vacancies: " + ", ".join(missing) + ". You cannot simulate games until all roles are filled.")
    else:
        st.success("All roles filled. You're cleared to play.")

    st.markdown("### Current Staff")
    roles = ["HC", "OC", "DC", "Scout"]
    cols = st.columns(4)
    for i, role in enumerate(roles):
        with cols[i]:
            c = st.session_state.staff.get(role)
            if not c:
                st.warning(f"{role} VACANT")
            else:
                rating = role_display_rating(c, role)
                badge_cls = "badge-green" if rating >= 8 else ("badge-yellow" if rating >= 5 else "badge-red")
                st.markdown(
                    f"<div class='box'><b>{role}</b><br>{c['name']}<br>"
                    f"<span class='badge {badge_cls}'>RATING {rating}</span>"
                    f"<span class='badge badge-gray'>TRAIT {c.get('trait','None')}</span><br>"
                    f"<div class='small'>Salary: {helper_format_cash(c.get('salary',0))}</div></div>",
                    unsafe_allow_html=True,
                )
                if st.button("Fire", key=f"fire_{role}"):
                    del st.session_state.staff[role]
                    add_news(f"Fired {role}. Market opens.")
                    st.rerun()

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("### Job Market")
    if not missing:
        st.caption("No open roles. Fire a coach to open the market.")
        return

    scout_cost = 25_000
    refresh_cost = 75_000

    for role in missing:
        st.markdown(f"#### {role} Candidates")
        ensure_candidates_for_role(role)

        top_bar = st.columns([1.4, 1.2, 1.0])
        with top_bar[0]:
            st.caption(f"Scout reveals true ratings and traits.")
        with top_bar[1]:
            if st.button(f"Refresh Market ({helper_format_cash(refresh_cost)})", key=f"refresh_{role}"):
                if st.session_state.budget >= refresh_cost:
                    st.session_state.budget -= refresh_cost
                    refresh_candidates(role)
                    add_news(f"Refreshed {role} candidate pool.")
                    st.rerun()
        with top_bar[2]:
            if st.button("Promote GA (Free)", key=f"ga_{role}"):
                st.session_state.staff[role] = generate_ga_coach(role)
                if role in st.session_state.candidates:
                    del st.session_state.candidates[role]
                add_news(f"Promoted GA to {role}.")
                st.rerun()

        cols = st.columns(3)
        for i, cand in enumerate(st.session_state.candidates[role]):
            with cols[i]:
                if cand.get("scouted"):
                    r_val = role_display_rating(cand, role)
                    trait_txt = cand.get("trait", "None")
                    show_rtg = str(r_val)
                else:
                    r_val = role_display_rating(cand, role)
                    trait_txt = "???"
                    show_rtg = get_letter_grade(r_val)

                salary = cand.get("salary", 0)
                st.markdown(
                    f"<div class='box'><b>{cand['name']}</b><br>"
                    f"<span class='badge badge-gray'>{cand.get('history','')}</span><br>"
                    f"<span class='badge'>OVR {show_rtg}</span>"
                    f"<span class='badge badge-gray'>TRAIT {trait_txt}</span><br>"
                    f"<div style='font-weight:800;margin-top:6px'>{helper_format_cash(salary)}</div></div>",
                    unsafe_allow_html=True,
                )

                b1, b2 = st.columns(2)
                if b1.button("Hire", key=f"hire_{role}_{i}"):
                    if st.session_state.budget >= salary:
                        st.session_state.budget -= salary
                        cand["scouted"] = True
                        st.session_state.staff[role] = cand
                        del st.session_state.candidates[role]
                        add_news(f"Hired {role}: {cand['name']}.")
                        st.rerun()
                    else:
                        st.toast("Not enough budget.")

                if (not cand.get("scouted")) and b2.button(f"Scout ({helper_format_cash(scout_cost)})", key=f"scout_{role}_{i}"):
                    if st.session_state.budget >= scout_cost:
                        st.session_state.budget -= scout_cost
                        cand["scouted"] = True
                        add_news(f"Scouted {role} candidate: {cand['name']}.")
                        st.rerun()
                    else:
                        st.toast("Not enough budget.")

def render_matchup_breakdown(factors: dict):
    st.markdown(
        f"""
<div class='grid2'>
  <div class='row'><span>Talent gap</span><b>{factors['talent_gap']}</b></div>
  <div class='row'><span>Coaching net</span><b>{factors['coaching_net']}</b></div>
  <div class='row'><span>Scheme bonus</span><b>{factors['scheme_bonus']}</b></div>
  <div class='row'><span>Home-field</span><b>{factors['home_bonus']}</b></div>
  <div class='row'><span>Luck</span><b>{factors['luck']}</b></div>
  <div class='row'><span>Variance (sd)</span><b>{factors['sd']}</b></div>
</div>
""",
        unsafe_allow_html=True,
    )

def next_game_preview():
    wk = st.session_state.season_week
    if wk >= 12 or not st.session_state.schedule:
        return

    opp = st.session_state.schedule[wk]
    opp_data = st.session_state.opponents_db.get(opp, {})
    my_off, my_def, my_ovr = calc_my_units()

    opp_off = opp_data.get("OffOVR", opp_data.get("OVR", 70))
    opp_def = opp_data.get("DefOVR", opp_data.get("OVR", 70))
    opp_ovr = opp_data.get("OVR", int((opp_off + opp_def) / 2))
    opp_coaches = opp_data.get("Coaches", {"OC": 5, "DC": 5})
    opp_schemes = {"Off": opp_data.get("OffScheme", "Pro Style"), "Def": opp_data.get("DefScheme", "Man Coverage")}

    site = "HOME" if (wk % 2 == 0) else "AWAY"
    is_rival = (opp == st.session_state.team_rival)

    proj, proj_f = project_margin_only(
        my_off, my_def, opp_off, opp_def,
        st.session_state.staff, st.session_state.my_schemes, opp_schemes,
        st.session_state.season_plan, opp_coaches,
        site, is_rival,
        st.session_state.facilities["Stadium"], opp_data.get("Stadium", 6)
    )

    st.markdown("### Next Game Preview")
    st.markdown(
        f"<div class='box'><b>Week {wk+1}: {site}</b> vs <b>{opp}</b> "
        f"<span class='badge badge-gray'>{'RIVAL' if is_rival else 'GAME'}</span><br>"
        f"<span class='badge'>You OVR {my_ovr} (Off {my_off} / Def {my_def})</span>"
        f"<span class='badge'>Opp OVR {int(opp_ovr)} (Off {int(opp_off)} / Def {int(opp_def)})</span><br>"
        f"<span class='badge badge-gray'>Projected margin (no luck): {proj:+.1f}</span><br>"
        f"<span class='small'>Schemes: You {st.session_state.my_schemes['Off']} vs {opp_schemes['Def']} • "
        f"Opp {opp_schemes['Off']} vs You {st.session_state.my_schemes['Def']}</span></div>",
        unsafe_allow_html=True,
    )
    with st.expander("Projected factor breakdown (no luck)"):
        render_matchup_breakdown({**proj_f, "luck": 0.0})

def pay_annual_revenue_if_needed():
    if st.session_state.revenue_paid_this_year:
        return
    rev = engine_calculate_revenue(st.session_state.school_tier, st.session_state.facilities["Marketing"], st.session_state.inflation)
    st.session_state.budget += rev
    st.session_state.revenue_report = "End-of-season distribution: +" + helper_format_cash(rev)
    st.session_state.revenue_paid_this_year = True
    add_news("Annual revenue posted: +" + helper_format_cash(rev))

def simulate_one_week():
    if st.session_state.season_complete:
        return

    missing = staff_missing_roles()
    if missing:
        st.toast("Fill vacancies before simulating.")
        return

    if not st.session_state.schedule:
        st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)

    wk = st.session_state.season_week
    if wk >= 12:
        st.session_state.season_complete = True
        return

    opp = st.session_state.schedule[wk]
    opp_data = st.session_state.opponents_db.get(opp, {})
    opp_off = opp_data.get("OffOVR", opp_data.get("OVR", 70))
    opp_def = opp_data.get("DefOVR", opp_data.get("OVR", 70))
    opp_coaches = opp_data.get("Coaches", {"OC": 5, "DC": 5})
    opp_schemes = {"Off": opp_data.get("OffScheme", "Pro Style"), "Def": opp_data.get("DefScheme", "Man Coverage")}
    opp_stadium = opp_data.get("Stadium", 6)

    my_off, my_def, my_ovr = calc_my_units()

    is_rival = (opp == st.session_state.team_rival)
    site = "HOME" if (wk % 2 == 0) else "AWAY"

    res = engine_play_game(
        my_off, my_def,
        opp_off, opp_def,
        st.session_state.staff,
        st.session_state.my_schemes,
        opp_schemes,
        st.session_state.season_plan,
        opp_coaches,
        site,
        is_rival,
        st.session_state.facilities["Stadium"],
        opp_stadium,
    )

    if res["result"] == "W":
        st.session_state.record["w"] += 1
        st.session_state.job_security = int(clamp(st.session_state.job_security + (5 if is_rival else 2), 0, 100))
    else:
        st.session_state.record["l"] += 1
        pen = 2 if st.session_state.tenure <= 2 else 5
        st.session_state.job_security = int(clamp(st.session_state.job_security - pen, 0, 100))

    log = {
        "Week": wk + 1,
        "Opponent": opp,
        "Site": site,
        "Rival": is_rival,
        "Result": res["result"],
        "Score": res["score"],
        "YourOff": my_off,
        "YourDef": my_def,
        "OppOff": int(opp_off),
        "OppDef": int(opp_def),
        "OppOVR": int(opp_data.get("OVR", (opp_off + opp_def) / 2)),
        "YourSchemes": {"Off": st.session_state.my_schemes["Off"], "Def": st.session_state.my_schemes["Def"]},
        "OppSchemes": {"Off": opp_schemes["Off"], "Def": opp_schemes["Def"]},
        "YourCoaches": {"OC": st.session_state.staff.get("OC", {}).get("off", 5), "DC": st.session_state.staff.get("DC", {}).get("def", 5)},
        "OppCoaches": {"OC": opp_coaches.get("OC", 5), "DC": opp_coaches.get("DC", 5)},
        "Margin": res["margin"],
        "Factors": res["factors"],
    }
    st.session_state.season_logs.append(log)
    add_news(f"Week {wk+1}: {res['result']} {res['score']} vs {opp} ({site})")

    st.session_state.season_week += 1
    if st.session_state.season_week >= 12:
        st.session_state.season_complete = True
        pay_annual_revenue_if_needed()

def simulate_to_week(target_week: int):
    target_idx = clamp(target_week, 1, 12)
    while st.session_state.season_week < target_idx and not st.session_state.season_complete:
        simulate_one_week()

def simulate_rest_of_season():
    while not st.session_state.season_complete:
        simulate_one_week()

def show_season_hub():
    st.subheader("Season Hub")

    if not st.session_state.schedule:
        st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)

    next_game_preview()

    c1, c2, c3 = st.columns(3)
    st.session_state.season_plan = c1.selectbox("Game Plan", ["Normal", "Conservative", "Aggressive"], index=["Normal","Conservative","Aggressive"].index(st.session_state.season_plan))
    st.session_state.my_schemes["Off"] = c2.selectbox("Offense", SCHEMES["Offense"], index=SCHEMES["Offense"].index(st.session_state.my_schemes["Off"]))
    st.session_state.my_schemes["Def"] = c3.selectbox("Defense", SCHEMES["Defense"], index=SCHEMES["Defense"].index(st.session_state.my_schemes["Def"]))

    missing = staff_missing_roles()
    if missing:
        st.warning("Cannot simulate until staff is filled: " + ", ".join(missing))

    if not st.session_state.season_complete:
        b1, b2, b3, b4 = st.columns(4)
        if b1.button("Sim Next Week", type="primary", disabled=bool(missing)):
            simulate_one_week()
            st.rerun()

        target = b2.slider("Sim Through Week", 1, 12, min(12, st.session_state.season_week + 1))
        if b2.button("Run", key="sim_through", disabled=bool(missing)):
            simulate_to_week(target)
            st.rerun()

        if b3.button("Sim Rest of Season", disabled=bool(missing)):
            simulate_rest_of_season()
            st.rerun()

        if b4.button("Sim Full Season (Fast)", disabled=bool(missing)):
            simulate_rest_of_season()
            st.rerun()
    else:
        st.success("Regular season complete.")
        if not st.session_state.revenue_paid_this_year:
            pay_annual_revenue_if_needed()

        if st.button("Proceed to Postseason", type="primary"):
            start_postseason()
            st.session_state.game_state = "POSTSEASON"
            st.rerun()

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    for i, opp in enumerate(st.session_state.schedule):
        week_num = i + 1
        opp_data = st.session_state.opponents_db.get(opp, {})
        opp_off = int(opp_data.get("OffOVR", opp_data.get("OVR", 70)))
        opp_def = int(opp_data.get("DefOVR", opp_data.get("OVR", 70)))
        opp_ovr = int(opp_data.get("OVR", (opp_off + opp_def) / 2))
        opp_off_s = opp_data.get("OffScheme", "Pro Style")
        opp_def_s = opp_data.get("DefScheme", "Man Coverage")
        opp_coaches = opp_data.get("Coaches", {"OC": 5, "DC": 5})

        is_rival = (opp == st.session_state.team_rival)
        site = "HOME" if (i % 2 == 0) else "AWAY"

        log = next((x for x in st.session_state.season_logs if x["Week"] == week_num), None)
        if log:
            css = "win" if log["Result"] == "W" else "loss"
            title = f"Week {week_num}: {log['Result']} {log['Score']} vs {opp} ({log['Site']})"
        else:
            css = "pending"
            title = f"Week {week_num}: {site} vs {opp}"

        extra = " rival" if is_rival else ""
        st.markdown(f"<div class='card {css}{extra}'><b>{title}</b><br>", unsafe_allow_html=True)

        my_off, my_def, my_ovr = calc_my_units()
        st.markdown(
            f"<span class='badge'>You OVR {my_ovr} (Off {my_off} / Def {my_def})</span>"
            f"<span class='badge'>Opp OVR {opp_ovr} (Off {opp_off} / Def {opp_def})</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<span class='badge badge-gray'>Schemes: You {st.session_state.my_schemes['Off']} vs {opp_def_s}</span>"
            f"<span class='badge badge-gray'>Opp {opp_off_s} vs You {st.session_state.my_schemes['Def']}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<span class='badge badge-gray'>Coaches: You {st.session_state.staff.get('OC',{}).get('off','?')}/{st.session_state.staff.get('DC',{}).get('def','?')} "
            f"vs Opp {opp_coaches.get('OC',5)}/{opp_coaches.get('DC',5)}</span>",
            unsafe_allow_html=True,
        )

        if log:
            with st.expander("Why we won/lost (factors)"):
                render_matchup_breakdown(log["Factors"])

        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# UI: POSTSEASON
# ==============================================================================
def bracket_round_name(rnd: int) -> str:
    return {1: "Opening Round", 2: "Quarterfinals", 3: "Semifinals", 4: "National Championship"}.get(rnd, "CFP")

def render_bracket(data: dict):
    st.markdown(f"<div class='bracket'><div class='brtxt'>CFP — {bracket_round_name(data['Round'])}</div>", unsafe_allow_html=True)
    for m in data["Matches"]:
        t1 = m["team1"]
        t2 = m["team2"]
        s1 = m.get("seed1")
        s2 = m.get("seed2")

        left = f"<span class='brseed'>#{s1}</span>{t1}" if s1 else t1
        right = f"<span class='brseed'>#{s2}</span>{t2}" if s2 else t2

        if t1 == st.session_state.team_name:
            left = f"<span class='hi'>★ {left}</span>"
        if t2 == st.session_state.team_name:
            right = f"<span class='hi'>★ {right}</span>"

        if m["winner"] is None:
            mid = "vs"
        else:
            mid = f"✅ {m['winner']}"
        score = m["score"] if m["score"] else ""

        st.markdown(f"<div class='brrow'><div>{left}</div><div>{mid} {score}</div><div style='text-align:right'>{right}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_matchup_card(teamA: str, teamB: str, host: str | None):
    a_off, a_def, a_ovr, a_std = get_team_units(teamA)
    b_off, b_def, b_ovr, b_std = get_team_units(teamB)

    a_staff = ai_staff_from_team(teamA)
    b_coaches = st.session_state.opponents_db.get(teamB, {}).get("Coaches", {"OC": 5, "DC": 5}) if teamB != st.session_state.team_name else {
        "OC": st.session_state.staff.get("OC", {}).get("off", 5),
        "DC": st.session_state.staff.get("DC", {}).get("def", 5),
    }
    a_schemes = get_team_schemes(teamA)
    b_schemes = get_team_schemes(teamB)

    if host is None:
        site = "NEUTRAL"
    else:
        site = "HOME" if host == teamA else "AWAY"

    proj, proj_f = project_margin_only(
        a_off, a_def, b_off, b_def,
        a_staff, a_schemes, b_schemes,
        "Normal", b_coaches,
        site, False,
        a_std, b_std
    )

    st.markdown(
        f"<div class='box'><b>{teamA}</b> vs <b>{teamB}</b> "
        f"<span class='badge badge-gray'>{site}</span><br>"
        f"<span class='badge'>Team A OVR {a_ovr} (Off {a_off} / Def {a_def})</span>"
        f"<span class='badge'>Team B OVR {b_ovr} (Off {b_off} / Def {b_def})</span><br>"
        f"<span class='badge badge-gray'>Projected margin (A): {proj:+.1f}</span><br>"
        f"<span class='small'>Schemes: A {a_schemes['Off']} vs {b_schemes['Def']} • B {b_schemes['Off']} vs A {a_schemes['Def']}</span></div>",
        unsafe_allow_html=True
    )
    with st.expander("Projected factors (no luck)"):
        render_matchup_breakdown({**proj_f, "luck": 0.0})

def postseason_payout(round_num: int, win: bool, title: bool = False):
    if not win:
        return 0, 0, 0
    if title:
        return 25_000_000, 4, 10
    payout = {1: 4_000_000, 2: 6_000_000, 3: 10_000_000}.get(round_num, 3_000_000)
    prestige = {1: 1, 2: 1, 3: 2}.get(round_num, 1)
    sec = {1: 3, 2: 3, 3: 5}.get(round_num, 3)
    return payout, prestige, sec

def show_postseason():
    st.title("🏟️ Postseason Hub")
    data = st.session_state.postseason_data

    if not data:
        st.error("No postseason data found. Return to dashboard.")
        if st.button("Back to Dashboard"):
            st.session_state.game_state = "DASHBOARD"
            st.rerun()
        return

    # Bowl path
    if data["Type"] == "BOWL":
        opp = data["Opponent"]
        bowl = data["Bowl"]
        st.markdown(f"<div class='box'><h2 style='margin:0'>{bowl}</h2><div class='small'>Rank #{data['Rank']} • Neutral Site</div></div>", unsafe_allow_html=True)
        render_matchup_card(st.session_state.team_name, opp, host=None)

        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            my_off, my_def, _, my_std = get_team_units(st.session_state.team_name)
            o_off, o_def, _, o_std = get_team_units(opp)

            opp_coaches = st.session_state.opponents_db.get(opp, {}).get("Coaches", {"OC": 5, "DC": 5})
            opp_schemes = get_team_schemes(opp)

            res = engine_play_game(
                my_off, my_def, o_off, o_def,
                st.session_state.staff, st.session_state.my_schemes, opp_schemes,
                "Normal", opp_coaches,
                "NEUTRAL", False,
                my_std, o_std
            )

            win = (res["result"] == "W")
            st.markdown(f"### Result: **{res['result']} {res['score']}** vs {opp}")
            with st.expander("Why (factors)"):
                render_matchup_breakdown(res["factors"])

            if win:
                bonus = 2_000_000
                st.session_state.budget += bonus
                st.session_state.prestige = int(clamp(st.session_state.prestige + 1, 20, 99))
                st.session_state.job_security = int(clamp(st.session_state.job_security + 4, 0, 100))
                st.session_state.career_stats["bowl_w"] += 1
                add_news(f"Bowl win! +{helper_format_cash(bonus)} and +Prestige.")
            else:
                st.session_state.career_stats["bowl_l"] += 1
                add_news("Bowl loss. Regroup for the offseason.")

            # Career totals
            st.session_state.career_stats["w"] += st.session_state.record["w"]
            st.session_state.career_stats["l"] += st.session_state.record["l"]

            hist = {"Year": st.session_state.year, "Record": f"{st.session_state.record['w']}-{st.session_state.record['l']}", "Rank": f"#{data['Rank']}", "Postseason": bowl}
            st.session_state.history.append(hist)

            if st.button("Proceed to Summary"):
                st.session_state.game_state = "SUMMARY"
                st.rerun()

        return

    # CFP path
    if data["Type"] == "CFP":
        st.subheader(f"CFP — {bracket_round_name(data['Round'])}")
        render_bracket(data)

        # Find user's match this round (if any)
        user_team = st.session_state.team_name
        user_match = None
        for m in data["Matches"]:
            if m["team1"] == user_team or m["team2"] == user_team:
                user_match = m
                break

        if not data.get("UserAlive", True):
            st.error("You have been eliminated.")
            if st.button("Proceed to Summary", type="primary"):
                st.session_state.career_stats["w"] += st.session_state.record["w"]
                st.session_state.career_stats["l"] += st.session_state.record["l"]
                hist = {"Year": st.session_state.year, "Record": f"{st.session_state.record['w']}-{st.session_state.record['l']}", "Rank": "CFP", "Postseason": "Playoff Loss"}
                st.session_state.history.append(hist)
                st.session_state.game_state = "SUMMARY"
                st.rerun()
            return

        if user_match is None:
            st.success("You have a BYE this round.")
            if st.button("Simulate Round"):
                # simulate all AI games
                for m in data["Matches"]:
                    w, sc = simulate_ai_vs_ai(m["team1"], m["team2"], m.get("host"))
                    m["winner"] = w
                    m["score"] = sc
                cfp_advance_round(data)
                st.session_state.postseason_data = data
                st.rerun()
            return

        # Show user matchup preview
        opp = user_match["team2"] if user_match["team1"] == user_team else user_match["team1"]
        host = user_match.get("host")  # host team for round 1, else None
        st.markdown("### Your Matchup")
        render_matchup_card(user_team, opp, host=(host if host else None))

        # Determine site from host
        if host is None:
            site = "NEUTRAL"
        else:
            site = "HOME" if host == user_team else "AWAY"

        if st.button("PLAY CFP GAME 🏈", type="primary"):
            # User game
            my_off, my_def, _, my_std = get_team_units(user_team)
            o_off, o_def, _, o_std = get_team_units(opp)

            opp_coaches = st.session_state.opponents_db.get(opp, {}).get("Coaches", {"OC": 5, "DC": 5})
            opp_schemes = get_team_schemes(opp)

            res = engine_play_game(
                my_off, my_def, o_off, o_def,
                st.session_state.staff, st.session_state.my_schemes, opp_schemes,
                "Normal", opp_coaches,
                site, False,
                my_std, o_std
            )

            win = (res["result"] == "W")
            user_match["winner"] = user_team if win else opp
            user_match["score"] = res["score"]

            st.markdown(f"### Result: **{res['result']} {res['score']}** vs {opp}")
            with st.expander("Why (factors)"):
                render_matchup_breakdown(res["factors"])

            # Sim AI games in this round (excluding user match)
            for m in data["Matches"]:
                if m is user_match:
                    continue
                if m["winner"] is None:
                    w, sc = simulate_ai_vs_ai(m["team1"], m["team2"], m.get("host"))
                    m["winner"] = w
                    m["score"] = sc

            # Payouts
            if win:
                title = (data["Round"] == 4)
                payout, pres, sec = postseason_payout(data["Round"], True, title=title)
                st.session_state.budget += payout
                st.session_state.prestige = int(clamp(st.session_state.prestige + pres, 20, 99))
                st.session_state.job_security = int(clamp(st.session_state.job_security + sec, 0, 100))
                add_news(f"CFP win (Round {data['Round']}): +{helper_format_cash(payout)} (+Prestige).")
            else:
                data["UserAlive"] = False
                add_news("Eliminated from CFP.")

            # Advance round if possible
            if data.get("UserAlive", True):
                if data["Round"] == 4:
                    # Title won
                    st.session_state.career_stats["titles"] += 1
                    st.balloons()
                    add_news("NATIONAL CHAMPIONS!")
                    st.session_state.career_stats["w"] += st.session_state.record["w"]
                    st.session_state.career_stats["l"] += st.session_state.record["l"]
                    st.session_state.history.append({"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Postseason": "National Title"})
                    if st.button("Proceed to Summary", type="primary"):
                        st.session_state.game_state = "SUMMARY"
                        st.rerun()
                    return
                else:
                    cfp_advance_round(data)
            else:
                st.session_state.career_stats["w"] += st.session_state.record["w"]
                st.session_state.career_stats["l"] += st.session_state.record["l"]
                st.session_state.history.append({"Year": st.session_state.year, "Record": f"{st.session_state.record['w']}-{st.session_state.record['l']}", "Rank": "CFP", "Postseason": "Playoff Loss"})
                if st.button("Proceed to Summary", type="primary"):
                    st.session_state.game_state = "SUMMARY"
                    st.rerun()
                return

            st.session_state.postseason_data = data
            st.rerun()

# ==============================================================================
# UI: SUMMARY -> OFFSEASON
# ==============================================================================
def show_year_summary():
    st.title(f"{st.session_state.year} Summary")

    st.markdown(
        f"<div class='kpi'><b>War Chest:</b> {helper_format_cash(st.session_state.budget)} • "
        f"<b>Prestige:</b> {st.session_state.prestige} • <b>Inflation:</b> {st.session_state.inflation:.2f}x</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Career Snapshot")
    cs = st.session_state.career_stats
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Career Wins", cs["w"])
    c2.metric("Career Losses", cs["l"])
    c3.metric("Bowl W-L", f"{cs['bowl_w']}-{cs['bowl_l']}")
    c4.metric("Titles", cs["titles"])

    st.markdown("### Year History")
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    else:
        st.caption("No history logged yet.")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    if st.button("Enter Offseason Pipeline (NIL → Outreach → Top 8)", type="primary"):
        start_offseason()
        st.session_state.game_state = "OFFSEASON"
        st.rerun()

def show_offseason():
    st.title("🏈 Offseason Pipeline")
    st.caption("Step 1: NIL Prospects → Step 2: HS Outreach → Step 3: Top 8 Battles")
    st.write("Budget: **" + helper_format_cash(st.session_state.budget) + "**")

    step_map = {"NIL": 1, "OUTREACH": 2, "TOP8": 3, "DONE": 4}
    st.progress(min(1.0, step_map.get(st.session_state.offseason_stage, 1) / 4))

    if st.session_state.offseason_stage == "NIL":
        st.subheader("1) NIL Prospects")
        if not st.session_state.nil_board:
            st.info("No NIL prospects remain.")
        else:
            for i, p in enumerate(list(st.session_state.nil_board)):
                c1, c2, c3 = st.columns([3, 1.2, 1.2])
                c1.write(f"**{p['pos']} {p['name']}** • {p['type']} • Rating **{p['rating']}** • {p['trait']}")
                c2.write("Ask: **" + helper_format_cash(p["ask"]) + "**")
                if c3.button("Sign NIL", key=f"nil_{i}"):
                    sign_nil_prospect(i)
                    st.rerun()

        if st.button("Next → HS Outreach", type="primary"):
            st.session_state.offseason_stage = "OUTREACH"
            add_news("Offseason: HS Outreach phase begins.")
            st.rerun()

    elif st.session_state.offseason_stage == "OUTREACH":
        st.subheader("2) Overall HS Outreach (Position Investment)")
        hot = st.session_state.hotspots.get(st.session_state.home_region, [])
        st.info("Pipeline hotspots (" + st.session_state.home_region + "): " + ", ".join(hot))

        allocs = {}
        total = 0
        for p in POSITIONS:
            allocs[p] = st.number_input(f"{p} outreach", 0, 10_000_000, 0, step=100_000, key=f"out_{p}")
            total += allocs[p]

        st.metric("Total Spend", helper_format_cash(total))
        st.metric("Remaining if submitted", helper_format_cash(st.session_state.budget - total))

        if st.button("Run Outreach", type="primary"):
            res = run_outreach_investment(allocs)
            if not res:
                st.error("Over budget.")
            else:
                st.session_state.budget -= res["spent"]
                if res["booster"] > 0:
                    st.session_state.budget += res["booster"]
                    st.session_state.booster_bank += res["booster"]
                    st.toast("Boosters pop from gem buzz: +" + helper_format_cash(res["booster"]))

                for pos in POSITIONS:
                    loss = random.randint(1, 4)
                    st.session_state.roster[pos] = clamp(st.session_state.roster[pos] - loss + res["roster_delta"][pos], 40, 99)

                st.session_state.team_needs = compute_team_needs(st.session_state.roster, 3)
                st.session_state.outreach_result = res
                add_news("Outreach complete. Gems: " + str(len(res["gems"])) + ". Booster bump: " + helper_format_cash(res["booster"]))
                st.success("Outreach complete.")

        if st.button("Next → Top 8 Battles", type="primary"):
            st.session_state.offseason_stage = "TOP8"
            add_news("Offseason: Top 8 Battles begin.")
            st.rerun()

    elif st.session_state.offseason_stage == "TOP8":
        st.subheader("3) Top 8 Prospect Battles")
        strength = management_recruit_strength()
        st.info(f"Recruit pull: **{strength['overall']:.2f}x** | HC Recruit: **{strength['hc_r']}** | Scout: **{strength['scout_r']}**")
        st.caption("Team needs: " + ", ".join(st.session_state.team_needs))

        cols = st.columns(2)
        for idx, r in enumerate(st.session_state.top8_board):
            with cols[idx % 2]:
                stars = "⭐" * r["stars"]
                st.markdown(f"### {r['pos']} {r['name']}  {stars}")
                st.caption("Region: " + r["region"] + " | Need: " + ("YES" if r["pos"] in st.session_state.team_needs else "no"))

                st.write("NIL Ask:", helper_format_cash(r["nil_ask"]))
                st.write("Your Offer:", helper_format_cash(r["my_nil_offer"]))

                st.progress(min(1.0, r["my_interest"] / 100.0))

                a1, a2, a3 = st.columns(3)
                if a1.button("Visit (" + helper_format_cash(r["visit_cost"]) + ")", key=f"visit_{r['id']}"):
                    delta, cost = top8_apply_action(r, "VISIT")
                    if cost > 0 and st.session_state.budget >= cost:
                        st.session_state.budget -= cost
                        r["my_interest"] = clamp(r["my_interest"] + delta, 0, 100)
                        add_news("Top8 visit: " + r["name"] + " +" + str(delta) + " interest.")
                    st.rerun()

                if a2.button("Pitch (" + helper_format_cash(r["pitch_cost"]) + ")", key=f"pitch_{r['id']}"):
                    delta, cost = top8_apply_action(r, "PITCH")
                    if st.session_state.budget >= cost:
                        st.session_state.budget -= cost
                        r["my_interest"] = clamp(r["my_interest"] + delta, 0, 100)
                        add_news("Top8 pitch: " + r["name"] + " +" + str(delta) + " interest.")
                    st.rerun()

                max_offer = min(6_000_000, st.session_state.budget + r["my_nil_offer"])
                offer = st.slider("NIL Offer", 0, int(max_offer), int(r["my_nil_offer"]), step=100_000, key=f"nil_slider_{r['id']}")
                if a3.button("Submit NIL", key=f"nil_btn_{r['id']}"):
                    ok, bump = top8_submit_nil(r, offer)
                    if ok:
                        add_news("Top8 NIL submitted: " + r["name"] + " (+" + str(bump) + " interest).")
                    st.rerun()

        st.divider()
        c1, c2 = st.columns(2)

        if c1.button("Advance Week (AI Push)"):
            for r in st.session_state.top8_board:
                top8_ai_tick(r)
                r["my_interest"] = clamp(r["my_interest"] + random.randint(-1, 2), 0, 100)
            add_news("Top8 advances a week. Rivals push hard.")
            st.rerun()

        if c2.button("Signing Day: Resolve Top 8", type="primary"):
            signed, missed, roster_add, booster = resolve_top8_signing_day()
            for pos, val in roster_add.items():
                st.session_state.roster[pos] = clamp(st.session_state.roster[pos] + val, 40, 99)

            if booster > 0:
                st.session_state.budget += booster
                st.session_state.booster_bank += booster
                st.toast("Boosters explode: +" + helper_format_cash(booster))

            add_news("Top8 Signing Day: signed " + str(len(signed)) + "/8. Booster payout: " + helper_format_cash(booster))
            st.session_state.offseason_stage = "DONE"
            st.rerun()

    elif st.session_state.offseason_stage == "DONE":
        st.success("Offseason complete — launching new season...")

        st.session_state.opponents_db = engine_evolve_universe(st.session_state.opponents_db, st.session_state.inflation)

        st.session_state.inflation *= 1.05
        st.session_state.year += 1
        st.session_state.tenure += 1
        st.session_state.hotspots = generate_hotspots()

        st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
        st.session_state.season_week = 0
        st.session_state.season_complete = False
        st.session_state.season_plan = "Normal"
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.revenue_report = None
        st.session_state.revenue_paid_this_year = False

        st.session_state.nil_board = []
        st.session_state.outreach_result = None
        st.session_state.top8_board = []
        st.session_state.offseason_ready = False
        st.session_state.offseason_stage = "NIL"

        st.session_state.postseason_data = None

        time.sleep(0.2)
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

def show_fired():
    st.error("FIRED! Your tenure has ended.")
    if st.button("Restart Career", type="primary"):
        st.session_state.clear()
        st.rerun()

def show_dashboard():
    thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < thresh:
        st.session_state.game_state = "FIRED"
        st.rerun()

    if st.session_state.revenue_report:
        st.success(st.session_state.revenue_report)

    my_off, my_def, my_ovr = calc_my_units()
    needs = compute_team_needs(st.session_state.roster, 3)
    st.session_state.team_needs = needs

    coach_power = (
        st.session_state.staff.get("OC", {}).get("off", 5)
        + st.session_state.staff.get("DC", {}).get("def", 5)
        + st.session_state.staff.get("HC", {}).get("recruit", 5)
        + st.session_state.staff.get("Scout", {}).get("recruit", 5)
    )

    st.markdown(
        f"<div class='kpi'><b>Year:</b> {st.session_state.year} • <b>Tenure:</b> {st.session_state.tenure} • "
        f"<b>Prestige:</b> {st.session_state.prestige} • <b>Security:</b> {st.session_state.job_security}%</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='kpi' style='background:{st.session_state.team_color}; color:white;'><h2 style='margin:0'>{st.session_state.team_name}</h2></div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("Team OVR", my_ovr, f"Off {my_off} / Def {my_def}")
    c3.metric("Coach Power", coach_power, "Consistency + Recruiting Edge")
    c4.metric("Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Program", "Staff", "Facilities", "Season", "News"])

    with tab1:
        st.subheader("Roster & Needs")
        st.caption("Team needs: " + ", ".join(needs))
        for p, v in st.session_state.roster.items():
            st.progress(v / 100.0, text=f"{p}: {int(v)}")

    with tab2:
        show_staff_hq()

    with tab3:
        st.subheader("Facilities")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Marketing", st.session_state.facilities["Marketing"], delta="More $ + recruiting pull")
            if st.button("Upgrade Marketing ($1M)", key="up_mkt"):
                if st.session_state.budget >= 1_000_000:
                    st.session_state.budget -= 1_000_000
                    st.session_state.facilities["Marketing"] += 1
                    add_news("Upgraded Marketing.")
                    st.rerun()
        with c2:
            st.metric("Training", st.session_state.facilities["Training"], delta="On-field unit boost")
            if st.button("Upgrade Training ($3M)", key="up_trn"):
                if st.session_state.budget >= 3_000_000:
                    st.session_state.budget -= 3_000_000
                    st.session_state.facilities["Training"] += 1
                    add_news("Upgraded Training.")
                    st.rerun()
        with c3:
            st.metric("Stadium", st.session_state.facilities["Stadium"], delta="Home-field advantage")
            if st.button("Upgrade Stadium ($10M)", key="up_std"):
                if st.session_state.budget >= 10_000_000:
                    st.session_state.budget -= 10_000_000
                    st.session_state.facilities["Stadium"] += 1
                    st.session_state.prestige = int(clamp(st.session_state.prestige + 1, 20, 99))
                    add_news("Upgraded Stadium (+Prestige).")
                    st.rerun()

    with tab4:
        show_season_hub()

    with tab5:
        st.subheader("Program Feed")
        if not st.session_state.news:
            st.caption("No news yet.")
        else:
            for item in st.session_state.news:
                st.write(item)

# ==============================================================================
# ROUTER
# ==============================================================================
if st.session_state.game_state == "SETUP":
    run_setup()
elif st.session_state.game_state == "DASHBOARD":
    show_dashboard()
elif st.session_state.game_state == "POSTSEASON":
    show_postseason()
elif st.session_state.game_state == "SUMMARY":
    show_year_summary()
elif st.session_state.game_state == "OFFSEASON":
    show_offseason()
elif st.session_state.game_state == "FIRED":
    show_fired()
