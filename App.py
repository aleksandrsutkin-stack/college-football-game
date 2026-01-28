"""
Build the Program: College Football CEO
Version 1.6 (The Expanded Stable Release)

Audit Log:
- Base: V1.4 Stable (Bracket Fixes + Deterministic RNG).
- Integrated: V1.5 Real World Universe (55+ Teams).
- Integrated: V1.5 Retention Ransom Phase (Offseason Step 1).
- Integrated: V1.5 Hall of Fame Retirement Logic.
"""

import streamlit as st
import random
import time
import json
import datetime
import math
import pandas as pd
import copy
from typing import List, Dict, Optional, Set

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

STATE_VERSION = 1.6

class GameState:
    SETUP = "SETUP"
    DASHBOARD = "DASHBOARD"
    SEASON_END = "SEASON_END"
    SELECTION_SUNDAY = "SELECTION_SUNDAY"
    POSTSEASON = "POSTSEASON"
    SEASON_RECAP = "SEASON_RECAP"
    OFFSEASON = "OFFSEASON"
    RECRUITING_WRAP = "RECRUITING_WRAP"
    FIRED = "FIRED"
    RETIREMENT = "RETIREMENT"

class GameConfig:
    POSITIONS = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
    REGION_STRENGTH = {"South": 1.08, "Midwest": 1.05, "West": 1.05, "North": 1.02}
    
    SCHEMES = {
        "Offense": ["Air Raid", "Smashmouth", "Pro Style"], 
        "Defense": ["3-3-5 Cloud", "4-4 Heavy", "Man Coverage"]
    }
    
    OFF_COUNTERED_BY = {"Air Raid": "3-3-5 Cloud", "Smashmouth": "4-4 Heavy", "Pro Style": "Man Coverage"}
    DEF_COUNTERS = {"3-3-5 Cloud": "Smashmouth", "4-4 Heavy": "Air Raid", "Man Coverage": "Pro Style"}

    TRAITS = ["❄️ Clutch", "🚀 Speedster", "🧠 General", "😤 Enforcer"]
    
    COACH_TRAITS = {
        "None": "None", "Recruiter": "+10% Recruiting", "Tactician": "+3 Game Boost", 
        "Air Raid": "+2 Scheme", "Smashmouth": "+2 Scheme", "Pro Style": "+2 Scheme"
    }

    BOWL_MAPPING = {
        "Elite": ["Rose Bowl", "Sugar Bowl", "Orange Bowl", "Cotton Bowl", "Peach Bowl", "Fiesta Bowl"],
        "High": ["Citrus Bowl", "Alamo Bowl", "Pop-Tarts Bowl", "Gator Bowl"],
        "Mid": ["Liberty Bowl", "Music City Bowl", "Las Vegas Bowl"],
        "Low": ["Gasparilla Bowl", "Boca Raton Bowl", "Potato Bowl"]
    }

    TROPHY_ICONS = {
        "National Title": "🏆", "CFP": "🏆", "Rose Bowl": "🌹", "Sugar Bowl": "🍬", "Orange Bowl": "🍊", 
        "Cotton Bowl": "🤠", "Peach Bowl": "🍑", "Fiesta Bowl": "🎉", "Citrus Bowl": "🍋", "Alamo Bowl": "🏰", 
        "Pop-Tarts Bowl": "🍪", "Gator Bowl": "🐊", "Liberty Bowl": "🗽", "Music City Bowl": "🎸", 
        "Las Vegas Bowl": "🎰", "Gasparilla Bowl": "🏴‍☠️", "Boca Raton Bowl": "🌴", "Potato Bowl": "🥔", 
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
        "San Jose State": {"color": "#0055A2"}, "Navy": {"color": "#00205B"}, "Army": {"color": "#D4BF91"},
        "Tulane": {"color": "#006747"}, "App State": {"color": "#FFCC00"}, "Toledo": {"color": "#15397F"}
    }

    # V1.6: Integrated Expanded Universe from V1.5
    REAL_WORLD_INIT = {
        # Elite Tier (90+ Prestige)
        "Indiana": {"Prestige": 99, "Talent": 86, "Tier": 1, "Rival": "Purdue"},
        "Ohio State": {"Prestige": 95, "Talent": 94, "Tier": 1, "Rival": "Michigan"},
        "Miami": {"Prestige": 94, "Talent": 89, "Tier": 1, "Rival": "Florida St"},
        "Oregon": {"Prestige": 93, "Talent": 92, "Tier": 1, "Rival": "Washington"},
        "Georgia": {"Prestige": 92, "Talent": 96, "Tier": 1, "Rival": "Florida"},
        "Ole Miss": {"Prestige": 91, "Talent": 88, "Tier": 1, "Rival": "Mississippi St"},
        "Notre Dame": {"Prestige": 92, "Talent": 93, "Tier": 1, "Rival": "USC"},
        
        # High Tier (85-89 Prestige)
        "Texas Tech": {"Prestige": 90, "Talent": 84, "Tier": 2, "Rival": "Baylor"},
        "Texas A&M": {"Prestige": 89, "Talent": 91, "Tier": 2, "Rival": "Texas"},
        "Alabama": {"Prestige": 85, "Talent": 95, "Tier": 1, "Rival": "Auburn"},
        "BYU": {"Prestige": 86, "Talent": 82, "Tier": 2, "Rival": "Utah"},
        "Clemson": {"Prestige": 88, "Talent": 87, "Tier": 2, "Rival": "South Carolina"},
        "Tennessee": {"Prestige": 87, "Talent": 86, "Tier": 2, "Rival": "Alabama"},
        "Penn State": {"Prestige": 86, "Talent": 88, "Tier": 2, "Rival": "Ohio State"},
        "Wisconsin": {"Prestige": 85, "Talent": 83, "Tier": 2, "Rival": "Minnesota"},
        
        # Good Tier (80-84 Prestige)
        "Texas": {"Prestige": 84, "Talent": 97, "Tier": 1, "Rival": "Oklahoma"},
        "Oklahoma": {"Prestige": 83, "Talent": 90, "Tier": 2, "Rival": "Texas"},
        "Utah": {"Prestige": 82, "Talent": 85, "Tier": 2, "Rival": "BYU"},
        "USC": {"Prestige": 79, "Talent": 89, "Tier": 2, "Rival": "Notre Dame"},
        "Michigan": {"Prestige": 78, "Talent": 91, "Tier": 2, "Rival": "Ohio State"},
        "LSU": {"Prestige": 76, "Talent": 92, "Tier": 2, "Rival": "Alabama"},
        "Washington": {"Prestige": 81, "Talent": 84, "Tier": 2, "Rival": "Oregon"},
        "Florida": {"Prestige": 80, "Talent": 86, "Tier": 2, "Rival": "Georgia"},
        
        # Competitive Tier (75-79 Prestige)
        "Boise State": {"Prestige": 76, "Talent": 82, "Tier": 2, "Rival": "Fresno St"},
        "Colorado": {"Prestige": 75, "Talent": 85, "Tier": 2, "Rival": "Nebraska"},
        "Iowa": {"Prestige": 77, "Talent": 81, "Tier": 2, "Rival": "Iowa State"},
        "Kansas State": {"Prestige": 76, "Talent": 80, "Tier": 2, "Rival": "Kansas"},
        "Louisville": {"Prestige": 75, "Talent": 79, "Tier": 2, "Rival": "Kentucky"},
        "NC State": {"Prestige": 74, "Talent": 78, "Tier": 3, "Rival": "UNC"},
        "Arizona": {"Prestige": 73, "Talent": 77, "Tier": 3, "Rival": "Arizona State"},
        
        # Mid Tier (70-74 Prestige)
        "Vanderbilt": {"Prestige": 80, "Talent": 78, "Tier": 3, "Rival": "Tennessee"},
        "Florida St": {"Prestige": 70, "Talent": 87, "Tier": 3, "Rival": "Miami"},
        "Tulane": {"Prestige": 74, "Talent": 77, "Tier": 3, "Rival": "LSU"},
        "Memphis": {"Prestige": 72, "Talent": 76, "Tier": 3, "Rival": "Ole Miss"},
        "UCF": {"Prestige": 71, "Talent": 75, "Tier": 3, "Rival": "USF"},
        
        # G5 Contenders (65-69 Prestige)
        "Navy": {"Prestige": 68, "Talent": 74, "Tier": 3, "Rival": "Army"},
        "Army": {"Prestige": 67, "Talent": 73, "Tier": 3, "Rival": "Navy"},
        "Air Force": {"Prestige": 66, "Talent": 72, "Tier": 3, "Rival": "Army"},
        "Toledo": {"Prestige": 69, "Talent": 75, "Tier": 3, "Rival": "Bowling Green"},
        "App State": {"Prestige": 70, "Talent": 76, "Tier": 3, "Rival": "Georgia Southern"},
    }

    CONFERENCES = {
        "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Ole Miss", "Florida", "Texas A&M", "Missouri", "Kentucky", "Vanderbilt", "Mississippi St"],
        "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington", "Nebraska", "Michigan St", "UCLA", "Indiana", "Purdue"],
        "ACC": ["Florida St", "Clemson", "Miami", "Louisville", "UNC", "Virginia Tech", "SMU", "Pitt", "NC State", "Stanford", "Cal"],
        "Big 12": ["Utah", "Kansas State", "Oklahoma St", "Arizona", "Colorado", "Texas Tech", "Baylor", "TCU", "BYU", "West Virginia", "Arizona State"],
        "Pac-12": ["Boise State", "Fresno St", "San Diego St", "Colorado St", "Oregon St", "Wash State"],
        "Indep": ["Notre Dame", "UConn", "UMass"],
        "MAC": ["Toledo", "Miami (OH)", "Ohio", "Northern Illinois", "Western Michigan", "Bowling Green"],
        "G5": ["Tulane", "Memphis", "Navy", "Army", "USF", "Liberty", "App State", "James Madison", "San Jose State", "Wyoming", "Air Force", "Nevada"]
    }
    
    ALL_TEAMS = [t for c in CONFERENCES.values() for t in c]

ALLOWED_SAVE_KEYS = {
    "state_version", "game_state", "year", "budget", "prestige", "job_security",
    "expected_wins", "tenure", "roster", "active_transfers", "stars", "staff",
    "facilities", "history", "record", "opponents_db", "my_schemes",
    "career_stats", "season_logs", "schedule", "season_simulated",
    "hotspots", "candidates", "postseason_data", "revenue_report", "inflation",
    "team_needs", "game_plan", "week_index", "news", "offseason_step",
    "nil_class", "hs_total_spend", "hs_shares", "hs_spend_by_pos",
    "hs_alloc_by_pos", "top8", "top8_resolved", "trophies", "conf_revenue_boost_mult",
    "pending_invite", "season_end_ready", "booster_rating", "ai_records",
    "selection_sunday_results", "ad_name", "team_name", "team_color",
    "team_conf", "team_rival", "home_region", "school_tier",
    "team_off", "team_def", "team_rating", "last_postseason_result",
    "achievements", "milestone_log", "conferences_map",
    "hs_last_results", "recruiting_summary", "postseason_flash",
    "last_known_team_name", "last_known_team_color", "retention_data"
}

try:
    st.set_page_config(page_title="Build the Program: College Football CEO", page_icon="🏈", layout="wide")
except Exception:
    pass

