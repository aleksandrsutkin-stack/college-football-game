# College Football V1 (Upgraded: Recruit Battles + Facilities Perks + Rankings/Selection Show)
import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# ZONE 1: CONFIGURATION & STATIC DATA
# ==============================================================================
try:
    st.set_page_config(page_title="College Football V1", page_icon="🏈", layout="wide")
except:
    pass

st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }

.security-box { background: #f8f9fa; padding: 12px; border-radius: 10px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
.security-safe { color: #28a745; font-weight: bold; }
.security-warm { color: #fd7e14; font-weight: bold; }
.security-hot { color: #dc3545; font-weight: bold; }

.finance-alert { background-color: #d1e7dd; color: #0f5132; border: 1px solid #badbcc; padding: 12px; border-radius: 10px; margin-bottom: 14px; text-align: center; font-weight: bold; }
.nil-alert { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; padding: 14px; border-radius: 10px; margin-bottom: 14px; text-align: center; font-size: 1.05em; font-weight: bold; }

.game-card { padding: 10px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #ddd; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.game-card-win { border-left: 5px solid #28a745; }
.game-card-loss { border-left: 5px solid #dc3545; }
.game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
.game-card-rival { border: 2px solid #ffc107 !important; background-color: #fffbf0 !important; }

.card-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 6px;}
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.9em; }
.stat-row { display: flex; justify-content: space-between; }

.staff-card { background: white; border: 1px solid #e0e0e0; border-radius: 12px; padding: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.staff-role { font-size: 0.78em; color: #666; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
.staff-name { font-size: 1.05em; font-weight: 900; color: #333; }
.badge { padding: 2px 7px; border-radius: 6px; font-size: 0.78em; font-weight: bold; margin-right: 6px; display: inline-block;}
.badge-tier-s { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-tier-a { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-tier-f { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-trait { background: #e2e3e5; color: #383d41; }

.recruit-card { background: white; border: 1px solid #eee; border-radius: 14px; padding: 12px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.recruit-top { display:flex; justify-content:space-between; font-weight:900; }
.mini { font-size: 0.88em; color:#555; }
.chip { display:inline-block; padding:2px 8px; border-radius:999px; background:#f3f4f6; margin-right:6px; font-size:0.78em; font-weight:700; }
.chip-hot { background:#fff3cd; border: 1px solid #ffeeba; }
.chip-need { background:#dbeafe; border: 1px solid #bfdbfe; }

.fac-card { background: white; border: 1px solid #eee; border-radius: 14px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.fac-title { font-weight: 900; font-size: 1.02em; }
.perk { font-size:0.9em; color:#444; margin-top:6px; padding-top:6px; border-top: 1px solid #f1f1f1; }
.perk b { color:#111; }
.news-box { background: #fff; border: 1px solid #eee; border-radius: 14px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.news-item { padding: 6px 0; border-bottom: 1px solid #f1f1f1; }
.news-item:last-child { border-bottom: none; }

.bracket-box { background-color: #111827; color: white; padding: 14px; border-radius: 14px; margin-bottom: 12px; }
.bracket-row { display:flex; justify-content:space-between; padding:6px; border-bottom:1px solid rgba(255,255,255,0.12); }
.bracket-row:last-child{ border-bottom:none; }
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
COACH_TRAITS = {"None": "None", "Recruiter": "+10% Recruiting", "Tactician": "+3 Game Boost",
                "Air Raid": "+2 Scheme", "Smashmouth": "+2 Scheme", "Pro Style": "+2 Scheme"}

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


# ==============================================================================
# ZONE 2: HELPERS
# ==============================================================================
def helper_format_cash(amount: int) -> str:
    return f"${amount/1000000:.1f}M" if amount >= 1000000 else f"${int(amount/1000)}K"

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def generate_name():
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Tank", "Arch", "Shedeur", "Quinn", "Travis", "Ashton", "Dylan", "Malik"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck", "Jeanty", "Judkins", "Carter", "Woods"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name():
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan", "Kalen"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman", "Lanning", "DeBoer"]
    return f"{random.choice(first)} {random.choice(last)}"

def get_letter_grade(val):
    if val >= 9: return "A+"
    if val >= 8: return "A"
    if val >= 7: return "B"
    if val >= 5: return "C"
    if val >= 3: return "D"
    return "F"

def calculate_saban_score(career_stats, prestige):
    return int((career_stats['w'] * 1) + (career_stats['bowl_w'] * 5) + (career_stats['titles'] * 50) + (prestige * 0.5))

def get_bowl_name(rank):
    if rank <= 12: return "CFP Playoff"
    if rank <= 25: return random.choice(BOWL_MAPPING["Elite"])
    if rank <= 40: return random.choice(BOWL_MAPPING["High"])
    if rank <= 80: return random.choice(BOWL_MAPPING["Mid"])
    return random.choice(BOWL_MAPPING["Low"])

def get_conference(team: str) -> str:
    for conf, teams in CONFERENCES.items():
        if team in teams:
            return conf
    return "G5"

def role_rating(cand: dict, role: str) -> int:
    if role in ["HC", "OC"]:
        return cand.get("off", 1)
    if role == "DC":
        return cand.get("def", 1)
    if role == "Scout":
        return cand.get("recruit", 1)
    return cand.get("off", 1)

def compute_team_needs(roster: dict, k: int = 3) -> list:
    sorted_pos = sorted(roster.items(), key=lambda x: x[1])
    return [p for p, _ in sorted_pos[:k]]

def add_news(text: str):
    if "news" not in st.session_state:
        st.session_state.news = []
    st.session_state.news.insert(0, f"{st.session_state.year}: {text}")
    st.session_state.news = st.session_state.news[:14]

def team_units_from_roster(roster: dict):
    off = (roster["QB"] * 0.35) + (roster["OL"] * 0.30) + (((roster["RB"] + roster["WR"]) / 2) * 0.35)
    defense = (roster["DL"] * 0.34) + (roster["LB"] * 0.33) + (roster["DB"] * 0.33)
    return off, defense

def facilities_perks():
    # milestone perks at 6/9/12 (UI + small logic hooks)
    return {
        "Marketing": {
            6: "Sponsor surge: +5% revenue",
            9: "National brand: +8% recruiting interest",
            12: "Mega donors: occasional +$2M NIL event"
        },
        "Training": {
            6: "Dev boost: +8% offseason conversion",
            9: "Sports science: slightly higher unit boost",
            12: "Elite pipeline: reduce offseason attrition"
        },
        "Stadium": {
            6: "Crowd noise: stronger home-field",
            9: "Night game aura: big home upset chance",
            12: "Dynasty cathedral: +1 prestige per year"
        }
    }

def fac_bonus_revenue(marketing_lvl: int):
    # milestone effect
    if marketing_lvl >= 6:
        return 1.05
    return 1.0

def fac_bonus_recruit_interest(marketing_lvl: int):
    if marketing_lvl >= 9:
        return 1.08
    return 1.0

def fac_bonus_donor_event(marketing_lvl: int):
    return marketing_lvl >= 12

def training_offseason_conversion(training_lvl: int):
    # base + milestone
    base = 0.58 + training_lvl * 0.015
    if training_lvl >= 6:
        base *= 1.08
    if training_lvl >= 9:
        base += 0.02
    return clamp(base, 0.58, 0.80)

def training_unit_boost(training_lvl: int):
    boost = training_lvl * 0.35
    if training_lvl >= 9:
        boost += 0.6
    return boost

def stadium_home_field(stadium_lvl: int):
    base = max(0.0, (stadium_lvl - 1) / 3.0)  # ~0..3.6
    if stadium_lvl >= 6:
        base += 0.4
    return base

def stadium_night_game_aura(stadium_lvl: int, is_home: bool):
    # small extra variance/edge at home if >=9
    if is_home and stadium_lvl >= 9 and random.random() < 0.18:
        return 2.0
    return 0.0

def stadium_prestige_tick(stadium_lvl: int):
    return 1 if stadium_lvl >= 12 else 0


# ==============================================================================
# ZONE 3: ENGINE
# ==============================================================================
def engine_calculate_revenue(tier, marketing_lvl, inflation):
    if not tier: tier = 3
    base = {1: 40000000, 2: 25000000, 3: 10000000, 4: 5000000}.get(tier, 5000000)
    marketing_bonus = marketing_lvl * 2000000
    total = (base + marketing_bonus) * inflation * fac_bonus_revenue(marketing_lvl)
    return int(total)

def engine_generate_coach(role, tier):
    cost = random.randint(4000000, 8000000) if tier == 1 else random.randint(500000, 3500000)
    trait_pool = list(COACH_TRAITS.keys())
    if role == "OC":
        trait_pool = ["Air Raid", "Smashmouth", "Pro Style", "Recruiter", "Tactician"]
    base = 8 if tier == 1 else (5 if tier == 2 else 1)
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
    base = base_ovr if base_ovr else (90 if tier == 1 else 74)
    roster = {}
    for p in POSITIONS:
        roster[p] = min(99, max(40, base + random.randint(-4, 4)))
    return roster

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
    else:
        random.shuffle(schedule)

    while len(schedule) > 12:
        schedule.pop(0)
    return schedule

# IMPORTANT CHANGE for "too many close games":
# - previous version averaged 120 sims, which makes luck cancel out and margins shrink.
# - here: compute expected margin + ONE luck draw (more realistic spread distribution).
def engine_play_game(
    my_off, my_def,
    opp_off, opp_def,
    staff, schemes, opp_schemes,
    game_plan,
    opp_coaches,
    is_home, is_rival,
    my_stadium_lvl, opp_stadium_lvl
):
    # 1) matchup talent (linear)
    talent_gap = ((my_off - opp_def) * 0.70) + ((my_def - opp_off) * 0.60)

    # 2) scheme
    scheme_bonus = 0.0
    if COUNTERS.get(opp_schemes.get('Def', "Man Coverage"), "Pro Style") == schemes.get('Off', "Pro Style"):
        scheme_bonus += 3.0
    elif COUNTERS.get(schemes.get('Off', "Pro Style"), "Man Coverage") == opp_schemes.get('Def', "Man Coverage"):
        scheme_bonus -= 3.0

    # 3) coaching
    my_oc = staff.get('OC', {'off': 3}).get('off', 3)
    my_dc = staff.get('DC', {'def': 3}).get('def', 3)
    opp_oc = opp_coaches.get('OC', 5)
    opp_dc = opp_coaches.get('DC', 5)

    def tier_bonus(r):
        if r >= 8: return 3.0
        if r <= 4: return -3.0
        return 0.0

    coaching_net = (tier_bonus(my_oc) - tier_bonus(opp_dc)) + (tier_bonus(my_dc) - tier_bonus(opp_oc))

    # traits (small)
    hc_trait = staff.get("HC", {}).get("trait", "None")
    if hc_trait == "Tactician":
        coaching_net += 1.0

    oc_trait = staff.get("OC", {}).get("trait", "None")
    if oc_trait in ["Air Raid", "Smashmouth", "Pro Style"] and oc_trait == schemes.get("Off"):
        scheme_bonus += 1.0

    # 4) home/away (true stadium)
    home_bonus = stadium_home_field(my_stadium_lvl) if is_home else -stadium_home_field(opp_stadium_lvl)
    home_bonus += stadium_night_game_aura(my_stadium_lvl, is_home)

    # 5) variance
    var_mult = 1.0
    if is_rival: var_mult *= 1.35
    if game_plan == "Aggressive": var_mult *= 1.20
    if game_plan == "Conservative": var_mult *= 0.85

    # One-shot luck (NOT averaged)
    base_sd = 9.0
    luck = random.gauss(0, base_sd * var_mult)

    margin = talent_gap + scheme_bonus + coaching_net + home_bonus + luck

    # Score model
    total_points = int(clamp(random.gauss(58, 14), 24, 95))
    spread = clamp(margin, -35, 35)
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
            "raw_roster": int((my_off + my_def) / 2),
            "margin": round(margin, 1)
        }
    }

def engine_evolve_universe(opponents_db):
    for team, data in opponents_db.items():
        wins = int((data['OVR'] / 100) * 12) + random.randint(-2, 2)
        wins = max(0, min(12, wins))

        change = 0
        if wins >= 10: change = 3
        elif wins <= 4: change = -3
        data['Prestige'] = max(20, min(99, data['Prestige'] + change))

        if data['Prestige'] > 80 and wins < 6:
            data['Coaches'] = {"OC": random.randint(7, 9), "DC": random.randint(7, 9)}
        elif data['Prestige'] < 70 and wins > 9:
            data['Coaches'] = {"OC": random.randint(3, 6), "DC": random.randint(3, 6)}

        base_ovr = int(data['Prestige'] * 0.9)
        data['OVR'] = base_ovr + random.randint(-3, 3)

        skew = random.randint(-3, 3)
        data["OffOVR"] = int(clamp(data["OVR"] + skew, 55, 99))
        data["DefOVR"] = int(clamp(data["OVR"] - skew, 55, 99))
        data["Stadium"] = int(clamp(data.get("Stadium", 6) + (1 if change > 0 and random.random() < 0.25 else 0), 1, 12))
    return opponents_db

def engine_generate_portal_players():
    players = []
    for _ in range(3):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(90, 99),
                        "cost": random.randint(3000000, 6000000), "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(3):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(80, 89),
                        "cost": random.randint(1000000, 2500000), "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(4):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(70, 78),
                        "cost": random.randint(150000, 500000), "trait": "None", "year": "Jr"})
    return players

def apply_development_pipeline(roster: dict, dev_bank: dict, training_lvl: int):
    out = dict(roster)
    if not dev_bank:
        return out

    conv = training_offseason_conversion(training_lvl)
    for pos, val in dev_bank.items():
        gain = val * conv
        out[pos] = clamp(out[pos] + gain, 40, 99)
    return out


# ==============================================================================
# RECRUIT BATTLES (Option #1)
# ==============================================================================
def recruit_gen(stars: int, pos: str, region: str, needs: list, marketing_lvl: int):
    name = generate_name()
    base_interest = random.randint(20, 45)
    if pos in needs:
        base_interest += 8
    if region == st.session_state.home_region:
        base_interest += 8
    base_interest = int(base_interest * fac_bonus_recruit_interest(marketing_lvl))

    nil_ask = {5: random.randint(1500000, 3500000),
               4: random.randint(700000, 1600000),
               3: random.randint(150000, 600000)}[stars]

    visit_cost = {5: 350000, 4: 250000, 3: 150000}[stars]
    pitch_cost = 100000  # "coach time" cost in budget abstraction
    return {
        "id": random.randint(10000, 99999),
        "name": name,
        "pos": pos,
        "stars": stars,
        "region": region,
        "my_interest": clamp(base_interest, 0, 100),
        "my_nil_offer": 0,
        "visited": False,
        "my_pitch": 0,
        "nil_ask": nil_ask,
        "visit_cost": visit_cost,
        "pitch_cost": pitch_cost,
        # 2 AI schools bidding
        "schools": [
            {"name": random.choice(ALL_TEAMS), "interest": random.randint(30, 70), "prest": 70},
            {"name": random.choice(ALL_TEAMS), "interest": random.randint(30, 70), "prest": 70}
        ],
        "committed": None
    }

def start_recruit_battles():
    needs = st.session_state.team_needs
    marketing_lvl = st.session_state.facilities["Marketing"]
    recruits = []
    regions = list(REGION_STRENGTH.keys())
    # 8 recruits: 2 five-stars, 3 four-stars, 3 three-stars
    star_plan = [5, 5, 4, 4, 4, 3, 3, 3]
    for s in star_plan:
        pos = random.choice(POSITIONS)
        region = random.choice(regions)
        recruits.append(recruit_gen(s, pos, region, needs, marketing_lvl))
    # normalize AI school prestige from db if available
    for r in recruits:
        for sc in r["schools"]:
            if sc["name"] in st.session_state.opponents_db:
                sc["prest"] = st.session_state.opponents_db[sc["name"]]["Prestige"]
    st.session_state.recruits = recruits
    st.session_state.recruit_week = 1
    st.session_state.recruit_stage = "WEEKS"  # WEEKS -> SIGNING -> DONE
    add_news("Recruiting board created: 8 key targets this cycle.")

def recruit_ai_tick(recruit):
    # AI schools gain interest based on prestige + noise
    for sc in recruit["schools"]:
        bump = (sc["prest"] - 60) * 0.08 + random.randint(-2, 5)
        sc["interest"] = clamp(sc["interest"] + bump, 0, 100)

def recruit_my_action_effect(recruit, action: str):
    # returns (delta_interest, cost)
    needs = st.session_state.team_needs
    marketing_lvl = st.session_state.facilities["Marketing"]
    stadium_lvl = st.session_state.facilities["Stadium"]
    training_lvl = st.session_state.facilities["Training"]

    need_bonus = 1.2 if recruit["pos"] in needs else 1.0
    pipeline_bonus = 1.15 if recruit["region"] == st.session_state.home_region else 1.0
    brand_bonus = fac_bonus_recruit_interest(marketing_lvl)
    stadium_pitch = 1.05 + (0.03 if stadium_lvl >= 6 else 0.0)
    training_pitch = 1.03 + (0.02 if training_lvl >= 6 else 0.0)

    base = 0
    cost = 0

    if action == "VISIT" and not recruit["visited"]:
        cost = recruit["visit_cost"]
        base = random.randint(6, 11) if recruit["stars"] >= 4 else random.randint(4, 9)
        base = base * need_bonus * pipeline_bonus * stadium_pitch
        recruit["visited"] = True

    elif action == "PITCH":
        cost = recruit["pitch_cost"]
        # coaching pitch depends on HC + scout + random
        hc = st.session_state.staff.get("HC", {}).get("recruit", 5)
        scout = st.session_state.staff.get("Scout", {}).get("recruit", 5)
        base = random.randint(3, 6) + (hc - 5) * 0.5 + (scout - 5) * 0.3
        base = base * need_bonus * brand_bonus * training_pitch

    elif action == "NIL":
        # user chooses amount via slider; processed elsewhere
        base = 0
        cost = 0

    return int(round(base)), int(cost)

def resolve_signing_day():
    signed = []
    missed = []
    dev_add = {p: 0.0 for p in POSITIONS}
    immediate_add = {p: 0.0 for p in POSITIONS}
    booster_cash = 0

    # donors event chance if marketing 12+
    if fac_bonus_donor_event(st.session_state.facilities["Marketing"]) and random.random() < 0.25:
        booster_cash += 2000000
        add_news("Mega donors ignite: +$2M NIL infusion (Marketing 12 perk).")

    for r in st.session_state.recruits:
        # final AI tick before decision
        recruit_ai_tick(r)

        # NIL effect: compare offer vs ask
        nil_ratio = 0.0
        if r["nil_ask"] > 0:
            nil_ratio = clamp(r["my_nil_offer"] / r["nil_ask"], 0.0, 2.0)

        nil_interest = int(round(10 * (nil_ratio ** 0.75)))  # diminishing returns
        if st.session_state.staff.get("HC", {}).get("trait") == "Recruiter":
            nil_interest = int(nil_interest * 1.08)

        my_final = clamp(r["my_interest"] + nil_interest, 0, 100)
        ai_finals = [sc["interest"] for sc in r["schools"]]

        # weighted choice (softmax-ish)
        # add slight randomness so flips can happen
        candidates = [("YOU", my_final)] + [(r["schools"][0]["name"], ai_finals[0]), (r["schools"][1]["name"], ai_finals[1])]
        weights = []
        for _, v in candidates:
            weights.append(max(1.0, (v + random.randint(-6, 6)) ** 1.25))

        pick = random.choices([c[0] for c in candidates], weights=weights, k=1)[0]
        r["committed"] = pick

        if pick == "YOU":
            signed.append(r)

            # convert recruit -> roster impact points (simple + fun)
            # immediate = freshmen impact, future = dev bank
            if r["stars"] == 5:
                pts = random.uniform(10, 15)
            elif r["stars"] == 4:
                pts = random.uniform(6, 10)
            else:
                pts = random.uniform(3, 6)

            # needs matter more
            if r["pos"] in st.session_state.team_needs:
                pts *= 1.15

            immediate = pts * 0.45
            future = pts * 0.55

            immediate_add[r["pos"]] += immediate
            dev_add[r["pos"]] += future

            # booster bump from landing elite guys
            if r["stars"] == 5:
                booster_cash += random.randint(250000, 750000)
            elif r["stars"] == 4 and random.random() < 0.25:
                booster_cash += random.randint(100000, 300000)

        else:
            missed.append(r)

    return signed, missed, immediate_add, dev_add, booster_cash


# ==============================================================================
# RANKINGS + SELECTION SHOW (Option #5)
# ==============================================================================
def compute_rank_score(team_name: str):
    # User team uses current record; AI uses OVR proxy
    if team_name == st.session_state.team_name:
        w = st.session_state.record["w"]
        l = st.session_state.record["l"]
        ovr = st.session_state.team_rating
        prest = st.session_state.prestige
        sos = estimate_sos_for_user()
    else:
        d = st.session_state.opponents_db.get(team_name, {})
        prest = d.get("Prestige", 70)
        ovr = d.get("OVR", 75)
        # proxy wins based on ovr with noise
        w = int((ovr / 100) * 12) + random.randint(-2, 2)
        w = clamp(w, 0, 12)
        l = 12 - w
        sos = 50 + random.randint(-8, 8)

    # scale: wins are king; then ovr; then prestige; then sos
    score = (w * 14.0) + (ovr * 1.2) + (prest * 0.55) + (sos * 0.20) - (l * 4.0)
    return score

def estimate_sos_for_user():
    # average opp OVR
    if not st.session_state.schedule:
        return 50
    vals = []
    for opp in st.session_state.schedule:
        od = st.session_state.opponents_db.get(opp, {})
        vals.append(od.get("OVR", 75))
    if not vals:
        return 50
    avg = sum(vals) / len(vals)
    # map 65..95 => ~35..75
    return clamp(int((avg - 65) * 2.0 + 35), 30, 80)

def build_rankings():
    rows = []
    for t in ALL_TEAMS:
        sc = compute_rank_score(t)
        if t == st.session_state.team_name:
            rows.append({"Team": t, "Conf": st.session_state.team_conf, "W": st.session_state.record["w"], "L": st.session_state.record["l"],
                         "OVR": st.session_state.team_rating, "Prestige": st.session_state.prestige, "Score": round(sc, 1)})
        else:
            d = st.session_state.opponents_db.get(t, {})
            rows.append({"Team": t, "Conf": get_conference(t), "W": int((d.get("OVR", 75) / 100) * 12), "L": 12 - int((d.get("OVR", 75) / 100) * 12),
                         "OVR": d.get("OVR", 75), "Prestige": d.get("Prestige", 70), "Score": round(sc, 1)})
    df = pd.DataFrame(rows).sort_values("Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df

def init_playoff_bracket_from_rankings(rank_df: pd.DataFrame):
    top12 = rank_df.head(12)["Team"].tolist()
    user_rank = int(rank_df[rank_df["Team"] == st.session_state.team_name]["Rank"].iloc[0])

    # seeds 1-4 bye
    qf_seeds = top12[:4]

    # round 1: 5v12 6v11 7v10 8v9
    r1_matches = [
        {"high": 5, "low": 12, "t1": top12[4], "t2": top12[11], "winner": None},
        {"high": 6, "low": 11, "t1": top12[5], "t2": top12[10], "winner": None},
        {"high": 7, "low": 10, "t1": top12[6], "t2": top12[9], "winner": None},
        {"high": 8, "low": 9,  "t1": top12[7], "t2": top12[8], "winner": None}
    ]
    return {"Type": "CFP", "Round": 1, "Matches": r1_matches, "Seeds": top12, "QF_Seeds": qf_seeds,
            "UserAlive": True, "Rank": user_rank}


# ==============================================================================
# ZONE 4: STATE
# ==============================================================================
def initialize_game_state():
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'SETUP'
        st.session_state.year = 2026
        st.session_state.budget = 0
        st.session_state.prestige = 50
        st.session_state.job_security = 80
        st.session_state.expected_wins = 6
        st.session_state.tenure = 1

        st.session_state.roster = {p: 75 for p in POSITIONS}
        st.session_state.active_transfers = {p: False for p in POSITIONS}
        st.session_state.staff = {}
        st.session_state.facilities = {"Marketing": 1, "Training": 1, "Stadium": 1}

        st.session_state.history = []
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.opponents_db = {}
        st.session_state.my_schemes = {"Off": "Pro Style", "Def": "Man Coverage"}
        st.session_state.career_stats = {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0}

        st.session_state.season_logs = []
        st.session_state.schedule = []
        st.session_state.season_done = False
        st.session_state.week_index = 0

        st.session_state.hotspots = {}
        st.session_state.portal_players = []
        st.session_state.candidates = {}

        st.session_state.postseason_data = {"Type": None}
        st.session_state.revenue_report = None
        st.session_state.inflation = 1.0
        st.session_state.team_needs = []
        st.session_state.game_plan = "Normal"
        st.session_state.news = []

        st.session_state.dev_bank = {p: 0.0 for p in POSITIONS}

        # Recruit battles state
        st.session_state.recruits = []
        st.session_state.recruit_week = 1
        st.session_state.recruit_stage = "WEEKS"

        # rankings
        st.session_state.rankings_df = None
        st.session_state.selection_revealed = False

def generate_hotspots():
    hotspots = {}
    for reg in REGION_STRENGTH.keys():
        hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

initialize_game_state()


# ==============================================================================
# ZONE 5: UI CONTROLLERS
# ==============================================================================
def run_setup():
    st.title("🏆 College Football V1")
    st.markdown("### Dynasty Mode (Jan 2026)")

    c1, c2 = st.columns(2)
    name = c1.text_input("AD Name", "Coach Prime")
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"])

    sorted_teams = sorted(REAL_WORLD_INIT.keys()) + sorted([t for t in ALL_TEAMS if t not in REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)

    if team in REAL_WORLD_INIT:
        d = REAL_WORLD_INIT[team]
        tier = d['Tier']
        budget = 25000000 if tier == 1 else (15000000 if tier == 2 else 5000000)
        conf = get_conference(team)
        rival = d.get('Rival', 'Rival')
    else:
        tier, budget, conf, rival = 3, 5000000, get_conference(team), "Rival"

    expect = 10 if tier == 1 else (8 if tier == 2 else (6 if tier == 3 else 4))
    st.info(f"**{team}** | Conf: {conf} | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival}")
    st.caption(f"Expectation: {expect}+ Wins")

    if st.button("Start Dynasty", type="primary"):
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = TEAMS_DB.get(team, {}).get('color', '#333333')
        st.session_state.team_conf = conf
        st.session_state.team_rival = rival
        st.session_state.home_region = "South"
        st.session_state.expected_wins = expect
        st.session_state.school_tier = tier
        st.session_state.budget = int(budget * (0.75 if diff == "Hard" else 1.25 if diff == "Easy" else 1.0))

        st.session_state.roster = engine_generate_roster(tier, REAL_WORLD_INIT.get(team, {}).get('Talent'))
        st.session_state.prestige = REAL_WORLD_INIT.get(team, {}).get('Prestige', 60)
        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)

        st.session_state.staff = {}
        for r in ["HC", "OC", "DC", "Scout"]:
            st.session_state.staff[r] = engine_generate_coach(r, tier)

        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}

        # Opponent DB includes Off/Def split + Stadium
        st.session_state.opponents_db = {}
        for opp in ALL_TEAMS:
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                base = data['Talent']
                skew = random.randint(-3, 3)
                st.session_state.opponents_db[opp] = {
                    "Prestige": data['Prestige'],
                    "OVR": base,
                    "OffOVR": int(clamp(base + skew, 55, 99)),
                    "DefOVR": int(clamp(base - skew, 55, 99)),
                    "Off": random.choice(list(SCHEMES["Offense"])),
                    "Def": random.choice(list(SCHEMES["Defense"])),
                    "Coaches": {"OC": random.randint(5, 9), "DC": random.randint(5, 9)},
                    "Stadium": int(clamp(round(data['Prestige'] / 10), 1, 12))
                }
            else:
                pres = 85 if opp in CONFERENCES['SEC'] else 65
                ovr = 82 if opp in CONFERENCES['SEC'] else 70
                skew = random.randint(-3, 3)
                st.session_state.opponents_db[opp] = {
                    "Prestige": pres, "OVR": ovr,
                    "OffOVR": int(clamp(ovr + skew, 55, 99)),
                    "DefOVR": int(clamp(ovr - skew, 55, 99)),
                    "Off": "Pro Style", "Def": "Man Coverage",
                    "Coaches": {"OC": 5, "DC": 5},
                    "Stadium": int(clamp(round(pres / 10), 1, 12))
                }

        st.session_state.hotspots = generate_hotspots()
        st.session_state.schedule = engine_generate_schedule(team, conf, rival)

        st.session_state.week_index = 0
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.season_done = False
        st.session_state.dev_bank = {p: 0.0 for p in POSITIONS}

        st.session_state.recruits = []
        st.session_state.recruit_week = 1
        st.session_state.recruit_stage = "WEEKS"
        st.session_state.rankings_df = None
        st.session_state.selection_revealed = False

        add_news(f"{team} hires {st.session_state.staff['HC']['name']} as HC.")
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()

def show_facilities_tab():
    perks = facilities_perks()
    m, t, s = st.session_state.facilities["Marketing"], st.session_state.facilities["Training"], st.session_state.facilities["Stadium"]

    c1, c2, c3 = st.columns(3)
    for col, name, lvl, cost, desc in [
        (c1, "Marketing", m, 1000000, "Revenue + Recruiting Brand"),
        (c2, "Training", t, 3000000, "Unit Boost + Development Conversion"),
        (c3, "Stadium",  s, 10000000, "Home Field + Prestige")
    ]:
        with col:
            st.markdown(f"<div class='fac-card'><div class='fac-title'>🏗️ {name} — Level {lvl}</div><div class='mini'>{desc}</div>", unsafe_allow_html=True)
            st.progress(min(1.0, lvl / 12.0))
            # show next milestone perk
            milestone_text = None
            for ms in [6, 9, 12]:
                if lvl < ms:
                    milestone_text = f"Next perk at **{ms}**: {perks[name][ms]}"
                    break
            if milestone_text is None:
                milestone_text = f"Max perks unlocked: {perks[name][12]}"

            st.markdown(f"<div class='perk'>✨ {milestone_text}</div></div>", unsafe_allow_html=True)

            if st.button(f"Upgrade {name} ({helper_format_cash(cost)})", key=f"up_{name}"):
                if st.session_state.budget >= cost:
                    st.session_state.budget -= cost
                    st.session_state.facilities[name] += 1
                    # stadium prestige milestone
                    if name == "Stadium":
                        st.session_state.prestige = min(99, st.session_state.prestige + 1)
                    add_news(f"{name} upgraded to Level {st.session_state.facilities[name]}.")
                    st.rerun()

def show_rankings_tab():
    st.subheader("🏅 National Rankings (Top 25)")
    df = build_rankings()
    st.session_state.rankings_df = df
    top25 = df.head(25).copy()

    # highlight user row
    def style_row(row):
        if row["Team"] == st.session_state.team_name:
            return ["background-color: #fffbf0; font-weight: 900;"] * len(row)
        return [""] * len(row)

    st.dataframe(top25.style.apply(style_row, axis=1), use_container_width=True, height=600)
    user_row = df[df["Team"] == st.session_state.team_name].iloc[0]
    st.info(f"Your current rank projection: **#{int(user_row['Rank'])}** (Score: {user_row['Score']})")

def show_dashboard():
    thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < thresh:
        st.session_state.game_state = "FIRED"
        st.rerun()

    # annual stadium prestige tick (12+)
    tick = stadium_prestige_tick(st.session_state.facilities["Stadium"])
    if tick and not st.session_state.get("prestige_ticked_this_year", False):
        st.session_state.prestige = min(99, st.session_state.prestige + tick)
        st.session_state.prestige_ticked_this_year = True
        add_news("Stadium 12 perk: prestige rises (+1).")

    if st.session_state.revenue_report:
        st.markdown(f"<div class='finance-alert'>💰 FINANCIAL REPORT<br>{st.session_state.revenue_report}</div>", unsafe_allow_html=True)

    sec = st.session_state.job_security
    sec_cls = "security-safe" if sec > 75 else ("security-warm" if sec > 40 else "security-hot")

    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Security: <span class='{sec_cls}'>{sec}%</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 12px; color: white;'><h2 style='margin:0'>{st.session_state.team_name}</h2></div>", unsafe_allow_html=True)

    # team unit ratings
    my_off_raw, my_def_raw = team_units_from_roster(st.session_state.roster)
    boost = training_unit_boost(st.session_state.facilities["Training"])
    my_off = clamp(my_off_raw + boost, 40, 99)
    my_def = clamp(my_def_raw + boost, 40, 99)
    team_ovr = int(clamp(0.52 * my_off + 0.48 * my_def, 40, 99))

    st.session_state.my_off = my_off
    st.session_state.my_def = my_def
    st.session_state.team_rating = team_ovr

    raw_roster_val = int(sum(st.session_state.roster.values()) / 7)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("Team OVR", team_ovr, f"Raw Talent: {raw_roster_val}")
    c3.metric("Off / Def", f"{int(my_off)} / {int(my_def)}")
    c4.metric("Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    c5.metric("Legacy Score", saban, f"Titles: {st.session_state.career_stats['titles']}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Strategy", "Staff", "Facilities+", "Season (Weekly)", "Rankings"])

    with tab1:
        c1, c2 = st.columns(2)
        st.session_state.my_schemes["Off"] = c1.selectbox("Offense", SCHEMES["Offense"])
        st.session_state.my_schemes["Def"] = c2.selectbox("Defense", SCHEMES["Defense"])
        st.write("Unit Strength")
        for p, v in st.session_state.roster.items():
            lab = f"{p}: {int(v)}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.progress(min(1.0, v / 100), lab)

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
                        <div><span class='badge {badge_cls}'>RATING: {rtg}</span><span class='badge badge-trait'>{c.get('trait','None')}</span></div>
                        <div class='mini'>{helper_format_cash(c.get('salary',0))}</div>
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
                for i, cand in enumerate(st.session_state.candidates[role]):
                    with cols[i]:
                        rr = role_rating(cand, role)
                        vis_rate = f"{rr}" if cand['scouted'] else f"{get_letter_grade(rr)}"
                        vis_trait = cand['trait'] if cand['scouted'] else "???"
                        st.markdown(f"""
                        <div class='staff-card'>
                            <div class='staff-name'>{cand['name']}</div>
                            <div class='mini'>{cand['history']}</div>
                            <div style='margin:6px 0'><span class='badge badge-trait'>{role} OVR: {vis_rate}</span><span class='badge badge-trait'>Trait: {vis_trait}</span></div>
                            <div style='font-weight:900'>{helper_format_cash(cand['salary'])}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        b1, b2 = st.columns(2)
                        if b1.button("Hire", key=f"h_{role}_{i}"):
                            if st.session_state.budget >= cand['salary']:
                                st.session_state.budget -= cand['salary']
                                st.session_state.staff[role] = cand
                                add_news(f"{st.session_state.team_name} hires {cand['name']} as {role}.")
                                del st.session_state.candidates[role]
                                st.rerun()
                        if not cand['scouted'] and b2.button("Scout ($25k)", key=f"sc_{role}_{i}"):
                            if st.session_state.budget >= 25000:
                                st.session_state.budget -= 25000
                                cand['scouted'] = True
                                st.rerun()

                if st.button("Promote GA (Free)", key=f"ga_{role}"):
                    ga = {"name": f"GA {generate_name()}", "role": role,
                          "off": random.randint(1, 3), "def": random.randint(1, 3), "recruit": random.randint(1, 2),
                          "trait": "None", "salary": 50000, "history": "Former Player", "scouted": True}
                    st.session_state.staff[role] = ga
                    add_news(f"{st.session_state.team_name} promotes {ga['name']} to {role}.")
                    st.rerun()

    with tab3:
        show_facilities_tab()

    with tab5:
        show_rankings_tab()

    with tab4:
        if len(st.session_state.staff) < 4:
            st.error("Fill Staff First!")
            return

        if not st.session_state.schedule:
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)

        st.session_state.game_plan = st.selectbox("Weekly Gameplan", ["Conservative", "Normal", "Aggressive"],
                                                  index=["Conservative", "Normal", "Aggressive"].index(st.session_state.game_plan))

        # schedule display
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
        st.markdown("### 🗞️ News Feed")
        st.markdown("<div class='news-box'>", unsafe_allow_html=True)
        if st.session_state.news:
            for n in st.session_state.news[:9]:
                st.markdown(f"<div class='news-item'>• {n}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='news-item'>• No headlines yet.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        if not st.session_state.season_done:
            wk = st.session_state.week_index
            if wk < 12:
                opp = st.session_state.schedule[wk]
                opp_data = st.session_state.opponents_db.get(opp, {"OffOVR": 78, "DefOVR": 78, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 6})
                is_riv = (opp == st.session_state.team_rival)
                is_home = (wk % 2 == 0)

                st.subheader(f"Next Game: Week {wk+1} {'vs' if is_home else '@'} {opp} (Off/Def: {opp_data['OffOVR']}/{opp_data['DefOVR']})")
                if is_riv:
                    st.warning("RIVALRY WEEK: More chaos, bigger stakes!")

                colA, colB = st.columns(2)
                if colA.button("🏈 PLAY WEEK", type="primary"):
                    res = engine_play_game(
                        my_off=st.session_state.my_off,
                        my_def=st.session_state.my_def,
                        opp_off=opp_data.get("OffOVR", opp_data.get("OVR", 80)),
                        opp_def=opp_data.get("DefOVR", opp_data.get("OVR", 80)),
                        staff=st.session_state.staff,
                        schemes=st.session_state.my_schemes,
                        opp_schemes={"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                        game_plan=st.session_state.game_plan,
                        opp_coaches=opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                        is_home=is_home,
                        is_rival=is_riv,
                        my_stadium_lvl=st.session_state.facilities["Stadium"],
                        opp_stadium_lvl=opp_data.get("Stadium", 6)
                    )

                    if res['result'] == "W":
                        st.session_state.record["w"] += 1
                        st.session_state.career_stats["w"] += 1
                        st.session_state.job_security = min(100, st.session_state.job_security + (6 if is_riv else 2))
                        add_news(f"{st.session_state.team_name} wins Week {wk+1} vs {opp} ({res['score']}).")
                    else:
                        st.session_state.record["l"] += 1
                        st.session_state.career_stats["l"] += 1
                        pen = 2 if st.session_state.tenure <= 2 else 5
                        st.session_state.job_security = max(0, st.session_state.job_security - pen)
                        add_news(f"{st.session_state.team_name} loses Week {wk+1} vs {opp} ({res['score']}).")

                    st.session_state.season_logs.append({
                        "Week": wk + 1,
                        "Opponent": opp,
                        "Score": f"{res['result']} {res['score']}",
                        "Stats": res['stats']
                    })

                    st.session_state.week_index += 1
                    if st.session_state.week_index >= 12:
                        st.session_state.season_done = True
                        add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")
                    st.rerun()

                if colB.button("⏩ SIM REST OF SEASON"):
                    while not st.session_state.season_done:
                        wk2 = st.session_state.week_index
                        if wk2 >= 12:
                            st.session_state.season_done = True
                            break
                        opp2 = st.session_state.schedule[wk2]
                        opp_data2 = st.session_state.opponents_db.get(opp2, {"OffOVR": 78, "DefOVR": 78, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 6})
                        is_riv2 = (opp2 == st.session_state.team_rival)
                        is_home2 = (wk2 % 2 == 0)

                        res2 = engine_play_game(
                            my_off=st.session_state.my_off,
                            my_def=st.session_state.my_def,
                            opp_off=opp_data2.get("OffOVR", opp_data2.get("OVR", 80)),
                            opp_def=opp_data2.get("DefOVR", opp_data2.get("OVR", 80)),
                            staff=st.session_state.staff,
                            schemes=st.session_state.my_schemes,
                            opp_schemes={"Off": opp_data2.get("Off", "Pro Style"), "Def": opp_data2.get("Def", "Man Coverage")},
                            game_plan=st.session_state.game_plan,
                            opp_coaches=opp_data2.get("Coaches", {"OC": 5, "DC": 5}),
                            is_home=is_home2,
                            is_rival=is_riv2,
                            my_stadium_lvl=st.session_state.facilities["Stadium"],
                            opp_stadium_lvl=opp_data2.get("Stadium", 6)
                        )

                        if res2['result'] == "W":
                            st.session_state.record["w"] += 1
                            st.session_state.career_stats["w"] += 1
                        else:
                            st.session_state.record["l"] += 1
                            st.session_state.career_stats["l"] += 1
                            pen = 2 if st.session_state.tenure <= 2 else 5
                            st.session_state.job_security = max(0, st.session_state.job_security - pen)

                        st.session_state.season_logs.append({
                            "Week": wk2 + 1,
                            "Opponent": opp2,
                            "Score": f"{res2['result']} {res2['score']}",
                            "Stats": res2['stats']
                        })
                        st.session_state.week_index += 1

                    add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")
                    st.rerun()

        if st.session_state.season_done:
            st.write("### Season Results (Recap)")
            for log in st.session_state.season_logs:
                res = "W" if log['Score'].startswith("W") else "L"
                css = "game-card-win" if res == "W" else "game-card-loss"
                s = log['Stats']
                st.markdown(f"""
                <div class='game-card {css}'>
                    <div class='card-header'><span>{log['Score']}</span><span>vs {log['Opponent']}</span></div>
                    <div class='stat-grid'>
                        <div class='stat-row'><span>⚔️ Off vs Def</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div>
                        <div class='stat-row'><span>🛡️ Def vs Off</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div>
                        <div class='stat-row'><span>🧠 Staff</span><span>{s['staff'][0]} vs {s['staff'][1]}</span></div>
                        <div class='stat-row'><span>📈 Margin</span><span>{s['margin']}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            if st.button("Proceed to Selection Show", type="primary"):
                st.session_state.rankings_df = build_rankings()
                st.session_state.selection_revealed = False
                st.session_state.game_state = "POSTSEASON"
                st.rerun()

def show_postseason():
    st.title("🏟️ Selection Show / Postseason")
    # Build rankings if needed
    if st.session_state.rankings_df is None:
        st.session_state.rankings_df = build_rankings()

    df = st.session_state.rankings_df
    user_row = df[df["Team"] == st.session_state.team_name].iloc[0]
    user_rank = int(user_row["Rank"])

    st.markdown("<div class='bracket-box'><h2 style='margin:0'>CFP Committee Reveal</h2><div style='opacity:0.85'>Top 12 + Bowl placements</div></div>", unsafe_allow_html=True)

    top12 = df.head(12).copy()
    st.subheader("Top 12 Seeds")
    for _, row in top12.iterrows():
        tag = " ⭐ YOU" if row["Team"] == st.session_state.team_name else ""
        st.markdown(f"<div class='bracket-row'><span>#{int(row['Rank'])} {row['Team']}{tag}</span><span>Score: {row['Score']}</span></div>", unsafe_allow_html=True)

    st.divider()

    if user_rank <= 12:
        if not st.session_state.selection_revealed:
            st.success(f"You're in the CFP! Committee seed: **#{user_rank}**")
            st.session_state.selection_revealed = True

        if "postseason_data" not in st.session_state or st.session_state.postseason_data.get("Type") != "CFP":
            st.session_state.postseason_data = init_playoff_bracket_from_rankings(df)

        data = st.session_state.postseason_data
        st.subheader(f"CFP Round: {['Opening Rd', 'Quarterfinals', 'Semifinals', 'Championship'][data['Round'] - 1]}")

        st.write("--- Bracket Status ---")
        for m in data['Matches']:
            if m.get('winner'):
                res_txt = f"✅ {m['winner']} advances"
            else:
                res_txt = f"{m['t1']} vs {m['t2']}"
            st.markdown(f"<div class='bracket-row'>{res_txt}</div>", unsafe_allow_html=True)

        # Find user match
        user_match = None
        for m in data['Matches']:
            if m['t1'] == st.session_state.team_name or m['t2'] == st.session_state.team_name:
                user_match = m
                break

        if data['UserAlive'] and user_match:
            opp = user_match['t2'] if user_match['t1'] == st.session_state.team_name else user_match['t1']
            opp_data = st.session_state.opponents_db.get(opp, {"OffOVR": 85, "DefOVR": 85, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 8})

            st.info(f"Your Matchup: vs {opp} (Off/Def: {opp_data['OffOVR']}/{opp_data['DefOVR']})")

            if st.button("PLAY PLAYOFF GAME 🏈", type="primary"):
                res = engine_play_game(
                    my_off=st.session_state.my_off,
                    my_def=st.session_state.my_def,
                    opp_off=opp_data.get("OffOVR", opp_data.get("OVR", 85)),
                    opp_def=opp_data.get("DefOVR", opp_data.get("OVR", 85)),
                    staff=st.session_state.staff,
                    schemes=st.session_state.my_schemes,
                    opp_schemes={"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                    game_plan=st.session_state.game_plan,
                    opp_coaches=opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                    is_home=False, is_rival=False,
                    my_stadium_lvl=st.session_state.facilities["Stadium"],
                    opp_stadium_lvl=opp_data.get("Stadium", 8)
                )

                next_round_teams = []
                for m in data['Matches']:
                    if m == user_match:
                        if res['result'] == "W":
                            m['winner'] = st.session_state.team_name
                            next_round_teams.append(st.session_state.team_name)
                            st.toast("VICTORY! Advancing...")
                            add_news(f"{st.session_state.team_name} advances in the CFP! ({res['score']})")
                        else:
                            m['winner'] = opp
                            next_round_teams.append(opp)
                            st.session_state.postseason_data['UserAlive'] = False
                            st.error(f"Eliminated by {opp}")
                            add_news(f"{st.session_state.team_name} eliminated by {opp}. ({res['score']})")
                    else:
                        winner = random.choice([m['t1'], m['t2']])
                        m['winner'] = winner
                        next_round_teams.append(winner)

                time.sleep(0.4)

                if st.session_state.postseason_data['UserAlive']:
                    if data['Round'] == 4:
                        st.session_state.budget += 50000000
                        st.session_state.career_stats['titles'] += 1
                        st.balloons()
                        st.success("NATIONAL CHAMPIONS!")
                        add_news(f"{st.session_state.team_name} wins the NATIONAL TITLE!")
                        hist = {"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Bowl": "National Title"}
                        st.session_state.history.append(hist)
                        st.session_state.game_state = "SUMMARY"
                        st.rerun()
                    else:
                        new_matches = []
                        if data['Round'] == 1:
                            seeds = data['QF_Seeds']
                            for i in range(4):
                                new_matches.append({"t1": seeds[i], "t2": next_round_teams[3 - i], "winner": None})
                        elif data['Round'] == 2:
                            new_matches.append({"t1": next_round_teams[0], "t2": next_round_teams[3], "winner": None})
                            new_matches.append({"t1": next_round_teams[1], "t2": next_round_teams[2], "winner": None})
                        elif data['Round'] == 3:
                            new_matches.append({"t1": next_round_teams[0], "t2": next_round_teams[1], "winner": None})

                        st.session_state.postseason_data['Round'] += 1
                        st.session_state.postseason_data['Matches'] = new_matches
                        st.rerun()
                else:
                    hist = {"Year": st.session_state.year, "Record": "Playoff Loss", "Rank": f"#{data.get('Rank', '?')}", "Bowl": "CFP"}
                    st.session_state.history.append(hist)
                    st.session_state.game_state = "SUMMARY"
                    st.rerun()

        elif data['UserAlive'] and not user_match:
            st.success("You have a BYE week.")
            if st.button("Simulate Round"):
                next_round_teams = []
                for m in data['Matches']:
                    winner = random.choice([m['t1'], m['t2']])
                    m['winner'] = winner
                    next_round_teams.append(winner)

                if data['Round'] == 1:
                    seeds = data['QF_Seeds']
                    new_matches = []
                    for i in range(4):
                        new_matches.append({"t1": seeds[i], "t2": next_round_teams[3 - i], "winner": None})

                    st.session_state.postseason_data['Round'] += 1
                    st.session_state.postseason_data['Matches'] = new_matches
                    st.rerun()

    else:
        bowl = get_bowl_name(user_rank)
        candidates = [t for t in ALL_TEAMS if t != st.session_state.team_name]
        opp = random.choice(candidates)
        opp_data = st.session_state.opponents_db.get(opp, {"OffOVR": 80, "DefOVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 7})

        st.warning(f"Outside CFP cutoff. Bowl bid: **{bowl}**")
        st.markdown(f"<div class='bracket-box'><h3 style='margin:0'>{bowl}</h3><h2 style='margin:8px 0 0 0'>VS {opp}</h2></div>", unsafe_allow_html=True)

        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            res = engine_play_game(
                my_off=st.session_state.my_off,
                my_def=st.session_state.my_def,
                opp_off=opp_data.get("OffOVR", opp_data.get("OVR", 80)),
                opp_def=opp_data.get("DefOVR", opp_data.get("OVR", 80)),
                staff=st.session_state.staff,
                schemes=st.session_state.my_schemes,
                opp_schemes={"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                game_plan=st.session_state.game_plan,
                opp_coaches=opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                is_home=False, is_rival=False,
                my_stadium_lvl=st.session_state.facilities["Stadium"],
                opp_stadium_lvl=opp_data.get("Stadium", 7)
            )

            wins = st.session_state.record['w'] + (1 if res['result'] == "W" else 0)
            losses = st.session_state.record['l'] + (1 if res['result'] == "L" else 0)

            if res['result'] == "W":
                st.session_state.budget += 2000000
                st.toast("🎳 BOWL WIN BONUS: $2M")
                st.session_state.career_stats['bowl_w'] += 1
                add_news(f"{st.session_state.team_name} wins {bowl}! ({res['score']})")
            else:
                st.session_state.career_stats['bowl_l'] += 1
                add_news(f"{st.session_state.team_name} loses {bowl}. ({res['score']})")

            delta = wins - st.session_state.expected_wins
            if delta > 0:
                st.session_state.budget += delta * 1000000
            elif delta < 0:
                st.session_state.budget -= abs(delta) * 500000

            hist = {"Year": st.session_state.year, "Record": f"{wins}-{losses}", "Rank": f"#{user_rank}", "Bowl": bowl}
            st.session_state.history.append(hist)
            st.session_state.game_state = "SUMMARY"
            st.rerun()

def show_year_summary():
    st.title(f"{st.session_state.year} Summary")
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    else:
        st.info("No season history yet.")

    st.markdown(f"<div class='nil-alert'>💰 WAR CHEST AVAILABLE FOR NIL: {helper_format_cash(st.session_state.budget)}</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Enter Portal", type="primary"):
            st.session_state.portal_players = engine_generate_portal_players()
            st.session_state.game_state = "PORTAL"
            st.rerun()
    with c2:
        if st.button("Go Straight to Recruiting"):
            st.session_state.game_state = "RECRUITING"
            st.rerun()

def show_portal():
    st.title("Transfer Portal")
    st.write(f"Budget: {helper_format_cash(st.session_state.budget)}")

    for i, p in enumerate(list(st.session_state.portal_players)):
        c1, c2 = st.columns([3, 1])
        c1.write(f"{p['pos']} {p['name']} ({p['rating']}) - {helper_format_cash(p['cost'])}")
        if c2.button("Sign", key=f"p_{i}"):
            if st.session_state.budget >= p['cost']:
                st.session_state.budget -= p['cost']
                st.session_state.roster[p['pos']] = p['rating']
                st.session_state.active_transfers[p['pos']] = True
                st.session_state.portal_players.pop(i)
                add_news(f"{st.session_state.team_name} signs portal {p['pos']} {p['name']} ({p['rating']}).")
                st.rerun()

    if st.button("Go to Recruiting"):
        st.session_state.game_state = "RECRUITING"
        st.rerun()

def show_recruiting():
    st.title("Recruiting: Recruit Battles")
    st.write(f"Budget: {helper_format_cash(st.session_state.budget)}")
    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    needs = st.session_state.team_needs
    st.markdown(f"<div class='recruiting-intel'>Pipeline Bonus ({st.session_state.home_region}): {', '.join(hot)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='recruiting-intel'>Team Needs: <b>{', '.join(needs)}</b></div>", unsafe_allow_html=True)

    if not st.session_state.recruits:
        if st.button("Generate Recruiting Board (8 Targets)", type="primary"):
            start_recruit_battles()
            st.rerun()
        return

    # Recruiting weeks
    if st.session_state.recruit_stage == "WEEKS":
        st.subheader(f"Recruiting Week {st.session_state.recruit_week} / 3")

        cols = st.columns(2)
        for idx, r in enumerate(st.session_state.recruits):
            with cols[idx % 2]:
                stars = "⭐" * r["stars"]
                is_need = r["pos"] in needs
                is_hot = r["pos"] in hot
                chips = ""
                if is_need: chips += "<span class='chip chip-need'>NEED</span>"
                if is_hot: chips += "<span class='chip chip-hot'>PIPELINE</span>"
                chips += f"<span class='chip'>{r['region']}</span>"

                st.markdown(f"""
                <div class='recruit-card'>
                  <div class='recruit-top'><span>{r['pos']} {r['name']}</span><span>{stars}</span></div>
                  <div class='mini'>{chips}</div>
                  <div class='mini' style='margin-top:6px'>NIL Ask: <b>{helper_format_cash(r['nil_ask'])}</b> | Your Offer: <b>{helper_format_cash(r['my_nil_offer'])}</b></div>
                  <div class='mini'>Visited: <b>{"Yes" if r["visited"] else "No"}</b> | Pitch: <b>{r["my_pitch"]}</b></div>
                  <div class='mini' style='margin-top:6px'><b>Your Interest</b>: {int(r['my_interest'])}/100</div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(min(1.0, r["my_interest"] / 100.0))

                # show rivals
                sc1, sc2 = r["schools"][0], r["schools"][1]
                st.caption(f"Competing: {sc1['name']} ({int(sc1['interest'])}) • {sc2['name']} ({int(sc2['interest'])})")

                # actions
                a1, a2, a3 = st.columns(3)

                if a1.button(f"Host Visit ({helper_format_cash(r['visit_cost'])})", key=f"visit_{r['id']}"):
                    delta, cost = recruit_my_action_effect(r, "VISIT")
                    if r["visited"]:
                        if st.session_state.budget >= cost:
                            st.session_state.budget -= cost
                            r["my_interest"] = clamp(r["my_interest"] + delta, 0, 100)
                            add_news(f"Visit weekend: {r['name']} interest +{delta}.")
                        else:
                            st.toast("Not enough budget for visit.")
                    st.rerun()

                if a2.button(f"Coach Pitch ({helper_format_cash(r['pitch_cost'])})", key=f"pitch_{r['id']}"):
                    delta, cost = recruit_my_action_effect(r, "PITCH")
                    if st.session_state.budget >= cost:
                        st.session_state.budget -= cost
                        r["my_pitch"] += 1
                        r["my_interest"] = clamp(r["my_interest"] + delta, 0, 100)
                        add_news(f"Coach pitch: {r['name']} interest +{delta}.")
                    else:
                        st.toast("Not enough budget for pitch.")
                    st.rerun()

                # NIL slider + commit offer button
                nil_step = 100000
                max_offer = min(5000000, st.session_state.budget + r["my_nil_offer"])
                offer = st.slider("Set NIL Offer", 0, int(max_offer), int(r["my_nil_offer"]), step=nil_step, key=f"nil_{r['id']}")
                if a3.button("Submit NIL", key=f"nilbtn_{r['id']}"):
                    delta_cost = offer - r["my_nil_offer"]
                    if delta_cost > 0 and st.session_state.budget < delta_cost:
                        st.toast("Not enough budget for that NIL offer.")
                    else:
                        st.session_state.budget -= max(0, delta_cost)
                        r["my_nil_offer"] = offer
                        # small immediate interest bump for showing serious money
                        bump = int(round(3 * ((offer / max(1, r["nil_ask"])) ** 0.55)))
                        bump = clamp(bump, 0, 8)
                        r["my_interest"] = clamp(r["my_interest"] + bump, 0, 100)
                        add_news(f"NIL offer updated for {r['name']} (+{bump} interest).")
                    st.rerun()

        st.divider()
        c1, c2 = st.columns(2)

        if c1.button("Advance Week"):
            # AI gains, plus your board volatility
            for r in st.session_state.recruits:
                recruit_ai_tick(r)
                # small drift
                drift = random.randint(-1, 2)
                r["my_interest"] = clamp(r["my_interest"] + drift, 0, 100)

            st.session_state.recruit_week += 1
            if st.session_state.recruit_week >= 4:
                st.session_state.recruit_stage = "SIGNING"
                add_news("Recruiting ends. Signing Day begins.")
            st.rerun()

        if c2.button("Skip to Signing Day"):
            st.session_state.recruit_stage = "SIGNING"
            add_news("Recruiting ends early. Signing Day begins.")
            st.rerun()

    elif st.session_state.recruit_stage == "SIGNING":
        st.subheader("🎓 Signing Day")
        if st.button("Reveal Commitments", type="primary"):
            signed, missed, immediate_add, dev_add, booster_cash = resolve_signing_day()

            # apply roster changes with attrition + immediate recruit impact
            for p in POSITIONS:
                loss = 10 if st.session_state.active_transfers[p] else random.randint(2, 5)
                st.session_state.active_transfers[p] = False
                st.session_state.roster[p] = clamp(st.session_state.roster[p] - loss + immediate_add.get(p, 0.0), 40, 99)

            # dev bank add
            for p in POSITIONS:
                st.session_state.dev_bank[p] = st.session_state.dev_bank.get(p, 0.0) + dev_add.get(p, 0.0)

            # apply offseason development now (uses training conversion)
            st.session_state.roster = apply_development_pipeline(
                st.session_state.roster,
                st.session_state.dev_bank,
                training_lvl=st.session_state.facilities["Training"]
            )
            # decay dev bank
            st.session_state.dev_bank = {p: st.session_state.dev_bank.get(p, 0.0) * 0.25 for p in POSITIONS}

            # booster cash
            if booster_cash > 0:
                st.session_state.budget += booster_cash
                st.toast(f"Boosters react to recruiting: +{helper_format_cash(booster_cash)}")

            # revenue payout
            rev = engine_calculate_revenue(st.session_state.school_tier, st.session_state.facilities['Marketing'], st.session_state.inflation)
            st.session_state.budget += rev
            st.session_state.revenue_report = f"Season Budget Injection: +{helper_format_cash(rev)}"

            # update needs
            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)

            # evolve universe, year advance
            st.session_state.opponents_db = engine_evolve_universe(st.session_state.opponents_db)
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.inflation *= 1.05
            st.session_state.prestige_ticked_this_year = False

            # reset season
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
            st.session_state.hotspots = generate_hotspots()
            st.session_state.week_index = 0
            st.session_state.record = {"w": 0, "l": 0}
            st.session_state.season_logs = []
            st.session_state.season_done = False

            # clear recruiting board
            st.session_state.recruit_stage = "DONE"

            # news + summary
            add_news(f"Signing Day complete: {len(signed)} commits. Needs now: {', '.join(st.session_state.team_needs)}.")
            st.rerun()

        # preview commitments (current leaders)
        st.caption("Current leaders (unofficial):")
        for r in st.session_state.recruits:
            my_val = r["my_interest"] + int(round(10 * ((r["my_nil_offer"] / max(1, r["nil_ask"])) ** 0.75)))
            best_ai = max(r["schools"][0]["interest"], r["schools"][1]["interest"])
            leader = "YOU" if my_val >= best_ai else (r["schools"][0]["name"] if r["schools"][0]["interest"] >= r["schools"][1]["interest"] else r["schools"][1]["name"])
            st.write(f"- {r['pos']} {r['name']} ({'⭐'*r['stars']}): Leader = **{leader}**")

    elif st.session_state.recruit_stage == "DONE":
        st.success("Offseason complete. Returning to dashboard...")
        time.sleep(0.3)
        st.session_state.recruits = []
        st.session_state.recruit_week = 1
        st.session_state.recruit_stage = "WEEKS"
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

def show_fired():
    st.error("FIRED! Your tenure has ended.")
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.write(f"Final Legacy (Saban) Score: **{saban}**")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()

def show_retirement():
    st.title("Retirement")
    st.write("Thanks for playing!")
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.write(f"Final Legacy (Saban) Score: **{saban}**")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()

# ==============================================================================
# ROUTER
# ==============================================================================
if st.session_state.game_state == 'SETUP':
    run_setup()
elif st.session_state.game_state == 'FIRED':
    show_fired()
elif st.session_state.game_state == 'DASHBOARD':
    show_dashboard()
elif st.session_state.game_state == 'POSTSEASON':
    show_postseason()
elif st.session_state.game_state == 'SUMMARY':
    show_year_summary()
elif st.session_state.game_state == 'PORTAL':
    show_portal()
elif st.session_state.game_state == 'RECRUITING':
    show_recruiting()
elif st.session_state.game_state == 'RETIREMENT':
    show_retirement()
