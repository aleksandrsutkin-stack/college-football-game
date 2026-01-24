import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# College Football V1 (Streamlit)
# Offseason Pipeline: NIL -> Outreach -> Top 8 Battles
# AI recruiting spend (Proposal G) included
# ==============================================================================

try:
    st.set_page_config(page_title="College Football V1", page_icon="🏈", layout="wide")
except Exception:
    pass

st.markdown(
    """
<style>
.stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: 800; }
.small { font-size: 0.9em; color: #666; }
.kpi { background: #f8f9fa; border: 1px solid #e6e6e6; padding: 12px; border-radius: 10px; }
.box { background: white; border: 1px solid #eee; padding: 12px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
.badge { padding: 2px 8px; border-radius: 8px; border: 1px solid #ddd; font-weight: 800; font-size: 0.8em; display: inline-block; }
.badge-green { background: #eaf7ea; border-color: #cfe9cf; color: #1f6c1f; }
.badge-yellow { background: #fff6db; border-color: #ffe6a6; color: #7a5b00; }
.badge-red { background: #fdecec; border-color: #f7caca; color: #8a1a1a; }
.card { border: 1px solid #eee; border-left: 6px solid #ddd; border-radius: 12px; padding: 12px; margin-bottom: 10px; background: white; }
.win { border-left-color: #2e7d32; }
.loss { border-left-color: #c62828; }
.pending { border-left-color: #6c757d; background: #f8f9fa; }
.rival { border: 2px solid #ffc107; background: #fffaf0; }
.hr { border-top: 1px solid #eee; margin: 10px 0; }
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
    st.session_state.news = st.session_state.news[:30]

def generate_hotspots():
    hotspots = {}
    for reg in REGION_STRENGTH.keys():
        hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

def get_bowl_name(rank: int) -> str:
    if rank <= 12:
        return "CFP Playoff"
    if rank <= 25:
        return random.choice(BOWL_MAPPING["Elite"])
    if rank <= 40:
        return random.choice(BOWL_MAPPING["High"])
    if rank <= 80:
        return random.choice(BOWL_MAPPING["Mid"])
    return random.choice(BOWL_MAPPING["Low"])

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

# ==============================================================================
# PROGRAM / FACILITY EFFECTS
# ==============================================================================
def training_unit_boost(training_lvl: int) -> float:
    return 0.8 + training_lvl * 0.55

def stadium_home_field(stadium_lvl: int) -> float:
    return clamp(0.6 * stadium_lvl - 1.0, 0.0, 8.0)

def stadium_night_game_aura(stadium_lvl: int, is_home: bool) -> float:
    if not is_home:
        return 0.0
    if stadium_lvl >= 8 and random.random() < 0.22:
        return random.uniform(0.8, 2.2)
    return 0.0

# ==============================================================================
# ENGINE: ECONOMY / GENERATION
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
# GAME SIM (management-driven)
# ==============================================================================
def engine_play_game(
    my_off, my_def,
    opp_off, opp_def,
    staff, schemes, opp_schemes,
    game_plan,
    opp_coaches,
    is_home, is_rival,
    my_stadium_lvl, opp_stadium_lvl,
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

    home_bonus = stadium_home_field(my_stadium_lvl) if is_home else -stadium_home_field(opp_stadium_lvl)
    home_bonus += stadium_night_game_aura(my_stadium_lvl, is_home)

    var_mult = 1.0
    if is_rival:
        var_mult *= 1.20
    if game_plan == "Aggressive":
        var_mult *= 1.12
    if game_plan == "Conservative":
        var_mult *= 0.85

    coach_consistency = clamp((my_hc - 5) * 0.06 + (my_oc - 5) * 0.04 + (my_dc - 5) * 0.04, -0.20, 0.25)
    sd = base_sd * var_mult * (1.0 - coach_consistency)

    luck = random.gauss(0, sd)
    margin = talent_gap + scheme_bonus + coaching_net + home_bonus + luck

    total_points = int(clamp(random.gauss(56, 12), 24, 92))
    spread = clamp(margin, -42, 42)

    my_score = int(round((total_points / 2) + (spread / 2)))
    opp_score = int(total_points - my_score)
    my_score = int(clamp(my_score, 0, 70))
    opp_score = int(clamp(opp_score, 0, 70))

    return {
        "result": "W" if margin > 0 else "L",
        "score": f"{my_score}-{opp_score}",
        "stats": {
            "off_vs_def": [int(my_off), int(opp_def)],
            "def_vs_off": [int(my_def), int(opp_off)],
            "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"],
            "margin": round(margin, 1),
            "sd": round(sd, 1),
        },
    }

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
    add_news("NIL signing: " + p["pos"] + " " + p["name"] + " (" + str(p["rating"]) + ") for " + helper_format_cash(p_
