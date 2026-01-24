import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# COLLEGE FOOTBALL MOGUL V7 — SINGLE FILE APP
# - Includes normalize_shares fix
# - Includes Offseason Hub + NIL + HS Outreach + Top-8 Battles
# - Includes tiered home field advantage logic
# ==============================================================================

# ==============================================================================
# ZONE 1: CONFIGURATION & STATIC DATA
# ==============================================================================
try:
    st.set_page_config(page_title="College Football Mogul V7", page_icon="🏈", layout="wide")
except Exception:
    pass

st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }

.security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
.security-safe { color: #28a745; font-weight: bold; }
.security-warm { color: #fd7e14; font-weight: bold; }
.security-hot { color: #dc3545; font-weight: bold; }

.finance-alert { background-color: #d1e7dd; color: #0f5132; border: 1px solid #badbcc; padding: 15px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-weight: bold; }
.nil-alert { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; padding: 18px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-size: 1.1em; font-weight: bold; }

.game-card { padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #ddd; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.game-card-win { border-left: 5px solid #28a745; }
.game-card-loss { border-left: 5px solid #dc3545; }
.game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa; }
.game-card-rival { border: 2px solid #ffc107 !important; background-color: #fffbf0 !important; }

.card-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 5px;}
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.85em; }
.stat-row { display: flex; justify-content: space-between; }

.staff-card { background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
.staff-role { font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.staff-name { font-size: 1.1em; font-weight: 800; color: #333; }
.badge { padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; margin-right: 5px; display: inline-block;}
.badge-tier-s { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-tier-a { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-tier-f { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-trait { background: #e2e3e5; color: #383d41; }

.recruiting-intel { background-color: #e0f7fa; border-left: 5px solid #006064; padding: 12px; margin-bottom: 10px; border-radius: 4px; }
.bracket-box { background-color: #2c3e50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
.bracket-row { display: flex; justify-content: space-between; padding: 6px; border-bottom: 1px solid #444; }
.news-box { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.news-item { padding: 6px 0; border-bottom: 1px solid #f1f1f1; }
.news-item:last-child { border-bottom: none; }

.small-muted { font-size: 0.85em; color: #666; }
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
    return int((career_stats['w'] * 1) + (career_stats['bowl_w'] * 5) + (career_stats['titles'] * 50) + (prestige * 0.5))

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

# ✅ FIXED VERSION (prevents NameError + handles missing/blank values)
def normalize_shares(shares: dict):
    """
    Normalize a {pos: share} dict into percent shares that sum to 100.
    Safe if shares is missing keys or has None/string/nan values.
    """
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

# ✅ Home field tier system proposal implemented here
def home_field_points(stadium_level: int, is_home: bool) -> float:
    lvl = int(stadium_level)
    if is_home:
        # <7 does nothing; 9+ helps a lot
        if lvl <= 6:
            return 0.0
        if lvl <= 8:
            return 1.0
        if lvl <= 10:
            return 3.0
        return 4.0
    else:
        # small chance of hostile-road effect when opponent stadium is big
        if lvl >= 9 and random.random() < 0.25:
            return -1.5
        if lvl >= 11 and random.random() < 0.25:
            return -2.0
        return 0.0

def engine_play_game(my_rating, opp_rating, staff, schemes, opp_schemes, game_plan, opp_coaches, is_home, is_rival, stadium_level, my_roster):
    """
    A more management-driven engine:
    - Talent gap matters (quadratic form)
    - Scheme matters (counter bonus)
    - Coaching matters (tier bonus)
    - Home field uses tiered system (<7 none, 9+ meaningful)
    - Gameplan affects variance
    """

    # Roster weighted offense/defense (for visuals)
    my_off = (my_roster["QB"] * 0.32) + (my_roster["OL"] * 0.25) + ((my_roster["RB"] + my_roster["WR"]) / 2 * 0.43)
    my_def = (my_roster["DL"] * 0.34) + (my_roster["LB"] * 0.33) + (my_roster["DB"] * 0.33)

    # Talent gap: quadratic makes elite teams feel elite
    talent_gap = (float(my_rating)**2 - float(opp_rating)**2) / 125.0

    # Scheme bonus: counters swing a bit
    scheme_bonus = 0.0
    opp_def = opp_schemes.get("Def", "Man Coverage")
    my_off_s = schemes.get("Off", "Pro Style")
    if COUNTERS.get(opp_def) == my_off_s:
        scheme_bonus += 3.5
    if COUNTERS.get(my_off_s) == opp_def:
        scheme_bonus -= 3.5

    # Coaching net
    my_oc = staff.get("OC", {"off": 3}).get("off", 3)
    my_dc = staff.get("DC", {"def": 3}).get("def", 3)
    opp_oc = opp_coaches.get("OC", 5)
    opp_dc = opp_coaches.get("DC", 5)

    coaching_net = ((get_tier_bonus(my_oc) - get_tier_bonus(opp_dc)) * 1.15) + ((get_tier_bonus(my_dc) - get_tier_bonus(opp_oc)) * 1.15)

    # Trait impacts (small but noticeable)
    hc_trait = staff.get("HC", {}).get("trait", "None")
    if hc_trait == "Tactician":
        coaching_net += 1.25
    if hc_trait == "Recruiter":
        coaching_net += 0.35  # mild in-game leadership bump

    oc_trait = staff.get("OC", {}).get("trait", "None")
    if oc_trait in ["Air Raid", "Smashmouth", "Pro Style"] and oc_trait == my_off_s:
        scheme_bonus += 1.5

    # Home field advantage (tiered)
    hf = home_field_points(stadium_level, is_home)

    # Variance & game plan
    var_mult = 1.0
    if is_rival:
        var_mult *= 1.4
    if game_plan == "Aggressive":
        var_mult *= 1.35
    elif game_plan == "Conservative":
        var_mult *= 0.80

    # Monte Carlo
    sims = []
    for _ in range(120):
        luck = random.gauss(0, 3.1 * var_mult)
        sims.append(talent_gap + scheme_bonus + coaching_net + hf + luck)
    margin = sum(sims) / len(sims)

    # Score considerations: higher spreads generally mean larger win margins
    total_points = int(max(24, min(90, random.gauss(56, 10))))
    spread = max(-28, min(28, margin))

    my_score = int(round((total_points / 2) + (spread / 2)))
    opp_score = int(total_points - my_score)

    my_score = max(0, min(70, my_score))
    opp_score = max(0, min(70, opp_score))

    visual_my_off = int(my_off + get_tier_bonus(my_oc))
    visual_my_def = int(my_def + get_tier_bonus(my_dc))

    return {
        "result": "W" if margin > 0 else "L",
        "score": f"{my_score}-{opp_score}",
        "margin": float(margin),
        "components": {
            "talent_gap": float(talent_gap),
            "scheme_bonus": float(scheme_bonus),
            "coaching_net": float(coaching_net),
            "home_field": float(hf),
            "plan": game_plan
        },
        "stats": {
            "qb_duel": [int(my_roster["QB"]), int(opp_rating)],
            "off_vs_def": [visual_my_off, int(opp_rating + get_tier_bonus(opp_dc))],
            "def_vs_off": [visual_my_def, int(opp_rating + get_tier_bonus(opp_oc))],
            "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"],
            "raw_roster": int((my_off + my_def) / 2)
        }
    }

def engine_evolve_universe(opponents_db):
    for team, data in opponents_db.items():
        wins = int((data["OVR"] / 100) * 12) + random.randint(-2, 2)
        wins = max(0, min(12, wins))

        change = 0
        if wins >= 10:
            change = 3
        elif wins <= 4:
            change = -3
        data["Prestige"] = max(20, min(99, data["Prestige"] + change))

        # simple coaching carousel
        if data["Prestige"] > 80 and wins < 6:
            data["Coaches"] = {"OC": random.randint(7, 9), "DC": random.randint(7, 9)}
        elif data["Prestige"] < 70 and wins > 9:
            data["Coaches"] = {"OC": random.randint(3, 6), "DC": random.randint(3, 6)}

        base_ovr = int(data["Prestige"] * 0.9)
        data["OVR"] = base_ovr + random.randint(-3, 3)
    return opponents_db

def engine_generate_portal_players():
    players = []
    for _ in range(3):
        players.append({"name": generate_name(), "pos": random.choice(POSITIONS), "rating": random.randint(90, 99),
                        "cost": random.randint(3_000_000, 6_000_000), "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(3):
        players.append({"name": generate_name(), "pos": random.choice(POSITIONS), "rating": random.randint(80, 89),
                        "cost": random.randint(1_000_000, 2_500_000), "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(4):
        players.append({"name": generate_name(), "pos": random.choice(POSITIONS), "rating": random.randint(70, 78),
                        "cost": random.randint(150_000, 500_000), "trait": "None", "year": "Jr"})
    return players

# HS outreach -> roster deltas + chance of gems + booster bonus
def process_hs_outreach(total_spend: int, shares_pct: dict, staff: dict, prestige: int, inflation: float, hotspots: dict, home_region: str, team_needs: list):
    """
    total_spend: dollars allocated to HS outreach
    shares_pct: {pos: pct} sums to 100
    returns: {roster_updates, gems, booster_bonus}
    """
    results = {"roster_updates": {}, "gems": [], "booster_bonus": 0, "spent": int(total_spend)}
    total_spend = max(0, int(total_spend))
    scout = staff.get("Scout", {"recruit": 1}).get("recruit", 1)
    hc_trait = staff.get("HC", {}).get("trait", "None")

    # cost efficiency via scout
    efficiency = 0.85 if scout >= 8 else (1.0 if scout >= 5 else 1.15)

    base_cost = 900_000 * float(inflation) * float(efficiency)  # scaling point
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
        dim = (spend_ratio ** 0.85)  # diminishing returns

        change = dim * pipeline_bonus * need_bonus * prestige_factor
        change = max(-4, min(12, change))

        # recruiter trait helps
        if hc_trait == "Recruiter":
            change *= 1.08

        # gem chance
        gem_chance = 0.08
        if pos in team_needs:
            gem_chance += 0.07
        if pos in hot_positions:
            gem_chance += 0.05
        if scout >= 8:
            gem_chance += 0.03
        if hc_trait == "Recruiter":
            gem_chance += 0.02

        if amt > base_cost * 1.25 and random.random() < gem_chance:
            star = generate_star_player(pos, tier=1)
            star["name"] += " (GEM)"
            results["gems"].append(star)
            change += 5
            # booster “we found a dude” money
            results["booster_bonus"] += 250_000 + random.randint(0, 250_000)

        results["roster_updates"][pos] = change

    return results

def generate_nil_prospects(team_needs: list):
    pool = []
    for _ in range(6):
        pos = random.choice(team_needs if team_needs and random.random() < 0.6 else POSITIONS)
        rating = random.randint(86, 97)
        ask = int(random.randint(900_000, 5_500_000) * (1.0 + (rating - 85) / 40))
        pool.append({"name": generate_name(), "pos": pos, "rating": rating, "ask": ask, "trait": random.choice(TRAITS), "year": "Fr"})
    pool.sort(key=lambda x: x["rating"], reverse=True)
    return pool[:5]

def generate_top8_prospects(team_needs: list):
    recruits = []
    for i in range(8):
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
            "status": "OPEN"
        })
    recruits.sort(key=lambda x: x["rating"], reverse=True)
    return recruits

def top8_commit_chance(recruit: dict, spend_by_pos: dict, staff: dict, prestige: int) -> float:
    scout = staff.get("Scout", {"recruit": 1}).get("recruit", 1)
    hc_trait = staff.get("HC", {}).get("trait", "None")

    # baseline
    chance = 0.18

    # prestige is a big lever for elite guys
    chance += (max(40, min(99, prestige)) - 60) * 0.004  # ~ +0.16 across range

    # scout rating helps
    chance += (scout - 5) * 0.02  # scout 9 -> +0.08

    # recruiter trait
    if hc_trait == "Recruiter":
        chance += 0.05

    # position spend helps
    pos = recruit["pos"]
    spend = float(spend_by_pos.get(pos, 0.0))
    chance += min(0.20, spend / 10_000_000)  # $10M on a pos -> +0.20 max

    # clamp
    return max(0.05, min(0.80, chance))


# ==============================================================================
# ZONE 4: STATE + CFP BRACKET
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
        st.session_state.season_simulated = False  # true after Week 12
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
        st.session_state.nil_prospects = []
        st.session_state.hs_total_spend = 0
        st.session_state.hs_shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
        st.session_state.hs_spend_by_pos = {p: 0 for p in POSITIONS}
        st.session_state.top8 = []
        st.session_state.top8_resolved = set()

    # safety defaults
    for k, v in {
        "inflation": 1.0,
        "revenue_report": None,
        "postseason_data": {"Type": None, "Rank": 0, "Round": 0, "Matches": []},
        "team_needs": [],
        "game_plan": "Normal",
        "week_index": 0,
        "news": [],
        "offseason_step": 1,
        "nil_prospects": [],
        "hs_total_spend": 0,
        "hs_shares": {p: 100.0 / len(POSITIONS) for p in POSITIONS},
        "hs_spend_by_pos": {p: 0 for p in POSITIONS},
        "top8": [],
        "top8_resolved": set()
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

def generate_hotspots():
    hotspots = {}
    for reg in REGION_STRENGTH.keys():
        hotspots[reg] = random.sample(POSITIONS, 2)
    return hotspots

def init_playoff_bracket(user_rank, user_team_name):
    # top 12 by OVR, but insert user at rank
    sorted_ai = [(t, d) for t, d in st.session_state.opponents_db.items() if t != user_team_name]
    sorted_ai = sorted(sorted_ai, key=lambda x: x[1]["OVR"], reverse=True)

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

initialize_game_state()


# ==============================================================================
# ZONE 5: UI / FLOW
# ==============================================================================
def run_setup():
    st.title("🏆 College Football Mogul V7")
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

        # Staff
        st.session_state.staff = {}
        for r in ["HC", "OC", "DC", "Scout"]:
            st.session_state.staff[r] = engine_generate_coach(r, tier)

        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}

        # Universe
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

        # Season state
        st.session_state.week_index = 0
        st.session_state.record = {"w": 0, "l": 0}
        st.session_state.season_logs = []
        st.session_state.season_simulated = False

        # Offseason defaults
        st.session_state.offseason_step = 1
        st.session_state.nil_prospects = []
        st.session_state.hs_total_spend = 0
        st.session_state.hs_shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
        st.session_state.hs_spend_by_pos = {p: 0 for p in POSITIONS}
        st.session_state.top8 = []
        st.session_state.top8_resolved = set()

        add_news(f"{team} hires {st.session_state.staff['HC']['name']} as HC.")
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

def show_dashboard():
    thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < thresh:
        st.session_state.game_state = "FIRED"
        st.rerun()

    if st.session_state.revenue_report:
        st.markdown(f"<div class='finance-alert'>💰 FINANCIAL REPORT<br>{st.session_state.revenue_report}</div>", unsafe_allow_html=True)

    sec = st.session_state.job_security
    sec_cls = "security-safe" if sec > 75 else ("security-warm" if sec > 40 else "security-hot")
    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Security: <span class='{sec_cls}'>{sec}%</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 5px; color: white;'><h2>{st.session_state.team_name}</h2></div>", unsafe_allow_html=True)

    # Team OVR
    raw_roster_val = int(sum(st.session_state.roster.values()) / len(POSITIONS))
    curr_ovr = int(
        (st.session_state.roster["QB"] * 0.30) +
        (st.session_state.roster["OL"] * 0.25) +
        ((st.session_state.roster["RB"] + st.session_state.roster["WR"]) / 2 * 0.45) +
        (st.session_state.facilities["Training"] * 0.5)
    )
    st.session_state.team_rating = curr_ovr

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("Team OVR", curr_ovr, f"Raw Talent: {raw_roster_val}")
    c3.metric("Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    c4.metric("Legacy Score", saban, f"Titles: {st.session_state.career_stats['titles']}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Strategy", "Staff", "Facilities", "Season (Weekly)", "Legacy"])

    with tab1:
        c1, c2 = st.columns(2)
        st.session_state.my_schemes["Off"] = c1.selectbox("Offense", SCHEMES["Offense"], index=SCHEMES["Offense"].index(st.session_state.my_schemes.get("Off","Pro Style")))
        st.session_state.my_schemes["Def"] = c2.selectbox("Defense", SCHEMES["Defense"], index=SCHEMES["Defense"].index(st.session_state.my_schemes.get("Def","Man Coverage")))

        st.write("Unit Strength")
        for p, v in st.session_state.roster.items():
            lab = f"{p}: {int(v)}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.progress(min(1.0, v / 100.0), lab)

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
            st.metric("Training", st.session_state.facilities["Training"], delta="OVR Boost")
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

        # Schedule view
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
            for n in st.session_state.news[:8]:
                st.markdown(f"<div class='news-item'>• {n}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='news-item'>• No headlines yet.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # Weekly play controls
        if not st.session_state.season_simulated:
            wk = st.session_state.week_index
            if wk < 12:
                opp = st.session_state.schedule[wk]
                opp_data = st.session_state.opponents_db.get(opp, {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 7})
                is_riv = (opp == st.session_state.team_rival)

                st.subheader(f"Next Game: Week {wk+1} vs {opp} (OVR: {opp_data['OVR']})")
                st.caption(f"Your Stadium Level: {st.session_state.facilities['Stadium']} | Opp Stadium: {opp_data.get('Stadium',7)}")

                if is_riv:
                    st.warning("RIVALRY WEEK: More chaos, bigger stakes!")

                colA, colB = st.columns(2)
                if colA.button("🏈 PLAY WEEK", type="primary"):
                    res = engine_play_game(
                        st.session_state.team_rating,
                        opp_data["OVR"],
                        st.session_state.staff,
                        st.session_state.my_schemes,
                        {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                        st.session_state.game_plan,
                        opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                        is_home=(wk % 2 == 0),
                        is_rival=is_riv,
                        stadium_level=st.session_state.facilities["Stadium"],
                        my_roster=st.session_state.roster
                    )

                    # Save log with more detail
                    st.session_state.season_logs.append({
                        "Week": wk + 1,
                        "Opponent": opp,
                        "Score": f"{res['result']} {res['score']}",
                        "Stats": res["stats"],
                        "Explain": res["components"],
                        "OppOVR": opp_data["OVR"]
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

                    # End of regular season -> pay annual revenue HERE (your request)
                    if st.session_state.week_index >= 12:
                        st.session_state.season_simulated = True
                        rev = engine_calculate_revenue(st.session_state.school_tier, st.session_state.facilities["Marketing"], st.session_state.inflation)
                        st.session_state.budget += rev
                        st.session_state.revenue_report = f"End of Regular Season Payout: +{helper_format_cash(rev)}"
                        add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")

                    st.rerun()

                if colB.button("⏩ SIM REST OF SEASON"):
                    while not st.session_state.season_simulated:
                        wk2 = st.session_state.week_index
                        if wk2 >= 12:
                            st.session_state.season_simulated = True
                            break
                        opp2 = st.session_state.schedule[wk2]
                        opp_data2 = st.session_state.opponents_db.get(opp2, {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 7})
                        is_riv2 = (opp2 == st.session_state.team_rival)

                        res2 = engine_play_game(
                            st.session_state.team_rating,
                            opp_data2["OVR"],
                            st.session_state.staff,
                            st.session_state.my_schemes,
                            {"Off": opp_data2.get("Off", "Pro Style"), "Def": opp_data2.get("Def", "Man Coverage")},
                            st.session_state.game_plan,
                            opp_data2.get("Coaches", {"OC": 5, "DC": 5}),
                            is_home=(wk2 % 2 == 0),
                            is_rival=is_riv2,
                            stadium_level=st.session_state.facilities["Stadium"],
                            my_roster=st.session_state.roster
                        )

                        st.session_state.season_logs.append({
                            "Week": wk2 + 1,
                            "Opponent": opp2,
                            "Score": f"{res2['result']} {res2['score']}",
                            "Stats": res2["stats"],
                            "Explain": res2["components"],
                            "OppOVR": opp_data2["OVR"]
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

                        if st.session_state.week_index >= 12:
                            st.session_state.season_simulated = True

                    rev = engine_calculate_revenue(st.session_state.school_tier, st.session_state.facilities["Marketing"], st.session_state.inflation)
                    st.session_state.budget += rev
                    st.session_state.revenue_report = f"End of Regular Season Payout: +{helper_format_cash(rev)}"
                    add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")
                    st.rerun()

            else:
                st.session_state.season_simulated = True

        # Recap + explanation
        if st.session_state.season_simulated:
            st.write("### Season Results (Recap)")
            for log in st.session_state.season_logs:
                res = "W" if log["Score"].startswith("W") else "L"
                css = "game-card-win" if res == "W" else "game-card-loss"
                s = log["Stats"]
                st.markdown(f"""
                <div class='game-card {css}'>
                    <div class='card-header'><span>{log['Score']}</span><span>vs {log['Opponent']} (OVR {log.get('OppOVR','?')})</span></div>
                    <div class='stat-grid'>
                        <div class='stat-row'><span>🔥 QB Duel</span><span>{s['qb_duel'][0]} vs {s['qb_duel'][1]}</span></div>
                        <div class='stat-row'><span>⚔️ Off vs Def</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div>
                        <div class='stat-row'><span>🛡️ Def vs Off</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div>
                        <div class='stat-row'><span>🧠 Staff</span><span>{s['staff'][0]} vs {s['staff'][1]}</span></div>
                        <div class='stat-row'><span>💪 Raw Talent</span><span>{s['raw_roster']}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Why this result? Week {log['Week']} vs {log['Opponent']}"):
                    e = log.get("Explain", {})
                    st.write(f"Talent gap: **{e.get('talent_gap',0):.2f}**")
                    st.write(f"Scheme bonus: **{e.get('scheme_bonus',0):.2f}**")
                    st.write(f"Coaching net: **{e.get('coaching_net',0):.2f}**")
                    st.write(f"Home field: **{e.get('home_field',0):.2f}**")
                    st.write(f"Gameplan: **{e.get('plan','Normal')}**")

            if st.button("Proceed to Postseason", type="primary"):
                wins = st.session_state.record["w"]
                rank = 130 - (wins * 10)
                rank = max(1, rank)

                if rank <= 12:
                    st.session_state.postseason_data = init_playoff_bracket(rank, st.session_state.team_name)
                else:
                    bowl = get_bowl_name(rank)
                    candidates = [t for t in ALL_TEAMS if t != st.session_state.team_name]
                    opp = random.choice(candidates)
                    st.session_state.postseason_data = {
                        "Type": "BOWL",
                        "Bowl": bowl,
                        "Rank": rank,
                        "Opponent": opp,
                        "OppData": st.session_state.opponents_db.get(opp, {"OVR": 85, "Off":"Pro Style","Def":"Man Coverage","Coaches":{"OC":5,"DC":5},"Stadium":8})
                    }

                st.session_state.game_state = "POSTSEASON"
                st.rerun()

    with tab5:
        st.subheader("🏛️ Trophy Case")
        cs = st.session_state.career_stats
        st.write(f"**Titles:** {cs['titles']}  |  **Bowl W-L:** {cs['bowl_w']}-{cs['bowl_l']}  |  **Career W-L:** {cs['w']}-{cs['l']}")
        st.write(f"**Current Prestige:** {st.session_state.prestige}")
        st.write(f"**Legacy (Saban) Score:** {calculate_saban_score(cs, st.session_state.prestige)}")
        st.divider()
        st.subheader("📚 Season History")
        if st.session_state.history:
            st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
        else:
            st.info("No completed seasons yet. Win some hardware!")


def show_postseason():
    st.title("Postseason Hub")
    data = st.session_state.postseason_data

    if data.get("Type") == "BOWL":
        st.markdown(f"<div class='bracket-box'><h3>{data['Bowl']}</h3><h1>VS {data['Opponent']}</h1></div>", unsafe_allow_html=True)
        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            opp_data = data["OppData"]
            res = engine_play_game(
                st.session_state.team_rating,
                opp_data["OVR"],
                st.session_state.staff,
                st.session_state.my_schemes,
                {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                st.session_state.game_plan,
                opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                is_home=False,
                is_rival=False,
                stadium_level=st.session_state.facilities["Stadium"],
                my_roster=st.session_state.roster
            )

            wins = st.session_state.record["w"] + (1 if res["result"] == "W" else 0)
            losses = st.session_state.record["l"] + (1 if res["result"] == "L" else 0)

            if res["result"] == "W":
                st.session_state.budget += 2_000_000
                st.session_state.career_stats["bowl_w"] += 1
                add_news(f"{st.session_state.team_name} wins {data['Bowl']}! ({res['score']})")
                st.toast("🎳 BOWL WIN BONUS: $2M")
            else:
                st.session_state.career_stats["bowl_l"] += 1
                add_news(f"{st.session_state.team_name} falls in {data['Bowl']} ({res['score']})")

            # expectation booster effect
            delta = wins - st.session_state.expected_wins
            if delta > 0:
                st.session_state.budget += delta * 1_000_000
            elif delta < 0:
                st.session_state.budget -= abs(delta) * 500_000

            # end season record snapshot
            hist = {"Year": st.session_state.year, "Record": f"{wins}-{losses}", "Rank": f"#{data['Rank']}", "Bowl": data["Bowl"]}
            st.session_state.history.append(hist)

            st.session_state.game_state = "OFFSEASON"
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

        # find user match
        user_match = None
        for m in data["Matches"]:
            if m["t1"] == st.session_state.team_name or m["t2"] == st.session_state.team_name:
                user_match = m
                break

        if data.get("UserAlive") and user_match:
            opp = user_match["t2"] if user_match["t1"] == st.session_state.team_name else user_match["t1"]
            opp_data = st.session_state.opponents_db.get(opp, {"OVR": 88, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": 9})

            st.info(f"Your Matchup: vs {opp} (OVR: {opp_data['OVR']})")
            if st.button("PLAY PLAYOFF GAME 🏈", type="primary"):
                res = engine_play_game(
                    st.session_state.team_rating,
                    opp_data["OVR"],
                    st.session_state.staff,
                    st.session_state.my_schemes,
                    {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                    st.session_state.game_plan,
                    opp_data.get("Coaches", {"OC": 5, "DC": 5}),
                    is_home=False,
                    is_rival=False,
                    stadium_level=st.session_state.facilities["Stadium"],
                    my_roster=st.session_state.roster
                )

                next_round_teams = []

                # resolve all matches this round
                for m in data["Matches"]:
                    if m is user_match:
                        if res["result"] == "W":
                            m["winner"] = st.session_state.team_name
                            next_round_teams.append(st.session_state.team_name)
                            add_news(f"{st.session_state.team_name} advances in the CFP!")
                            st.toast("VICTORY! Advancing...")
                        else:
                            m["winner"] = opp
                            next_round_teams.append(opp)
                            st.session_state.postseason_data["UserAlive"] = False
                            add_news(f"{st.session_state.team_name} is eliminated by {opp}.")
                            st.error(f"Eliminated by {opp}")
                    else:
                        # AI sim uses OVR weighting (fixes random-feel)
                        t1 = m["t1"]
                        t2 = m["t2"]
                        o1 = st.session_state.opponents_db.get(t1, {"OVR": 82})["OVR"] if t1 != st.session_state.team_name else st.session_state.team_rating
                        o2 = st.session_state.opponents_db.get(t2, {"OVR": 82})["OVR"] if t2 != st.session_state.team_name else st.session_state.team_rating
                        p = o1 / max(1.0, (o1 + o2))
                        winner = t1 if random.random() < p else t2
                        m["winner"] = winner
                        next_round_teams.append(winner)

                time.sleep(0.8)

                if st.session_state.postseason_data["UserAlive"]:
                    if data["Round"] == 4:
                        st.session_state.budget += 50_000_000
                        st.session_state.career_stats["titles"] += 1
                        st.balloons()
                        st.success("NATIONAL CHAMPIONS!")
                        add_news(f"{st.session_state.team_name} wins the NATIONAL TITLE!")
                        hist = {"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Bowl": "National Title"}
                        st.session_state.history.append(hist)

                        st.session_state.game_state = "OFFSEASON"
                        st.session_state.offseason_step = 1
                        st.rerun()
                    else:
                        # build next round bracket
                        new_matches = []
                        if data["Round"] == 1:
                            seeds = data["QF_Seeds"]
                            for i in range(4):
                                new_matches.append({"t1": seeds[i], "t2": next_round_teams[3 - i], "winner": None})
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
                    st.session_state.game_state = "OFFSEASON"
                    st.session_state.offseason_step = 1
                    st.rerun()
        else:
            st.info("You are no longer alive in the bracket (or you had a BYE).")
            if st.button("Continue to Offseason", type="primary"):
                st.session_state.game_state = "OFFSEASON"
                st.session_state.offseason_step = 1
                st.rerun()


def show_offseason():
    st.title("Offseason Hub")
    st.markdown(f"<div class='nil-alert'>💰 Offseason Budget: {helper_format_cash(st.session_state.budget)}</div>", unsafe_allow_html=True)

    steps = ["1) NIL Prospects", "2) HS Outreach", "3) Top-8 Battles", "Finish Offseason"]
    st.session_state.offseason_step = st.radio(
        "Offseason Steps",
        [1, 2, 3, 4],
        format_func=lambda x: steps[x-1],
        index=max(0, min(3, int(st.session_state.offseason_step)-1))
    )

    if st.session_state.offseason_step == 1:
        show_offseason_nil()

    elif st.session_state.offseason_step == 2:
        show_offseason_hs_outreach()

    elif st.session_state.offseason_step == 3:
        show_offseason_top8()

    else:
        st.subheader("✅ Wrap Up Offseason")
        st.write("This will advance the year, evolve the universe, reset the season schedule, and return to Dashboard.")
        if st.button("Advance to Next Season", type="primary"):
            # Clear rental flags (portal guys wear off after a year)
            for p in POSITIONS:
                st.session_state.active_transfers[p] = False

            # evolve universe
            st.session_state.opponents_db = engine_evolve_universe(st.session_state.opponents_db)

            # advance year
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.inflation *= 1.05

            # new needs
            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)

            # reset season state
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)
            st.session_state.hotspots = generate_hotspots()
            st.session_state.week_index = 0
            st.session_state.record = {"w": 0, "l": 0}
            st.session_state.season_logs = []
            st.session_state.season_simulated = False

            # reset offseason artifacts
            st.session_state.nil_prospects = []
            st.session_state.hs_total_spend = 0
            st.session_state.hs_shares = {p: 100.0 / len(POSITIONS) for p in POSITIONS}
            st.session_state.hs_spend_by_pos = {p: 0 for p in POSITIONS}
            st.session_state.top8 = []
            st.session_state.top8_resolved = set()

            add_news(f"New season begins. Needs: {', '.join(st.session_state.team_needs)}.")
            st.session_state.game_state = "DASHBOARD"
            st.rerun()

def show_offseason_nil():
    st.subheader("1) NIL Prospects")
    needs = st.session_state.get("team_needs", [])

    if not st.session_state.nil_prospects:
        st.session_state.nil_prospects = generate_nil_prospects(needs)

    st.markdown(f"<div class='recruiting-intel'>Team Needs: <b>{', '.join(needs)}</b></div>", unsafe_allow_html=True)
    st.write("Sign 0–5 NIL prospects. These are immediate roster upgrades, but expensive.")

    for i, p in enumerate(list(st.session_state.nil_prospects)):
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"⭐ {p['pos']} {p['name']} ({p['rating']}) — {p['trait']}")
        c2.write(f"NIL Ask: {helper_format_cash(p['ask'])}")
        if c3.button("Sign", key=f"nil_{i}"):
            if st.session_state.budget >= p["ask"]:
                st.session_state.budget -= p["ask"]
                st.session_state.roster[p["pos"]] = max(st.session_state.roster[p["pos"]], p["rating"])
                add_news(f"{st.session_state.team_name} lands NIL prospect {p['pos']} {p['name']} ({p['rating']}).")
                st.session_state.nil_prospects.pop(i)
                st.rerun()
            else:
                st.error("Not enough budget.")

    if st.button("Refresh Prospects (Free)"):
        st.session_state.nil_prospects = generate_nil_prospects(needs)
        st.rerun()

def show_offseason_hs_outreach():
    st.subheader("2) HS Outreach (Fast Input)")
    st.write("Pick a **total HS outreach spend** once, then allocate by position using % sliders (auto-normalized).")

    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    needs = st.session_state.get("team_needs", [])
    st.markdown(f"<div class='recruiting-intel'>Pipeline Bonus ({st.session_state.home_region}): {', '.join(hot)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='recruiting-intel'>Team Needs: <b>{', '.join(needs)}</b></div>", unsafe_allow_html=True)

    max_spend = max(0, int(st.session_state.budget))
    st.session_state.hs_total_spend = st.slider(
        "Total HS Outreach Spend",
        min_value=0,
        max_value=max_spend,
        value=min(int(st.session_state.hs_total_spend), max_spend),
        step=100_000
    )

    # Start from stored shares
    shares = dict(st.session_state.hs_shares)

    st.write("### Allocate % by Position (we auto-normalize to 100%)")
    cols = st.columns(2)
    for idx, pos in enumerate(POSITIONS):
        with cols[idx % 2]:
            default = float(shares.get(pos, 100.0 / len(POSITIONS)))
            shares[pos] = st.slider(
                f"{pos} %{' (NEED)' if pos in needs else ''}",
                min_value=0.0,
                max_value=60.0,
                value=float(max(0.0, min(60.0, default))),
                step=1.0,
                key=f"hs_pct_{pos}"
            )

    # ✅ normalize (this is where your previous crash was happening)
    shares = normalize_shares(shares)
    st.session_state.hs_shares = shares

    # compute spend-by-pos
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

        res = process_hs_outreach(
            total_spend=st.session_state.hs_total_spend,
            shares_pct=shares,
            staff=st.session_state.staff,
            prestige=st.session_state.prestige,
            inflation=st.session_state.inflation,
            hotspots=st.session_state.hotspots,
            home_region=st.session_state.home_region,
            team_needs=needs
        )

        # apply spend
        st.session_state.budget -= res["spent"]

        # apply booster bonus
        if res["booster_bonus"] > 0:
            st.session_state.budget += res["booster_bonus"]
            st.toast(f"💎 Booster bonus: {helper_format_cash(res['booster_bonus'])}")
            add_news("Boosters celebrate a surprise GEM discovery!")

        # apply roster updates (small decay + gain)
        for p, g in res["roster_updates"].items():
            loss = random.randint(1, 4)
            st.session_state.roster[p] = max(40, min(99, int(st.session_state.roster[p] - loss + g)))

        # add gems as stars
        if res["gems"]:
            st.session_state.stars.extend(res["gems"])
            add_news(f"Recruiting staff finds {len(res['gems'])} GEM(s)!")

        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
        add_news("HS outreach completed. Rankings buzz increases.")
        st.success("HS Outreach complete! Your roster has been updated.")
        st.rerun()

def show_offseason_top8():
    st.subheader("3) Top-8 Prospect Battles")
    st.write("These are elite recruits. **Coach quality, scout quality, prestige, and HS spend in that position** all matter. Winning a battle can also trigger booster money.")

    needs = st.session_state.get("team_needs", [])
    if not st.session_state.top8:
        st.session_state.top8 = generate_top8_prospects(needs)
        st.session_state.top8_resolved = set()

    spend_by_pos = st.session_state.get("hs_spend_by_pos", {p: 0 for p in POSITIONS})

    st.markdown(f"<div class='recruiting-intel'>Your leverage comes from: Prestige, Scout rating, Recruiter trait, and HS spend by position.</div>", unsafe_allow_html=True)

    for r in st.session_state.top8:
        rid = r["id"]
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])

        c1.write(f"🏅 {r['pos']} {r['name']} ({r['rating']}) — {r['trait']}")
        c2.write(f"Ask: {helper_format_cash(r['ask'])}")

        chance = top8_commit_chance(r, spend_by_pos, st.session_state.staff, st.session_state.prestige)
        c3.write(f"Chance: {int(chance*100)}%")

        already = rid in st.session_state.top8_resolved
        if already:
            c4.write("✅ Done")
            continue

        if c4.button("Pitch", key=f"pitch_{rid}"):
            # pitching costs some money (NIL + travel)
            pitch_cost = int(max(250_000, r["ask"] * 0.10))
            if st.session_state.budget < pitch_cost:
                st.error("Not enough budget to pitch this recruit.")
                continue

            st.session_state.budget -= pitch_cost

            if random.random() < chance:
                # commit
                st.session_state.roster[r["pos"]] = max(st.session_state.roster[r["pos"]], r["rating"])
                st.session_state.stars.append({
                    "id": rid, "name": r["name"], "pos": r["pos"], "rating": r["rating"], "year": "Fr", "trait": r["trait"]
                })
                # booster bonus on elite commits
                booster = int(random.randint(500_000, 3_500_000) * (1.0 + (r["rating"] - 90) / 25))
                st.session_state.budget += booster
                add_news(f"{st.session_state.team_name} lands TOP-8 recruit {r['pos']} {r['name']} ({r['rating']})! Boosters donate {helper_format_cash(booster)}.")
                st.success(f"COMMIT! Boosters donate {helper_format_cash(booster)}.")
            else:
                add_news(f"{st.session_state.team_name} loses a Top-8 battle for {r['pos']} {r['name']}.")
                st.warning("Missed! Another school won this battle.")

            st.session_state.top8_resolved.add(rid)
            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
            st.rerun()

    st.divider()
    remaining = 8 - len(st.session_state.top8_resolved)
    st.write(f"Battles remaining: **{remaining}**")
    if remaining == 0:
        st.success("Top-8 battles completed. You can finish the offseason now.")


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
if st.session_state.game_state == "SETUP":
    run_setup()
elif st.session_state.game_state == "FIRED":
    show_fired()
elif st.session_state.game_state == "DASHBOARD":
    show_dashboard()
elif st.session_state.game_state == "POSTSEASON":
    show_postseason()
elif st.session_state.game_state == "OFFSEASON":
    show_offseason()
elif st.session_state.game_state == "RETIREMENT":
    show_retirement()
else:
    # Fallback to dashboard
    st.session_state.game_state = "DASHBOARD"
    st.rerun()