st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
.game-card, .staff-card, .news-box, .security-box, .trophy-tile, .resume-box { color: #111111 !important; }
.security-box { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
.security-safe { color: #28a745; font-weight: bold; }
.security-warm { color: #fd7e14; font-weight: bold; }
.security-hot { color: #dc3545; font-weight: bold; }
.finance-alert { background-color: #d1e7dd; color: #0f5132 !important; border: 1px solid #badbcc; padding: 15px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-weight: bold; }
.nil-alert { background-color: #cff4fc; color: #055160 !important; border: 1px solid #b6effb; padding: 18px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-size: 1.1em; font-weight: bold; }
.game-card { padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #ddd; background: white !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05); color: #111111 !important; }
.game-card-win { border-left: 5px solid #28a745; background: #f8fff9 !important; }
.game-card-loss { border-left: 5px solid #dc3545; background: #fff8f8 !important; }
.game-card-pending { border-left: 5px solid #6c757d; background: #f8f9fa !important; }
.game-card-rival { border-left: 5px solid #fd7e14; background: #fff4e6 !important; }
.card-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 8px; color: #111111 !important; }
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.85em; color: #111111 !important; }
.stat-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px dotted #eee; color: #111111 !important; }
.staff-card { background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
.staff-role { font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.staff-name { font-size: 1.1em; font-weight: 800; color: #333; }
.badge { padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; margin-right: 5px; display: inline-block;}
.badge-tier-s { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-tier-a { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-tier-f { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-trait { background: #e2e3e5; color: #383d41; }
.recruiting-intel { background-color: #e0f7fa; color: #006064 !important; border-left: 5px solid #006064; padding: 12px; margin-bottom: 10px; border-radius: 4px; }
.news-box { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.news-item { padding: 6px 10px; border-bottom: 1px solid #f1f1f1; font-size: 0.9em; }
.news-item-good { border-left: 4px solid #28a745; background-color: #f0fff4; }
.news-item-bad { border-left: 4px solid #dc3545; background-color: #fff5f5; }
.trophy-tile { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 10px; }
.newspaper-head { font-family: 'Georgia', serif; font-size: 2em; text-align: center; border-bottom: 3px double #333; padding-bottom: 10px; margin-bottom: 20px; color: #2c3e50; background: #fdfbf7; padding-top: 20px; }
.newspaper-sub { font-family: 'Georgia', serif; font-style: italic; text-align: center; color: #555; margin-bottom: 20px; }
.booster-meter-container { background: #eee; height: 20px; border-radius: 10px; margin-top: 5px; overflow: hidden; border: 1px solid #ccc; }
.booster-meter-fill { height: 100%; transition: width 0.5s; }
.resume-box { background-color: #fff; border: 2px solid #333; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
.resume-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: center; }
.resume-label { font-size: 0.8em; text-transform: uppercase; color: #666; letter-spacing: 1px; }
.resume-val { font-size: 1.2em; font-weight: bold; }

.rank-grid { display: grid; grid-template-columns: 50px 1fr 100px 90px; gap: 10px; align-items: center; padding: 8px; border-bottom: 1px solid #eee; background: white; color: #333; }
.rank-grid-user { background: #e3f2fd !important; border-left: 5px solid #2196f3; font-weight: bold; }
.rank-num { font-weight: bold; color: #555; text-align: center; }
.rank-team { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.rank-rec { text-align: right; }
.rank-status { text-align: right; font-weight: bold; font-size: 0.9em; }

.vip-seed-card { background: #fffbeb; border: 2px solid #f1c40f; border-radius: 8px; padding: 15px; text-align: center; height: 100%; }
.vip-seed-num { font-size: 1.5em; font-weight: 900; color: #b7791f; }
.vip-seed-team { font-weight: bold; font-size: 1.1em; margin: 5px 0; }
.vip-badge { display: inline-block; background: #f1c40f; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.7em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CORE UTILITIES
# ==============================================================================

def safe_int(value, default: int = 0) -> int:
    try:
        if value is None or value == "": return default
        return int(float(value))
    except (ValueError, TypeError): return default

def safe_float(value, default: float = 0.0) -> float:
    try:
        if value is None or value == "": return default
        return float(value)
    except (ValueError, TypeError): return default

def safe_dict(x):
    return x if isinstance(x, dict) else {}

def clamp_budget() -> None:
    try:
        st.session_state.budget = max(0, int(st.session_state.get("budget", 0) or 0))
    except Exception:
        st.session_state.budget = 0

def safe_toast(msg: str) -> None:
    try: st.toast(msg)
    except Exception:
        try: st.info(msg)
        except Exception: pass

# ==============================================================================
# FORMATTING & VALIDATION
# ==============================================================================

def helper_format_cash(amount: int) -> str:
    try: amount = int(amount)
    except Exception: amount = 0
    return f"${amount/1_000_000:.1f}M" if amount >= 1_000_000 else f"${int(amount/1_000)}K"

def format_position_delta(delta: float) -> str:
    try: delta = float(delta)
    except Exception: delta = 0.0
    sign = "+" if delta >= 0 else ""
    return f"{sign}{int(round(delta))}"

def get_letter_grade(rating: int) -> str:
    if rating >= 9: return "A+"
    elif rating >= 8: return "A"
    elif rating >= 7: return "B"
    elif rating >= 5: return "C"
    elif rating >= 3: return "D"
    else: return "F"

def validate_budget_input(amount: int, max_budget: int, action: str = "transaction") -> bool:
    amount = safe_int(amount, 0)
    max_budget = safe_int(max_budget, 0)
    if amount < 0:
        st.error(f"❌ Invalid {action}: Amount cannot be negative (${amount:,})")
        return False
    if amount > max_budget:
        st.error(f"❌ Insufficient funds for {action}\n\nNeed: {helper_format_cash(amount)}\nHave: {helper_format_cash(max_budget)}\nShort: {helper_format_cash(amount - max_budget)}")
        return False
    return True

# ==============================================================================
# GENERATORS
# ==============================================================================

def generate_name() -> str:
    first = ["Marcus", "Trey", "Deion", "Caleb", "Jalen", "Bo", "Ty", "Zay", "Kool-Aid", "Tank", "Arch", "Shedeur", "Quinn", "Travis", "Ashton", "Jaxson", "Miller"]
    last = ["King", "Sanders", "Ewers", "Milroe", "Hunter", "Bond", "Nix", "Penix", "Bowers", "Manning", "Gabriel", "Beck", "Jeanty", "Judkins", "Dart", "Moss"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_coach_name() -> str:
    first = ["Kirby", "Nick", "Ryan", "Lane", "Dabo", "Lincoln", "Steve", "Chip", "Deion", "Marcus", "Dan", "Kalen", "Matt", "Luke"]
    last = ["Smart", "Saban", "Day", "Kiffin", "Swinney", "Riley", "Sarkisian", "Kelly", "Sanders", "Freeman", "Lanning", "DeBoer", "Rhule", "Fickell"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_star_player(pos: str, tier: int = 1) -> dict:
    base = 86 if tier == 1 else 78
    return {"name": generate_name(), "pos": pos, "rating": random.randint(base, min(99, base + 10))}

def generate_ga_coach(role: str) -> dict:
    base = random.randint(2, 5)
    return {"name": generate_coach_name() + " (GA)", "role": role, "off": min(10, base + random.randint(0, 2)), "def": min(10, base + random.randint(0, 2)), "recruit": min(10, base + random.randint(0, 2)), "trait": "None", "salary": 0, "history": "Internal Promotion", "scouted": True}

# ==============================================================================
# MANAGERS
# ==============================================================================

class BudgetManager:
    @staticmethod
    def get_current() -> int:
        return safe_int(st.session_state.get("budget", 0), 0)
    
    @staticmethod
    def spend(amount: int, description: str, show_toast: bool = True) -> bool:
        amount = safe_int(amount, 0)
        if not validate_budget_input(amount, BudgetManager.get_current(), description):
            return False
        st.session_state.budget = BudgetManager.get_current() - amount
        clamp_budget()
        if show_toast: safe_toast(f"Spent {helper_format_cash(amount)} on {description}")
        return True
    
    @staticmethod
    def add(amount: int, description: str, show_toast: bool = True) -> None:
        amount = safe_int(amount, 0)
        st.session_state.budget = BudgetManager.get_current() + amount
        clamp_budget()
        if show_toast and amount > 0: safe_toast(f"Received {helper_format_cash(amount)}: {description}")
        if description: add_news(description)
    
    @staticmethod
    def calculate_revenue(tier: int, marketing_level: int, inflation: float) -> int:
        base_revenue = {1: 22_000_000, 2: 14_000_000, 3: 6_000_000, 4: 3_000_000}.get(tier, 3_000_000)
        marketing_bonus = safe_int(marketing_level, 0) * 1_500_000
        total = (base_revenue + marketing_bonus) * float(inflation)
        conf_boost = float(st.session_state.get("conf_revenue_boost_mult", 1.0))
        total *= conf_boost
        return int(total)

class OpponentManager:
    @staticmethod
    def get(team_name: str) -> dict:
        if "opponents_db" not in st.session_state: st.session_state.opponents_db = {}
        if team_name not in st.session_state.opponents_db:
            st.session_state.opponents_db[team_name] = {"Prestige": 60, "OVR": 75}
        
        opp = st.session_state.opponents_db[team_name]
        opp.setdefault("Prestige", 60); opp.setdefault("OVR", 75)
        
        if "OffOVR" not in opp or "DefOVR" not in opp:
            base = safe_int(opp.get("OVR", 75), 75)
            # FIX: Deterministic Opponent Stats (V1.3)
            rr = make_deterministic_rng("opp_split", team_name, st.session_state.get("year", 0))
            opp["OffOVR"] = max(50, min(99, base + rr.randint(-3, 3)))
            opp["DefOVR"] = max(50, min(99, base + rr.randint(-3, 3)))
        
        if "Coaches" not in opp or not isinstance(opp.get("Coaches"), dict):
            opp["Coaches"] = {"OC": 5, "DC": 5}
        else:
            opp["Coaches"].setdefault("OC", 5); opp["Coaches"].setdefault("DC", 5)
            
        opp.setdefault("Stadium", 7)
        opp.setdefault("Off", "Pro Style"); opp.setdefault("Def", "Man Coverage")
        return opp
    
    @staticmethod
    def evolve_universe() -> None:
        if "opponents_db" not in st.session_state: return
        for team, data in st.session_state.opponents_db.items():
            base_ovr = safe_int(data.get("OVR", 75), 75)
            wins = int((base_ovr / 100) * 12) + random.randint(-2, 2)
            wins = max(0, min(12, wins))
            prev_prestige = safe_int(data.get("Prestige", 60), 60)
            change = 3 if wins >= 10 else (-3 if wins <= 4 else 0)
            data["Prestige"] = max(20, min(99, prev_prestige + change))
            
            if data["Prestige"] > 80 and wins < 6:
                data["Coaches"] = {"OC": random.randint(7, 9), "DC": random.randint(7, 9)}
            elif data["Prestige"] < 70 and wins > 9:
                data["Coaches"] = {"OC": random.randint(3, 6), "DC": random.randint(3, 6)}
            
            base_from_prestige = int(data["Prestige"] * 0.9)
            data["OVR"] = base_from_prestige + random.randint(-3, 3)
            
            if random.random() < 0.35:
                data.pop("OffOVR", None); data.pop("DefOVR", None)

# ==============================================================================
# OTHER HELPERS
# ==============================================================================
def make_deterministic_rng(*parts) -> random.Random:
    base = (str(st.session_state.get("state_version", "")), str(st.session_state.get("year", "")), str(st.session_state.get("team_name", "")))
    seed_str = "|".join([*base, *[str(p) for p in parts]])
    return random.Random(seed_str)

def game_rng(year: int, week: int, opp: str, mode: str = "PLAY") -> random.Random:
    """V1.3: Stable seed for a specific game instance to prevent reroll abuse."""
    return make_deterministic_rng("game", mode, int(year), int(week), str(opp))

def add_news(msg: str):
    if "news" not in st.session_state or st.session_state.news is None: st.session_state.news = []
    stamp = datetime.datetime.now().strftime("%b %d")
    st.session_state.news.insert(0, {"ts": stamp, "text": msg}) 
    st.session_state.news = st.session_state.news[:40]

def render_news_box():
    with st.sidebar:
        st.divider()
        st.subheader("🗞️ News Wire")
        items = st.session_state.get("news", []) or []
        if not items: 
            st.caption("No headlines yet.")
            return
        
        good_keys = ["win", "wins", "advances", "upgrade", "signs", "committed", "found", "promotes", "hires"]
        bad_keys = ["lose", "loses", "falls", "eliminated", "fired", "pressure", "overdraft"]
        
        for it in items[:15]:
            txt = it if isinstance(it, str) else f"{it.get('ts','')}"
            if isinstance(it, dict) and it.get("text"):
                 txt += f" - {it.get('text','')}"
            
            content_lower = txt.lower()
            css_class = "news-item"
            if any(k in content_lower for k in good_keys): css_class += " news-item-good"
            elif any(k in content_lower for k in bad_keys): css_class += " news-item-bad"
            
            st.markdown(f"<div class='{css_class}'>{txt}</div>", unsafe_allow_html=True)

def html_rank_row(rank, team, wins, losses, conf, is_user):
    bg_class = "rank-grid-user" if is_user else "rank-grid"
    status = "🏆 CFP" if rank <= 12 else ("🎳 BOWL" if wins >= 6 else "❌ OUT")
    return f"""
    <div class='{bg_class}'>
        <div class='rank-num'>#{rank}</div>
        <div class='rank-team'>{team} <span style='font-size:0.8em; color:#666'>({conf})</span></div>
        <div class='rank-rec'><b>{wins}-{losses}</b></div>
        <div class='rank-status'>{status}</div>
    </div>
    """

def get_conferences_map():
    if "conferences_map" not in st.session_state or not isinstance(st.session_state.conferences_map, dict):
        st.session_state.conferences_map = {k: list(v) for k, v in GameConfig.CONFERENCES.items()}
    for k, v in GameConfig.CONFERENCES.items(): st.session_state.conferences_map.setdefault(k, list(v))
    return st.session_state.conferences_map

def get_conference(team: str) -> str:
    conf_map = get_conferences_map()
    for conf, teams in conf_map.items():
        if team in teams: return conf
    return "G5"

def compute_team_needs(roster: dict, k: int = 3) -> list:
    roster = roster or {}
    vals = [(pos, safe_int(roster.get(pos, 75), 75)) for pos in GameConfig.POSITIONS]
    vals.sort(key=lambda x: x[1])
    return [p for p, _ in vals[:max(1, int(k))]]

def role_rating(coach: dict, role: str) -> int:
    if not coach: return 0
    if role == "HC": v = (safe_int(coach.get("off"), 0) + safe_int(coach.get("def"), 0) + safe_int(coach.get("recruit"), 0)) / 3
    elif role == "OC": v = safe_int(coach.get("off"), 0)
    elif role == "DC": v = safe_int(coach.get("def"), 0)
    elif role == "Scout": v = safe_int(coach.get("recruit"), 0)
    else: v = safe_int(coach.get("off"), 0)
    return int(max(0, min(10, round(v))))

def get_bowl_name(user_rank: int) -> str:
    if user_rank <= 14: tier = "High"
    elif user_rank <= 20: tier = "Mid"
    else: tier = "Low"
    return random.choice(GameConfig.BOWL_MAPPING.get(tier, ["Gator Bowl"]))

def get_season_metrics():
    logs = st.session_state.get("season_logs", []) or []
    if not logs: return (0, "N/A", "N/A")
    opp_ovrs = [safe_int(x.get("OppOVR", 70), 70) for x in logs]
    avg_sos = int(round(sum(opp_ovrs) / max(1, len(opp_ovrs))))
    best_win_ovr = -1; best_win_label = "N/A"; worst_loss_ovr = 999; worst_loss_label = "N/A"
    for x in logs:
        opp = x.get("Opponent", "Opponent"); ovr = safe_int(x.get("OppOVR", 70), 70)
        is_win = str(x.get("Score", "")).startswith("W")
        if is_win and ovr > best_win_ovr: best_win_ovr = ovr; best_win_label = f"{opp} (OVR {ovr})"
        if (not is_win) and ovr < worst_loss_ovr: worst_loss_ovr = ovr; worst_loss_label = f"{opp} (OVR {ovr})"
    return (avg_sos, best_win_label, worst_loss_label)

def build_season_summary_dict():
    w = safe_int(st.session_state.record.get("w", 0), 0); l = safe_int(st.session_state.record.get("l", 0), 0)
    sos, best_win, worst_loss = get_season_metrics()
    expect = safe_int(st.session_state.get("expected_wins", 6), 6); delta = w - expect
    final_rank = "NR"
    results = st.session_state.get("selection_sunday_results", []) or []
    for i, t in enumerate(results):
        if t.get("IsUser") or t.get("Team") == st.session_state.team_name: final_rank = f"#{i+1}"; break
    postseason = st.session_state.get("last_postseason_result", "NONE")
    return {"Record": f"{w}-{l}", "SOS": sos, "BestWin": best_win, "WorstLoss": worst_loss, "ExpectedWins": expect, "Delta": delta, "FinalRank": final_rank, "Postseason": postseason}

def generate_hotspots():
   regions = list(GameConfig.REGION_STRENGTH.keys()) or ["South", "Midwest", "West", "North"]
   out = {}
   for r in regions:
       out[r] = random.sample(GameConfig.POSITIONS, k=2)
   return out

def calculate_committee_score(team_name, wins, losses, conf, sos_score):
    score = (wins * 105) - (losses * 115)
    if conf in ["SEC", "Big Ten"]: score += 140
    elif conf in ["ACC", "Big 12"]: score += 80
    score += (sos_score * 3.0)
    if conf in ["G5", "MAC", "Indep"] and losses > 0: 
        score -= 300
    return int(score)

def trophy_icon(name: str) -> str:
    return GameConfig.TROPHY_ICONS.get(name, GameConfig.TROPHY_ICONS.get("Bowl Win", "🎳"))

def award_trophy(trophy_name: str):
    if "trophies" not in st.session_state:
        st.session_state.trophies = []
    st.session_state.trophies.append({
        "Year": st.session_state.year,
        "Name": trophy_name,
        "Icon": trophy_icon(trophy_name)
    })

def render_trophy_gallery(title_text: str = "🏆 Trophy Gallery"):
    st.subheader(title_text)
    trophies = st.session_state.get("trophies", []) or []
    if not trophies:
        st.info("No trophies yet. Win a bowl or a title to start your case.")
        return
    trophies_sorted = sorted(trophies, key=lambda x: int(x.get("Year", 0)), reverse=True)
    cols = st.columns(4)
    for i, t in enumerate(trophies_sorted[:24]):
        with cols[i % 4]:
            icon = t.get("Icon", "🏆")
            name = t.get("Name", "Trophy")
            year = t.get("Year", "?")
            st.markdown(
                f"<div class='trophy-tile'>"
                f"<div style='font-size:2em'>{icon}</div>"
                f"<div style='font-weight:800'>{name}</div>"
                f"<div class='small-muted'>Year {year}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

def render_cfp_bracket_tree(data: dict):
    """V1.3/V1.4 Fixed Bracket with Correct Indentation"""
    st.subheader("🏆 College Football Playoff Bracket")
    
    seeds = data.get("Seeds", ["TBD"]*12)
    matches = data.get("Matches", [])
    round_num = data.get("Round", 1)
    
    # Determine which teams are still alive
    alive_teams = set()
    for m in matches:
        if not m.get("winner"):
            if m.get("t1"): alive_teams.add(m["t1"])
            if m.get("t2"): alive_teams.add(m["t2"])
        else:
            alive_teams.add(m["winner"])
    
    # Add top 4 seeds if round 1
    if round_num == 1:
        for i in range(4):
            if i < len(seeds):
                alive_teams.add(seeds[i])
    
    st.markdown("""
    <style>
    .bracket-container { display: flex; justify-content: space-around; gap: 20px; margin: 20px 0; overflow-x: auto; }
    .bracket-round { display: flex; flex-direction: column; justify-content: space-around; min-width: 200px; }
    .bracket-matchup { background: white; border: 2px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 8px 0; position: relative; }
    .bracket-matchup.active { border-color: #2196F3; box-shadow: 0 0 10px rgba(33, 150, 243, 0.3); }
    .bracket-matchup.completed { background: #f5f5f5; border-color: #4CAF50; }
    .bracket-matchup.user-involved { border: 3px solid #FF9800; background: #FFF3E0; }
    .bracket-seed { display: inline-block; background: #333; color: white; width: 24px; height: 24px; line-height: 24px; text-align: center; border-radius: 50%; font-weight: bold; font-size: 0.8em; margin-right: 8px; }
    .bracket-team { font-weight: bold; color: #333; margin: 4px 0; padding: 4px; display: flex; align-items: center; justify-content: space-between; }
    .bracket-team.winner { background: #E8F5E9; border-left: 4px solid #4CAF50; }
    .bracket-team.loser { color: #999; text-decoration: line-through; }
    .bracket-score { font-weight: bold; margin-left: 10px; color: #666; }
    .bracket-round-title { text-align: center; font-weight: bold; text-transform: uppercase; color: #666; margin-bottom: 10px; font-size: 0.9em; letter-spacing: 1px; }
    .bracket-bye { background: #E3F2FD; border: 2px dashed #2196F3; color: #1976D2; font-style: italic; text-align: center; }
    </style>
    """, unsafe_allow_html=True)
    
    user_team = st.session_state.team_name
    
    if round_num == 1:
        html = "<div class='bracket-container'>"
        html += "<div class='bracket-round'><div class='bracket-round-title'>Opening Round</div>"
        display_order = [matches[3], matches[0], matches[1], matches[2]] if len(matches)>=4 else matches
        for i, m in enumerate(display_order):
            t1, t2 = m.get("t1", "TBD"), m.get("t2", "TBD")
            s1, s2 = m.get("s1", ""), m.get("s2", "")
            winner = m.get("winner")
            matchup_class = "bracket-matchup"
            if winner: matchup_class += " completed"
            if user_team in [t1, t2]: matchup_class += " user-involved"
            html += f"<div class='{matchup_class}'><div class='bracket-team {'winner' if winner == t1 else ('loser' if winner else '')}'><span>{t1}</span>{'<span class=bracket-score>'+str(s1)+'</span>' if s1 else ''}</div><div class='bracket-team {'winner' if winner == t2 else ('loser' if winner else '')}'><span>{t2}</span>{'<span class=bracket-score>'+str(s2)+'</span>' if s2 else ''}</div></div>"
        html += "</div>"
        
        html += "<div class='bracket-round'><div class='bracket-round-title'>Quarterfinals</div>"
        qf_seeds = data.get("QF_Seeds", seeds[:4])
        for i, seed_team in enumerate(qf_seeds):
            matchup_class = "bracket-matchup bracket-bye"
            if user_team == seed_team: matchup_class += " user-involved"
            html += f"<div class='{matchup_class}'><div class='bracket-team'><span><span class='bracket-seed'>{i+1}</span>{seed_team}</span></div><div style='text-align:center; color:#666; font-size:0.85em; margin-top:8px;'>BYE</div></div>"
        html += "</div>"
        
        html += "<div class='bracket-round'><div class='bracket-round-title'>Semifinals</div><div class='bracket-matchup' style='opacity:0.4;'><div style='text-align:center; padding:20px; color:#999;'>TBD</div></div><div class='bracket-matchup' style='opacity:0.4;'><div style='text-align:center; padding:20px; color:#999;'>TBD</div></div></div>"
        html += "</div>"
    
    elif round_num == 2:
        html = "<div class='bracket-container'>"
        html += "<div class='bracket-round'><div class='bracket-round-title'>Quarterfinals</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            t1, t2 = m.get("t1", "TBD"), m.get("t2", "TBD")
            s1, s2 = m.get("s1", ""), m.get("s2", "")
            winner = m.get("winner")
            matchup_class = "bracket-matchup"
            if not winner: matchup_class += " active"
            else: matchup_class += " completed"
            if user_team in [t1, t2]: matchup_class += " user-involved"
            html += f"<div class='{matchup_class}'><div class='bracket-team {'winner' if winner == t1 else ('loser' if winner else '')}'><span><span class='bracket-seed'>{seed_map.get(t1, '?')}</span>{t1}</span>{'<span class=bracket-score>'+str(s1)+'</span>' if s1 else ''}</div><div class='bracket-team {'winner' if winner == t2 else ('loser' if winner else '')}'><span><span class='bracket-seed'>{seed_map.get(t2, '?')}</span>{t2}</span>{'<span class=bracket-score>'+str(s2)+'</span>' if s2 else ''}</div></div>"
        html += "</div>"
        html += "<div class='bracket-round'><div class='bracket-round-title'>Semifinals</div><div class='bracket-matchup' style='opacity:0.6;'><div style='text-align:center; padding:20px; color:#999;'>Awaiting QF Results</div></div><div class='bracket-matchup' style='opacity:0.6;'><div style='text-align:center; padding:20px; color:#999;'>Awaiting QF Results</div></div></div>"
        html += "<div class='bracket-round'><div class='bracket-round-title'>Championship</div><div class='bracket-matchup' style='opacity:0.3;'><div style='text-align:center; padding:30px; color:#999;'>🏆</div></div></div>"
        html += "</div>"
    
    elif round_num == 3:
        html = "<div class='bracket-container'>"
        html += "<div class='bracket-round'><div class='bracket-round-title'>Semifinals</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            t1, t2 = m.get("t1", "TBD"), m.get("t2", "TBD")
            s1, s2 = m.get("s1", ""), m.get("s2", "")
            winner = m.get("winner")
            matchup_class = "bracket-matchup"
            if not winner: matchup_class += " active"
            else: matchup_class += " completed"
            if user_team in [t1, t2]: matchup_class += " user-involved"
            html += f"<div class='{matchup_class}'><div class='bracket-team {'winner' if winner == t1 else ('loser' if winner else '')}'><span><span class='bracket-seed'>{seed_map.get(t1, '?')}</span>{t1}</span>{'<span class=bracket-score>'+str(s1)+'</span>' if s1 else ''}</div><div class='bracket-team {'winner' if winner == t2 else ('loser' if winner else '')}'><span><span class='bracket-seed'>{seed_map.get(t2, '?')}</span>{t2}</span>{'<span class=bracket-score>'+str(s2)+'</span>' if s2 else ''}</div></div>"
        html += "</div>"
        html += "<div class='bracket-round'><div class='bracket-round-title'>National Championship</div><div class='bracket-matchup active' style='padding:30px;'><div style='text-align:center; font-size:2em;'>🏆</div><div style='text-align:center; color:#666; margin-top:10px;'>Awaiting Semifinal Results</div></div></div>"
        html += "</div>"
    
    else: # Championship
        html = "<div class='bracket-container' style='justify-content:center;'>"
        html += "<div class='bracket-round'><div class='bracket-round-title'>National Championship</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            t1, t2 = m.get("t1", "TBD"), m.get("t2", "TBD")
            s1, s2 = m.get("s1", ""), m.get("s2", "")
            winner = m.get("winner")
            matchup_class = "bracket-matchup"
            if not winner: matchup_class += " active"
            else: matchup_class += " completed"
            if user_team in [t1, t2]: matchup_class += " user-involved"
            html += f"<div class='{matchup_class}' style='min-width:300px;'><div style='text-align:center; font-size:1.5em; margin-bottom:10px;'>🏆</div><div class='bracket-team {'winner' if winner == t1 else ('loser' if winner else '')}'><span><span class='bracket-seed'>{seed_map.get(t1, '?')}</span>{t1}</span>{'<span class=bracket-score>'+str(s1)+'</span>' if s1 else ''}</div><div class='bracket-team {'winner' if winner == t2 else ('loser' if winner else '')}'><span><span class='bracket-seed'>{seed_map.get(t2, '?')}</span>{t2}</span>{'<span class=bracket-score>'+str(s2)+'</span>' if s2 else ''}</div></div>"
        html += "</div></div>"
    
    st.markdown(html, unsafe_allow_html=True)

def calculate_saban_score(career_stats, prestige):
    return int(
        (career_stats.get("w", 0) * 1) +
        (career_stats.get("bowl_w", 0) * 5) +
        (career_stats.get("titles", 0) * 50) +
        (prestige * 0.5)
    )

def apply_conference_move(to_conf: str, boost_mult: float):
    conf_map = get_conferences_map()
    team = st.session_state.team_name
    cur_conf = st.session_state.team_conf
    if cur_conf in conf_map and team in conf_map[cur_conf]:
        conf_map[cur_conf].remove(team)
    if to_conf not in conf_map:
        conf_map[to_conf] = []
    if team not in conf_map[to_conf]:
        conf_map[to_conf].append(team)
    st.session_state.team_conf = to_conf
    st.session_state.conf_revenue_boost_mult = float(boost_mult)
    add_news(f"{team} joins the {to_conf}.")

def apply_roster_attrition():
    attrition_log = []
    for p in GameConfig.POSITIONS:
        current = st.session_state.roster[p]
        base_loss = random.randint(3, 7)
        talent_surplus = max(0, current - 75)
        draft_loss = int(talent_surplus * 0.35)
        total_loss = base_loss + draft_loss
        new_val = max(40, current - total_loss)
        st.session_state.roster[p] = new_val
        attrition_log.append(f"{p}: -{total_loss}")
    add_news(f"Graduation & Draft departures: {', '.join(attrition_log)}")

def end_regular_season_and_stay_on_results():
    if st.session_state.season_end_ready:
        return
    st.session_state.season_simulated = True
    st.session_state.season_end_ready = True
    rev = BudgetManager.calculate_revenue(
        st.session_state.school_tier,
        st.session_state.facilities["Marketing"],
        st.session_state.inflation
    )
    BudgetManager.add(rev, f"End of Regular Season Payout", show_toast=False)
    st.session_state.revenue_report = f"End of Regular Season Payout: +{helper_format_cash(rev)}"
    add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")
    st.session_state.ai_records = simulate_ai_regular_season_seeded(st.session_state.year)
    st.session_state.game_state = GameState.SEASON_END

def normalize_shares(shares: dict):
    def _val(pos):
        try:
            return max(0.0, float(shares.get(pos, 0.0)))
        except Exception:
            return 0.0
    total = sum(_val(p) for p in GameConfig.POSITIONS)
    if total <= 0:
        return {p: 100.0 / len(GameConfig.POSITIONS) for p in GameConfig.POSITIONS}
    return {p: (_val(p) / total) * 100.0 for p in GameConfig.POSITIONS}

# ==============================================================================
# ZONE 3: ENGINE
# ==============================================================================

def engine_generate_coach(role, tier):
    cost = random.randint(4_000_000, 8_000_000) if tier == 1 else random.randint(500_000, 3_500_000)
    trait_pool = list(GameConfig.COACH_TRAITS.keys())
    if role == "OC": trait_pool = ["Air Raid", "Smashmouth", "Pro Style", "Recruiter", "Tactician"]
    base = 8 if tier == 1 else (5 if tier == 2 else 2)
    return {"name": generate_coach_name(), "role": role, "off": min(10, base + random.randint(0, 3)), "def": min(10, base + random.randint(0, 3)), "recruit": min(10, base + random.randint(0, 3)), "trait": random.choice(trait_pool), "salary": cost, "history": "External Hire", "scouted": False}

def engine_generate_roster(tier, base_ovr=None):
    base = base_ovr if base_ovr is not None else (90 if tier == 1 else (82 if tier == 2 else 74))
    roster = {}
    for p in GameConfig.POSITIONS: roster[p] = min(99, max(40, int(base + random.randint(-4, 4))))
    return roster

def engine_generate_schedule(my_team, my_conf, rival):
    conf_map = get_conferences_map()
    year_seed = int(st.session_state.get("year", 0) or 0)
    seed_str = f"{my_team}|{my_conf}|{rival}|{year_seed}"
    rng = random.Random(seed_str)

    conf_foes = [t for t in conf_map.get(my_conf, conf_map.get("G5", [])) if t != my_team]
    schedule = rng.sample(conf_foes, min(8, len(conf_foes)))

    pool = [t for t in GameConfig.ALL_TEAMS if t != my_team and t not in schedule]
    rng.shuffle(pool)

    for opp in pool:
        if len(schedule) >= 12: break
        schedule.append(opp)

    if rival in GameConfig.ALL_TEAMS and rival != my_team and rival not in schedule:
        if len(schedule) >= 12: schedule[-1] = rival
        else: schedule.append(rival)
    elif rival in schedule:
        schedule.remove(rival)
        schedule.append(rival)

    if len(schedule) < 12:
        pad_pool = [t for t in GameConfig.ALL_TEAMS if t != my_team and t not in schedule]
        rng.shuffle(pad_pool)
        schedule.extend(pad_pool[: max(0, 12 - len(schedule))])

    rng.shuffle(schedule)
    return schedule[:12]

def get_tier_bonus(rating):
    if rating >= 8: return 3
    if rating <= 4: return -3
    return 0

def home_field_points(stadium_level: int) -> float:
    lvl = int(stadium_level)
    if lvl <= 6: return 0.0
    if lvl <= 8: return 2.5
    return 4.0

def compute_team_unit_ratings(roster: dict, staff: dict, facilities: dict):
    roster = roster or {}; staff = staff or {}; facilities = facilities or {}
    r = {p: safe_int(roster.get(p, 75), 75) for p in GameConfig.POSITIONS}
    oc = safe_int((staff.get("OC") or {}).get("off", 3), 3)
    dc = safe_int((staff.get("DC") or {}).get("def", 3), 3)
    training = safe_int(facilities.get("Training", 1), 1)
    off = (r["QB"] * 0.34) + (r["OL"] * 0.26) + ((r["RB"] + r["WR"]) / 2 * 0.40)
    deff = (r["DL"] * 0.32) + (r["LB"] * 0.28) + (r["DB"] * 0.40)
    off += oc * 1.2; deff += dc * 1.2; off += training * 0.8; deff += training * 0.8
    return (int(max(40, min(99, round(off)))), int(max(40, min(99, round(deff)))), int(max(40, min(99, round((sum(r.values()) / len(r)) if r else 75)))))

def engine_play_game_v8(my_off, my_def, opp_off, opp_def, staff, schemes, opp_schemes, game_plan, opp_coaches, is_home, is_rival, my_stadium_level, opp_stadium_level, rng=None):
    rng = rng or random.Random()
    
    # V1.1: TALENT WEIGHT INCREASED TO 0.75
    my_edge = (my_off - opp_def) * 0.75
    opp_edge = (opp_off - my_def) * 0.75
    
    scheme_bonus_my = scheme_bonus_opp = 0.0
    my_off_s = schemes.get("Off", "Pro Style"); opp_def_s = opp_schemes.get("Def", "Man Coverage")

    if GameConfig.OFF_COUNTERED_BY.get(my_off_s) == opp_def_s: scheme_bonus_my -= 2.5; scheme_bonus_opp += 1.0
    if GameConfig.DEF_COUNTERS.get(opp_def_s) == my_off_s: scheme_bonus_my += 2.5; scheme_bonus_opp -= 1.0

    oc_obj = safe_dict(staff.get("OC")); dc_obj = safe_dict(staff.get("DC"))
    my_oc = safe_int(oc_obj.get("off", 3), 3); my_dc = safe_int(dc_obj.get("def", 3), 3)
    opp_coaches = safe_dict(opp_coaches)
    opp_oc = safe_int(opp_coaches.get("OC", 5), 5); opp_dc = safe_int(opp_coaches.get("DC", 5), 5)

    coaching_my = (get_tier_bonus(my_oc) - get_tier_bonus(opp_dc)) * 1.20
    coaching_opp = (get_tier_bonus(opp_oc) - get_tier_bonus(my_dc)) * 1.20

    hc_trait = safe_dict(staff.get("HC")).get("trait", "None")
    if hc_trait == "Tactician": coaching_my += 0.9
    elif hc_trait == "Recruiter": coaching_my += 0.25

    oc_trait = safe_dict(staff.get("OC")).get("trait", "None")
    if oc_trait in ["Air Raid", "Smashmouth", "Pro Style"] and oc_trait == my_off_s: scheme_bonus_my += 1.0

    hf = home_field_points(my_stadium_level) if is_home else 0.0
    opp_hf = home_field_points(opp_stadium_level) if not is_home else 0.0

    var_mult = 1.0
    if is_rival: var_mult *= 1.35
    if game_plan == "Aggressive": var_mult *= 1.25
    elif game_plan == "Conservative": var_mult *= 0.85

    base_pts = 27.5
    exp_my = base_pts + my_edge + scheme_bonus_my + coaching_my + hf
    exp_opp = base_pts + opp_edge + scheme_bonus_opp + coaching_opp + opp_hf
    exp_my = max(10, min(50, exp_my)); exp_opp = max(10, min(50, exp_opp))

    # V1.1: VARIANCE REDUCED TO 5.5
    my_score = int(round(rng.gauss(exp_my, 5.5 * var_mult)))
    opp_score = int(round(rng.gauss(exp_opp, 5.5 * var_mult)))

    if my_score == opp_score:
        my_score += rng.choice([0, 3, 7]); opp_score += rng.choice([0, 0, 3])

    my_score = max(0, min(70, my_score)); opp_score = max(0, min(70, opp_score))
    explain = {"my_off": my_off, "my_def": my_def, "opp_off": opp_off, "opp_def": opp_def, "my_edge": float(my_edge), "opp_edge": float(opp_edge), "scheme_my": float(scheme_bonus_my), "scheme_opp": float(scheme_bonus_opp), "coach_my": float(coaching_my), "coach_opp": float(coaching_opp), "home_field": float(hf), "plan": game_plan}
    stats = {"qb_duel": [int((st.session_state.get("roster", {}) or {}).get("QB", 75)), int(max(60, min(99, opp_off)))], "off_vs_def": [int(my_off), int(opp_def)], "def_vs_off": [int(my_def), int(opp_off)], "staff": [f"{my_oc}/{my_dc}", f"{opp_oc}/{opp_dc}"], "raw_roster": int((my_off + my_def) / 2)}
    return {"result": "W" if my_score > opp_score else "L", "score": f"{my_score}-{opp_score}", "stats": stats, "explain": explain}

def simulate_ai_regular_season_seeded(seed: int):
    rnd = random.Random(seed); results = []
    if len(st.session_state.opponents_db) < len(GameConfig.ALL_TEAMS):
        for t in GameConfig.ALL_TEAMS:
            if t not in st.session_state.opponents_db: st.session_state.opponents_db[t] = {"Prestige": 60, "OVR": 75}

    for team in sorted(st.session_state.opponents_db.keys()):
        if team == st.session_state.team_name: continue
        data = st.session_state.opponents_db[team]; prestige = data.get("Prestige", 60); conf = get_conference(team)
        if prestige > 90: wins = rnd.choices([12, 11, 10, 9], weights=[10, 30, 40, 20])[0]
        elif prestige > 80: wins = rnd.choices([11, 10, 9, 8, 7], weights=[5, 20, 35, 30, 10])[0]
        elif prestige > 60: wins = rnd.choices([9, 8, 7, 6, 5], weights=[10, 25, 30, 25, 10])[0]
        else: wins = rnd.choices([6, 5, 4, 3, 2], weights=[10, 30, 30, 20, 10])[0]
        losses = 12 - wins
        base_sos = 80 if conf == "SEC" else 78 if conf == "Big Ten" else 72 if conf in ["ACC", "Big 12"] else 60
        sos = base_sos + rnd.randint(-5, 5)
        results.append({"Team": team, "Wins": wins, "Losses": losses, "Conf": conf, "Prestige": prestige, "SOS": sos})
    return results

# ==============================================================================
# ZONE 4: STATE MANAGEMENT
# ==============================================================================
def sync_team_ratings():
    if "roster" in st.session_state and "staff" in st.session_state and "facilities" in st.session_state:
        try:
            res = compute_team_unit_ratings(st.session_state.roster, st.session_state.staff, st.session_state.facilities)
            st.session_state.team_off = res[0]; st.session_state.team_def = res[1]; st.session_state.team_rating = res[2]
        except Exception:
            st.session_state.team_off = int(st.session_state.get("team_off", 75) or 75)
            st.session_state.team_def = int(st.session_state.get("team_def", 75) or 75)
            st.session_state.team_rating = int(st.session_state.get("team_rating", 75) or 75)

def migrate_state():
    if "state_version" not in st.session_state: st.session_state.state_version = 0.0
    if isinstance(st.session_state.get("top8_resolved"), list): st.session_state.top8_resolved = set(st.session_state.top8_resolved)

    defaults = {
        "year": 2026, "prestige": 60, "job_security": 75, "expected_wins": 6, "tenure": 1,
        "history": [], "schedule": [], "season_simulated": False, "active_transfers": {p: False for p in GameConfig.POSITIONS},
        "inflation": 1.0, "revenue_report": None, "postseason_data": {"Type": None, "Rank": 0, "Round": 0, "Matches": []},
        "team_needs": [], "game_plan": "Normal", "week_index": 0, "news": [], "offseason_step": 1,
        "nil_class": [], "hs_total_spend": 0, "hs_shares": {p: 100.0 / len(GameConfig.POSITIONS) for p in GameConfig.POSITIONS},
        "hs_spend_by_pos": {p: 0 for p in GameConfig.POSITIONS}, "hs_alloc_by_pos": {p: 0 for p in GameConfig.POSITIONS},
        "top8": [], "top8_resolved": set(), "trophies": [], "conf_revenue_boost_mult": 1.0,
        "pending_invite": None, "season_end_ready": False, "booster_rating": 50, "ai_records": [],
        "selection_sunday_results": [], "last_postseason_result": "NONE",
        "ad_name": "Coach Prime", "team_name": "Unknown U", "team_color": "#333333", "team_conf": "G5",
        "team_rival": "Rival", "home_region": "South", "school_tier": 3, "achievements": [], "milestone_log": [],
        "conferences_map": {k: list(v) for k,v in GameConfig.CONFERENCES.items()},
        "hs_last_results": None, "recruiting_summary": None,
        "career_stats": {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0},
        "my_schemes": {"Off": "Pro Style", "Def": "Man Coverage"},
        "candidates": {}, "opponents_db": {}, "season_logs": [], "budget": 0, "staff": {}, "stars": [],
        "last_known_team_name": None, "last_known_team_color": None, "retention_data": []
    }

    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

    for k in ["year", "budget", "prestige", "job_security", "expected_wins", "tenure", "week_index", "booster_rating", "school_tier"]:
        try: st.session_state[k] = int(st.session_state.get(k, 0) or 0)
        except Exception: st.session_state[k] = int(defaults.get(k, 0) or 0)

    st.session_state.roster = st.session_state.get("roster", {}) or {p: 75 for p in GameConfig.POSITIONS}
    for p in GameConfig.POSITIONS:
        if p not in st.session_state.roster: st.session_state.roster[p] = 75

    st.session_state.staff = st.session_state.get("staff", {}) or {}
    st.session_state.facilities = st.session_state.get("facilities", {}) or {"Marketing": 1, "Training": 1, "Stadium": 1}
    for k, default_val in {"Marketing": 1, "Training": 1, "Stadium": 1}.items():
        if k not in st.session_state.facilities or st.session_state.facilities[k] in [None, ""]:
            st.session_state.facilities[k] = default_val

    st.session_state.record = st.session_state.get("record", {}) or {"w": 0, "l": 0}
    st.session_state.hotspots = st.session_state.get("hotspots", {}) or generate_hotspots()
    st.session_state.team_needs = st.session_state.get("team_needs", []) or compute_team_needs(st.session_state.roster, k=3)

    get_conferences_map()
    tc = st.session_state.team_conf
    if tc not in st.session_state.conferences_map: st.session_state.conferences_map[tc] = []
    if st.session_state.team_name not in st.session_state.conferences_map[tc]:
        st.session_state.conferences_map[tc].append(st.session_state.team_name)

    # Initialize recruiting inputs in session state if missing
    for p in GameConfig.POSITIONS:
        key = f"hs_pos_input_{p}_v28"
        if key not in st.session_state:
            st.session_state[key] = int(st.session_state.get("hs_alloc_by_pos", {}).get(p, 0) or 0)

    sync_team_ratings()
    st.session_state.state_version = STATE_VERSION
    
    try:
        tn = st.session_state.get("team_name")
        if tn and tn != "Unknown U":
            st.session_state["last_known_team_name"] = tn
            st.session_state["last_known_team_color"] = st.session_state.get("team_color", "#333333")
    except Exception: pass

    def _is_json_safe(x):
        if x is None or isinstance(x, (bool, int, float, str)): return True
        if isinstance(x, (list, tuple)): return all(_is_json_safe(i) for i in x)
        if isinstance(x, dict): return all(isinstance(k, str) and _is_json_safe(v) for k, v in x.items())
        if isinstance(x, set): return all(_is_json_safe(i) for i in x)
        return False

def init_session_state_defaults():
    if "game_state" not in st.session_state: st.session_state.game_state = GameState.SETUP
    migrate_state()

# ==============================================================================
# ZONE 5: SAVE/LOAD UI
# ==============================================================================
def safe_json_default(obj):
    if isinstance(obj, set): return list(obj)
    if isinstance(obj, (datetime.date, datetime.datetime)): return obj.isoformat()
    return str(obj)

def render_system_sidebar():
    with st.sidebar:
        st.header("💾 CEO System"); st.caption(f"Version {STATE_VERSION}")
        if st.button("Export Save File"):
            state_copy = dict(st.session_state)
            if "top8_resolved" in state_copy: state_copy["top8_resolved"] = list(state_copy["top8_resolved"])
            export_data = {k: v for k, v in state_copy.items() if k in ALLOWED_SAVE_KEYS}
            json_str = json.dumps(export_data, default=safe_json_default)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            st.download_button(label="📥 Download JSON", data=json_str, file_name=f"CFB_CEO_Save_{timestamp}.json", mime="application/json")
        
        uploaded_file = st.file_uploader("Import Save File", type=["json"])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                for k, v in data.items():
                    if k in ALLOWED_SAVE_KEYS:
                        if k == "top8_resolved": st.session_state[k] = set(v) if isinstance(v, list) else set()
                        else: st.session_state[k] = v
                migrate_state(); st.session_state.candidates = {}; sync_team_ratings()
                st.success("Save Loaded Successfully! Reloading..."); time.sleep(1); st.rerun()
            except Exception as e:
                st.error(f"Error loading save: {e}")
                
        # V1.1: Render News in Sidebar
        render_news_box()

# ==============================================================================
# ZONE 6: UI - RECRUITING COMPONENTS
# ==============================================================================

def render_hs_results_summary() -> bool:
    last = st.session_state.get("hs_last_results", None)
    if not last: return False
    st.success("✅ HS Outreach Complete — Results Summary")
    cA, cB, cC = st.columns(3)
    cA.metric("Spent", helper_format_cash(last.get("spent", 0)))
    cB.metric("Booster Bonus", helper_format_cash(last.get("booster_bonus", 0)))
    cC.metric("Hidden Gems", int(last.get("gem_count", 0)))
    st.markdown("### 📈 Position Improvements")
    pos_changes = last.get("pos_changes", {}) or {}
    for p in GameConfig.POSITIONS:
        delta = pos_changes.get(p, 0)
        st.write(f"{p}: **{format_position_delta(delta)}**")
    
    # Corrected Step flow: 3 -> 4
    if st.button("Dismiss & Continue to Top-8 →", type="primary"):
        st.session_state.hs_last_results = None
        st.session_state.offseason_step = 4
        st.rerun()
        
    st.divider()
    return True

def cb_set_balanced():
    for p in GameConfig.POSITIONS:
        st.session_state[f"hs_pos_input_{p}_v28"] = 500_000

def cb_set_needs():
    needs = st.session_state.get("team_needs", [])
    for p in GameConfig.POSITIONS:
        val = 1_250_000 if p in needs else 100_000
        st.session_state[f"hs_pos_input_{p}_v28"] = val

def cb_clear_all():
    for p in GameConfig.POSITIONS:
        st.session_state[f"hs_pos_input_{p}_v28"] = 0

def execute_hs_outreach(budget: int, alloc: dict, needs: List[str]) -> None:
    if not BudgetManager.spend(budget, "HS recruiting", show_toast=False): return
    res = process_hs_outreach(budget, alloc, st.session_state.staff, st.session_state.prestige, st.session_state.inflation, st.session_state.hotspots, st.session_state.home_region, needs, is_dollars=True)
    
    if res["booster_bonus"] > 0:
        BudgetManager.add(res["booster_bonus"], "Boosters go wild over surprise recruits!", show_toast=True)
    
    for p, gain in res["roster_updates"].items():
        loss = random.randint(1, 4)
        current = safe_int(st.session_state.roster.get(p, 75), 75)
        st.session_state.roster[p] = max(40, min(99, current - loss + int(gain)))
    
    if res["gems"]:
        st.session_state.stars.extend(res["gems"])
        add_news(f"Scouts found {len(res['gems'])} hidden gems!")
    
    st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
    sync_team_ratings()
    st.session_state.hs_last_results = {"spent": int(res.get("spent", 0) or 0), "booster_bonus": int(res.get("booster_bonus", 0) or 0), "pos_changes": dict(res.get("roster_updates", {}) or {}), "gem_count": len(res["gems"])}
    safe_toast("HS Outreach complete! See results above.")
    st.rerun()

def show_offseason_hs_outreach():
    if render_hs_results_summary(): return
    st.subheader("3) HS Outreach: The War Room")
    st.write("Directly invest in position groups to find talent.")
    
    hot = st.session_state.hotspots.get(st.session_state.home_region, [])
    needs = st.session_state.get("team_needs", [])
    max_budget = BudgetManager.get_current()
    
    current_spend = 0
    allocations = {}
    for p in GameConfig.POSITIONS:
        key = f"hs_pos_input_{p}_v28"
        val = safe_int(st.session_state.get(key, 0))
        current_spend += val
        allocations[p] = val
        
    remaining = max_budget - current_spend
    
    c1, c2, c3 = st.columns([1, 1, 2])
    c1.metric("Team Budget", helper_format_cash(max_budget))
    c2.metric("Allocated", helper_format_cash(current_spend))
    if remaining >= 0:
        c3.metric("Remaining", helper_format_cash(remaining), delta="Safe")
    else:
        c3.metric("Overdraft", helper_format_cash(remaining), delta="-Over Budget", delta_color="inverse")

    st.divider()
    
    b1, b2, b3 = st.columns(3)
    b1.button("⚖️ Auto-Fill: Balanced ($3.5M)", on_click=cb_set_balanced, use_container_width=True)
    b2.button("🎯 Auto-Fill: Needs ($4M)", on_click=cb_set_needs, use_container_width=True)
    b3.button("❌ Clear All", on_click=cb_clear_all, use_container_width=True)
    
    st.write("### Position Investment")
    cols = st.columns(4)
    for idx, p in enumerate(GameConfig.POSITIONS):
        with cols[idx % 4]:
            badges = ""
            if p in needs: badges += " 🔴"
            if p in hot: badges += " 🔥"
            st.number_input(
                f"{p}{badges}",
                min_value=0,
                max_value=max_budget,
                step=100_000,
                format="%d",
                key=f"hs_pos_input_{p}_v28"
            )

    st.divider()
    st.markdown(f"<div style='text-align: center; font-size: 1.2em; margin-bottom: 10px;'>Total Investment: <b>{helper_format_cash(current_spend)}</b></div>", unsafe_allow_html=True)
    
    disabled_confirm = (remaining < 0) or (current_spend == 0)
    if st.button("Confirm & Run Recruiting 🚀", type="primary", disabled=disabled_confirm, use_container_width=True):
        st.session_state.hs_total_spend = current_spend
        st.session_state.hs_alloc_by_pos = allocations
        execute_hs_outreach(current_spend, allocations, needs)

def generate_nil_class_15(team_needs: list):
    def mk(tier: int, pos: str):
        if tier == 1: rating = random.randint(90, 99); ask = int(random.randint(2_500_000, 9_000_000) * (1.0 + (rating - 90) / 25)); badge = "Tier 1"
        elif tier == 2: rating = random.randint(84, 89); ask = int(random.randint(900_000, 3_500_000) * (1.0 + (rating - 84) / 35)); badge = "Tier 2"
        else: rating = random.randint(76, 83); ask = int(random.randint(200_000, 1_200_000) * (1.0 + (rating - 76) / 40)); badge = "Tier 3"
        return {"id": random.randint(10_000, 99_999), "tier": tier, "tier_label": badge, "name": generate_name(), "pos": pos, "rating": rating, "ask": ask, "trait": random.choice(GameConfig.TRAITS), "status": "AVAILABLE"}
    needs = team_needs[:] if team_needs else GameConfig.POSITIONS[:]; pool=[]
    for _ in range(5): pos = random.choice(needs if random.random() < 0.70 else GameConfig.POSITIONS); pool.append(mk(1, pos))
    for _ in range(5): pos = random.choice(needs if random.random() < 0.60 else GameConfig.POSITIONS); pool.append(mk(2, pos))
    for _ in range(5): pos = random.choice(needs if random.random() < 0.50 else GameConfig.POSITIONS); pool.append(mk(3, pos))
    pool.sort(key=lambda x: (x["tier"], -x["rating"])); return pool

def show_offseason_nil_v8():
    st.subheader("2) NIL Prospects (Class of 15)")
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
                if BudgetManager.spend(p["ask"], f"sign {p['pos']} {p['name']}"):
                    st.session_state.roster[p["pos"]] = max(st.session_state.roster[p["pos"]], p["rating"])
                    p["status"] = "SIGNED"
                    add_news(f"{st.session_state.team_name} signs NIL {p['tier_label']} {p['pos']} {p['name']} ({p['rating']}).")
                    sync_team_ratings(); safe_toast("Signed ✔️"); st.rerun()

def process_hs_outreach(total_spend: int, shares_or_alloc: dict, staff: dict, prestige: int, inflation: float, hotspots: dict, home_region: str, team_needs: list, is_dollars: bool = False):
    results = {"roster_updates": {}, "gems": [], "booster_bonus": 0, "spent": int(total_spend)}
    total_spend = max(0, int(total_spend))
    staff = staff or {}
    scout = safe_int((staff.get("Scout") or {}).get("recruit", 1), 1)
    hc_trait = (staff.get("HC") or {}).get("trait", "None")

    efficiency = 0.85 if scout >= 8 else (1.0 if scout >= 5 else 1.15)
    base_cost = 900_000 * float(inflation) * float(efficiency)
    hot_positions = hotspots.get(home_region, [])
    
    if is_dollars:
        allocated = 0
        for p in GameConfig.POSITIONS:
            try: allocated += int(float(shares_or_alloc.get(p, 0) or 0))
            except: pass
        spent = max(0, min(total_spend, allocated))
    else:
        spent = total_spend
    
    results = {"roster_updates": {}, "gems": [], "booster_bonus": 0, "spent": int(spent)}

    for pos in GameConfig.POSITIONS:
        raw = float(shares_or_alloc.get(pos, 0.0) or 0.0)
        if is_dollars: amt = max(0.0, raw)
        else: pct = raw; amt = total_spend * (pct / 100.0)
        
        if amt <= 0: results["roster_updates"][pos] = -random.randint(1, 3); continue
        cap = base_cost * 2.0; effective_spend = cap * (1 - math.exp(-amt / cap))
        spend_ratio = effective_spend / max(1.0, base_cost); dim = spend_ratio ** 0.85
        pipeline_bonus = 1.15 if pos in hot_positions else 1.0
        need_bonus = 1.25 if pos in team_needs else 1.0
        prestige_factor = max(0.85, min(1.20, (prestige / 75) ** 0.35))
        change = dim * pipeline_bonus * need_bonus * prestige_factor
        change = max(-4, min(12, change))
        if hc_trait == "Recruiter": change *= 1.08
        gem_chance = 0.08
        if pos in team_needs: gem_chance += 0.07
        if pos in hot_positions: gem_chance += 0.05
        if scout >= 8: gem_chance += 0.03
        if hc_trait == "Recruiter": gem_chance += 0.02
        if amt > base_cost * 1.25 and random.random() < gem_chance:
            star = generate_star_player(pos, tier=1); star["name"] += " (GEM)"; results["gems"].append(star)
            change += 5; results["booster_bonus"] += 250_000 + random.randint(0, 250_000)
        results["roster_updates"][pos] = change
    return results

def generate_top8_prospects(team_needs: list):
    recruits = []
    for _ in range(8):
        pos = random.choice(team_needs if team_needs and random.random() < 0.65 else GameConfig.POSITIONS)
        rating = random.randint(90, 99)
        ask = int(random.randint(2_000_000, 8_000_000) * (1.0 + (rating - 90) / 35))
        recruits.append({"id": random.randint(10_000, 99_999), "name": generate_name(), "pos": pos, "rating": rating, "ask": ask, "trait": random.choice(GameConfig.TRAITS), "status": "OPEN", "note": ""})
    recruits.sort(key=lambda x: x["rating"], reverse=True); return recruits

def top8_commit_chance(recruit: dict, spend_by_pos: dict, staff: dict, prestige: int) -> float:
    staff = staff or {}
    scout = safe_int((staff.get("Scout") or {}).get("recruit", 1), 1)
    hc_trait = (staff.get("HC") or {}).get("trait", "None")

    chance = 0.18
    chance += (max(40, min(99, prestige)) - 60) * 0.004
    chance += (scout - 5) * 0.02
    if hc_trait == "Recruiter": chance += 0.05
    pos = recruit["pos"]; spend = float(spend_by_pos.get(pos, 0.0))
    chance += min(0.20, spend / 10_000_000)
    return max(0.05, min(0.80, chance))

def show_offseason_top8_v8():
    st.subheader("4) Top-8 Battles — Close on Elites")
    needs = st.session_state.get("team_needs", [])
    current_budget = int(st.session_state.get("budget", 0) or 0)
    if not st.session_state.get("top8"):
        st.session_state.top8 = generate_top8_prospects(needs)
        add_news("Top-8 board posted: 8 elite prospects.")
    if "top8_resolved" not in st.session_state: st.session_state.top8_resolved = set()

    st.markdown(f"<div class='nil-alert'>Available: <b>{helper_format_cash(current_budget)}</b></div>", unsafe_allow_html=True)
    
    for r in st.session_state.top8:
        rid = int(r["id"]); pos = r["pos"]; ask = int(r["ask"])
        already = rid in st.session_state.top8_resolved
        c1, c2, c3 = st.columns([4, 2, 2])
        with c1: 
            st.markdown(f"⭐ **{pos} {r['name']} ({r['rating']})**")
            st.caption(f"Wants: {helper_format_cash(ask)} | Trait: {r.get('trait','')}")
        with c2:
            row_budget = int(st.session_state.get("budget", 0) or 0)
            max_offer = max(0, min(row_budget, max(ask * 2, 250_000)))
            default_offer = int(r.get("offer", 0) or 0)
            default_offer = max(0, min(default_offer, max_offer))
            offer = st.slider(f"Offer vs Want ({helper_format_cash(ask)})", 0, max_offer, default_offer, step=250_000, key=f"offer_{rid}")
            r["offer"] = int(offer)
            
            offer_val = int(r.get("offer", 0) or 0)
            if offer_val <= 0: st.caption("Set an offer to pitch.")
            elif offer_val < ask: st.warning("Below ask")
            elif offer_val < int(ask * 1.25): st.success("Meets ask")
            else: st.success("Overpay (strong pitch)")

        with c3:
            if r.get("status") == "COMMITTED": st.success("✅ COMMITTED")
            elif r.get("status") == "LOST": st.error("❌ LOST")
            else:
                chance = top8_commit_chance(
                    r, 
                    {pos: float(r.get("offer", 0) or 0)}, 
                    st.session_state.staff, 
                    st.session_state.prestige
                )
                st.write(f"Chance: **{int(chance*100)}%**")
                if st.button("Pitch", key=f"pitch_{rid}", disabled=already or r["offer"]<=0):
                    if BudgetManager.spend(r["offer"], "pitch"):
                        if random.random() < chance:
                            r["status"] = "COMMITTED"
                            st.session_state.roster[pos] = max(st.session_state.roster[pos], r["rating"])
                            safe_toast("Committed!")
                        else:
                            r["status"] = "LOST" 
                            safe_toast("Lost recruit.")
                        st.session_state.top8_resolved.add(rid)
                        st.rerun()

    st.divider()
    if st.button("Simulate Remaining Pitches"):
        for r in st.session_state.top8:
            rid = int(r["id"])
            if rid not in st.session_state.top8_resolved and r.get("status") == "OPEN":
                st.session_state.top8_resolved.add(rid)
                r["status"] = "LOST" 
        st.rerun()

# --- V1.5/V1.6: RETENTION RANSOM LOGIC ---
def generate_retention_demands() -> List[Dict]:
    """Generates 3 random retention demands from current roster."""
    demands = []
    # Pick 3 random positions
    targets = random.sample(GameConfig.POSITIONS, 3)
    
    for pos in targets:
        current_rating = st.session_state.roster.get(pos, 75)
        # Cost formula: (Rating - 60) * 50k, min 250k
        # Example: 90 rating -> 30 * 50k = 1.5M
        base_cost = max(250_000, (current_rating - 60) * 50_000)
        # Add random variance
        cost = int(base_cost * random.uniform(0.8, 1.2))
        
        demands.append({
            "pos": pos,
            "rating": current_rating,
            "cost": cost,
            "status": "PENDING" # PENDING, PAID, LEFT
        })
    return demands

def show_retention_phase():
    st.subheader("1) Retention Ransom: The Transfer Portal")
    st.write("Before recruiting new talent, you must pay to keep your current stars.")
    
    if "retention_data" not in st.session_state or not st.session_state.retention_data:
        st.session_state.retention_data = generate_retention_demands()
    
    demands = st.session_state.retention_data
    pending_count = sum(1 for d in demands if d["status"] == "PENDING")
    
    cols = st.columns(3)
    for i, d in enumerate(demands):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"### {d['pos']} Group")
                st.metric("Current Rating", d['rating'])
                st.metric("Demanding", helper_format_cash(d['cost']))
                
                if d["status"] == "PENDING":
                    if st.button(f"Pay to Keep", key=f"pay_{i}"):
                        if BudgetManager.spend(d["cost"], f"Retention: {d['pos']}"):
                            d["status"] = "PAID"
                            safe_toast(f"{d['pos']} group stays!")
                            st.rerun()
                    
                    if st.button(f"Let them Transfer", key=f"leave_{i}"):
                        d["status"] = "LEFT"
                        # Penalty: Lose 6-9 points
                        loss = random.randint(6, 9)
                        st.session_state.roster[d['pos']] = max(40, d['rating'] - loss)
                        add_news(f"Star players transfer out! {d['pos']} drops -{loss}.")
                        st.rerun()
                elif d["status"] == "PAID":
                    st.success("✅ RETAINED")
                else:
                    st.error("❌ LEFT TEAM")

    st.divider()
    if pending_count == 0:
        if st.button("Continue to NIL Recruiting →", type="primary"):
            st.session_state.offseason_step = 2
            st.rerun()
    else:
        st.info("Resolve all retention demands to proceed.")

def compute_recruiting_class_grade():
    nil = st.session_state.get("nil_class", []) or []
    top8 = st.session_state.get("top8", []) or []
    stars = st.session_state.get("stars", []) or []
    tier_points = 0; tier_counts = {1: 0, 2: 0, 3: 0}
    for p in nil:
        if p.get("status") == "SIGNED":
            tier = int(p.get("tier", 3)); tier_counts[tier] = tier_counts.get(tier, 0) + 1; tier_points += {1: 12, 2: 7, 3: 3}.get(tier, 3)
    top8_commits = [r for r in top8 if r.get("status") == "COMMITTED"]
    top8_points = len(top8_commits) * 10
    gem_count = 0
    for s in stars:
        if "(GEM)" in str(s.get("name", "")): gem_count += 1
    gem_points = gem_count * 6
    score = tier_points + top8_points + gem_points
    if score >= 70: grade = "A+"
    elif score >= 55: grade = "A"
    elif score >= 42: grade = "B"
    elif score >= 30: grade = "C"
    elif score >= 18: grade = "D"
    else: grade = "F"
    breakdown = {"score": score, "nil_signed": sum(tier_counts.values()), "tier_counts": tier_counts, "top8_commits": len(top8_commits), "gems_found": gem_count, "points": {"nil": tier_points, "top8": top8_points, "gems": gem_points}}
    return grade, score, breakdown

def show_offseason():
    sync_team_ratings()
    year = safe_int(st.session_state.get("year", 2026), 2026)
    st.title(f"🏈 Offseason {year}")
    
    budget = safe_int(st.session_state.get("budget", 0), 0)
    prestige = safe_int(st.session_state.get("prestige", 60), 60)
    st.markdown(
        f"<div class='nil-alert'>Budget: <b>{helper_format_cash(budget)}</b> | "
        f"Prestige: <b>{prestige}</b></div>",
        unsafe_allow_html=True
    )
    
    step = safe_int(st.session_state.get("offseason_step", 1), 1)
    
    # V1.6: Updated Flow
    # 1. Retention -> 2. NIL -> 3. HS -> 4. Top 8
    
    if step == 1:
        show_retention_phase()
        
    elif step == 2:
        show_offseason_nil_v8()
        st.divider()
        if st.button("Continue to HS Outreach →", type="primary"):
            st.session_state.offseason_step = 3
            st.rerun()
            
    elif step == 3:
        show_offseason_hs_outreach()
        st.divider()
        block_continue = st.session_state.get("hs_last_results") is not None
        if st.button("Continue to Top-8 Battles →", type="primary", disabled=block_continue):
            st.session_state.offseason_step = 4
            st.rerun()
        if block_continue:
            st.info("Dismiss HS Outreach results above to continue.")

    elif step == 4:
        show_offseason_top8_v8()
        st.divider()
        if st.button("Finish Recruiting & Advance Season →", type="primary"):
            # ... (End logic remains same, just clear retention data too)
            grade, score, breakdown = compute_recruiting_class_grade()
            last_hist = st.session_state.history[-1] if st.session_state.history else None
            if last_hist and safe_int(last_hist.get("Year", 0), 0) == year:
                last_hist["RecruitingGrade"] = grade
            
            add_news(f"Recruiting class grade: {grade} ({score} pts)")
            st.session_state.year += 1; st.session_state.tenure += 1
            st.session_state.inflation = safe_float(st.session_state.get("inflation", 1.0), 1.0) * 1.02
            OpponentManager.evolve_universe()
            
            invite = maybe_generate_conference_invite()
            if not invite: ai_conference_swap_lightweight()
            
            st.session_state.schedule = engine_generate_schedule(
                st.session_state.team_name, 
                st.session_state.team_conf, 
                st.session_state.team_rival
            )
            st.session_state.week_index = 0; st.session_state.record = {"w": 0, "l": 0}; st.session_state.season_logs = []; st.session_state.season_simulated = False; st.session_state.season_end_ready = False; st.session_state.revenue_report = None
            st.session_state.nil_class = []; st.session_state.hs_total_spend = 0
            st.session_state.top8 = []; st.session_state.top8_resolved = set()
            st.session_state.offseason_step = 1
            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
            st.session_state.hotspots = generate_hotspots()
            sync_team_ratings()
            
            # Reset offseason states
            st.session_state.hs_last_results = None
            st.session_state.retention_data = [] # Clear retention
            for p in GameConfig.POSITIONS: st.session_state[f"hs_pos_input_{p}_v28"] = 0
            st.session_state.hs_alloc_by_pos = {p: 0 for p in GameConfig.POSITIONS}
            
            st.session_state.recruiting_summary = {"grade": grade, "score": score, "breakdown": breakdown}
            st.session_state.game_state = GameState.RECRUITING_WRAP; st.rerun()

def show_recruiting_wrap():
    st.title("📦 Recruiting Wrap-Up")

    summary = st.session_state.get("recruiting_summary", {})
    if not summary:
        st.warning("No recruiting summary found.")
        if st.button("Back to Dashboard"):
            st.session_state.game_state = GameState.DASHBOARD
            st.rerun()
        return

    grade = summary.get("grade", "N/A")
    score = summary.get("score", 0)
    bd = summary.get("breakdown", {}) or {}

    st.success(f"Recruiting Grade: **{grade}**")
    st.write(f"Score: **{score}** points")
    st.caption("Tip: Strong recruiting improves next season’s OFF/DEF and keeps boosters happy.")

    c1, c2, c3 = st.columns(3)
    c1.metric("NIL Signed", int(bd.get("nil_signed", 0)))
    c2.metric("Top-8 Commits", int(bd.get("top8_commits", 0)))
    c3.metric("Gems Found", int(bd.get("gems_found", 0)))

    pts = bd.get("points", {}) or {}
    st.markdown("### 📊 Points Breakdown")
    st.write(f"• NIL points: **{int(pts.get('nil', 0))}**")
    st.write(f"• Top-8 points: **{int(pts.get('top8', 0))}**")
    st.write(f"• Gems points: **{int(pts.get('gems', 0))}**")

    st.divider()

    if st.button("Begin New Season →", type="primary"):
        st.session_state.recruiting_summary = None
        st.session_state.game_state = GameState.DASHBOARD
        st.rerun()

def maybe_generate_conference_invite():
    if st.session_state.get("pending_invite"): return st.session_state.pending_invite
    conf_map = get_conferences_map(); team = st.session_state.team_name; cur_conf = st.session_state.team_conf
    prestige = int(st.session_state.get("prestige", 60) or 60); booster = int(st.session_state.get("booster_rating", 50) or 50)
    wins = int((st.session_state.get("record") or {}).get("w", 0) or 0)
    chance = 0.05
    if wins >= 9: chance += 0.08
    if wins >= 11: chance += 0.10
    if booster >= 80: chance += 0.06
    if prestige >= 80: chance += 0.06
    targets = []
    if cur_conf == "G5":
        if prestige >= 74 or wins >= 10: targets += ["Big 12", "ACC"]
        if prestige >= 84 or wins >= 11: targets += ["Big Ten", "SEC"]
    elif cur_conf in ["ACC", "Big 12"]:
        if prestige >= 86 or wins >= 11: targets += ["Big Ten", "SEC"]
    targets = [t for t in targets if t in conf_map and t != cur_conf]
    if not targets: return None
    if random.random() > min(0.35, chance): return None
    to_conf = random.choice(targets)
    base_mult = 1.10
    if to_conf == "SEC": base_mult = 1.18
    elif to_conf == "Big Ten": base_mult = 1.16
    note = "Blue-blood TV deal + tougher road games." if to_conf in ["SEC", "Big Ten"] else "New media deal."
    st.session_state.pending_invite = {"to_conf": to_conf, "boost_mult": base_mult, "note": note}
    add_news(f"{team} receives a conference invite to the {to_conf}.")
    return st.session_state.pending_invite

def ai_conference_swap_lightweight():
    conf_map = get_conferences_map(); user_team = st.session_state.team_name
    if random.random() > 0.10: return None
    pools = [("ACC", "Big 12"), ("Big Ten", "SEC"), ("G5", "Big 12")]
    from_conf, to_conf = random.choice(pools)
    from_list = [t for t in conf_map.get(from_conf, []) if t != user_team]
    if not from_list: return None
    team = random.choice(from_list)
    conf_map[from_conf].remove(team)
    conf_map.setdefault(to_conf, []).append(team)
    add_news(f"Realignment: {team} moves from {from_conf} to {to_conf}.")

# ==============================================================================
# ZONE 9: VIEW FUNCTIONS - SCREENS
# ==============================================================================

def run_setup():
    st.title("🏆 Build the Program: CEO")
    st.markdown("### Dynasty Mode Setup")
    c1, c2 = st.columns(2)
    name = c1.text_input("AD Name", st.session_state.get("ad_name", "Coach Prime"))
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    sorted_teams = sorted(GameConfig.REAL_WORLD_INIT.keys()) + sorted([t for t in GameConfig.ALL_TEAMS if t not in GameConfig.REAL_WORLD_INIT])
    team = st.selectbox("Select Team", sorted_teams)
    if team in GameConfig.REAL_WORLD_INIT:
        d = GameConfig.REAL_WORLD_INIT[team]; tier = d["Tier"]; budget = 25_000_000 if tier == 1 else (15_000_000 if tier == 2 else 5_000_000)
        conf = get_conference(team); rival = d.get("Rival", "Rival")
    else:
        tier, budget, conf, rival = 3, 5_000_000, get_conference(team), "Rival"
    expect = 10 if tier == 1 else (8 if tier == 2 else (6 if tier == 3 else 4))
    st.info(f"**{team}** | Conf: {conf} | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival}")
    st.caption(f"Expectation: {expect}+ Wins")
    if st.button("Start Dynasty", type="primary"):
        # Explicit Setup Initialization
        st.session_state.year = 2026
        st.session_state.tenure = 1
        st.session_state.job_security = 75
        st.session_state.ad_name = name; st.session_state.team_name = team
        st.session_state.team_color = GameConfig.TEAMS_DB.get(team, {}).get("color", "#333333")
        st.session_state.team_conf = conf; st.session_state.team_rival = rival; st.session_state.home_region = "South"; st.session_state.school_tier = tier
        st.session_state.expected_wins = expect; st.session_state.school_tier = tier
        st.session_state.budget = int(budget * (0.75 if diff == "Hard" else 1.25 if diff == "Easy" else 1.0))
        st.session_state.roster = engine_generate_roster(tier, GameConfig.REAL_WORLD_INIT.get(team, {}).get("Talent"))
        st.session_state.prestige = GameConfig.REAL_WORLD_INIT.get(team, {}).get("Prestige", 60)
        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
        st.session_state.staff = {}
        for r in ["HC", "OC", "DC", "Scout"]: st.session_state.staff[r] = engine_generate_coach(r, tier)
        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}
        st.session_state.opponents_db = {}
        for opp in GameConfig.ALL_TEAMS:
            if opp in GameConfig.REAL_WORLD_INIT:
                data = GameConfig.REAL_WORLD_INIT[opp]
                st.session_state.opponents_db[opp] = {"Prestige": data["Prestige"], "OVR": data["Talent"], "Off": random.choice(GameConfig.SCHEMES["Offense"]), "Def": random.choice(GameConfig.SCHEMES["Defense"]), "Coaches": {"OC": random.randint(5, 9), "DC": random.randint(5, 9)}, "Stadium": random.randint(5, 11)}
            else:
                pres = 85 if opp in GameConfig.CONFERENCES["SEC"] else 65; ovr = 82 if opp in GameConfig.CONFERENCES["SEC"] else 70
                st.session_state.opponents_db[opp] = {"Prestige": pres, "OVR": ovr, "Off": "Pro Style", "Def": "Man Coverage", "Coaches": {"OC": 5, "DC": 5}, "Stadium": random.randint(4, 10)}
        if "conferences_map" not in st.session_state: st.session_state.conferences_map = {k: list(v) for k, v in GameConfig.CONFERENCES.items()}
        if conf not in st.session_state.conferences_map: st.session_state.conferences_map[conf] = []
        if team not in st.session_state.conferences_map[conf]: st.session_state.conferences_map[conf].append(team)
        st.session_state.hotspots = generate_hotspots()
        st.session_state.schedule = engine_generate_schedule(team, conf, rival)
        st.session_state.week_index = 0; st.session_state.record = {"w": 0, "l": 0}; st.session_state.season_logs = []; st.session_state.season_simulated = False; st.session_state.season_end_ready = False
        st.session_state.offseason_step = 1; st.session_state.nil_class = []; st.session_state.hs_total_spend = 0
        st.session_state.hs_shares = {p: 100.0 / len(GameConfig.POSITIONS) for p in GameConfig.POSITIONS}; st.session_state.hs_spend_by_pos = {p: 0 for p in GameConfig.POSITIONS}; st.session_state.hs_alloc_by_pos = {p: 0 for p in GameConfig.POSITIONS}
        st.session_state.top8 = []; st.session_state.top8_resolved = set()
        st.session_state.trophies = []; st.session_state.conf_revenue_boost_mult = 1.0; st.session_state.pending_invite = None; st.session_state.booster_rating = 50; st.session_state.ai_records = []; st.session_state.selection_sunday_results = []; st.session_state.last_postseason_result = "NONE"
        st.session_state.achievements = []; st.session_state.milestone_log = []
        
        # Init V28 recruiting keys
        for p in GameConfig.POSITIONS: st.session_state[f"hs_pos_input_{p}_v28"] = 0
        
        add_news(f"{team} hires {st.session_state.staff['HC']['name']} as HC."); st.session_state.game_state = GameState.DASHBOARD; st.rerun()

def show_dashboard():
    sync_team_ratings()
    thresh = 0 if st.session_state.tenure <= 2 else 30
    if st.session_state.job_security < thresh:
        st.session_state.game_state = GameState.FIRED
        st.rerun()

    if st.session_state.get("pending_invite"):
        inv = st.session_state.pending_invite
        st.markdown(f"""
        <div style="background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid #f1c40f;">
            <h3>📨 Conference Invite: {inv['to_conf']}</h3>
            <p>The {inv['to_conf']} formally invites {st.session_state.team_name} to join the conference.</p>
            <p><i>"{inv['note']}"</i></p>
            <p><b>Effect:</b> Revenue boost (x{inv['boost_mult']}), Prestige Boost, but Harder Schedule.</p>
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("✅ Accept Invitation", type="primary"):
            apply_conference_move(inv['to_conf'], inv['boost_mult'])
            st.session_state.pending_invite = None
            safe_toast(f"Welcome to the {inv['to_conf']}!")
            st.rerun()
        if c2.button("❌ Decline (Stay)", type="secondary"):
            st.session_state.pending_invite = None
            add_news(f"{st.session_state.team_name} declines invitation to {inv['to_conf']}.")
            st.rerun()

    if st.session_state.season_end_ready:
        st.markdown("""<div style="background:#ffcccb; padding:10px; border-radius:5px; text-align:center; border:2px solid #e00; color: #333;"><h3>🚨 SEASON COMPLETE</h3><p>The regular season is over. Go to results/postseason.</p></div>""", unsafe_allow_html=True)
        if st.button("Resume Postseason / Season End", type="primary"):
            st.session_state.game_state = GameState.SEASON_END; st.rerun()

    if st.session_state.revenue_report:
        st.markdown(f"<div class='finance-alert'>💰 FINANCIAL REPORT<br>{st.session_state.revenue_report}</div>", unsafe_allow_html=True)

    sec = st.session_state.job_security
    sec_cls = "security-safe" if sec > 75 else ("security-warm" if sec > 40 else "security-hot")
    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Security: <span class='{sec_cls}'>{sec}%</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 5px; color: white;'><h2>{st.session_state.team_name}</h2></div>", unsafe_allow_html=True)

    try:
        rv = st.session_state.get("roster", {}) or {}
        raw_roster_val = int(sum(int(v) for v in rv.values()) / max(1, len(rv)))
    except Exception: raw_roster_val = 75

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    ovr_val = safe_int(st.session_state.get("team_rating", 75), 75)
    off_val = safe_int(st.session_state.get("team_off", 75), 75)
    def_val = safe_int(st.session_state.get("team_def", 75), 75)

    c2.metric("OVR", ovr_val)
    c3.metric("OFF", off_val, f"Raw: {raw_roster_val}")
    c4.metric("DEF", def_val)
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    c5.metric("Legacy", saban, f"Titles: {st.session_state.career_stats['titles']}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Strategy", "Staff", "Facilities", "Season (Weekly)", "Legacy"])

    with tab1:
        c1, c2 = st.columns(2)
        st.session_state.my_schemes["Off"] = c1.selectbox("Offense", GameConfig.SCHEMES["Offense"], index=GameConfig.SCHEMES["Offense"].index(st.session_state.my_schemes.get("Off", "Pro Style")))
        st.session_state.my_schemes["Def"] = c2.selectbox("Defense", GameConfig.SCHEMES["Defense"], index=GameConfig.SCHEMES["Defense"].index(st.session_state.my_schemes.get("Def", "Man Coverage")))
        st.write("Unit Strength")
        for p, v in st.session_state.roster.items():
            lab = f"{p}: {int(v)}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.progress(min(1.0, v / 100.0), text=lab)
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
                    st.markdown(f"<div class='staff-card'><div class='staff-role'>{role}</div><div class='staff-name'>{c['name']}</div><div><span class='badge {badge_cls}'>RATING: {rtg}</span><span class='badge badge-trait'>Trait: {c.get('trait','None')}</span></div><div class='small-muted'>{helper_format_cash(c.get('salary',0))}</div></div>", unsafe_allow_html=True)
                    if st.button("Fire", key=f"fire_{role}"):
                        add_news(f"{st.session_state.team_name} parts ways with {c['name']} ({role}).")
                        del st.session_state.staff[role]; st.rerun()
                else: st.warning(f"{role} VACANT")

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
                        st.markdown(f"<div class='staff-card'><div class='staff-name'>{cand['name']}</div><div class='small-muted'>{cand.get('history','')}</div><div style='margin:5px 0'><span class='badge badge-trait'>{role} OVR: {vis_rate}</span><span class='badge badge-trait'>Trait: {vis_trait}</span></div><div style='font-weight:bold'>{helper_format_cash(cand['salary'])}</div></div>", unsafe_allow_html=True)
                        b1, b2 = st.columns(2)
                        if b1.button("Hire", key=f"hire_{role}_{j}"):
                            if BudgetManager.spend(cand["salary"], f"hire {role}"):
                                st.session_state.staff[role] = cand
                                add_news(f"{st.session_state.team_name} hires {cand['name']} as {role}.")
                                if role in st.session_state.candidates: del st.session_state.candidates[role]
                                st.rerun()
                        if not cand.get("scouted") and b2.button("Scout ($25k)", key=f"sc_{role}_{j}"):
                            if BudgetManager.spend(25_000, "scout candidate"):
                                cand["scouted"] = True; st.rerun()
                if st.button(f"Promote GA (Free)", key=f"ga_{role}"):
                    ga = generate_ga_coach(role)
                    st.session_state.staff[role] = ga
                    add_news(f"{st.session_state.team_name} promotes {ga['name']} to {role}.")
                    if role in st.session_state.candidates: del st.session_state.candidates[role]
                    st.rerun()
        else: st.info("No vacancies. Fire someone to shop the market.")

    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Marketing", st.session_state.facilities["Marketing"], delta="Rev: +$1.5M/yr")
            if st.button("Upgrade ($1M)", key="um"):
                if BudgetManager.spend(1_000_000, "upgrade marketing"):
                    st.session_state.facilities["Marketing"] += 1; add_news("Marketing upgraded. Boosters are pleased."); st.rerun()
        with c2:
            st.metric("Training", st.session_state.facilities["Training"], delta="OFF/DEF Boost")
            if st.button("Upgrade ($3M)", key="ut"):
                if BudgetManager.spend(3_000_000, "upgrade training"):
                    st.session_state.facilities["Training"] += 1; add_news("Training upgraded. Player development improves."); st.rerun()
        with c3:
            st.metric("Stadium", st.session_state.facilities["Stadium"], delta="Home Field (Tiered)")
            st.caption("Tier: <7 none, 7–8 small, 9+ big.")
            if st.button("Upgrade ($10M)", key="us"):
                if BudgetManager.spend(10_000_000, "upgrade stadium"):
                    st.session_state.facilities["Stadium"] += 1; st.session_state.prestige = min(99, st.session_state.prestige + 1)
                    add_news("Stadium upgraded. Home field advantage grows."); st.rerun()

    with tab4:
        if len(st.session_state.staff) < 4: st.error("Fill Staff First!"); return
        if not st.session_state.schedule:
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)

        # --- V28.3: REORDERED LAYOUT (BETTER SPACING) ---
        sched = st.session_state.schedule or []
        sched_len = len(sched)
        
        if not st.session_state.season_simulated:
            wk = int(st.session_state.get("week_index", 0) or 0)
            if wk >= len(sched): end_regular_season_and_stay_on_results(); st.rerun()

            opp = sched[wk]
            opp_data = OpponentManager.get(opp)
            is_riv = (opp == st.session_state.team_rival)
            opp_off = int(opp_data["OffOVR"]); opp_def = int(opp_data["DefOVR"])

            # 1. Header & Matchup
            st.subheader(f"Next Game: Week {wk+1} vs {opp}")
            if is_riv: st.warning("RIVALRY WEEK: More chaos, bigger stakes!")
            
            my_off_val = off_val; my_def_val = def_val
            st.caption(f"Matchup: Your OFF {my_off_val} vs Opp DEF {opp_def} | Your DEF {my_def_val} vs Opp OFF {opp_off}")

            # 2. Controls Row (V28.3 Layout)
            ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([1, 2, 2])
            with ctrl_c1:
                st.markdown("<strong>Strategy</strong>", unsafe_allow_html=True)
                st.session_state.game_state = GameState.DASHBOARD 
                st.session_state.game_plan = st.selectbox("Game Plan", ["Conservative", "Normal", "Aggressive"], index=["Conservative", "Normal", "Aggressive"].index(st.session_state.game_plan), label_visibility="collapsed")

            def play_one_week():
                try:
                    is_home = (wk % 2 == 0); loc_str = "HOME" if is_home else "@AWAY"
                    # FIX V1.3: Deterministic Game RNG
                    rng = game_rng(st.session_state.year, wk + 1, opp, mode="PLAY")
                    res = engine_play_game_v8(my_off_val, my_def_val, opp_off, opp_def, st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")}, st.session_state.game_plan, opp_data.get("Coaches", {"OC": 5, "DC": 5}), is_home, is_riv, st.session_state.facilities["Stadium"], opp_data.get("Stadium", 7), rng=rng)
                except Exception as e:
                    st.error(f"⚠️ Game simulation error: {str(e)}"); st.warning("Generating fallback result to preserve your save...")
                    loc_str = "HOME" if (wk % 2 == 0) else "@AWAY"
                    res = {"result": "L", "score": "0-7", "stats": {"qb_duel": [75, 80], "off_vs_def": [75, 80], "def_vs_off": [75, 80], "staff": ["5/5", "5/5"], "raw_roster": 75}, "explain": {"my_off": my_off_val, "my_def": my_def_val, "opp_off": opp_off, "opp_def": opp_def, "my_edge": 0.0, "opp_edge": 0.0, "scheme_my": 0.0, "scheme_opp": 0.0, "coach_my": 0.0, "coach_opp": 0.0, "home_field": 0.0, "plan": st.session_state.game_plan}}
                
                st.session_state.season_logs.append({"Week": wk + 1, "Opponent": opp, "Score": f"{res['result']} {res['score']}", "Stats": res["stats"], "Explain": res["explain"], "OppOVR": int(opp_data.get("OVR", 80)), "Loc": loc_str})
                if res["result"] == "W":
                    st.session_state.record["w"] += 1; st.session_state.career_stats["w"] += 1
                    st.session_state.job_security = min(100, st.session_state.job_security + (5 if is_riv else 2))
                    add_news(f"{st.session_state.team_name} wins Week {wk+1} vs {opp} ({res['score']}).")
                else:
                    st.session_state.record["l"] += 1; st.session_state.career_stats["l"] += 1
                    pen = 2 if st.session_state.tenure <= 2 else 5
                    st.session_state.job_security = max(0, st.session_state.job_security - pen)
                    add_news(f"{st.session_state.team_name} loses Week {wk+1} vs {opp} ({res['score']}).")
                st.session_state.week_index += 1
                if st.session_state.week_index >= 12: end_regular_season_and_stay_on_results()

            with ctrl_c2:
                st.markdown("<strong>Action</strong>", unsafe_allow_html=True)
                if st.button(f"🏈 Play Week {wk+1}", type="primary", use_container_width=True): play_one_week(); st.rerun()
            with ctrl_c3:
                st.markdown("<strong>Simulate</strong>", unsafe_allow_html=True)
                if st.button("⏩ Sim Season", use_container_width=True):
                    while not st.session_state.season_simulated:
                        wk2 = st.session_state.week_index; sched2 = st.session_state.schedule or []
                        if wk2 >= len(sched2) or wk2 >= 12: break
                        opp2 = sched2[wk2]; opp_data2 = OpponentManager.get(opp2)
                        is_riv2 = (opp2 == st.session_state.team_rival); is_home2 = (wk2 % 2 == 0); loc_str2 = "HOME" if is_home2 else "@AWAY"
                        # FIX V1.3: Deterministic SIM RNG
                        rng = game_rng(st.session_state.year, wk2 + 1, opp2, mode="SIM")
                        res2 = engine_play_game_v8(my_off_val, my_def_val, int(opp_data2["OffOVR"]), int(opp_data2["DefOVR"]), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data2.get("Off", "Pro Style"), "Def": opp_data2.get("Def", "Man Coverage")}, st.session_state.game_plan, opp_data2.get("Coaches", {"OC": 5, "DC": 5}), is_home=is_home2, is_rival=is_riv2, my_stadium_level=st.session_state.facilities["Stadium"], opp_stadium_level=opp_data2.get("Stadium", 7), rng=rng)
                        st.session_state.season_logs.append({"Week": wk2 + 1, "Opponent": opp2, "Score": f"{res2['result']} {res2['score']}", "Stats": res2["stats"], "Explain": res2["explain"], "OppOVR": int(opp_data2.get("OVR", 80)), "Loc": loc_str2})
                        if res2["result"] == "W":
                            st.session_state.record["w"] += 1; st.session_state.career_stats["w"] += 1
                            st.session_state.job_security = min(100, st.session_state.job_security + (5 if is_riv else 2))
                        else:
                            st.session_state.record["l"] += 1; st.session_state.career_stats["l"] += 1
                            pen = 2 if st.session_state.tenure <= 2 else 5; st.session_state.job_security = max(0, st.session_state.job_security - pen)
                        st.session_state.week_index += 1
                    end_regular_season_and_stay_on_results(); st.rerun()

            st.divider()

        # 3. Schedule Grid
        c1, c2 = st.columns(2)
        with c1:
            st.caption("Weeks 1–6")
            for i in range(min(6, sched_len)):
                opp = sched[i]; played = next((x for x in st.session_state.season_logs if x["Week"] == i + 1), None)
                is_rival = opp == st.session_state.team_rival
                if played:
                    res = "W" if played["Score"].startswith("W") else "L"; css = "game-card-win" if res == "W" else "game-card-loss"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1}: {played['Score']} vs {opp}</div>", unsafe_allow_html=True)
                else:
                    css = "game-card-rival" if is_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)
        with c2:
            st.caption("Weeks 7–12")
            for i in range(6, min(12, sched_len)):
                opp = sched[i]; played = next((x for x in st.session_state.season_logs if x["Week"] == i + 1), None)
                is_rival = opp == st.session_state.team_rival
                if played:
                    res = "W" if played["Score"].startswith("W") else "L"; css = "game-card-win" if res == "W" else "game-card-loss"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1}: {played['Score']} vs {opp}</div>", unsafe_allow_html=True)
                else:
                    css = "game-card-rival" if is_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)

        st.divider()
        # V28.3: Removed News from here (moved to Sidebar or Season End bottom)
        render_news_box() 
        st.divider()

    with tab5:
        st.subheader("🏛️ Trophy Case (Quick View)")
        cs = st.session_state.career_stats
        st.write(f"**Titles:** {cs['titles']}  |  **Bowl W-L:** {cs['bowl_w']}-{cs['bowl_l']}  |  **Career W-L:** {cs['w']}-{cs['l']}")
        st.write(f"**Current Prestige:** {st.session_state.prestige}")
        st.write(f"**Legacy (Saban) Score:** {calculate_saban_score(cs, st.session_state.prestige)}")
        st.divider(); render_trophy_gallery("🏆 Trophy Case Gallery"); st.divider()
        render_achievements_panel(); st.divider(); render_dynasty_timeline()
        
        # V27.6: RETIREMENT BUTTON IN LEGACY TAB
        st.divider()
        if st.button("🚪 Retire from Coaching", type="secondary"):
            st.session_state.game_state = GameState.RETIREMENT
            st.rerun()

def show_fired():
    st.error("FIRED! Your tenure has ended.")
    saban = calculate_saban_score(st.session_state.career_stats, st.session_state.prestige)
    st.write(f"Final Legacy (Saban) Score: **{saban}**")
    render_trophy_gallery("🏛️ Your Trophy Gallery (Career)")
    if st.button("Restart Career"): st.session_state.clear(); st.rerun()

def show_retirement():
    st.title("🏆 Hall of Fame Induction")
    st.markdown("Your coaching career has come to an end.")
    
    # Calculate Stats
    cs = st.session_state.career_stats
    total_games = cs['w'] + cs['l']
    win_pct = (cs['w'] / total_games * 100) if total_games > 0 else 0.0
    titles = cs['titles']
    
    # Determine Tier
    if titles >= 5: tier = "🐐 GOAT (Saban Tier)"
    elif titles >= 2 or win_pct > 75: tier = "🏛️ Hall of Fame (Urban/Dabo Tier)"
    elif titles >= 1 or win_pct > 65: tier = "⭐ Elite (Kirby/Ryan Day Tier)"
    elif win_pct > 55: tier = "✅ Respectable (Franklin/Kelly Tier)"
    else: tier = "❌ Forgotten (Hot Seat Tier)"
    
    st.markdown(f"""
    <div style='background: #2c3e50; color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h2>Career Summary</h2>
        <div style='font-size: 3em; font-weight: bold; margin: 10px 0;'>{cs['w']} - {cs['l']}</div>
        <div style='font-size: 1.2em; opacity: 0.8;'>Win Percentage: {win_pct:.1f}%</div>
        <div style='margin-top: 20px; font-size: 1.5em; color: #f1c40f; font-weight: bold;'>{tier}</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("National Titles", titles, help="Record: Nick Saban (7)")
    c2.metric("Bowl Record", f"{cs['bowl_w']}-{cs['bowl_l']}")
    c3.metric("Years Coached", st.session_state.tenure)
    
    st.divider()
    render_trophy_gallery("🏆 Final Trophy Case")
    
    if st.button("Start New Career"):
        st.session_state.clear()
        st.rerun()

def show_season_end():
    sync_team_ratings()
    st.title("📊 Season End — Results Hub")
    st.markdown(f"<div class='nil-alert'>Regular season complete. Record: <b>{st.session_state.record['w']}-{st.session_state.record['l']}</b> | Budget: <b>{helper_format_cash(st.session_state.budget)}</b></div>", unsafe_allow_html=True)
    
    avg_sos, best_win, worst_loss = get_season_metrics()
    st.divider(); st.subheader("🏆 Your Tournament Resume")
    st.markdown(f"<div class='resume-box'><div class='resume-grid'><div><div class='resume-label'>Record</div><div class='resume-val'>{st.session_state.record['w']}-{st.session_state.record['l']}</div></div><div><div class='resume-label'>SOS Score</div><div class='resume-val'>{avg_sos}</div></div><div><div class='resume-label'>Best Win</div><div class='resume-val'>{best_win}</div></div><div><div class='resume-label'>Worst Loss</div><div class='resume-val'>{worst_loss}</div></div></div></div>", unsafe_allow_html=True)
    st.subheader("Game-by-game recap")
    for log in st.session_state.season_logs:
        res = "W" if log["Score"].startswith("W") else "L"; css = "game-card-win" if res == "W" else "game-card-loss"; s = log["Stats"]
        st.markdown(f"<div class='game-card {css}'><div class='card-header'><span>{log['Score']}</span><span>vs {log['Opponent']} (OVR {log.get('OppOVR','?')})</span></div><div class='stat-grid'><div class='stat-row'><span>🔥 QB Duel</span><span>{s['qb_duel'][0]} vs {s['qb_duel'][1]}</span></div><div class='stat-row'><span>⚔️ OFF vs DEF</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div><div class='stat-row'><span>🛡️ DEF vs OFF</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div><div class='stat-row'><span>🧠 Staff</span><span>{s['staff'][0]} vs {s['staff'][1]}</span></div><div class='stat-row'><span>💪 Raw</span><span>{s['raw_roster']}</span></div></div></div>", unsafe_allow_html=True)

    st.divider(); c1, c2 = st.columns(2)
    if c1.button("Enter Selection Sunday (Reveal Rankings) 🏆", type="primary"):
        st.session_state.last_postseason_result = "NONE"
        if not st.session_state.ai_records: st.session_state.ai_records = simulate_ai_regular_season_seeded(st.session_state.year)
        all_teams = st.session_state.ai_records[:]
        user_score = calculate_committee_score(st.session_state.team_name, st.session_state.record['w'], st.session_state.record['l'], st.session_state.team_conf, avg_sos)
        all_teams.append({"Team": st.session_state.team_name, "Wins": st.session_state.record['w'], "Losses": st.session_state.record['l'], "Conf": st.session_state.team_conf, "Score": user_score, "IsUser": True})
        for t in all_teams:
            if "Score" not in t:
                t["Score"] = calculate_committee_score(t["Team"], t["Wins"], t["Losses"], t["Conf"], t.get("SOS", 60)); t["IsUser"] = False
        all_teams.sort(key=lambda x: x["Score"], reverse=True)
        st.session_state.selection_sunday_results = all_teams
        st.session_state.game_state = GameState.SELECTION_SUNDAY; st.rerun()
    
    # V28.3: Moved News to Bottom
    st.divider()
    render_news_box()

def show_selection_sunday():
    sync_team_ratings()
    st.title("🏆 SELECTION SUNDAY")
    st.markdown("The Committee has met. Here are the final rankings.")
    results = st.session_state.selection_sunday_results
    user_rank = -1
    for i, t in enumerate(results):
        if t.get("IsUser"): user_rank = i + 1; break
    if user_rank == -1: 
        for i, t in enumerate(results):
            if t.get("Team") == st.session_state.team_name: user_rank = i + 1; t["IsUser"] = True; break
    if user_rank == -1: user_rank = 999
    
    # --- PINNED USER ROW (always visible) ---
    user_row = next((t for t in results if t.get("IsUser") or t.get("Team") == st.session_state.team_name), None)
    if user_row:
        st.subheader("🎯 Your Team (Pinned)")
        # V28.3: Use helper for identical HTML
        st.markdown(html_rank_row(user_rank, user_row['Team'], user_row['Wins'], user_row['Losses'], user_row['Conf'], True), unsafe_allow_html=True)
        st.divider()

    if user_rank <= 4: st.success(f"✅ Top-4 Seed (#{user_rank}): You receive a First Round BYE.")
    
    # --- 1. TOP 4 VIP ROW ---
    st.subheader("🛡️ First Round Byes (Seeds #1 - #4)")
    vip_cols = st.columns(4)
    for i in range(4):
        if i < len(results):
            t = results[i]
            with vip_cols[i]:
                is_u = t.get("IsUser", False)
                border = "2px solid #2196f3" if is_u else "2px solid #f1c40f"
                bg = "#e3f2fd" if is_u else "#fffbeb"
                st.markdown(
                    f"<div style='background:{bg}; border:{border}; border-radius:8px; padding:15px; text-align:center; height:100%;'>"
                    f"<div style='font-size:1.5em; font-weight:900; color:#b7791f;'>#{i+1}</div>"
                    f"<div style='font-weight:bold; font-size:1.1em; margin:5px 0;'>{t['Team']}</div>"
                    f"<div style='font-size:0.9em; color:#666;'>{t['Wins']}-{t['Losses']}</div>"
                    f"<div style='margin-top:5px;'><span class='vip-badge'>BYE</span></div>"
                    f"</div>", unsafe_allow_html=True
                )
    st.divider()

    # --- 2. FIRST ROUND MATCHUPS (5-12) ---
    st.subheader("⚔️ First Round Matchups")
    # Matchups: 5v12, 6v11, 7v10, 8v9
    m_cols = st.columns(4)
    pairs = [(4, 11), (5, 10), (6, 9), (7, 8)] # Indices in 0-based list
    
    for idx, (h, l) in enumerate(pairs):
        if l < len(results):
            high = results[h]; low = results[l]
            with m_cols[idx]:
                st.markdown(
                    f"<div style='background:white; border:1px solid #ddd; border-radius:8px; padding:10px; text-align:center; box-shadow:0 2px 4px rgba(0,0,0,0.05);'>"
                    f"<div style='font-weight:bold; border-bottom:1px solid #eee; padding-bottom:5px;'>Match {idx+1}</div>"
                    f"<div style='margin-top:8px;'>#{h+1} {high['Team']}</div>"
                    f"<div style='color:#888; font-size:0.8em;'>vs</div>"
                    f"<div style='margin-bottom:8px;'>#{l+1} {low['Team']}</div>"
                    f"</div>", unsafe_allow_html=True
                )
    st.divider()

    # --- 3. THE BUBBLE & REST (Dataframe) ---
    st.subheader("📉 The Bubble & Rankings")
    rest_data = []
    for i, t in enumerate(results[12:25]):
        rank = i + 13
        status = "❌ OUT"
        if safe_int(t.get("Wins"),0) >= 6: status = "🎳 BOWL"
        if t.get("IsUser"): status += " (YOU)"
        rest_data.append({
            "Rank": rank,
            "Team": t["Team"],
            "Record": f"{t['Wins']}-{t['Losses']}",
            "Conf": t["Conf"],
            "Status": status
        })
    
    if rest_data:
        df = pd.DataFrame(rest_data)
        st.dataframe(df, hide_index=True, use_container_width=True)

    # --- 4. USER CONTEXT (If outside top 25) ---
    if user_rank > 25:
        st.warning(f"You are ranked #{user_rank}. (Not shown in Top 25)")

    st.divider()
    
    user_wins = st.session_state.record['w']
    if user_wins < 6:
        st.error("❌ You did not qualify for a bowl game (less than 6 wins).")
        st.session_state.last_postseason_result = "NO_BOWL"
        if st.button("End Season -> Offseason", type="primary"):
            st.session_state.history.append({"Year": st.session_state.year, "Record": f"{user_wins}-{st.session_state.record['l']}", "Rank": "NR", "Bowl": "None", "PostseasonResult": "NO_BOWL"})
            st.session_state.game_state = GameState.SEASON_RECAP; st.rerun()
    elif user_rank <= 12:
        st.success(f"🎉 You made the COLLEGE FOOTBALL PLAYOFF! (Rank #{user_rank})")
        if st.button("Advance to CFP 🏆", type="primary"):
            st.session_state.postseason_data = init_playoff_bracket(user_rank, st.session_state.team_name)
            st.session_state.game_state = GameState.POSTSEASON; st.rerun()
    else:
        st.info(f"🎳 You are invited to a Bowl Game! (Rank #{user_rank})")
        if st.button("Accept Bowl Invite", type="primary"):
            bowl = get_bowl_name(user_rank); candidates = [t["Team"] for t in results if not t.get("IsUser")]
            opp = random.choice(candidates) if candidates else "FCS West"
            st.session_state.postseason_data = {"Type": "BOWL", "Bowl": bowl, "Rank": user_rank, "Opponent": opp, "OppData": OpponentManager.get(opp)}
            st.session_state.game_state = GameState.POSTSEASON; st.rerun()

def show_postseason():
    sync_team_ratings()
    st.title("Postseason Hub")
    data = st.session_state.postseason_data or {}
    if not data.get("Type"): st.warning("Postseason data missing. Returning to Season End."); st.session_state.game_state = GameState.SEASON_END; st.rerun()

    if data.get("Type") == "BOWL":
        bowl_name = data.get("Bowl", "Bowl Game"); opponent = data.get("Opponent", "Opponent")
        st.markdown(f"<div class='bracket-box'><h3>{bowl_name}</h3><h1>VS {opponent}</h1></div>", unsafe_allow_html=True)
        
        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            opp_data = OpponentManager.get(opponent)
            res = engine_play_game_v8(st.session_state.team_off, st.session_state.team_def, int(opp_data.get("OffOVR", 80)), int(opp_data.get("DefOVR", 80)), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")}, st.session_state.game_plan, opp_data.get("Coaches", {"OC": 5, "DC": 5}), is_home=False, is_rival=False, my_stadium_level=st.session_state.facilities.get("Stadium", 7), opp_stadium_level=opp_data.get("Stadium", 8), rng=random.Random())
            st.session_state.postseason_flash = {"res": res, "bowl": bowl_name, "opp": opponent}
            st.rerun()

        if "postseason_flash" in st.session_state:
            flash = st.session_state.postseason_flash
            res = flash["res"]
            css = "game-card-win" if res["result"] == "W" else "game-card-loss"
            s = res["stats"]
            st.markdown(f"""
            <div class='game-card {css}'>
                <div class='card-header'><span>{res['score']}</span><span>vs {flash['opp']}</span></div>
                <div class='stat-grid'>
                    <div class='stat-row'><span>🔥 QB Duel</span><span>{s['qb_duel'][0]} vs {s['qb_duel'][1]}</span></div>
                    <div class='stat-row'><span>⚔️ OFF vs DEF</span><span>{s['off_vs_def'][0]} vs {s['off_vs_def'][1]}</span></div>
                    <div class='stat-row'><span>🛡️ DEF vs OFF</span><span>{s['def_vs_off'][0]} vs {s['def_vs_off'][1]}</span></div>
                </div>
            </div>""", unsafe_allow_html=True)
            
            if st.button("Continue to Offseason ->", type="primary"):
                wins = st.session_state.record["w"] + (1 if res["result"] == "W" else 0)
                losses = st.session_state.record["l"] + (1 if res["result"] == "L" else 0)
                if res["result"] == "W":
                    st.session_state.last_postseason_result = "BOWL_WIN"
                    BudgetManager.add(2_000_000, "Bowl Win Bonus")
                    st.session_state.career_stats["bowl_w"] += 1; add_news(f"{st.session_state.team_name} wins {flash['bowl']}! ({res['score']})"); award_trophy(flash['bowl'] if flash['bowl'] in GameConfig.TROPHY_ICONS else "Bowl Win")
                else:
                    st.session_state.last_postseason_result = "BOWL_LOSS"; st.session_state.career_stats["bowl_l"] += 1
                    add_news(f"{st.session_state.team_name} falls in {flash['bowl']} ({res['score']})")

                delta = wins - st.session_state.expected_wins
                if delta > 0: BudgetManager.add(delta * 1_000_000, "Performance Bonus")
                elif delta < 0: BudgetManager.spend(abs(delta) * 500_000, "Missed Expectations Penalty")

                st.session_state.history.append({"Year": st.session_state.year, "Record": f"{wins}-{losses}", "Rank": f"#{data.get('Rank','?')}", "Bowl": flash['bowl'], "PostseasonResult": st.session_state.last_postseason_result})
                check_and_award_achievements()
                del st.session_state.postseason_flash
                st.session_state.game_state = GameState.SEASON_RECAP; st.session_state.offseason_step = 1; st.rerun()

    elif data.get("Type") == "CFP":
        # FIX V1.3: New Visual Bracket
        render_cfp_bracket_tree(st.session_state.postseason_data)
        st.divider()

        user_match = None
        matches = data.get("Matches", [])
        round_num = int(data.get("Round", 1))
        
        for m in matches:
            if m.get("t1") == st.session_state.team_name or m.get("t2") == st.session_state.team_name: user_match = m; break

        if not user_match and data.get("UserAlive") and round_num == 1:
            st.success("✅ FIRST ROUND BYE"); st.info("You are a Top-4 Seed. You automatically advance to the Quarterfinals.")
            if st.button("Simulate Opening Round & Advance", type="primary"):
                # Save History for Bracket
                data.setdefault("History", []).append(copy.deepcopy(matches))
                
                seed_map = st.session_state.postseason_data.get("SeedMap", {}); next_round_teams = []
                for m in matches:
                    t1, t2 = m.get("t1"), m.get("t2"); o1 = st.session_state.opponents_db.get(t1, {"OVR": 82}).get("OVR", 82); o2 = st.session_state.opponents_db.get(t2, {"OVR": 82}).get("OVR", 82)
                    p = o1 / max(1.0, (o1 + o2)); winner = t1 if random.random() < p else t2
                    
                    s_win = int(random.gauss(34, 7)); s_loss = int(random.gauss(20, 7))
                    if s_win <= s_loss: s_win = s_loss + 3 
                    if winner == t1: m["s1"], m["s2"] = s_win, s_loss
                    else: m["s1"], m["s2"] = s_loss, s_win
                    m["winner"] = winner; next_round_teams.append((winner, seed_map.get(winner, 99)))
                    
                seeds = data.get("Seeds", []); new_matches = []
                if len(seeds) >= 4 and len(matches) >= 4:
                    # Map winners from specific matches (0=5v12, 1=6v11, 2=7v10, 3=8v9)
                    w_8v9 = matches[3].get("winner")
                    w_5v12 = matches[0].get("winner")
                    w_6v11 = matches[1].get("winner")
                    w_7v10 = matches[2].get("winner")
                    new_matches.append({"t1": seeds[0], "t2": w_8v9, "winner": None}) 
                    new_matches.append({"t1": seeds[3], "t2": w_5v12, "winner": None}) 
                    new_matches.append({"t1": seeds[2], "t2": w_6v11, "winner": None}) 
                    new_matches.append({"t1": seeds[1], "t2": w_7v10, "winner": None}) 

                st.session_state.postseason_data["Round"] = 2; st.session_state.postseason_data["Matches"] = new_matches; st.rerun()
                add_news(f"{st.session_state.team_name} advances to Quarterfinals after Bye."); st.rerun()

        elif data.get("UserAlive") and user_match:
            opp = user_match["t2"] if user_match["t1"] == st.session_state.team_name else user_match["t1"]
            opp_data = OpponentManager.get(opp)
            st.info(f"Your Matchup: vs {opp} (OVR: {opp_data.get('OVR',88)} | OFF {int(opp_data.get('OffOVR',80))} / DEF {int(opp_data.get('DefOVR',80))})")
            if st.button("PLAY PLAYOFF GAME 🏈", type="primary"):
                # FIX V1.3: Game RNG
                rng = game_rng(st.session_state.year, 20, opp, mode="PLAY")
                res = engine_play_game_v8(st.session_state.team_off, st.session_state.team_def, int(opp_data.get("OffOVR", 80)), int(opp_data.get("DefOVR", 80)), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")}, st.session_state.game_plan, opp_data.get("Coaches", {"OC": 5, "DC": 5}), is_home=False, is_rival=False, my_stadium_level=st.session_state.facilities.get("Stadium", 7), opp_stadium_level=opp_data.get("Stadium", 9), rng=rng)
                
                try: my_s, opp_s = [int(x) for x in str(res.get("score","0-0")).split("-")]
                except: my_s, opp_s = 0, 0
                if user_match.get("t1") == st.session_state.team_name: user_match["s1"], user_match["s2"] = my_s, opp_s
                else: user_match["s1"], user_match["s2"] = opp_s, my_s

                # Save History
                data.setdefault("History", []).append(copy.deepcopy(matches))

                next_round_teams = []; seed_map = st.session_state.postseason_data.get("SeedMap", {})
                for m in matches:
                    if m is user_match:
                        if res["result"] == "W":
                            m["winner"] = st.session_state.team_name; next_round_teams.append((st.session_state.team_name, seed_map.get(st.session_state.team_name, 99)))
                            add_news(f"{st.session_state.team_name} advances in the CFP!"); safe_toast("VICTORY! Advancing...")
                            BudgetManager.add(5_000_000, "CFP Round Bonus")
                        else:
                            m["winner"] = opp; next_round_teams.append((opp, seed_map.get(opp, 99))); st.session_state.postseason_data["UserAlive"] = False
                            st.session_state.last_postseason_result = "CFP_LOSS"; add_news(f"{st.session_state.team_name} is eliminated by {opp}."); st.error(f"Eliminated by {opp}")
                    else:
                        t1, t2 = m.get("t1"), m.get("t2")
                        if not t1 or not t2: continue
                        o1 = st.session_state.opponents_db.get(t1, {"OVR": 82}).get("OVR", 82); o2 = st.session_state.opponents_db.get(t2, {"OVR": 82}).get("OVR", 82)
                        p = o1 / max(1.0, (o1 + o2)); winner = t1 if random.random() < p else t2
                        
                        s_win = int(random.gauss(34, 7)); s_loss = int(random.gauss(20, 7))
                        if s_win <= s_loss: s_win = s_loss + 3 
                        if winner == t1: m["s1"], m["s2"] = s_win, s_loss
                        else: m["s1"], m["s2"] = s_loss, s_win
                        
                        m["winner"] = winner; next_round_teams.append((winner, seed_map.get(winner, 99)))
                time.sleep(0.6)
                if st.session_state.postseason_data.get("UserAlive"):
                    if round_num == 4:
                        st.session_state.last_postseason_result = "TITLE"
                        BudgetManager.add(50_000_000, "NATIONAL CHAMPIONSHIP!")
                        st.session_state.career_stats["titles"] += 1; st.balloons(); st.success("NATIONAL CHAMPIONS!")
                        add_news(f"{st.session_state.team_name} wins the NATIONAL TITLE!"); award_trophy("National Title")
                        check_and_award_achievements()
                        st.session_state.history.append({"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Bowl": "National Title", "PostseasonResult": "TITLE"})
                        st.session_state.game_state = GameState.SEASON_RECAP; st.session_state.offseason_step = 1; st.rerun()
                    else:
                        new_matches = []
                        if round_num == 2:
                            if len(matches) >= 4:
                                new_matches.append({"t1": matches[0]["winner"], "t2": matches[1]["winner"], "winner": None})
                                new_matches.append({"t1": matches[2]["winner"], "t2": matches[3]["winner"], "winner": None})
                        elif round_num == 3:
                            if len(matches) >= 2:
                                new_matches.append({"t1": matches[0]["winner"], "t2": matches[1]["winner"], "winner": None})
                        st.session_state.postseason_data["Round"] = round_num + 1; st.session_state.postseason_data["Matches"] = new_matches; st.rerun()
                else:
                    st.session_state.history.append({"Year": st.session_state.year, "Record": "Playoff Loss", "Rank": f"#{data.get('Rank','?')}", "Bowl": "CFP", "PostseasonResult": "CFP_LOSS"})
                    st.session_state.game_state = GameState.SEASON_RECAP; st.session_state.offseason_step = 1; st.rerun()
        else:
            st.info("You are no longer alive in the bracket.")
            if st.button("Close Season → Recap", type="primary"): st.session_state.game_state = GameState.SEASON_RECAP; st.session_state.offseason_step = 1; st.rerun()

def show_season_recap():
    sync_team_ratings()
    st.title(f"SEASON RECAP: {st.session_state.year}")
    summary = build_season_summary_dict()
    result_flag = st.session_state.get("last_postseason_result", "NONE")
    if result_flag == "TITLE": headline = "DYNASTY! NATIONAL CHAMPIONS!"; subhead = f"{st.session_state.team_name} shocks the world!"
    elif summary["Delta"] >= 3: headline = "Exceeding All Expectations!"; subhead = "Fans are ecstatic."
    elif summary["Delta"] <= -3: headline = "Disaster in the Making?"; subhead = "Boosters grow restless."
    else: headline = "Season Concludes"; subhead = f"The {st.session_state.team_name} finish with a record of {summary['Record']}."
    st.markdown(f"<div class='newspaper-head'>{headline}</div><div class='newspaper-sub'>{subhead}</div>", unsafe_allow_html=True)
    st.subheader("📌 Season Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Record", summary["Record"]); c2.metric("Final Rank", summary["FinalRank"]); c3.metric("SOS", summary["SOS"]); c4.metric("Postseason", summary["Postseason"])
    st.markdown(f"<div class='resume-box'><div class='resume-grid'><div><div class='resume-label'>Best Win</div><div class='resume-val'>{summary['BestWin']}</div></div><div><div class='resume-label'>Worst Loss</div><div class='resume-val'>{summary['WorstLoss']}</div></div><div><div class='resume-label'>Expectation</div><div class='resume-val'>{summary['ExpectedWins']} wins</div></div><div><div class='resume-label'>Result vs Expectation</div><div class='resume-val'>{('+' if summary['Delta']>=0 else '') + str(summary['Delta'])}</div></div></div></div>", unsafe_allow_html=True)
    st.divider()
    current_boost = st.session_state.booster_rating
    booster_change = summary["Delta"] * 5
    if result_flag == "TITLE": booster_change += 25
    elif result_flag == "BOWL_WIN": booster_change += 8
    elif result_flag == "CFP_LOSS": booster_change += 12
    elif result_flag == "BOWL_LOSS": booster_change += 3
    elif result_flag == "NO_BOWL": booster_change -= 8
    new_boost = max(0, min(100, current_boost + booster_change))
    meter_color = "#28a745" if new_boost > 60 else ("#dc3545" if new_boost < 40 else "#ffc107")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💰 Booster Confidence")
        st.markdown(f"<div class='booster-meter-container'><div class='booster-meter-fill' style='width: {new_boost}%; background-color: {meter_color};'></div></div><div style='text-align:center; font-weight:bold; margin-top:5px;'>{new_boost}/100</div>", unsafe_allow_html=True)
        if new_boost > 80: st.success("Boosters are happy! Budget bonus incoming.")
        elif new_boost < 30: st.error("Boosters are angry. Job security at risk.")
    with c2:
        st.subheader("🏆 Legacy Growth")
        try: wins_added = int(st.session_state.record.get("w", 0))
        except: wins_added = 0
        added_titles = 1 if result_flag == "TITLE" else 0
        st.write(f"Wins Added: +{wins_added}"); st.write(f"Titles Added: +{added_titles}")
    st.divider()
    if st.button("Close the Book on " + str(st.session_state.year) + " -> Go to Offseason", type="primary"):
        st.session_state.booster_rating = new_boost
        if new_boost >= 80:
            BudgetManager.add(3_000_000, "Booster Performance Bonus")
        elif new_boost <= 20:
            st.session_state.job_security -= 10; safe_toast("Booster Pressure: Security -10")
        
        apply_roster_attrition()
        
        check_and_award_achievements()
        st.session_state.game_state = GameState.OFFSEASON; st.session_state.offseason_step = 1; st.rerun()

    st.divider()
    if st.button("🚪 Retire from Coaching (End Career)", type="secondary"):
        st.session_state.game_state = GameState.RETIREMENT
        st.rerun()

# ==============================================================================
# ZONE 7: INITIALIZATION & ROUTER
# ==============================================================================
REQUIRED_FUNCS = [
    "run_setup", "show_dashboard", "show_season_end", "show_selection_sunday",
    "show_postseason", "show_season_recap", "show_offseason", "show_recruiting_wrap",
    "show_fired", "show_retirement",
    "generate_nil_class_15", "process_hs_outreach", "generate_top8_prospects", "top8_commit_chance",
    "compute_recruiting_class_grade", "maybe_generate_conference_invite", "ai_conference_swap_lightweight",
    "generate_hotspots"
]

def _similar(name: str):
    funcs = [k for k, v in globals().items() if callable(v)]
    key = name.lower().replace("_", "")
    return [f for f in funcs if key in f.lower().replace("_", "")][:5]

missing = [fn for fn in REQUIRED_FUNCS if fn not in globals()]
if missing:
    st.error("Missing required functions:")
    for fn in missing:
        sims = _similar(fn)
        if sims:
            st.write(f"- {fn} (similar: {', '.join(sims)})")
        else:
            st.write(f"- {fn}")
    st.stop()

init_session_state_defaults()
render_system_sidebar()

if st.session_state.game_state == GameState.SETUP:
    run_setup()
elif st.session_state.game_state == GameState.FIRED:
    show_fired()
elif st.session_state.game_state == GameState.DASHBOARD:
    show_dashboard()
elif st.session_state.game_state == GameState.SEASON_END:
    if st.session_state.team_name == "Unknown U":
        st.warning("⚠️ Team Identity Lost! The previous crash may have reset your team name.")
        suggested = st.session_state.get("last_known_team_name")
        if suggested and suggested in GameConfig.ALL_TEAMS:
            st.info(f"Suggested restore: **{suggested}**")
            if st.button("Restore Suggested Team", type="primary"):
                st.session_state.team_name = suggested
                st.session_state.team_color = st.session_state.get("last_known_team_color") or GameConfig.TEAMS_DB.get(suggested, {}).get("color", "#333333")
                st.rerun()

        c_fix1, c_fix2 = st.columns([3, 1])
        new_name_fix = c_fix1.selectbox("Restore Your Team:", sorted(GameConfig.ALL_TEAMS))
        if c_fix2.button("Restore Name"):
            st.session_state.team_name = new_name_fix
            st.session_state.team_color = GameConfig.TEAMS_DB.get(new_name_fix, {}).get("color", "#333333")
            st.rerun()
    show_season_end()
elif st.session_state.game_state == GameState.SELECTION_SUNDAY:
    show_selection_sunday()
elif st.session_state.game_state == GameState.POSTSEASON:
    show_postseason()
elif st.session_state.game_state == GameState.SEASON_RECAP:
    show_season_recap()
elif st.session_state.game_state == GameState.OFFSEASON:
    show_offseason()
elif st.session_state.game_state == GameState.RECRUITING_WRAP:
    show_recruiting_wrap()
elif st.session_state.game_state == GameState.RETIREMENT:
    show_retirement()
else:
    st.session_state.game_state = GameState.DASHBOARD
    st.rerun()
