import streamlit as st
import random
import time
import pandas as pd

# ==============================================================================
# College Football Mogul V4
# UI/UX upgrades implemented:
# 1) Offseason Hub w/ progress + gating
# 2) Top-8 battle commit odds meter (You vs 2 competitors)
# 3) Postseason bracket UI upgraded (seeds + OVR chips + separate sim buttons)
# 4) Prospect cards w/ filters + sorting
# 5) Game log expanders w/ full calc breakdown (talent/scheme/coaching/home/luck)
# ==============================================================================

try:
    st.set_page_config(page_title="College Football Mogul V4", page_icon="🏈", layout="wide")
except Exception:
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
.finance-alert { background-color: #d1e7dd; color: #0f5132; border: 1px solid #badbcc; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: bold; }
.nil-alert { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-size: 1.1em; font-weight: bold; }

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
.small-muted { font-size:0.85em; color:#666; }

/* Recruiting */
.recruiting-intel { background-color: #e0f7fa; border-left: 5px solid #006064; padding: 15px; margin-bottom: 20px; border-radius: 4px; }
.prospect-card { border:1px solid #ddd; border-radius:10px; padding:12px; background:#fff; margin-bottom:10px; }
.prospect-title { font-weight:800; font-size:1.05em; }

/* Bracket */
.bracket-box { background-color: #2c3e50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
.bracket-row { display: flex; justify-content: space-between; padding: 8px 10px; border-bottom: 1px solid #444; }
.seed-chip { background:#111827; color:white; border-radius:999px; padding:2px 10px; font-size:0.8em; }
.ovr-chip { background:#f3f4f6; color:#111827; border-radius:999px; padding:2px 10px; font-size:0.8em; border:1px solid #e5e7eb; }
.team-chip { display:flex; gap:8px; align-items:center; }
</style>
""", unsafe_allow_html=True)

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
COACH_TRAITS = {"None": "None", "Recruiter": "+10% Recruiting", "Tactician": "+3 Game Boost",
                "Air Raid": "+2 Scheme", "Smashmouth": "+2 Scheme", "Pro Style": "+2 Scheme"}
BOWL_MAPPING = {
    "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
    "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"],
    "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"],
    "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"],
}

TEAMS_DB = {
    "Georgia": {"color": "#BA0C2F"}, "Alabama": {"color": "#9E1B32"}, "Ohio State": {"color": "#BB0000"},
    "Michigan": {"color": "#00274C"}, "Texas": {"color": "#BF5700"}, "Oklahoma": {"color": "#841617"},
    "Oregon": {"color": "#154733"}, "Washington": {"color": "#4B2E83"}, "Florida St": {"color": "#782F40"},
    "Miami": {"color": "#005030"}, "Penn State": {"color": "#041E42"}, "Notre Dame": {"color": "#0C2340"},
    "LSU": {"color": "#461D7C"}, "Ole Miss": {"color": "#CE1126"}, "Tennessee": {"color": "#FF8200"},
    "Auburn": {"color": "#0C2340"}, "Indiana": {"color": "#990000"}, "Purdue": {"color": "#CEB888"},
    "Colorado": {"color": "#CFB87C"}, "USC": {"color": "#990000"}, "Boise State": {"color": "#0033A0"},
    "San Jose State": {"color": "#0055A2"},
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
    "Tulane": {"Prestige": 74, "Talent": 77, "Tier": 3, "Rival": "LSU"},
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
def helper_format_cash(amount: int) -> str:
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
    if val >= 8: return "A"
    if val >= 7: return "B"
    if val >= 5: return "C"
    if val >= 3: return "D"
    return "F"


def get_bowl_name(rank: int) -> str:
    if rank <= 12: return "CFP Playoff"
    if rank <= 25: return random.choice(BOWL_MAPPING["Elite"])
    if rank <= 40: return random.choice(BOWL_MAPPING["High"])
    if rank <= 80: return random.choice(BOWL_MAPPING["Mid"])
    return random.choice(BOWL_MAPPING["Low"])


def generate_star_player(position, tier):
    return {"id": random.randint(10000, 99999), "name": generate_name(), "pos": position,
            "rating": min(99, 85 + random.randint(0, 10)), "year": "Fr", "trait": random.choice(TRAITS)}


def generate_ga_coach(role):
    return {"name": f"GA {generate_name()}", "role": role, "off": random.randint(1, 3),
            "def": random.randint(1, 3), "recruit": random.randint(1, 2), "trait": "None",
            "salary": 50000, "history": "Former Player", "scouted": True}


# ==============================================================================
# ENGINE
# ==============================================================================
def engine_calculate_revenue(tier, marketing_lvl, inflation):
    if not tier: tier = 3
    base = {1: 40_000_000, 2: 25_000_000, 3: 10_000_000, 4: 5_000_000}.get(tier, 5_000_000)
    marketing_bonus = marketing_lvl * 2_000_000
    return int((base + marketing_bonus) * inflation)


def engine_generate_coach(role, tier):
    cost = random.randint(4_000_000, 8_000_000) if tier == 1 else random.randint(500_000, 3_500_000)
    trait_pool = list(COACH_TRAITS.keys())
    if role == "OC":
        trait_pool = ["Air Raid", "Smashmouth", "Pro Style", "Recruiter", "Tactician"]
    base = 8 if tier == 1 else (5 if tier == 2 else 1)
    return {"name": generate_coach_name(), "role": role,
            "off": min(10, base + random.randint(0, 3)),
            "def": min(10, base + random.randint(0, 3)),
            "recruit": min(10, base + random.randint(0, 3)),
            "trait": random.choice(trait_pool),
            "salary": cost, "history": "External Hire", "scouted": False}


def engine_generate_roster(tier, base_ovr=None):
    base = base_ovr if base_ovr else (90 if tier == 1 else 74)
    return {p: min(99, max(40, base + random.randint(-4, 4))) for p in POSITIONS}


def engine_generate_schedule(my_team, my_conf, rival):
    conf_foes = [t for t in CONFERENCES.get(my_conf, CONFERENCES['G5']) if t != my_team]
    schedule = random.sample(conf_foes, 8) if len(conf_foes) >= 8 else list(conf_foes)

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


def engine_play_game(my_rating, opp_rating, staff, schemes, opp_schemes, game_plan, opp_coaches, is_home, is_rival, fac_lvl, my_roster):
    # Unit strength
    my_off = (my_roster["QB"] * 0.30) + (my_roster["OL"] * 0.25) + (((my_roster["RB"] + my_roster["WR"]) / 2) * 0.45)
    my_def = sum(my_roster[p] for p in ["DL", "LB", "DB"]) / 3

    # Talent gap
    talent_gap = (my_rating**2 - opp_rating**2) / 125.0

    # Scheme chess
    scheme_bonus = 0
    if COUNTERS.get(opp_schemes['Def']) == schemes['Off']:
        scheme_bonus += 4
    elif COUNTERS.get(schemes['Off']) == opp_schemes['Def']:
        scheme_bonus -= 4

    # Coaching
    my_oc = staff.get('OC', {'off': 3}).get('off', 3)
    my_dc = staff.get('DC', {'def': 3}).get('def', 3)
    opp_oc = opp_coaches.get('OC', 5)
    opp_dc = opp_coaches.get('DC', 5)

    def tier_bonus(r):
        if r >= 8: return 3
        if r <= 4: return -3
        return 0

    coaching_net = ((tier_bonus(my_oc) - tier_bonus(opp_dc)) * 1.1) + ((tier_bonus(my_dc) - tier_bonus(opp_oc)) * 1.1)

    # Environment & variance
    home_bonus = 3 if (is_home and fac_lvl > 8) else (-3 if (not is_home and random.random() < 0.30) else 0)
    var_mult = 2.0 if is_rival else 1.0
    if game_plan == "Aggressive":
        var_mult *= 1.5

    sims = []
    luck_samples = []
    for _ in range(100):
        luck = random.gauss(0, 3.0 * var_mult)
        luck_samples.append(luck)
        sims.append(talent_gap + scheme_bonus + coaching_net + home_bonus + luck)

    margin = sum(sims) / len(sims)

    my_score = int(28 + (margin / 1.5)) if margin > 0 else int(24 + (margin / 1.5))
    opp_score = int(my_score - margin)

    visual_my_off = int(my_off + tier_bonus(my_oc))
    visual_my_def = int(my_def + tier_bonus(my_dc))

    breakdown = {
        "my_rating": my_rating,
        "opp_rating": opp_rating,
        "talent_gap": talent_gap,
        "scheme_bonus": scheme_bonus,
        "coaching_net": coaching_net,
        "home_bonus": home_bonus,
        "luck_avg": sum(luck_samples)/len(luck_samples),
        "var_mult": var_mult,
        "my_oc": my_oc,
        "my_dc": my_dc,
        "opp_oc": opp_oc,
        "opp_dc": opp_dc,
        "my_off_unit": my_off,
        "my_def_unit": my_def,
    }

    return {
        "result": "W" if margin > 0 else "L",
        "score": f"{max(0, my_score)}-{max(0, opp_score)}",
        "stats": {
            "qb_duel": [int(my_roster["QB"]), int(opp_rating)],
            "off_vs_def": [visual_my_off, int(opp_rating + tier_bonus(opp_dc))],
            "def_vs_off": [visual_my_def, int(opp_rating + tier_bonus(opp_oc))],
            "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"],
            "raw_roster": int((my_off + my_def) / 2),
            "scheme": [schemes["Off"], opp_schemes["Def"]],
        },
        "breakdown": breakdown
    }


def engine_evolve_universe(opponents_db):
    for _, data in opponents_db.items():
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
    return opponents_db


def engine_generate_portal_players():
    players = []
    for _ in range(3):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(90, 99),
                        "cost": random.randint(3_000_000, 6_000_000), "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(3):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(80, 89),
                        "cost": random.randint(1_000_000, 2_500_000), "trait": random.choice(TRAITS), "year": "Sr"})
    for _ in range(4):
        players.append({"name": f"{generate_name()}", "pos": random.choice(POSITIONS), "rating": random.randint(70, 78),
                        "cost": random.randint(150_000, 500_000), "trait": "None", "year": "Jr"})
    return players


# ==============================================================================
# Recruiting Boards + Processing
# ==============================================================================
def generate_nil_board(num=10):
    board = []
    for _ in range(num):
        pos = random.choice(POSITIONS)
        rating = random.randint(84, 98)
        ask = int(random.randint(800_000, 5_000_000) * st.session_state.inflation)
        board.append({
            "id": random.randint(10000, 99999),
            "name": generate_name(),
            "pos": pos,
            "rating": rating,
            "trait": random.choice(TRAITS),
            "ask": ask,
            "status": "Open",
            "notes": random.choice(["Early enrollee", "Wants playing time", "Big NIL market", "Wants winning culture", "Family ties"])
        })
    return board


def generate_top8_battles():
    battles = []
    for i in range(8):
        pos = random.choice(POSITIONS)
        rating = random.randint(92, 99)
        ask = int(random.randint(2_500_000, 10_000_000) * st.session_state.inflation)
        rivals = random.sample([t for t in ALL_TEAMS if t != st.session_state.team_name], 2)
        battles.append({
            "id": random.randint(10000, 99999),
            "rank": i + 1,
            "name": generate_name(),
            "pos": pos,
            "rating": rating,
            "ask": ask,
            "trait": random.choice(TRAITS),
            "competitors": rivals,
            "status": "Open",
        })
    return battles


def process_outreach(budget, allocations, staff, prestige, inflation):
    cost = sum(allocations.values())
    if cost > budget:
        return None

    results = {"roster_updates": {}, "gems": [], "cost": cost, "booster_bonus": 0}
    scout_rate = staff.get('Scout', {'recruit': 1}).get('recruit', 1)
    hc_trait = staff.get('HC', {'trait': 'None'}).get('trait', 'None')
    recruiter_boost = 1.10 if hc_trait == "Recruiter" else 1.0

    cost_mult = 1.2
    if scout_rate >= 8: cost_mult = 0.8
    elif scout_rate >= 5: cost_mult = 1.0

    base_cost = 800_000 * inflation * cost_mult
    home_region = st.session_state.home_region
    hot_positions = st.session_state.hotspots.get(home_region, [])

    for pos, amount in allocations.items():
        if amount < base_cost * 0.5:
            change = -random.randint(2, 6)
        else:
            pipeline_bonus = 1.15 if pos in hot_positions else 1.0
            change = (amount / base_cost) * pipeline_bonus * recruiter_boost

            gem_chance = 0.08 + (0.01 * scout_rate)
            if amount > base_cost * 1.2 and random.random() < gem_chance:
                change += 5
                new_star = generate_star_player(pos, 1)
                new_star['name'] += " (GEM)"
                results["gems"].append(new_star)
                results["booster_bonus"] += int(250_000 * inflation)

        results["roster_updates"][pos] = change

    return results


# ==============================================================================
# Postseason Helpers
# ==============================================================================
def init_playoff_bracket(user_rank, user_team_name):
    sorted_ai = sorted(st.session_state.opponents_db.items(), key=lambda x: x[1]['OVR'], reverse=True)
    top_12 = []
    ai_idx = 0
    for r in range(1, 13):
        if r == user_rank:
            top_12.append(user_team_name)
        else:
            top_12.append(sorted_ai[ai_idx][0])
            ai_idx += 1

    r1_matches = [
        {"seed1": 5, "seed2": 12, "t1": top_12[4], "t2": top_12[11], "winner": None},
        {"seed1": 6, "seed2": 11, "t1": top_12[5], "t2": top_12[10], "winner": None},
        {"seed1": 7, "seed2": 10, "t1": top_12[6], "t2": top_12[9], "winner": None},
        {"seed1": 8, "seed2": 9,  "t1": top_12[7], "t2": top_12[8], "winner": None},
    ]
    qf_seeds = [top_12[0], top_12[1], top_12[2], top_12[3]]
    qf_seed_nums = [1, 2, 3, 4]
    return {
        "Type": "CFP", "Round": 1, "Matches": r1_matches,
        "Seeds": top_12, "QF_Seeds": qf_seeds, "QF_SeedNums": qf_seed_nums,
        "UserAlive": True, "UserRank": user_rank
    }


def team_ovr(team):
    if team == st.session_state.team_name:
        return st.session_state.team_rating
    return st.session_state.opponents_db.get(team, {"OVR": 80}).get("OVR", 80)


def weighted_game_winner(t1, t2):
    o1 = team_ovr(t1)
    o2 = team_ovr(t2)
    delta = o1 - o2
    p = 0.50 + (delta * 0.015)
    p = max(0.15, min(0.85, p))
    return t1 if random.random() < p else t2


# ==============================================================================
# STATE
# ==============================================================================
def generate_hotspots():
    return {reg: random.sample(POSITIONS, 2) for reg in REGION_STRENGTH.keys()}


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
        st.session_state.portal_players = []
        st.session_state.candidates = {}
        st.session_state.postseason_data = {"Type": None, "Rank": 0, "Round": 0, "Matches": []}
        st.session_state.revenue_report = None
        st.session_state.inflation = 1.0

        # Offseason pipeline
        st.session_state.offseason = {
            "nil_board": [],
            "nil_signed": [],
            "outreach_done": False,
            "top8_board": [],
            "top8_signed": [],
            "completed": False,
        }

    if 'offseason' not in st.session_state:
        st.session_state.offseason = {"nil_board": [], "nil_signed": [], "outreach_done": False, "top8_board": [], "top8_signed": [], "completed": False}
    if 'inflation' not in st.session_state:
        st.session_state.inflation = 1.0


initialize_game_state()

# ==============================================================================
# OFFSEASON HUB + GATING
# ==============================================================================
def kickoff_offseason():
    st.session_state.offseason = {
        "nil_board": generate_nil_board(num=10),
        "nil_signed": [],
        "outreach_done": False,
        "top8_board": generate_top8_battles(),
        "top8_signed": [],
        "completed": False,
    }
    st.session_state.game_state = "OFFSEASON_HUB"


def recruiting_power_score():
    scout = st.session_state.staff.get("Scout", {"recruit": 3}).get("recruit", 3)
    hc = st.session_state.staff.get("HC", {"recruit": 3, "trait": "None"})
    hc_rec = hc.get("recruit", 3)
    trait = hc.get("trait", "None")
    trait_bonus = 0.10 if trait == "Recruiter" else 0.0
    base = (0.35 * (scout / 10)) + (0.35 * (hc_rec / 10)) + (0.30 * (st.session_state.prestige / 100))
    return min(1.25, base + trait_bonus)


def show_offseason_hub():
    st.title("🧭 Offseason Hub")
    st.write(f"Budget: **{helper_format_cash(st.session_state.budget)}** • Prestige: **{st.session_state.prestige}** • Inflation: **{st.session_state.inflation:.2f}**")

    nil_done = len(st.session_state.offseason.get("nil_signed", [])) > 0 or all(p["status"] != "Open" for p in st.session_state.offseason.get("nil_board", []))
    outreach_done = st.session_state.offseason.get("outreach_done", False)
    top8_done = len(st.session_state.offseason.get("top8_signed", [])) > 0 or all(p["status"] != "Open" for p in st.session_state.offseason.get("top8_board", []))

    progress = (1 if nil_done else 0) + (1 if outreach_done else 0) + (1 if top8_done else 0)
    st.progress(progress / 3.0, text=f"Offseason progress: {progress}/3 steps")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 1) NIL Prospects")
        st.caption("Sign up to 3 NIL targets.")
        if st.button("Enter NIL", type="primary", key="hub_nil"):
            st.session_state.game_state = "OFFSEASON_NIL"
            st.rerun()

    with c2:
        st.markdown("### 2) Outreach")
        st.caption("Spend by position, find gems, earn booster $.")
        if st.button("Enter Outreach", disabled=not nil_done, type="primary", key="hub_outreach"):
            st.session_state.game_state = "OFFSEASON_OUTREACH"
            st.rerun()
        if not nil_done:
            st.info("Locked until NIL step is done (sign or resolve the board).")

    with c3:
        st.markdown("### 3) Top-8 Battles")
        st.caption("Battle for elite recruits; coaches & scouts matter.")
        if st.button("Enter Top-8", disabled=not outreach_done, type="primary", key="hub_top8"):
            st.session_state.game_state = "OFFSEASON_TOP8"
            st.rerun()
        if not outreach_done:
            st.info("Locked until Outreach is finalized.")

    st.divider()
    if st.button("Finish Offseason → Start Next Season", disabled=not (nil_done and outreach_done and top8_done), type="primary"):
        advance_to_next_year()
        st.rerun()


def advance_to_next_year():
    st.session_state.opponents_db = engine_evolve_universe(st.session_state.opponents_db)
    st.session_state.year += 1
    st.session_state.tenure += 1
    st.session_state.inflation *= 1.05
    st.session_state.season_simulated = False
    st.session_state.schedule = []
    st.session_state.hotspots = generate_hotspots()
    st.session_state.postseason_data = {"Type": None, "Rank": 0, "Round": 0, "Matches": []}
    st.session_state.revenue_report = None
    st.session_state.offseason["completed"] = True
    st.session_state.game_state = "DASHBOARD"


# ==============================================================================
# UI: SETUP
# ==============================================================================
def run_setup():
    st.title("🏆 College Football Mogul V4")
    st.markdown("### Dynasty Mode (Jan 2026)")
    c1, c2 = st.columns(2)
    name = c1.text_input("AD Name", "Coach Prime")
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"])

    sorted_teams = sorted(REAL_WORLD_INIT.keys()) + sorted([t for t in ALL_TEAMS if t not in REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)

    if team in REAL_WORLD_INIT:
        d = REAL_WORLD_INIT[team]
        tier = d['Tier']
        budget = 25_000_000 if tier == 1 else (15_000_000 if tier == 2 else 5_000_000)
        conf = "SEC" if team in CONFERENCES["SEC"] else ("Big Ten" if team in CONFERENCES["Big Ten"] else "G5")
        rival = d.get('Rival', 'Rival')
    else:
        tier, budget, conf, rival = 3, 5_000_000, "G5", "Rival"
        for c, t_list in CONFERENCES.items():
            if team in t_list:
                conf = c

    expect = 10 if tier == 1 else (8 if tier == 2 else (6 if tier == 3 else 4))
    st.info(f"**{team}** | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival}")
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

        for r in ["HC", "OC", "DC", "Scout"]:
            st.session_state.staff[r] = engine_generate_coach(r, tier)

        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}

        for opp in ALL_TEAMS:
            if opp in REAL_WORLD_INIT:
                data = REAL_WORLD_INIT[opp]
                st.session_state.opponents_db[opp] = {
                    "Prestige": data['Prestige'],
                    "OVR": data['Talent'],
                    "Off": random.choice(list(SCHEMES["Offense"])),
                    "Def": random.choice(list(SCHEMES["Defense"])),
                    "Coaches": {"OC": random.randint(5, 9), "DC": random.randint(5, 9)}
                }
            else:
                pres = 85 if opp in CONFERENCES.get('SEC', []) else 65
                ovr = 82 if opp in CONFERENCES.get('SEC', []) else 70
                st.session_state.opponents_db[opp] = {"Prestige": pres, "OVR": ovr, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}}

        st.session_state.hotspots = generate_hotspots()
        st.session_state.schedule = engine_generate_schedule(team, conf, rival)
        st.session_state.game_state = 'DASHBOARD'
        st.rerun()


# ==============================================================================
# UI: DASHBOARD
# ==============================================================================
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

    raw_roster_val = int(sum(st.session_state.roster.values()) / 7)
    curr_ovr = int(
        (st.session_state.roster['QB'] * 0.30)
        + (st.session_state.roster['OL'] * 0.25)
        + (((st.session_state.roster['RB'] + st.session_state.roster['WR']) / 2) * 0.45)
        + (st.session_state.facilities['Training'] * 0.5)
    )
    st.session_state.team_rating = curr_ovr

    c1, c2, c3 = st.columns(3)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("Team OVR", curr_ovr, f"Raw Talent: {raw_roster_val}")
    c3.metric("Record", f"{st.session_state.record['w']}-{st.session_state.record['l']}")

    tab1, tab2, tab3, tab4 = st.tabs(["Strategy", "Staff", "Facilities", "Season"])

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
                    rtg = c['off'] if role in ['HC', 'OC'] else (c['def'] if role == 'DC' else c['recruit'])
                    badge_cls = "badge-tier-s" if rtg >= 8 else ("badge-tier-a" if rtg >= 5 else "badge-tier-f")
                    st.markdown(f"""
                    <div class='staff-card'>
                        <div class='staff-role'>{role}</div>
                        <div class='staff-name'>{c['name']}</div>
                        <div><span class='badge {badge_cls}'>RATING: {rtg}</span>
                             <span class='badge badge-trait'>TRAIT: {c.get('trait','None')}</span></div>
                        <div class='small-muted'>{helper_format_cash(c.get('salary',0))} / yr</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Fire", key=f"fire_{role}"):
                        del st.session_state.staff[role]
                        st.session_state.candidates.pop(role, None)
                        st.rerun()
                else:
                    st.warning(f"{role} VACANT")

        st.divider()
        st.markdown("### 📋 Job Market (Fill Vacancies)")
        vacancies = [r for r in roles if r not in st.session_state.staff]
        if vacancies:
            for role in vacancies:
                if role not in st.session_state.candidates:
                    st.session_state.candidates[role] = [engine_generate_coach(role, random.randint(1, 3)) for _ in range(3)]

                cols = st.columns(3)
                for i, cand in enumerate(st.session_state.candidates[role]):
                    with cols[i]:
                        vis_rate = f"{cand['off']}" if cand['scouted'] else f"{get_letter_grade(cand['off'])}"
                        vis_trait = cand['trait'] if cand['scouted'] else "???"
                        st.markdown(f"""
                        <div class='staff-card'>
                            <div class='staff-name'>{cand['name']}</div>
                            <div class='small-muted'>{cand['history']}</div>
                            <div style='margin:5px 0'>
                                <span class='badge badge-trait'>OVR: {vis_rate}</span>
                                <span class='badge badge-trait'>TRAIT: {vis_trait}</span>
                            </div>
                            <div style='font-weight:bold'>{helper_format_cash(cand['salary'])}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        b1, b2 = st.columns(2)
                        if b1.button("Hire", key=f"h_{role}_{i}"):
                            if st.session_state.budget >= cand['salary']:
                                st.session_state.budget -= cand['salary']
                                st.session_state.staff[role] = cand
                                st.session_state.candidates.pop(role, None)
                                st.rerun()
                            else:
                                st.error("Not enough budget.")
                        if (not cand['scouted']) and b2.button("Scout ($25k)", key=f"sc_{role}_{i}"):
                            if st.session_state.budget >= 25_000:
                                st.session_state.budget -= 25_000
                                cand['scouted'] = True
                                st.rerun()

                if st.button("Promote GA (Free)", key=f"ga_{role}"):
                    st.session_state.staff[role] = generate_ga_coach(role)
                    st.session_state.candidates.pop(role, None)
                    st.rerun()
        else:
            st.success("Staff complete.")

    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Marketing", st.session_state.facilities['Marketing'], delta="Rev: +$2M/yr")
            if st.button("Upgrade ($1M)", key="um"):
                if st.session_state.budget >= 1_000_000:
                    st.session_state.budget -= 1_000_000
                    st.session_state.facilities['Marketing'] += 1
                    st.rerun()
        with c2:
            st.metric("Training", st.session_state.facilities['Training'], delta="OVR Boost")
            if st.button("Upgrade ($3M)", key="ut"):
                if st.session_state.budget >= 3_000_000:
                    st.session_state.budget -= 3_000_000
                    st.session_state.facilities['Training'] += 1
                    st.rerun()
        with c3:
            st.metric("Stadium", st.session_state.facilities['Stadium'], delta="Prestige")
            if st.button("Upgrade ($10M)", key="us"):
                if st.session_state.budget >= 10_000_000:
                    st.session_state.budget -= 10_000_000
                    st.session_state.facilities['Stadium'] += 1
                    st.rerun()

    with tab4:
        if len(st.session_state.staff) < 4:
            st.error("Fill Staff First!")
            return

        if not st.session_state.season_simulated:
            if not st.session_state.schedule:
                st.session_state.schedule = engine_generate_schedule(
                    st.session_state.team_name,
                    st.session_state.team_conf,
                    st.session_state.team_rival
                )

            c1, c2 = st.columns(2)
            with c1:
                st.caption("First Half")
                for i in range(6):
                    opp = st.session_state.schedule[i]
                    css = "game-card-rival" if opp == st.session_state.team_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i + 1} vs {opp}</div>", unsafe_allow_html=True)
            with c2:
                st.caption("Second Half")
                for i in range(6, 12):
                    opp = st.session_state.schedule[i]
                    css = "game-card-rival" if opp == st.session_state.team_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i + 1} vs {opp}</div>", unsafe_allow_html=True)

            if st.button("▶️ SIMULATE SEASON", type="primary"):
                run_season()
        else:
            st.write("### Season Results (click to expand for full breakdown)")
            for log in st.session_state.season_logs:
                res = "W" if log['Score'].startswith("W") else "L"
                css = "game-card-win" if res == "W" else "game-card-loss"
                s = log['Stats']
                b = log["Breakdown"]

                with st.expander(f"Week {log['Week']}: {log['Score']} vs {log['Opponent']}"):
                    st.markdown(f"""
                    <div class='game-card {css}'>
                        <div class='card-header'><span class='card-score'>{log['Score']}</span><span>vs {log['Opponent']}</span></div>
                        <div class='stat-grid'>
                            <div class='stat-row'><span>🔥 QB Duel</span><span>{s['qb_duel'][0]} vs {s['qb_duel'][1]}</span></div>
                            <div class='stat-row'><span>⚔️ Off vs Def</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div>
                            <div class='stat-row'><span>🛡️ Def vs Off</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div>
                            <div class='stat-row'><span>🧠 Staff</span><span>{s['staff'][0]} vs {s['staff'][1]}</span></div>
                            <div class='stat-row'><span>🎯 Scheme</span><span>{s['scheme'][0]} vs {s['scheme'][1]}</span></div>
                            <div class='stat-row'><span>💪 Raw Talent</span><span>{s['raw_roster']}</span></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    st.subheader("Why did this happen?")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Your OVR", b["my_rating"])
                    c2.metric("Opp OVR", b["opp_rating"])
                    c3.metric("Talent Gap", f"{b['talent_gap']:+.2f}")

                    c4, c5, c6 = st.columns(3)
                    c4.metric("Scheme Bonus", f"{b['scheme_bonus']:+.2f}")
                    c5.metric("Coaching Net", f"{b['coaching_net']:+.2f}")
                    c6.metric("Home Bonus", f"{b['home_bonus']:+.2f}")

                    st.caption("Variance is higher in rivalry games and aggressive plans.")
                    st.write(f"Variance multiplier: **{b['var_mult']:.2f}** • Avg Luck: **{b['luck_avg']:+.2f}**")
                    st.write(f"Unit strength (pre-coach): Off **{b['my_off_unit']:.1f}** | Def **{b['my_def_unit']:.1f}**")
                    st.write(f"Coach ratings: Your OC/DC **{b['my_oc']}/{b['my_dc']}** vs Opp OC/DC **{b['opp_oc']}/{b['opp_dc']}**")

            if st.button("Proceed to Postseason", type="primary"):
                wins = st.session_state.record['w']
                rank = max(1, 130 - (wins * 10))
                if rank <= 12:
                    st.session_state.postseason_data = init_playoff_bracket(rank, st.session_state.team_name)
                else:
                    bowl = get_bowl_name(rank)
                    candidates = [t for t in ALL_TEAMS if t != st.session_state.team_name]
                    opp = random.choice(candidates)
                    st.session_state.postseason_data = {
                        "Type": "BOWL", "Bowl": bowl, "Rank": rank, "Opponent": opp,
                        "OppData": st.session_state.opponents_db.get(opp, {"OVR": 85, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 6, "DC": 6}})
                    }
                st.session_state.game_state = "POSTSEASON"
                st.rerun()


def run_season():
    wins = 0
    losses = 0
    logs = []
    bar = st.progress(0)
    total = len(st.session_state.schedule)

    for i, opp in enumerate(st.session_state.schedule):
        opp_data = st.session_state.opponents_db.get(opp, {"OVR": 80, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}})
        is_riv = (opp == st.session_state.team_rival)

        res = engine_play_game(
            st.session_state.team_rating,
            opp_data['OVR'],
            st.session_state.staff,
            st.session_state.my_schemes,
            {"Off": opp_data['Off'], "Def": opp_data['Def']},
            "Normal",
            opp_data['Coaches'],
            i % 2 == 0,
            is_riv,
            st.session_state.facilities['Stadium'],
            st.session_state.roster
        )

        if res['result'] == "W":
            wins += 1
            st.session_state.job_security = min(100, st.session_state.job_security + (5 if is_riv else 2))
        else:
            losses += 1
            pen = 2 if st.session_state.tenure <= 2 else 5
            st.session_state.job_security = max(0, st.session_state.job_security - pen)

        logs.append({"Week": i + 1, "Opponent": opp, "Score": f"{res['result']} {res['score']}", "Stats": res['stats'], "Breakdown": res["breakdown"]})
        bar.progress((i + 1) / total)

    st.session_state.record = {"w": wins, "l": losses}
    st.session_state.season_logs = logs
    st.session_state.season_simulated = True

    # Revenue after regular season, before postseason & signing
    rev = engine_calculate_revenue(st.session_state.school_tier, st.session_state.facilities['Marketing'], st.session_state.inflation)
    st.session_state.budget += rev
    st.session_state.revenue_report = f"Regular Season Revenue: +{helper_format_cash(rev)} (paid before postseason & signing)"
    st.rerun()


# ==============================================================================
# POSTSEASON (Upgraded UI)
# ==============================================================================
def bracket_row(seed1, t1, seed2, t2, winner=None):
    o1 = team_ovr(t1)
    o2 = team_ovr(t2)
    left = f"<div class='team-chip'><span class='seed-chip'>#{seed1}</span><b>{t1}</b><span class='ovr-chip'>OVR {o1}</span></div>"
    right = f"<div class='team-chip' style='justify-content:flex-end'><span class='ovr-chip'>OVR {o2}</span><b>{t2}</b><span class='seed-chip'>#{seed2}</span></div>"
    mid = "—"
    if winner:
        mid = f"✅ {winner}"
    st.markdown(f"<div class='bracket-row'>{left}<span>{mid}</span>{right}</div>", unsafe_allow_html=True)


def show_postseason():
    st.title("🏁 Postseason Hub")
    data = st.session_state.postseason_data
    if not data or not data.get("Type"):
        st.error("Postseason data missing. Returning to dashboard.")
        st.session_state.game_state = "DASHBOARD"
        st.rerun()

    if data["Type"] == "BOWL":
        st.markdown(f"<div class='bracket-box'><h3>{data['Bowl']}</h3><h1>VS {data['Opponent']}</h1></div>", unsafe_allow_html=True)
        opp = data["Opponent"]
        opp_data = data.get("OppData", st.session_state.opponents_db.get(opp, {"OVR": 85, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 6, "DC": 6}}))
        st.write(f"Opponent OVR: **{opp_data['OVR']}**")

        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            res = engine_play_game(
                st.session_state.team_rating,
                opp_data["OVR"],
                st.session_state.staff,
                st.session_state.my_schemes,
                {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                "Normal",
                opp_data.get("Coaches", {"OC": 6, "DC": 6}),
                False,
                False,
                st.session_state.facilities["Stadium"],
                st.session_state.roster
            )

            st.subheader(f"Result: {res['result']} {res['score']}")
            if res["result"] == "W":
                st.session_state.career_stats["bowl_w"] += 1
                win_bonus = int(2_000_000 * st.session_state.inflation)
                st.session_state.budget += win_bonus
                st.toast(f"🎳 Bowl Win Bonus: +{helper_format_cash(win_bonus)}")
            else:
                st.session_state.career_stats["bowl_l"] += 1

            wins = st.session_state.record["w"] + (1 if res["result"] == "W" else 0)
            losses = st.session_state.record["l"] + (1 if res["result"] == "L" else 0)
            st.session_state.history.append({"Year": st.session_state.year, "Record": f"{wins}-{losses}", "Rank": f"#{data['Rank']}", "Bowl": data["Bowl"]})

            kickoff_offseason()
            st.rerun()

        if st.button("Skip Bowl → Offseason", help="Useful for testing recruiting quickly"):
            kickoff_offseason()
            st.rerun()

    elif data["Type"] == "CFP":
        round_names = {1: "Opening Round", 2: "Quarterfinals", 3: "Semifinals", 4: "Championship"}
        st.header(f"CFP Round: {round_names.get(data['Round'], 'Round')}")

        # Display bracket
        st.write("### Bracket")
        for m in data["Matches"]:
            # Seed numbers known for round1; for later rounds, omit seed chips if not present
            s1 = m.get("seed1", "")
            s2 = m.get("seed2", "")
            if s1 == "": s1 = "—"
            if s2 == "": s2 = "—"
            bracket_row(s1, m["t1"], s2, m["t2"], m.get("winner"))

        # Find user match
        user_match = None
        for m in data["Matches"]:
            if m["t1"] == st.session_state.team_name or m["t2"] == st.session_state.team_name:
                user_match = m
                break

        colA, colB = st.columns([2, 1])

        with colA:
            if user_match and data.get("UserAlive", True):
                opp = user_match["t2"] if user_match["t1"] == st.session_state.team_name else user_match["t1"]
                st.info(f"Your matchup: **{st.session_state.team_name} vs {opp}** (OVR {st.session_state.team_rating} vs {team_ovr(opp)})")

                if st.button("PLAY MY GAME 🏈", type="primary"):
                    opp_data = st.session_state.opponents_db.get(opp, {"OVR": 88, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 7, "DC": 7}})
                    res = engine_play_game(
                        st.session_state.team_rating,
                        opp_data["OVR"],
                        st.session_state.staff,
                        st.session_state.my_schemes,
                        {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")},
                        "Normal",
                        opp_data.get("Coaches", {"OC": 7, "DC": 7}),
                        False,
                        False,
                        st.session_state.facilities["Stadium"],
                        st.session_state.roster
                    )

                    st.subheader(f"Your result: {res['result']} {res['score']}")

                    next_round_teams = []
                    for m in data["Matches"]:
                        if m is user_match:
                            if res["result"] == "W":
                                m["winner"] = st.session_state.team_name
                                next_round_teams.append(st.session_state.team_name)
                                st.toast("VICTORY! Advancing…")
                            else:
                                m["winner"] = opp
                                next_round_teams.append(opp)
                                st.session_state.postseason_data["UserAlive"] = False
                                st.error(f"Eliminated by {opp}")
                        else:
                            winner = weighted_game_winner(m["t1"], m["t2"])
                            m["winner"] = winner
                            next_round_teams.append(winner)

                    advance_cfp(next_round_teams)
                    st.rerun()
            else:
                st.warning("No user matchup found (bye) or you are eliminated.")

        with colB:
            st.write("### Sim controls")
            if st.button("SIM OTHER GAMES ONLY"):
                # Sim all games where user is not participating or when user has bye.
                next_round_teams = []
                for m in data["Matches"]:
                    if (m["t1"] == st.session_state.team_name or m["t2"] == st.session_state.team_name) and data.get("UserAlive", True):
                        # keep it unresolved until you play
                        if m.get("winner"):
                            next_round_teams.append(m["winner"])
                        else:
                            # placeholder; won't advance until played
                            pass
                    else:
                        winner = weighted_game_winner(m["t1"], m["t2"])
                        m["winner"] = winner
                        next_round_teams.append(winner)

                st.toast("Simmed other games.")
                st.rerun()

            if st.button("SIM ENTIRE ROUND (AUTO)", help="Will simulate your game too."):
                next_round_teams = []
                for m in data["Matches"]:
                    winner = weighted_game_winner(m["t1"], m["t2"])
                    m["winner"] = winner
                    next_round_teams.append(winner)
                    if (m["t1"] == st.session_state.team_name or m["t2"] == st.session_state.team_name) and winner != st.session_state.team_name:
                        st.session_state.postseason_data["UserAlive"] = False

                advance_cfp(next_round_teams, auto=True)
                st.rerun()

            st.divider()
            if st.button("Quit CFP → Offseason"):
                kickoff_offseason()
                st.rerun()


def advance_cfp(next_round_teams, auto=False):
    data = st.session_state.postseason_data

    # If user eliminated this round, end season and kickoff offseason
    if not st.session_state.postseason_data.get("UserAlive", True):
        hist = {"Year": st.session_state.year, "Record": "Playoff Loss", "Rank": f"#{data.get('UserRank','?')}", "Bowl": "CFP"}
        st.session_state.history.append(hist)
        kickoff_offseason()
        return

    # Title check (Round 4 completed)
    if data["Round"] == 4:
        title_bonus = int(50_000_000 * st.session_state.inflation)
        st.session_state.budget += title_bonus
        st.session_state.career_stats["titles"] += 1
        st.balloons()
        st.success(f"NATIONAL CHAMPIONS! +{helper_format_cash(title_bonus)}")
        st.session_state.history.append({"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Bowl": "National Title"})
        kickoff_offseason()
        return

    # Build next round
    new_matches = []
    if data["Round"] == 1:
        seeds = data["QF_Seeds"]
        seed_nums = data.get("QF_SeedNums", [1, 2, 3, 4])
        # match seeds vs winners in simple reverse order
        for i in range(4):
            new_matches.append({"t1": seeds[i], "t2": next_round_teams[3 - i], "winner": None, "seed1": seed_nums[i], "seed2": "W"})
    elif data["Round"] == 2:
        new_matches.append({"t1": next_round_teams[0], "t2": next_round_teams[3], "winner": None, "seed1": "W", "seed2": "W"})
        new_matches.append({"t1": next_round_teams[1], "t2": next_round_teams[2], "winner": None, "seed1": "W", "seed2": "W"})
    elif data["Round"] == 3:
        new_matches.append({"t1": next_round_teams[0], "t2": next_round_teams[1], "winner": None, "seed1": "W", "seed2": "W"})

    st.session_state.postseason_data["Round"] += 1
    st.session_state.postseason_data["Matches"] = new_matches


# ==============================================================================
# OFFSEASON: NIL (filters/sorting added)
# ==============================================================================
def show_offseason_nil():
    st.title("1) NIL Prospects (Signing Window)")
    st.write(f"Budget: **{helper_format_cash(st.session_state.budget)}**")

    if not st.session_state.offseason.get("nil_board"):
        st.session_state.offseason["nil_board"] = generate_nil_board(10)

    signed = st.session_state.offseason.get("nil_signed", [])
    st.markdown(f"<div class='nil-alert'>NIL Signed This Offseason: {len(signed)} / 3</div>", unsafe_allow_html=True)

    # Filters
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        pos_filter = st.multiselect("Filter positions", POSITIONS, default=[])
    with f2:
        min_rating = st.slider("Min rating", 70, 99, 84)
    with f3:
        max_ask = st.slider("Max ask (M)", 0.5, 12.0, 6.0, step=0.5)
    with f4:
        sort_by = st.selectbox("Sort", ["Rating (desc)", "Ask (asc)", "Value (rating/ask) (desc)"])

    power = recruiting_power_score()
    board = [p for p in st.session_state.offseason["nil_board"] if p["status"] == "Open"]
    if pos_filter:
        board = [p for p in board if p["pos"] in pos_filter]
    board = [p for p in board if p["rating"] >= min_rating and (p["ask"] <= max_ask * 1_000_000)]

    def value_score(p):
        return p["rating"] / max(1, p["ask"])

    if sort_by == "Rating (desc)":
        board.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "Ask (asc)":
        board.sort(key=lambda x: x["ask"])
    else:
        board.sort(key=value_score, reverse=True)

    for p in board:
        st.markdown(f"""
        <div class='prospect-card'>
          <div class='prospect-title'>#{p["id"]} • {p["pos"]} {p["name"]} ({p["rating"]})</div>
          <div class='small-muted'>{p["trait"]} • {p["notes"]}</div>
          <div style='margin-top:6px'><b>NIL Ask:</b> {helper_format_cash(p["ask"])}</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            overpay = st.slider(f"Sweetener — {p['name']}", 0, int(3_000_000 * st.session_state.inflation), 0,
                                step=int(250_000 * st.session_state.inflation), key=f"nil_sweet_{p['id']}")
        with c2:
            est = estimate_nil_odds(p, overpay, power)
            st.metric("Est. odds", f"{int(est*100)}%")
        with c3:
            if st.button("Offer", key=f"nil_offer_{p['id']}"):
                if len(signed) >= 3:
                    st.warning("You already signed 3 NIL prospects.")
                else:
                    cost = p["ask"] + overpay
                    if st.session_state.budget < cost:
                        st.error("Not enough budget.")
                    else:
                        if random.random() < est:
                            st.session_state.budget -= cost
                            p["status"] = "Signed"
                            st.session_state.offseason["nil_signed"].append(p)
                            st.session_state.roster[p["pos"]] = max(st.session_state.roster[p["pos"]], p["rating"])
                            st.toast(f"✅ SIGNED: {p['pos']} {p['name']} ({p['rating']})")
                        else:
                            p["status"] = "Lost"
                            st.error(f"❌ Lost {p['name']} to another school.")
                st.rerun()

    st.divider()
    if st.button("Back to Offseason Hub"):
        st.session_state.game_state = "OFFSEASON_HUB"
        st.rerun()


def estimate_nil_odds(p, overpay, power):
    spend_factor = min(0.20, (overpay / max(1, p["ask"])) * 0.12)
    base = 0.35 + (0.35 * power) + spend_factor
    return max(0.15, min(0.88, base))


# ==============================================================================
# OFFSEASON: Outreach
# ==============================================================================
def show_offseason_outreach():
    st.title("2) Overall High School Outreach (Position Investment)")
    st.write(f"Budget: **{helper_format_cash(st.session_state.budget)}**")
    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    st.markdown(f"<div class='recruiting-intel'>Pipeline Bonus ({st.session_state.home_region}): {', '.join(hot)}</div>", unsafe_allow_html=True)

    allocs = {}
    curr = 0
    for p in POSITIONS:
        allocs[p] = st.number_input(f"{p}", 0, 10_000_000, 0, step=100_000, key=f"out_{p}")
        curr += allocs[p]

    st.metric("Remaining", helper_format_cash(st.session_state.budget - curr))

    if st.button("Finalize Outreach", type="primary"):
        res = process_outreach(st.session_state.budget, allocs, st.session_state.staff, st.session_state.prestige, st.session_state.inflation)
        if not res:
            st.error("Over Budget")
            return

        st.session_state.budget -= res["cost"]

        if res["booster_bonus"] > 0:
            st.session_state.budget += res["booster_bonus"]
            st.toast(f"💎 Booster Gem Bonus: +{helper_format_cash(res['booster_bonus'])}")

        for p, g in res["roster_updates"].items():
            loss = 12 if st.session_state.active_transfers.get(p) else random.randint(2, 5)
            st.session_state.active_transfers[p] = False
            st.session_state.roster[p] = max(40, min(99, int(st.session_state.roster[p] - loss + g)))

        for gem in res["gems"]:
            st.session_state.stars.append(gem)

        st.session_state.offseason["outreach_done"] = True
        st.success("Outreach complete.")

        st.session_state.game_state = "OFFSEASON_HUB"
        st.rerun()

    if st.button("Back to Offseason Hub"):
        st.session_state.game_state = "OFFSEASON_HUB"
        st.rerun()


# ==============================================================================
# OFFSEASON: Top-8 (odds meter)
# ==============================================================================
def show_offseason_top8():
    st.title("3) Top-8 Prospect Battles (Big Board)")
    st.write(f"Budget: **{helper_format_cash(st.session_state.budget)}**")

    if not st.session_state.offseason.get("outreach_done", False):
        st.warning("Outreach not completed — returning to hub.")
        st.session_state.game_state = "OFFSEASON_HUB"
        st.rerun()

    if not st.session_state.offseason.get("top8_board"):
        st.session_state.offseason["top8_board"] = generate_top8_battles()

    signed = st.session_state.offseason.get("top8_signed", [])
    st.markdown(f"<div class='nil-alert'>Top-8 Signed: {len(signed)} / 2</div>", unsafe_allow_html=True)

    # Filters + sorting
    f1, f2, f3 = st.columns(3)
    with f1:
        pos_filter = st.multiselect("Filter positions", POSITIONS, default=[], key="top8_pos")
    with f2:
        min_rating = st.slider("Min rating", 85, 99, 92, key="top8_min")
    with f3:
        sort_by = st.selectbox("Sort", ["Rank (asc)", "Rating (desc)", "Ask (asc)"], key="top8_sort")

    board = [p for p in st.session_state.offseason["top8_board"] if p["status"] == "Open"]
    if pos_filter:
        board = [p for p in board if p["pos"] in pos_filter]
    board = [p for p in board if p["rating"] >= min_rating]

    if sort_by == "Rank (asc)":
        board.sort(key=lambda x: x["rank"])
    elif sort_by == "Rating (desc)":
        board.sort(key=lambda x: x["rating"], reverse=True)
    else:
        board.sort(key=lambda x: x["ask"])

    power = recruiting_power_score()
    scout = st.session_state.staff.get("Scout", {"recruit": 3}).get("recruit", 3)
    oc = st.session_state.staff.get("OC", {"off": 3}).get("off", 3)
    dc = st.session_state.staff.get("DC", {"def": 3}).get("def", 3)
    coach_strength = (oc + dc) / 20  # 0..1

    for p in board:
        # compute competitor "program strength" (ovr+prestige)
        comp1 = p["competitors"][0]
        comp2 = p["competitors"][1]
        comp1_strength = (team_ovr(comp1) / 100) * 0.60 + (st.session_state.opponents_db.get(comp1, {"Prestige": 70}).get("Prestige", 70) / 100) * 0.40
        comp2_strength = (team_ovr(comp2) / 100) * 0.60 + (st.session_state.opponents_db.get(comp2, {"Prestige": 70}).get("Prestige", 70) / 100) * 0.40

        st.markdown(f"""
        <div class='prospect-card'>
          <div class='prospect-title'>Top {p["rank"]} • {p["pos"]} {p["name"]} ({p["rating"]})</div>
          <div class='small-muted'>{p["trait"]} • Competing: {comp1} / {comp2}</div>
          <div style='margin-top:6px'><b>NIL Ask:</b> {helper_format_cash(p["ask"])}</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            push = st.slider(f"Extra push for {p['name']} (visits/media)", 0, int(5_000_000 * st.session_state.inflation), 0,
                             step=int(250_000 * st.session_state.inflation), key=f"top8_push_{p['id']}")

        # odds distribution across 3 teams
        you_prob, c1_prob, c2_prob = top8_odds_distribution(p, push, power, scout, coach_strength, comp1_strength, comp2_strength)

        with c2:
            st.write("Commit odds (est.)")
            st.progress(you_prob, text=f"You: {int(you_prob*100)}%")
            st.progress(c1_prob, text=f"{comp1}: {int(c1_prob*100)}%")
            st.progress(c2_prob, text=f"{comp2}: {int(c2_prob*100)}%")

        with c3:
            if st.button("Battle!", key=f"top8_battle_{p['id']}", type="primary"):
                if len(signed) >= 2:
                    st.warning("You already signed 2 Top-8 prospects.")
                else:
                    cost = p["ask"] + push
                    if st.session_state.budget < cost:
                        st.error("Not enough budget.")
                    else:
                        st.session_state.budget -= cost

                        # draw based on distribution
                        r = random.random()
                        if r < you_prob:
                            p["status"] = "Signed"
                            st.session_state.offseason["top8_signed"].append(p)
                            st.session_state.roster[p["pos"]] = max(st.session_state.roster[p["pos"]], p["rating"])
                            st.session_state.stars.append({"id": p["id"], "name": p["name"], "pos": p["pos"], "rating": p["rating"], "year": "Fr", "trait": p["trait"]})
                            booster = int(random.randint(1_000_000, 6_000_000) * st.session_state.inflation)
                            st.session_state.budget += booster
                            st.toast(f"✅ SIGNED Top-8! Booster payout: +{helper_format_cash(booster)}")
                        elif r < you_prob + c1_prob:
                            p["status"] = "Lost"
                            st.error(f"❌ Lost {p['name']} to {comp1}")
                        else:
                            p["status"] = "Lost"
                            st.error(f"❌ Lost {p['name']} to {comp2}")

                st.rerun()

    st.divider()
    if st.button("Back to Offseason Hub"):
        st.session_state.game_state = "OFFSEASON_HUB"
        st.rerun()


def top8_odds_distribution(p, push, power, scout, coach_strength, comp1_strength, comp2_strength):
    # Your score = power + scout + coach_strength + spend factor
    spend_factor = min(0.30, (push / max(1, p["ask"])) * 0.18)
    you_score = 0.35 + (0.45 * power) + (0.12 * (scout / 10)) + (0.20 * coach_strength) + spend_factor

    # Competitor scores based on their program strength + noise
    c1_score = 0.50 * comp1_strength + random.uniform(-0.03, 0.03)
    c2_score = 0.50 * comp2_strength + random.uniform(-0.03, 0.03)

    # Softmax
    exp_you = pow(2.71828, you_score)
    exp_c1 = pow(2.71828, c1_score)
    exp_c2 = pow(2.71828, c2_score)
    total = exp_you + exp_c1 + exp_c2
    you_prob = exp_you / total
    c1_prob = exp_c1 / total
    c2_prob = exp_c2 / total

    # Clamp for sanity
    you_prob = max(0.05, min(0.85, you_prob))
    # renormalize
    rest = 1.0 - you_prob
    c_sum = c1_prob + c2_prob
    if c_sum <= 0:
        c1_prob, c2_prob = rest / 2, rest / 2
    else:
        c1_prob = rest * (c1_prob / c_sum)
        c2_prob = rest * (c2_prob / c_sum)
    return you_prob, c1_prob, c2_prob


# ==============================================================================
# SUMMARY / PORTAL (Optional) + FIRED
# ==============================================================================
def show_year_summary():
    st.title(f"{st.session_state.year} Summary")
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    else:
        st.info("No history yet. Play a season first.")

    st.markdown(f"<div class='nil-alert'>💰 WAR CHEST AVAILABLE FOR NIL: {helper_format_cash(st.session_state.budget)}</div>", unsafe_allow_html=True)

    if st.button("Enter Portal (Optional)"):
        st.session_state.portal_players = engine_generate_portal_players()
        st.session_state.game_state = "PORTAL"
        st.rerun()

    if st.button("Skip Portal → Offseason Hub", type="primary"):
        kickoff_offseason()
        st.rerun()


def show_portal():
    st.title("Transfer Portal (Optional)")
    st.write(f"Budget: {helper_format_cash(st.session_state.budget)}")

    if not st.session_state.portal_players:
        st.session_state.portal_players = engine_generate_portal_players()

    for i, p in enumerate(list(st.session_state.portal_players)):
        c1, c2 = st.columns([3, 1])
        c1.write(f"{p['pos']} {p['name']} ({p['rating']}) - {helper_format_cash(p['cost'])}")
        if c2.button("Sign", key=f"p_{i}"):
            if st.session_state.budget >= p['cost']:
                st.session_state.budget -= p['cost']
                st.session_state.roster[p['pos']] = max(st.session_state.roster[p['pos']], p['rating'])
                st.session_state.active_transfers[p['pos']] = True
                st.session_state.portal_players.remove(p)
                st.rerun()
            else:
                st.error("Not enough budget.")

    if st.button("Proceed to Offseason Hub", type="primary"):
        kickoff_offseason()
        st.rerun()


def show_fired():
    st.error("FIRED! Your tenure has ended.")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()


def show_retirement():
    st.title("Retirement")
    st.write("Thanks for playing.")
    if st.button("Restart"):
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
elif st.session_state.game_state == 'OFFSEASON_HUB':
    show_offseason_hub()
elif st.session_state.game_state == 'OFFSEASON_NIL':
    show_offseason_nil()
elif st.session_state.game_state == 'OFFSEASON_OUTREACH':
    show_offseason_outreach()
elif st.session_state.game_state == 'OFFSEASON_TOP8':
    show_offseason_top8()
elif st.session_state.game_state == 'RETIREMENT':
    show_retirement()
else:
    st.session_state.game_state = "DASHBOARD"
    st.rerun()
