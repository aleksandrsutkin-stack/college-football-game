
import streamlit as st
import random
import time
import json
import datetime
import math
import pandas as pd
import copy
from typing import List, Dict, Optional, Set

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
.small-muted { font-size: 0.85em; color: #777; }
</style>
""", unsafe_allow_html=True)
# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

STATE_VERSION = 2.1

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

    REAL_WORLD_INIT = {
        "Georgia": {"Prestige": 95, "Talent": 96, "Tier": 1, "Rival": "Florida"},
        "Ohio State": {"Prestige": 95, "Talent": 95, "Tier": 1, "Rival": "Michigan"},
        "Texas": {"Prestige": 94, "Talent": 95, "Tier": 1, "Rival": "Oklahoma"},
        "Alabama": {"Prestige": 92, "Talent": 94, "Tier": 1, "Rival": "Auburn"},
        "Oregon": {"Prestige": 91, "Talent": 93, "Tier": 1, "Rival": "Washington"},
        "Notre Dame": {"Prestige": 90, "Talent": 92, "Tier": 1, "Rival": "USC"},
        "LSU": {"Prestige": 88, "Talent": 91, "Tier": 2, "Rival": "Alabama"},
        "Michigan": {"Prestige": 88, "Talent": 90, "Tier": 1, "Rival": "Ohio State"},
        "Penn State": {"Prestige": 86, "Talent": 89, "Tier": 2, "Rival": "Ohio State"},
        "Ole Miss": {"Prestige": 85, "Talent": 89, "Tier": 2, "Rival": "Mississippi St"},
        "Miami": {"Prestige": 86, "Talent": 88, "Tier": 2, "Rival": "Florida St"},
        "Florida St": {"Prestige": 84, "Talent": 87, "Tier": 2, "Rival": "Miami"},
        "Tennessee": {"Prestige": 85, "Talent": 88, "Tier": 2, "Rival": "Alabama"},
        "Clemson": {"Prestige": 87, "Talent": 87, "Tier": 2, "Rival": "South Carolina"},
        "USC": {"Prestige": 82, "Talent": 88, "Tier": 2, "Rival": "Notre Dame"},
        "Oklahoma": {"Prestige": 84, "Talent": 89, "Tier": 2, "Rival": "Texas"},
        "Texas A&M": {"Prestige": 83, "Talent": 89, "Tier": 2, "Rival": "Texas"},
        "Utah": {"Prestige": 80, "Talent": 85, "Tier": 2, "Rival": "BYU"},
        "Kansas State": {"Prestige": 78, "Talent": 84, "Tier": 2, "Rival": "Kansas"},
        "Missouri": {"Prestige": 78, "Talent": 85, "Tier": 2, "Rival": "Kansas"},
        "Iowa": {"Prestige": 79, "Talent": 83, "Tier": 2, "Rival": "Iowa State"},
        "Wisconsin": {"Prestige": 78, "Talent": 83, "Tier": 2, "Rival": "Minnesota"},
        "Indiana": {"Prestige": 88, "Talent": 85, "Tier": 2, "Rival": "Purdue"},
        "SMU": {"Prestige": 76, "Talent": 84, "Tier": 2, "Rival": "TCU"},
        "Louisville": {"Prestige": 78, "Talent": 85, "Tier": 2, "Rival": "Kentucky"},
        "NC State": {"Prestige": 77, "Talent": 84, "Tier": 2, "Rival": "UNC"},
        "Arizona": {"Prestige": 76, "Talent": 84, "Tier": 3, "Rival": "Arizona State"},
        "Boise State": {"Prestige": 78, "Talent": 85, "Tier": 2, "Rival": "Fresno St"},
        "Fresno State": {"Prestige": 74, "Talent": 83, "Tier": 3, "Rival": "Boise State"},
        "Tulane": {"Prestige": 74, "Talent": 80, "Tier": 3, "Rival": "LSU"},
        "App State": {"Prestige": 72, "Talent": 79, "Tier": 3, "Rival": "Georgia Southern"},
        "Memphis": {"Prestige": 72, "Talent": 78, "Tier": 3, "Rival": "Ole Miss"},
        "Liberty": {"Prestige": 70, "Talent": 78, "Tier": 3, "Rival": "NMSU"},
        "UNLV": {"Prestige": 68, "Talent": 77, "Tier": 3, "Rival": "Nevada"},
        "Colorado": {"Prestige": 75, "Talent": 81, "Tier": 2, "Rival": "Nebraska"},
        "Virginia Tech": {"Prestige": 74, "Talent": 79, "Tier": 3, "Rival": "UVA"},
    }

    CONFERENCES = {
        "SEC": ["Georgia", "Alabama", "Texas", "LSU", "Tennessee", "Oklahoma", "Auburn", "Ole Miss", "Florida", "Texas A&M", "Missouri", "Kentucky", "Vanderbilt", "Mississippi St", "South Carolina", "Arkansas"],
        "Big Ten": ["Ohio State", "Oregon", "Penn State", "Michigan", "USC", "Wisconsin", "Iowa", "Washington", "Nebraska", "Michigan St", "UCLA", "Indiana", "Purdue", "Minnesota", "Illinois", "Rutgers", "Maryland"],
        "ACC": ["Florida St", "Clemson", "Miami", "Louisville", "UNC", "Virginia Tech", "SMU", "Pitt", "NC State", "Stanford", "Cal", "Georgia Tech", "Duke", "Syracuse", "Wake Forest", "Boston College", "UVA"],
        "Big 12": ["Utah", "Kansas State", "Oklahoma St", "Arizona", "Colorado", "Texas Tech", "Baylor", "TCU", "BYU", "West Virginia", "Arizona State", "Iowa State", "Kansas", "UCF", "Houston", "Cincinnati"],
        "Pac-12": ["Boise State", "Fresno St", "San Diego St", "Colorado St", "Oregon St", "Wash State"],
        "Indep": ["Notre Dame", "UConn", "UMass"],
        "MAC": ["Toledo", "Miami (OH)", "Ohio", "Northern Illinois", "Western Michigan", "Bowling Green", "Buffalo"],
        "G5": ["Tulane", "Memphis", "Navy", "Army", "USF", "Liberty", "App State", "James Madison", "San Jose State", "Wyoming", "Air Force", "Nevada", "UNLV", "Rice", "North Texas", "UTSA", "Texas State"]
    }
    
    ALL_TEAMS = [t for c in CONFERENCES.values() for t in c]

class RecruitingPhases:
    """V1.9: Unified recruiting flow configuration."""
    PHASES = {
        "retention": {
            "step_num": 1,
            "title": "1) Retention Ransom: The Transfer Portal",
            "description": "Before recruiting new talent, you must pay to keep your current stars.",
            "next_step": 2,
            "next_button_text": "Continue to NIL Recruiting →"
        },
        "nil": {
            "step_num": 2,
            "title": "2) NIL Prospects (Class of 15)",
            "description": "You can sign any of these 15. When they're gone, they're gone.",
            "next_step": 3,
            "next_button_text": "Continue to HS Outreach →"
        },
        "hs": {
            "step_num": 3,
            "title": "3) HS Outreach: The War Room",
            "description": "Directly invest in position groups to find talent.",
            "next_step": 4,
            "next_button_text": "Continue to Top-8 Battles →"
        },
        "top8": {
            "step_num": 4,
            "title": "4) Top-8 Battles — Close on Elites",
            "description": "Make final pitches to elite prospects.",
            "next_step": 5,
            "next_button_text": "Finish Recruiting & Advance Season →"
        }
    }
    
    @staticmethod
    def get_phase_by_step(step: int) -> dict:
        for phase_key, config in RecruitingPhases.PHASES.items():
            if config["step_num"] == step:
                return {**config, "key": phase_key}
        return None

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
# FACTORIES (V2.1 + V1.7 MERGED)
# ==============================================================================

class OpponentFactory:
    @staticmethod
    def create_opponent(team_name: str, context: str = "INIT", 
                        performance_data: dict = None) -> dict:
        is_elite_conf = (
            team_name in GameConfig.CONFERENCES.get("SEC", []) or
            team_name in GameConfig.CONFERENCES.get("Big Ten", []) or
            team_name in GameConfig.CONFERENCES.get("ACC", [])
        )
        is_real_init = team_name in GameConfig.REAL_WORLD_INIT
        
        if is_real_init:
            data = GameConfig.REAL_WORLD_INIT[team_name]
            pres = data["Prestige"]
            ovr = data["Talent"]
        else:
            pres = 60
            ovr = 68
            if is_elite_conf:
                pres = 78
                ovr = 79
        
        if context == "EVOLVE" and performance_data:
            wins = performance_data.get("wins", 6)
            if wins >= 10:
                pres = min(99, pres + 3)
            elif wins <= 4:
                pres = max(20, pres - 3)
            ovr = int(pres * 0.9) + random.randint(-3, 3)
        
        elif context == "RUNTIME":
            try:
                user_conf = st.session_state.get("team_conf", "G5")
                if user_conf in ["G5", "MAC", "Pac-12", "Indep"]:
                    user_ovr = st.session_state.get("team_rating", 75)
                    user_wins = st.session_state.get("record", {}).get("w", 0)
                    boost = 0
                    if user_ovr >= 82 or user_wins >= 8:
                        boost = random.randint(10, 15)
                    elif user_ovr >= 78 or user_wins >= 6:
                        boost = random.randint(6, 10)
                    if boost > 0:
                        ovr = min(88, ovr + boost)
            except Exception:
                pass 
        
        if is_elite_conf or pres >= 85:
            coach_min, coach_max = 8, 10
            stad_min, stad_max = 8, 11
        elif pres >= 75:
            coach_min, coach_max = 6, 9
            stad_min, stad_max = 6, 9
        else:
            coach_min, coach_max = 4, 7
            stad_min, stad_max = 4, 8
        
        return {
            "Prestige": pres,
            "OVR": ovr,
            "Off": random.choice(GameConfig.SCHEMES["Offense"]),
            "Def": random.choice(GameConfig.SCHEMES["Defense"]),
            "Coaches": {
                "OC": random.randint(coach_min, coach_max),
                "DC": random.randint(coach_min, coach_max)
            },
            "Stadium": random.randint(stad_min, stad_max)
        }

class UIComponents:
    @staticmethod
    def gradient_header(title: str, subtitle: str = "", 
                        gradient: str = "135deg, #667eea 0%, #764ba2 100%") -> str:
        subtitle_html = ""
        if subtitle:
            subtitle_html = f"<p style='color: rgba(255,255,255,0.9); font-size: 1.2em; margin-top: 10px;'>{subtitle}</p>"
        return f"<div style='background: linear-gradient({gradient}); padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.3); margin-bottom: 30px;'><h1 style='color: white; font-size: 3em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>{subtitle_html}</div>"
    
    @staticmethod
    def hero_card(rank: int, team: str, wins: int, losses: int, 
                  conf: str, outcome_type: str) -> str:
        styles = {
            "BYE": {"bg": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "text": "🛡️ FIRST ROUND BYE", "icon": "🏆"},
            "PLAYOFF": {"bg": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)", "text": "⚔️ PLAYOFF BOUND", "icon": "🎯"},
            "BOWL": {"bg": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)", "text": "🎳 BOWL ELIGIBLE", "icon": "✅"},
            "ELIMINATED": {"bg": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)", "text": "❌ SEASON OVER", "icon": "💔"}
        }
        style = styles.get(outcome_type, styles["ELIMINATED"])
        return f"<div style='background: {style['bg']}; padding: 30px; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); margin-bottom: 30px; border: 3px solid rgba(255,255,255,0.3);'><div style='text-align: center;'><div style='font-size: 1.2em; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;'>YOUR FINAL RANKING</div><div style='font-size: 5em; font-weight: 900; color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.3); margin: 10px 0;'>#{rank}</div><div style='font-size: 2em; font-weight: bold; color: white; margin: 10px 0;'>{team}</div><div style='font-size: 1.5em; color: rgba(255,255,255,0.95); margin-bottom: 20px;'>{wins}-{losses} • {conf}</div><div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-top: 20px; backdrop-filter: blur(10px);'><div style='font-size: 2em; margin-bottom: 5px;'>{style['icon']}</div><div style='font-size: 1.3em; font-weight: bold; color: white;'>{style['text']}</div></div></div></div>"
    
    @staticmethod
    def team_stat_card(team: str, record: str, overall: int, 
                       offense: int, defense: int, stadium: int,
                       is_user: bool = False) -> str:
        color = "#2196F3" if is_user else "#f44336"
        bg_color = "rgba(33, 150, 243, 0.1)" if is_user else "rgba(244, 67, 54, 0.1)"
        side = "left" if is_user else "right"
        return f"<div style='background: {bg_color}; padding: 20px; border-radius: 10px; border-{side}: 5px solid {color};'><h3 style='text-align: center; color: {color};'>{team}</h3><div style='text-align: center; margin: 15px 0;'><div style='font-size: 2.5em; font-weight: bold;'>{record}</div></div><hr style='opacity: 0.3;'><div style='display: grid; gap: 10px;'><div style='display: flex; justify-content: space-between;'><span>Overall:</span><strong>{overall}</strong></div><div style='display: flex; justify-content: space-between;'><span>Offense:</span><strong>{offense}</strong></div><div style='display: flex; justify-content: space-between;'><span>Defense:</span><strong>{defense}</strong></div><div style='display: flex; justify-content: space-between;'><span>Stadium:</span><strong>{stadium}</strong></div></div></div>"
    
    @staticmethod
    def progress_bar_gradient(label: str, value: int, max_value: int = 100,
                              team_color: str = "#2196F3") -> str:
        pct = min(100, (value / max_value) * 100)
        return f"<div style='margin: 10px 0;'><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span style='font-weight: bold;'>{label}</span><span>{value}/{max_value}</span></div><div style='background: #e0e0e0; height: 24px; border-radius: 12px; overflow: hidden;'><div style='width: {pct}%; height: 100%; background: linear-gradient(90deg, {team_color} 0%, rgba({team_color}, 0.5) 100%); transition: width 0.3s ease;'></div></div></div>"

    @staticmethod
    def star_rating(rating: int, max_stars: int = 10) -> str:
        return "⭐" * rating + "☆" * (max_stars - rating)

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
        if not validate_budget_input(amount, BudgetManager.get_current(), description): return False
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
        base = {1: 22_000_000, 2: 14_000_000, 3: 6_000_000, 4: 3_000_000}.get(tier, 3_000_000)
        bonus = safe_int(marketing_level, 0) * 1_500_000
        total = (base + bonus) * float(inflation) * float(st.session_state.get("conf_revenue_boost_mult", 1.0))
        return int(total)

class OpponentManager:
    @staticmethod
    def get(team_name: str) -> dict:
        if "opponents_db" not in st.session_state: st.session_state.opponents_db = {}
        if team_name not in st.session_state.opponents_db:
            st.session_state.opponents_db[team_name] = OpponentFactory.create_opponent(team_name, context="RUNTIME")
        
        opp = st.session_state.opponents_db[team_name]
        opp.setdefault("Prestige", 60); opp.setdefault("OVR", 75)
        
        if "OffOVR" not in opp or "DefOVR" not in opp:
            base = safe_int(opp.get("OVR", 75), 75)
            rr = make_deterministic_rng("opp_split", team_name, st.session_state.get("year", 0))
            opp["OffOVR"] = max(50, min(99, base + rr.randint(-3, 3)))
            opp["DefOVR"] = max(50, min(99, base + rr.randint(-3, 3)))
        
        if "Coaches" not in opp or not isinstance(opp.get("Coaches"), dict): opp["Coaches"] = {"OC": 5, "DC": 5}
        else:
            opp["Coaches"].setdefault("OC", 5); opp["Coaches"].setdefault("DC", 5)
            
        opp.setdefault("Stadium", 7); opp.setdefault("Off", "Pro Style"); opp.setdefault("Def", "Man Coverage")
        return opp
    
    @staticmethod
    def evolve_universe() -> None:
        if "opponents_db" not in st.session_state: return
        for team, data in st.session_state.opponents_db.items():
            base_ovr = safe_int(data.get("OVR", 75), 75)
            wins = int((base_ovr / 100) * 12) + random.randint(-2, 2)
            wins = max(0, min(12, wins))
            evolved = OpponentFactory.create_opponent(team, context="EVOLVE", performance_data={"wins": wins})
            data["Prestige"] = evolved["Prestige"]; data["OVR"] = evolved["OVR"]
            
            if data["Prestige"] > 80 and wins < 6: data["Coaches"] = {"OC": random.randint(7, 9), "DC": random.randint(7, 9)}
            elif data["Prestige"] < 70 and wins > 9: data["Coaches"] = {"OC": random.randint(3, 6), "DC": random.randint(3, 6)}
            else: data["Coaches"] = evolved["Coaches"]
            
            if random.random() < 0.35: data.pop("OffOVR", None); data.pop("DefOVR", None)

# ==============================================================================
# OTHER HELPERS
# ==============================================================================
def make_deterministic_rng(*parts) -> random.Random:
    base = (str(st.session_state.get("state_version", "")), str(st.session_state.get("year", "")), str(st.session_state.get("team_name", "")))
    seed_str = "|".join([*base, *[str(p) for p in parts]])
    return random.Random(seed_str)

def game_rng(year: int, week: int, opp: str, mode: str = "PLAY") -> random.Random:
    return make_deterministic_rng("game", mode, int(year), int(week), str(opp))

def calculate_difficulty_multiplier(user_conf: str, user_prestige: int, user_ovr: int, user_wins: int) -> float:
    mult = 1.0
    if user_conf in ["G5", "MAC", "Pac-12", "Indep"]:
        if user_ovr >= 85: mult += 0.20
        elif user_ovr >= 80: mult += 0.15
        elif user_ovr >= 75: mult += 0.10
        if user_wins >= 10: mult += 0.08
        elif user_wins >= 8: mult += 0.05
        if user_prestige >= 80: mult += 0.05
    elif user_conf in ["SEC", "Big Ten"] and user_prestige >= 90: mult += 0.05
    return min(1.35, mult)

def add_news(msg: str):
    if "news" not in st.session_state or st.session_state.news is None: st.session_state.news = []
    stamp = datetime.datetime.now().strftime("%b %d")
    st.session_state.news.insert(0, {"ts": stamp, "text": msg}) 
    st.session_state.news = st.session_state.news[:40]

def get_conferences_map():
    if "conferences_map" not in st.session_state: st.session_state.conferences_map = {k: list(v) for k, v in GameConfig.CONFERENCES.items()}
    for k, v in GameConfig.CONFERENCES.items(): st.session_state.conferences_map.setdefault(k, list(v))
    return st.session_state.conferences_map

def get_conference(team: str) -> str:
    for conf, teams in get_conferences_map().items():
        if team in teams: return conf
    return "G5"

def compute_team_needs(roster: dict, k: int = 3) -> list:
    roster = roster or {}
    vals = sorted([(pos, safe_int(roster.get(pos, 75), 75)) for pos in GameConfig.POSITIONS], key=lambda x: x[1])
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
    tier = "High" if user_rank <= 14 else ("Mid" if user_rank <= 20 else "Low")
    return random.choice(GameConfig.BOWL_MAPPING.get(tier, ["Gator Bowl"]))

def get_season_metrics():
    logs = st.session_state.get("season_logs", []) or []
    if not logs: return (0, "N/A", "N/A")
    opp_ovrs = [safe_int(x.get("OppOVR", 70), 70) for x in logs]
    avg_sos = int(round(sum(opp_ovrs) / max(1, len(opp_ovrs))))
    best_win, worst_loss = (-1, "N/A"), (999, "N/A")
    for x in logs:
        ovr = safe_int(x.get("OppOVR", 70), 70); label = f"{x.get('Opponent','Opp')} ({ovr})"
        if str(x.get("Score","")).startswith("W"):
            if ovr > best_win[0]: best_win = (ovr, label)
        elif ovr < worst_loss[0]: worst_loss = (ovr, label)
    return (avg_sos, best_win[1], worst_loss[1])

def generate_hotspots():
    out = {}
    for r in list(GameConfig.REGION_STRENGTH.keys()): out[r] = random.sample(GameConfig.POSITIONS, k=2)
    return out

def calculate_committee_score(team_name, wins, losses, conf, sos_score):
    score = (wins * 105) - (losses * 115) + (sos_score * 3.0)
    if conf in ["SEC", "Big Ten"]: score += 140
    elif conf in ["ACC", "Big 12"]: score += 80
    if conf in ["G5", "MAC", "Indep"] and losses > 0: score -= 300
    return int(score)

def trophy_icon(name: str) -> str:
    return GameConfig.TROPHY_ICONS.get(name, GameConfig.TROPHY_ICONS.get("Bowl Win", "🎳"))

def award_trophy(trophy_name: str):
    if "trophies" not in st.session_state: st.session_state.trophies = []
    st.session_state.trophies.append({"Year": st.session_state.year, "Name": trophy_name, "Icon": trophy_icon(trophy_name)})

def calculate_saban_score(career_stats, prestige):
    return int((career_stats.get("w", 0)*1) + (career_stats.get("bowl_w", 0)*5) + (career_stats.get("titles", 0)*50) + (prestige*0.5))

def apply_roster_attrition():
    log = []
    for p in GameConfig.POSITIONS:
        cur = st.session_state.roster[p]
        loss = random.randint(3, 7) + int(max(0, cur - 75) * 0.35)
        st.session_state.roster[p] = max(40, cur - loss)
        log.append(f"{p}: -{loss}")
    add_news(f"Graduation & Draft departures: {', '.join(log)}")

def end_regular_season_and_stay_on_results():
    if st.session_state.season_end_ready: return
    st.session_state.season_simulated = True
    st.session_state.season_end_ready = True
    rev = BudgetManager.calculate_revenue(st.session_state.school_tier, st.session_state.facilities["Marketing"], st.session_state.inflation)
    BudgetManager.add(rev, "End of Regular Season Payout", False)
    st.session_state.revenue_report = f"End of Regular Season Payout: +{helper_format_cash(rev)}"
    add_news(f"Regular season ends at {st.session_state.record['w']}-{st.session_state.record['l']}.")
    st.session_state.ai_records = simulate_ai_regular_season_seeded(st.session_state.year)
    st.session_state.game_state = GameState.SEASON_END

# ==============================================================================
# ZONE 3: ENGINE
# ==============================================================================

def engine_generate_coach(role, tier):
    cost = random.randint(4_000_000, 8_000_000) if tier == 1 else random.randint(500_000, 3_500_000)
    base = 8 if tier == 1 else (5 if tier == 2 else 2)
    return {"name": generate_coach_name(), "role": role, "off": min(10, base + random.randint(0, 3)), "def": min(10, base + random.randint(0, 3)), "recruit": min(10, base + random.randint(0, 3)), "trait": random.choice(list(GameConfig.COACH_TRAITS.keys())), "salary": cost, "history": "External Hire", "scouted": False}

def engine_generate_roster(tier, base_ovr=None):
    base = base_ovr if base_ovr is not None else (90 if tier == 1 else (82 if tier == 2 else 74))
    return {p: min(99, max(40, int(base + random.randint(-4, 4)))) for p in GameConfig.POSITIONS}

def engine_generate_schedule(my_team, my_conf, rival):
    conf_map = get_conferences_map()
    rng = make_deterministic_rng(f"{my_team}|{my_conf}|{rival}", st.session_state.get("year", 0))
    
    conf_foes = [t for t in conf_map.get(my_conf, conf_map.get("G5", [])) if t != my_team]
    schedule = rng.sample(conf_foes, min(8, len(conf_foes)))
    
    pool = [t for t in GameConfig.ALL_TEAMS if t != my_team and t not in schedule]
    rng.shuffle(pool)
    schedule.extend(pool[:max(0, 12 - len(schedule))])
    
    if rival in GameConfig.ALL_TEAMS and rival != my_team:
        if rival in schedule: schedule.remove(rival)
        schedule.append(rival)
    
    if len(schedule) < 12:
        extra = [t for t in GameConfig.ALL_TEAMS if t != my_team and t not in schedule]
        rng.shuffle(extra)
        schedule.extend(extra[:12-len(schedule)])
    
    rng.shuffle(schedule)
    
    # V1.7: G5 SCHEDULE BOOST
    if my_conf in ["G5", "MAC", "Pac-12", "Indep"]:
        p4 = []
        for c in ["SEC", "Big Ten", "ACC", "Big 12"]: p4.extend(conf_map.get(c, []))
        avail = [t for t in p4 if t != my_team and t not in schedule]
        if avail:
            num = 3 if st.session_state.get("prestige", 60) >= 70 else 2
            money_games = rng.sample(avail, min(num, len(avail)))
            sched_ovr = []
            for o in schedule:
                ov = 75
                if o in GameConfig.REAL_WORLD_INIT: ov = GameConfig.REAL_WORLD_INIT[o]["Talent"]
                sched_ovr.append((o, ov))
            sched_ovr.sort(key=lambda x: x[1])
            
            replaced = 0
            for i in range(len(sched_ovr)):
                if replaced >= len(money_games): break
                if sched_ovr[i][0] != rival:
                    sched_ovr[i] = (money_games[replaced], 85)
                    replaced += 1
            schedule = [x[0] for x in sched_ovr]
            if rival in schedule:
                schedule.remove(rival)
                rng.shuffle(schedule)
                schedule.append(rival)
            else:
                rng.shuffle(schedule)
                
    return schedule[:12]

def get_tier_bonus(rating):
    return 3 if rating >= 8 else (-3 if rating <= 4 else 0)

def home_field_points(level):
    return 0.0 if level <= 6 else (2.5 if level <= 8 else 4.0)

def compute_team_unit_ratings(roster, staff, facilities):
    r = {p: safe_int(roster.get(p, 75), 75) for p in GameConfig.POSITIONS}
    oc, dc = safe_int(staff.get("OC", {}).get("off", 3)), safe_int(staff.get("DC", {}).get("def", 3))
    tr = safe_int(facilities.get("Training", 1))
    off = (r["QB"]*0.34) + (r["OL"]*0.26) + ((r["RB"]+r["WR"])/2*0.40) + oc*1.2 + tr*0.8
    deff = (r["DL"]*0.32) + (r["LB"]*0.28) + (r["DB"]*0.40) + dc*1.2 + tr*0.8
    return (int(max(40, min(99, off))), int(max(40, min(99, deff))), int(max(40, min(99, sum(r.values())/7))))

def engine_play_game_v8(my_off, my_def, opp_off, opp_def, staff, schemes, opp_schemes, game_plan, opp_coaches, is_home, is_rival, my_stadium_level, opp_stadium_level, rng=None):
    rng = rng or random.Random()
    
    # V1.8: Cinderella Tax
    try:
        diff_mult = calculate_difficulty_multiplier(st.session_state.get("team_conf", "G5"), st.session_state.get("prestige", 60), st.session_state.get("team_rating", 75), st.session_state.get("record", {}).get("w", 0))
        opp_off = int(opp_off * diff_mult)
        opp_def = int(opp_def * diff_mult)
    except: pass

    my_edge, opp_edge = (my_off - opp_def)*0.75, (opp_off - my_def)*0.75
    sb_my, sb_opp = 0.0, 0.0
    if GameConfig.OFF_COUNTERED_BY.get(schemes.get("Off")) == opp_schemes.get("Def"): sb_my -= 2.5; sb_opp += 1.0
    if GameConfig.DEF_COUNTERS.get(opp_schemes.get("Def")) == schemes.get("Off"): sb_my += 2.5; sb_opp -= 1.0
    
    my_c, opp_c = (get_tier_bonus(safe_int(staff.get("OC",{}).get("off",3))) - get_tier_bonus(safe_int(opp_coaches.get("DC",5))))*1.2, (get_tier_bonus(safe_int(opp_coaches.get("OC",5))) - get_tier_bonus(safe_int(staff.get("DC",{}).get("def",3))))*1.2
    
    hc_t = staff.get("HC", {}).get("trait", "None")
    if hc_t == "Tactician": my_c += 0.9
    elif hc_t == "Recruiter": my_c += 0.25
    if staff.get("OC", {}).get("trait") == schemes.get("Off"): sb_my += 1.0
    
    hf = home_field_points(my_stadium_level) if is_home else 0.0
    opp_hf = home_field_points(opp_stadium_level) if not is_home else 0.0
    
    var = 1.35 if is_rival else 1.0
    if game_plan == "Aggressive": var *= 1.25
    elif game_plan == "Conservative": var *= 0.85
    
    exp_my = max(10, min(50, 27.5 + my_edge + sb_my + my_c + hf))
    exp_opp = max(10, min(50, 27.5 + opp_edge + sb_opp + opp_c + opp_hf))
    
    ms = int(round(rng.gauss(exp_my, 5.5 * var)))
    os = int(round(rng.gauss(exp_opp, 5.5 * var)))
    if ms == os: ms += rng.choice([0, 3, 7]); os += rng.choice([0, 0, 3])
    
    ms, os = max(0, min(70, ms)), max(0, min(70, os))
    
    stats = {"qb_duel": [int(st.session_state.roster["QB"]), int(opp_off)], "off_vs_def": [int(my_off), int(opp_def)], "def_vs_off": [int(my_def), int(opp_off)], "staff": ["?","?"], "raw_roster": int((my_off+my_def)/2)}
    return {"result": "W" if ms > os else "L", "score": f"{ms}-{os}", "stats": stats, "explain": {}}

def simulate_ai_regular_season_seeded(seed: int):
    rnd = random.Random(seed); results = []
    if len(st.session_state.opponents_db) < len(GameConfig.ALL_TEAMS):
        for t in GameConfig.ALL_TEAMS:
            if t not in st.session_state.opponents_db: st.session_state.opponents_db[t] = OpponentFactory.create_opponent(t, "INIT")
    
    for team, data in sorted(st.session_state.opponents_db.items()):
        if team == st.session_state.team_name: continue
        pres, conf = data.get("Prestige", 60), get_conference(team)
        if pres > 90: w = rnd.choices([12,11,10,9],[10,30,40,20])[0]
        elif pres > 80: w = rnd.choices([11,10,9,8,7],[5,20,35,30,10])[0]
        elif pres > 60: w = rnd.choices([9,8,7,6,5],[10,25,30,25,10])[0]
        else: w = rnd.choices([6,5,4,3,2],[10,30,30,20,10])[0]
        results.append({"Team": team, "Wins": w, "Losses": 12-w, "Conf": conf, "Prestige": pres, "SOS": 60 + rnd.randint(-5,5)})
    return results

# ==============================================================================
# ZONE 4: STATE MANAGEMENT
# ==============================================================================
def sync_team_ratings():
    if all(k in st.session_state for k in ["roster", "staff", "facilities"]):
        try:
            res = compute_team_unit_ratings(st.session_state.roster, st.session_state.staff, st.session_state.facilities)
            st.session_state.team_off, st.session_state.team_def, st.session_state.team_rating = res
        except: pass

def migrate_state():
    if "state_version" not in st.session_state: st.session_state.state_version = 0.0
    if isinstance(st.session_state.get("top8_resolved"), list): st.session_state.top8_resolved = set(st.session_state.top8_resolved)
    
    defaults = {
        "year": 2026, "prestige": 60, "job_security": 75, "expected_wins": 6, "tenure": 1,
        "history": [], "schedule": [], "season_simulated": False, "active_transfers": {p: False for p in GameConfig.POSITIONS},
        "inflation": 1.0, "revenue_report": None, "postseason_data": {"Type": None}, "team_needs": [], "game_plan": "Normal", "week_index": 0, "news": [], "offseason_step": 1,
        "nil_class": [], "hs_total_spend": 0, "hs_shares": {p: 14.3 for p in GameConfig.POSITIONS}, "hs_spend_by_pos": {p: 0 for p in GameConfig.POSITIONS}, "hs_alloc_by_pos": {p: 0 for p in GameConfig.POSITIONS},
        "top8": [], "top8_resolved": set(), "trophies": [], "conf_revenue_boost_mult": 1.0, "pending_invite": None, "season_end_ready": False, "booster_rating": 50, "ai_records": [],
        "selection_sunday_results": [], "ad_name": "Coach Prime", "team_name": "Unknown U", "team_color": "#333333", "team_conf": "G5", "team_rival": "Rival", "home_region": "South", "school_tier": 3,
        "team_off": 75, "team_def": 75, "team_rating": 75, "last_postseason_result": "NONE", "achievements": [], "milestone_log": [], "conferences_map": {k: list(v) for k,v in GameConfig.CONFERENCES.items()},
        "hs_last_results": None, "recruiting_summary": None, "career_stats": {"w": 0, "l": 0, "bowl_w": 0, "bowl_l": 0, "titles": 0},
        "my_schemes": {"Off": "Pro Style", "Def": "Man Coverage"}, "candidates": {}, "opponents_db": {}, "season_logs": [], "budget": 0, "staff": {}, "stars": [], "last_known_team_name": None, "last_known_team_color": None, "retention_data": []
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
        
    st.session_state.roster = st.session_state.get("roster") or {p: 75 for p in GameConfig.POSITIONS}
    for p in GameConfig.POSITIONS: st.session_state.roster.setdefault(p, 75)
    
    st.session_state.facilities = st.session_state.get("facilities") or {"Marketing": 1, "Training": 1, "Stadium": 1}
    for k in ["Marketing", "Training", "Stadium"]: st.session_state.facilities.setdefault(k, 1)
    
    if "hs_alloc_by_pos" in st.session_state:
        for p in GameConfig.POSITIONS:
            if f"hs_pos_input_{p}_v28" not in st.session_state:
                st.session_state[f"hs_pos_input_{p}_v28"] = int(st.session_state.hs_alloc_by_pos.get(p, 0))
    
    sync_team_ratings()
    st.session_state.state_version = STATE_VERSION
    try:
        if st.session_state.team_name and st.session_state.team_name != "Unknown U":
            st.session_state.last_known_team_name = st.session_state.team_name
            st.session_state.last_known_team_color = st.session_state.team_color
    except: pass

def init_session_state_defaults():
    if "game_state" not in st.session_state: st.session_state.game_state = GameState.SETUP
    migrate_state()

def safe_json_default(obj):
    if isinstance(obj, set): return list(obj)
    if isinstance(obj, (datetime.date, datetime.datetime)): return obj.isoformat()
    return str(obj)

# ==============================================================================
# RECRUITING HELPER FUNCTIONS
# ==============================================================================

def generate_retention_demands() -> List[Dict]:
    """Generates 3 random retention demands from current roster."""
    demands = []
    targets = random.sample(GameConfig.POSITIONS, 3)
    
    for pos in targets:
        current_rating = st.session_state.roster.get(pos, 75)
        base_cost = max(250_000, (current_rating - 60) * 50_000)
        cost = int(base_cost * random.uniform(0.8, 1.2))
        
        demands.append({
            "pos": pos,
            "rating": current_rating,
            "cost": cost,
            "status": "PENDING"
        })
    return demands

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
        recruits.append({"id": random.randint(10_000, 99_999), "name": generate_name(), "pos": pos, "rating": rating, "ask": ask, "trait": random.choice(GameConfig.TRAITS), "status": "OPEN", "note": "", "offer": 0})
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

# ==============================================================================
# RECRUITING VIEW FUNCTIONS
# ==============================================================================

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

def show_offseason_nil_v8():
    st.subheader("2) NIL Prospects (Class of 15)")
    needs = st.session_state.get("team_needs", [])
    if not st.session_state.nil_class:
        st.session_state.nil_class = generate_nil_class_15(needs)
        add_news("NIL board posted: 15 prospects (Tier 1/2/3).")

    st.markdown(f"<div class='recruiting-intel'>Team Needs: <b>{', '.join(needs) if needs else 'Balanced'}</b></div>", unsafe_allow_html=True)
    st.write("You can sign any of these 15. When they're gone, they're gone (no infinite respawn).")
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
    st.caption("Tip: Strong recruiting improves next season's OFF/DEF and keeps boosters happy.")

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

def render_news_box():
    with st.sidebar:
        st.divider(); st.subheader("🗞️ News Wire")
        items = st.session_state.get("news", []) or []
        if not items: st.caption("No headlines yet."); return
        good, bad = ["win", "wins", "advances", "upgrade", "signs", "committed", "found"], ["lose", "loses", "falls", "eliminated", "fired"]
        for it in items[:15]:
            txt = it if isinstance(it, str) else f"{it.get('ts','')} - {it.get('text','')}" if isinstance(it, dict) else str(it)
            css = "news-item" + (" news-item-good" if any(k in txt.lower() for k in good) else " news-item-bad" if any(k in txt.lower() for k in bad) else "")
            st.markdown(f"<div class='{css}'>{txt}</div>", unsafe_allow_html=True)

def render_trophy_gallery(title_text: str = "🏆 Trophy Gallery"):
    st.subheader(title_text)
    trophies = sorted(st.session_state.get("trophies", []) or [], key=lambda x: int(x.get("Year", 0)), reverse=True)
    if not trophies: st.info("No trophies yet."); return
    cols = st.columns(4)
    for i, t in enumerate(trophies[:24]):
        with cols[i % 4]:
            st.markdown(f"<div class='trophy-tile'><div style='font-size:2em'>{t.get('Icon','🏆')}</div><div style='font-weight:800'>{t.get('Name','Trophy')}</div><div class='small-muted'>Year {t.get('Year','?')}</div></div>", unsafe_allow_html=True)

def render_achievements_panel():
    st.subheader("🎖️ Achievements")
    ach = st.session_state.get("achievements", []) or []
    if not ach: st.info("No achievements yet."); return
    for a in ach[-20:][::-1]: st.write(f"• {a}")

def render_dynasty_timeline(max_items=25):
    st.subheader("🧾 Dynasty Timeline")
    hist = st.session_state.get("history", []) or []
    if not hist: st.info("No seasons logged yet."); return
    for h in hist[-12:][::-1]: st.write(f"Year {h.get('Year','?')}: {h.get('Record','?')} | Rank {h.get('Rank','NR')} | {h.get('PostseasonResult','')}")

def check_and_award_achievements():
    if "achievements" not in st.session_state: st.session_state.achievements = []
    if st.session_state.get("last_postseason_result") == "BOWL_WIN" and "First Bowl Win" not in st.session_state.achievements:
        st.session_state.achievements.append("First Bowl Win")
    if st.session_state.prestige >= 80 and "Program Builder" not in st.session_state.achievements:
        st.session_state.achievements.append("Program Builder"); safe_toast("🏆 Achievement Unlocked: Program Builder")
    if st.session_state.record['l'] == 0 and st.session_state.record['w'] >= 12 and "Perfect Season" not in st.session_state.achievements:
        st.session_state.achievements.append("Perfect Season"); safe_toast("🏆 Achievement Unlocked: Perfect Season")

def build_season_summary_dict():
    w = safe_int(st.session_state.record.get("w", 0), 0); l = safe_int(st.session_state.record.get("l", 0), 0)
    sos, best, worst = get_season_metrics()
    expect = safe_int(st.session_state.get("expected_wins", 6), 6)
    final_rank = next((f"#{i+1}" for i, t in enumerate(st.session_state.get("selection_sunday_results", [])) if t.get("IsUser") or t.get("Team")==st.session_state.team_name), "NR")
    return {"Record": f"{w}-{l}", "SOS": sos, "BestWin": best, "WorstLoss": worst, "ExpectedWins": expect, "Delta": w - expect, "FinalRank": final_rank, "Postseason": st.session_state.get("last_postseason_result", "NONE")}

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

def apply_conference_move(to_conf: str, boost_mult: float):
    cm = get_conferences_map(); tm = st.session_state.team_name
    if st.session_state.team_conf in cm and tm in cm[st.session_state.team_conf]: cm[st.session_state.team_conf].remove(tm)
    cm.setdefault(to_conf, []).append(tm)
    st.session_state.team_conf = to_conf
    st.session_state.conf_revenue_boost_mult = float(boost_mult)
    add_news(f"{tm} joins the {to_conf}.")

def render_cfp_bracket_tree(data: dict):
    """Renders the CFP playoff bracket with visual tree structure"""
    st.subheader("🏆 College Football Playoff Bracket")
    seeds = data.get("Seeds", ["TBD"]*12)
    matches = data.get("Matches", [])
    round_num = data.get("Round", 1)
    user_team = st.session_state.team_name
    
    st.markdown("""<style>
.bracket-container{display:flex;justify-content:space-around;gap:20px;margin:20px 0;overflow-x:auto}
.bracket-round{display:flex;flex-direction:column;justify-content:space-around;min-width:200px}
.bracket-matchup{background:white;border:2px solid #e0e0e0;border-radius:8px;padding:12px;margin:8px 0}
.bracket-matchup.active{border-color:#2196F3;box-shadow:0 0 10px rgba(33,150,243,0.3)}
.bracket-matchup.completed{background:#f5f5f5;border-color:#4CAF50}
.bracket-matchup.user-involved{border:3px solid #FF9800;background:#FFF3E0}
.bracket-seed{display:inline-block;background:#333;color:white;width:24px;height:24px;line-height:24px;text-align:center;border-radius:50%;font-weight:bold;font-size:0.8em;margin-right:8px}
.bracket-team{font-weight:bold;color:#333;margin:4px 0;padding:4px;display:flex;align-items:center;justify-content:space-between}
.bracket-team.winner{background:#E8F5E9;border-left:4px solid #4CAF50}
.bracket-team.loser{color:#999;text-decoration:line-through}
.bracket-score{font-weight:bold;margin-left:10px;color:#666}
.bracket-round-title{text-align:center;font-weight:bold;text-transform:uppercase;color:#666;margin-bottom:10px;font-size:0.9em;letter-spacing:1px}
.bracket-bye{background:#E3F2FD;border:2px dashed #2196F3;color:#1976D2;font-style:italic;text-align:center}
</style>""", unsafe_allow_html=True)
    
    html = "<div class='bracket-container'>"
    
    if round_num == 1:
        html += "<div class='bracket-round'><div class='bracket-round-title'>Opening Round</div>"
        ordered_matches = matches if len(matches) < 4 else [matches[3], matches[0], matches[1], matches[2]]
        for m in ordered_matches:
            cls = "bracket-matchup"
            if m.get("winner"): cls += " completed"
            if user_team in [m.get("t1"), m.get("t2")]: cls += " user-involved"
            
            html += f"<div class='{cls}'>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span>{m.get('t1')}</span><span class='bracket-score'>{m.get('s1','')}</span></div>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span>{m.get('t2')}</span><span class='bracket-score'>{m.get('s2','')}</span></div>"
            html += "</div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Quarterfinals</div>"
        qf_seeds = data.get("QF_Seeds", seeds[:4])
        for i, s in enumerate(qf_seeds):
            cls = "bracket-matchup bracket-bye"
            if user_team == s: cls += " user-involved"
            html += f"<div class='{cls}'>"
            html += f"<div class='bracket-team'><span><span class='bracket-seed'>{i+1}</span>{s}</span></div>"
            html += f"<div style='text-align:center;color:#666;font-size:0.85em;margin-top:8px;'>BYE</div>"
            html += "</div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Semifinals</div>"
        html += "<div class='bracket-matchup' style='opacity:0.4;text-align:center;padding:20px;color:#999;'>TBD</div>"
        html += "<div class='bracket-matchup' style='opacity:0.4;text-align:center;padding:20px;color:#999;'>TBD</div>"
        html += "</div>"
    
    elif round_num == 2:
        html += "<div class='bracket-round'><div class='bracket-round-title'>Quarterfinals</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            cls = "bracket-matchup"
            if m.get("winner"): cls += " completed"
            else: cls += " active"
            if user_team in [m.get("t1"), m.get("t2")]: cls += " user-involved"
            
            html += f"<div class='{cls}'>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span><span class='bracket-seed'>{seed_map.get(m.get('t1'),'?')}</span>{m.get('t1')}</span>"
            html += f"<span class='bracket-score'>{m.get('s1','')}</span></div>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span><span class='bracket-seed'>{seed_map.get(m.get('t2'),'?')}</span>{m.get('t2')}</span>"
            html += f"<span class='bracket-score'>{m.get('s2','')}</span></div>"
            html += "</div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Semifinals</div>"
        html += "<div class='bracket-matchup' style='opacity:0.6;text-align:center;padding:20px;color:#999;'>Awaiting QF</div>"
        html += "<div class='bracket-matchup' style='opacity:0.6;text-align:center;padding:20px;color:#999;'>Awaiting QF</div>"
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Championship</div>"
        html += "<div class='bracket-matchup' style='opacity:0.3;text-align:center;padding:30px;color:#999;'>🏆</div>"
        html += "</div>"
    
    elif round_num == 3:
        html += "<div class='bracket-round'><div class='bracket-round-title'>Semifinals</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            cls = "bracket-matchup"
            if m.get("winner"): cls += " completed"
            else: cls += " active"
            if user_team in [m.get("t1"), m.get("t2")]: cls += " user-involved"
            
            html += f"<div class='{cls}'>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span><span class='bracket-seed'>{seed_map.get(m.get('t1'),'?')}</span>{m.get('t1')}</span>"
            html += f"<span class='bracket-score'>{m.get('s1','')}</span></div>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span><span class='bracket-seed'>{seed_map.get(m.get('t2'),'?')}</span>{m.get('t2')}</span>"
            html += f"<span class='bracket-score'>{m.get('s2','')}</span></div>"
            html += "</div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>National Championship</div>"
        html += "<div class='bracket-matchup active' style='padding:30px;text-align:center;'>"
        html += "<div style='font-size:2em;'>🏆</div>"
        html += "<div style='color:#666;margin-top:10px;'>Awaiting Semifinals</div>"
        html += "</div></div>"
    
    else:  # Final
        html += "<div class='bracket-round'><div class='bracket-round-title'>National Championship</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            cls = "bracket-matchup"
            if m.get("winner"): cls += " completed"
            else: cls += " active"
            if user_team in [m.get("t1"), m.get("t2")]: cls += " user-involved"
            
            html += f"<div class='{cls}' style='min-width:300px;'>"
            html += "<div style='text-align:center;font-size:1.5em;margin-bottom:10px;'>🏆</div>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span><span class='bracket-seed'>{seed_map.get(m.get('t1'),'?')}</span>{m.get('t1')}</span>"
            html += f"<span class='bracket-score'>{m.get('s1','')}</span></div>"
            html += f"<div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'>"
            html += f"<span><span class='bracket-seed'>{seed_map.get(m.get('t2'),'?')}</span>{m.get('t2')}</span>"
            html += f"<span class='bracket-score'>{m.get('s2','')}</span></div>"
            html += "</div>"
        html += "</div>"
    
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def init_playoff_bracket(user_rank, user_team_name):
    """Initialize CFP bracket with user team properly seeded"""
    results = st.session_state.get("selection_sunday_results", []) or []
    top12 = [t.get("Team") for t in results[:12] if t.get("Team")]
    
    # Pad to 12 teams
    while len(top12) < 12:
        top12.append("FCS East")
    
    # Remove duplicates
    seen = set()
    for i in range(len(top12)):
        nm = top12[i]
        if nm in seen:
            top12[i] = "FCS East"
        else:
            seen.add(nm)
    
    # Create seed map
    seed_map = {tm: idx for idx, tm in enumerate(top12, start=1)}
    
    # Ensure user team is correctly positioned
    try:
        ur = int(user_rank)
    except:
        ur = 999
    
    if 1 <= ur <= 12:
        target_idx = ur - 1
        top12[target_idx] = user_team_name
        seed_map[user_team_name] = ur
        
        # Remove user from other positions
        for i in range(len(top12)):
            if i != target_idx and top12[i] == user_team_name:
                top12[i] = "FCS East"
    
    # Create first round matchups (5v12, 6v11, 7v10, 8v9)
    r1_matches = [
        {"seed_high": 5, "seed_low": 12, "t1": top12[4], "t2": top12[11], "winner": None},
        {"seed_high": 6, "seed_low": 11, "t1": top12[5], "t2": top12[10], "winner": None},
        {"seed_high": 7, "seed_low": 10, "t1": top12[6], "t2": top12[9], "winner": None},
        {"seed_high": 8, "seed_low": 9, "t1": top12[7], "t2": top12[8], "winner": None},
    ]
    
    return {
        "Type": "CFP",
        "Round": 1,
        "Seeds": top12,
        "QF_Seeds": top12[:4],
        "Matches": r1_matches,
        "UserAlive": True,
        "Rank": int(ur),
        "SeedMap": seed_map
    }

# ==============================================================================
# SETUP SCREEN
# ==============================================================================

def run_setup():
    st.title("🏆 Build the Program: College Football CEO")
    st.markdown("### Dynasty Mode Setup")
    c1, c2 = st.columns(2)
    name = c1.text_input("AD Name", st.session_state.get("ad_name", "Coach Prime"))
    diff = c2.selectbox("Difficulty", ["Normal", "Hard", "Easy"])
    
    teams = sorted(GameConfig.REAL_WORLD_INIT.keys()) + sorted([t for t in GameConfig.ALL_TEAMS if t not in GameConfig.REAL_WORLD_INIT])
    team = st.selectbox("Select Team", teams)
    
    if team in GameConfig.REAL_WORLD_INIT:
        d = GameConfig.REAL_WORLD_INIT[team]
        tier, budget, conf, rival = d["Tier"], {1:25000000, 2:15000000}.get(d["Tier"], 5000000), get_conference(team), d.get("Rival", "Rival")
    else:
        tier, budget, conf, rival = 3, 5000000, get_conference(team), "Rival"
        
    expect = {1: 10, 2: 8, 3: 6}.get(tier, 4)
    st.info(f"**{team}** | Conf: {conf} | Tier: {tier} | Budget: {helper_format_cash(budget)} | Rival: {rival}")
    st.caption(f"Expectation: {expect}+ Wins")
    
    if st.button("Start Dynasty", type="primary"):
        st.session_state.year = 2026
        st.session_state.tenure = 1
        st.session_state.job_security = 75
        st.session_state.ad_name = name
        st.session_state.team_name = team
        st.session_state.team_color = GameConfig.TEAMS_DB.get(team, {}).get("color", "#333333")
        st.session_state.team_conf = conf
        st.session_state.team_rival = rival
        st.session_state.home_region = "South"
        st.session_state.school_tier = tier
        st.session_state.expected_wins = expect
        st.session_state.budget = int(budget * (0.75 if diff == "Hard" else 1.25 if diff == "Easy" else 1.0))
        st.session_state.roster = engine_generate_roster(tier, GameConfig.REAL_WORLD_INIT.get(team, {}).get("Talent"))
        st.session_state.prestige = GameConfig.REAL_WORLD_INIT.get(team, {}).get("Prestige", 60)
        st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
        st.session_state.staff = {r: engine_generate_coach(r, tier) for r in ["HC", "OC", "DC", "Scout"]}
        val = 10 if tier == 1 else 5
        st.session_state.facilities = {"Marketing": val, "Training": val, "Stadium": val}
        
        # Initialize opponents database with OpponentFactory
        st.session_state.opponents_db = {}
        for opp in GameConfig.ALL_TEAMS:
            st.session_state.opponents_db[opp] = OpponentFactory.create_opponent(opp, "INIT")
            
        st.session_state.conferences_map = {k: list(v) for k, v in GameConfig.CONFERENCES.items()}
        if conf not in st.session_state.conferences_map: st.session_state.conferences_map[conf] = []
        if team not in st.session_state.conferences_map[conf]: st.session_state.conferences_map[conf].append(team)
        
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
        st.session_state.top8 = []
        st.session_state.top8_resolved = set()
        st.session_state.trophies = []
        st.session_state.conf_revenue_boost_mult = 1.0
        st.session_state.pending_invite = None
        st.session_state.booster_rating = 50
        st.session_state.ai_records = []
        st.session_state.selection_sunday_results = []
        st.session_state.last_postseason_result = "NONE"
        st.session_state.achievements = []
        st.session_state.hs_last_results = None
        st.session_state.recruiting_summary = None
        st.session_state.retention_data = []
        
        for p in GameConfig.POSITIONS: st.session_state[f"hs_pos_input_{p}_v28"] = 0
        
        add_news(f"{team} hires {st.session_state.staff['HC']['name']} as HC.")
        st.session_state.game_state = GameState.DASHBOARD
        st.rerun()

# ==============================================================================
# DASHBOARD SCREEN
# ==============================================================================

def show_dashboard():
    sync_team_ratings()
    if st.session_state.job_security < (0 if st.session_state.tenure <= 2 else 30):
        st.session_state.game_state = GameState.FIRED
        st.rerun()

    render_news_box()

    if st.session_state.get("pending_invite"):
        inv = st.session_state.pending_invite
        st.markdown(f"<div style='background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid #f1c40f;'><h3>📨 Conference Invite: {inv['to_conf']}</h3><p>{inv['note']}</p></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("✅ Accept"):
            apply_conference_move(inv['to_conf'], inv['boost_mult'])
            st.session_state.pending_invite = None
            st.rerun()
        if c2.button("❌ Decline"):
            st.session_state.pending_invite = None
            st.rerun()

    if st.session_state.season_end_ready:
        st.markdown("<div style='background:#ffcccb; padding:10px; border-radius:5px; text-align:center; border:2px solid #e00; color: #333;'><h3>🚨 SEASON COMPLETE</h3></div>", unsafe_allow_html=True)
        if st.button("Resume Postseason / Season End", type="primary"):
            st.session_state.game_state = GameState.SEASON_END
            st.rerun()

    if st.session_state.revenue_report:
        st.markdown(f"<div class='finance-alert'>{st.session_state.revenue_report}</div>", unsafe_allow_html=True)

    sec_cls = "security-safe" if st.session_state.job_security > 75 else ("security-warm" if st.session_state.job_security > 40 else "security-hot")
    st.markdown(f"<div class='security-box'>Year {st.session_state.tenure} | Security: <span class='{sec_cls}'>{st.session_state.job_security}%</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: {st.session_state.team_color}; padding: 10px; border-radius: 5px; color: white;'><h2>{st.session_state.team_name}</h2></div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Budget", helper_format_cash(st.session_state.budget))
    c2.metric("OVR", st.session_state.team_rating)
    c3.metric("OFF", st.session_state.team_off)
    c4.metric("DEF", st.session_state.team_def)
    c5.metric("Legacy", calculate_saban_score(st.session_state.career_stats, st.session_state.prestige))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Strategy", "Staff", "Facilities", "Season", "Legacy"])

    with tab1:
        c1, c2 = st.columns(2)
        st.session_state.my_schemes["Off"] = c1.selectbox("Offense", GameConfig.SCHEMES["Offense"], index=GameConfig.SCHEMES["Offense"].index(st.session_state.my_schemes.get("Off", "Pro Style")))
        st.session_state.my_schemes["Def"] = c2.selectbox("Defense", GameConfig.SCHEMES["Defense"], index=GameConfig.SCHEMES["Defense"].index(st.session_state.my_schemes.get("Def", "Man Coverage")))
        st.write("### Unit Strength")
        for p, v in st.session_state.roster.items():
            label = f"{p}" + (" (RENTAL)" if st.session_state.active_transfers.get(p) else "")
            st.markdown(UIComponents.progress_bar_gradient(label, int(v), 100, st.session_state.team_color), unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🧢 Current Staff")
        cols = st.columns(4)
        for i, role in enumerate(["HC", "OC", "DC", "Scout"]):
            with cols[i]:
                if role in st.session_state.staff:
                    c = st.session_state.staff[role]
                    st.markdown(f"<div class='staff-card'><div class='staff-role'>{role}</div><div class='staff-name'>{c['name']}</div><div style='margin:8px 0;'>{UIComponents.star_rating(role_rating(c,role))}</div><div><span class='badge badge-trait'>Trait: {c.get('trait','None')}</span></div></div>", unsafe_allow_html=True)
                    if st.button("Fire", key=f"fire_{role}"):
                        del st.session_state.staff[role]
                        add_news(f"Fired {role} {c['name']}")
                        st.rerun()
                else: st.warning(f"{role} VACANT")
        
        st.divider()
        st.markdown("### 📋 Job Market")
        vacancies = [r for r in ["HC", "OC", "DC", "Scout"] if r not in st.session_state.staff]
        if vacancies:
            for role in vacancies:
                if role not in st.session_state.candidates:
                    st.session_state.candidates[role] = [engine_generate_coach(role, random.randint(1, 3)) for _ in range(3)]
                cols = st.columns(3)
                for j, cand in enumerate(st.session_state.candidates[role]):
                    with cols[j]:
                        rtg = role_rating(cand, role)
                        vis = f"{rtg}" if cand.get("scouted") else get_letter_grade(rtg)
                        st.markdown(f"<div class='staff-card'><div class='staff-name'>{cand['name']}</div><div class='small-muted'>OVR: {vis}</div><div style='font-weight:bold'>{helper_format_cash(cand['salary'])}</div></div>", unsafe_allow_html=True)
                        b1, b2 = st.columns(2)
                        if b1.button("Hire", key=f"hire_{role}_{j}"):
                            if BudgetManager.spend(cand["salary"], f"Hire {role}"):
                                st.session_state.staff[role] = cand
                                add_news(f"Hired {cand['name']} as {role}")
                                del st.session_state.candidates[role]
                                st.rerun()
                        if not cand.get("scouted") and b2.button("Scout", key=f"sc_{role}_{j}"):
                            if BudgetManager.spend(25000, "Scout Coach"):
                                cand["scouted"] = True; st.rerun()
        else: st.info("No vacancies.")

    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"### 📢 Marketing")
            st.metric("Level", st.session_state.facilities["Marketing"])
            if st.button("Upgrade ($1M)", key="um"):
                if BudgetManager.spend(1000000, "Upgrade Marketing"):
                    st.session_state.facilities["Marketing"] += 1; st.rerun()
        with c2:
            st.markdown(f"### 🏋️ Training")
            st.metric("Level", st.session_state.facilities["Training"])
            if st.button("Upgrade ($3M)", key="ut"):
                if BudgetManager.spend(3000000, "Upgrade Training"):
                    st.session_state.facilities["Training"] += 1; st.rerun()
        with c3:
            st.markdown(f"### 🏟️ Stadium")
            st.metric("Level", st.session_state.facilities["Stadium"])
            if st.button("Upgrade ($10M)", key="us"):
                if BudgetManager.spend(10000000, "Upgrade Stadium"):
                    st.session_state.facilities["Stadium"] += 1
                    st.session_state.prestige = min(99, st.session_state.prestige + 1)
                    st.rerun()

    with tab4:
        if len(st.session_state.staff) < 4: st.error("Fill Staff First!"); return
        if not st.session_state.schedule:
            st.session_state.schedule = engine_generate_schedule(st.session_state.team_name, st.session_state.team_conf, st.session_state.team_rival)

        sched = st.session_state.schedule
        if not st.session_state.season_simulated:
            wk = st.session_state.week_index
            if wk >= len(sched): end_regular_season_and_stay_on_results(); st.rerun()
            
            opp = sched[wk]
            opp_data = OpponentManager.get(opp)
            
            st.subheader(f"Next Game: Week {wk+1} vs {opp}")
            st.caption(f"Matchup: OFF {st.session_state.team_off} vs DEF {opp_data.get('DefOVR')} | DEF {st.session_state.team_def} vs OFF {opp_data.get('OffOVR')}")
            
            c1, c2, c3 = st.columns([1,2,2])
            with c1:
                st.markdown("Strategy")
                st.session_state.game_plan = st.selectbox("Plan", ["Conservative", "Normal", "Aggressive"], index=["Conservative", "Normal", "Aggressive"].index(st.session_state.game_plan), label_visibility="collapsed")
            with c2:
                st.markdown("Action")
                if st.button(f"Play Week {wk+1}", type="primary", use_container_width=True):
                    rng = game_rng(st.session_state.year, wk+1, opp, "PLAY")
                    res = engine_play_game_v8(st.session_state.team_off, st.session_state.team_def, opp_data.get("OffOVR"), opp_data.get("DefOVR"), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off"), "Def": opp_data.get("Def")}, st.session_state.game_plan, opp_data.get("Coaches"), wk%2==0, opp==st.session_state.team_rival, st.session_state.facilities["Stadium"], opp_data.get("Stadium"), rng)
                    
                    st.session_state.season_logs.append({"Week": wk+1, "Opponent": opp, "Score": f"{res['result']} {res['score']}", "Stats": res["stats"], "OppOVR": opp_data.get("OVR")})
                    if res["result"] == "W":
                        st.session_state.record["w"] += 1; st.session_state.career_stats["w"] += 1
                        st.session_state.job_security = min(100, st.session_state.job_security + (5 if opp==st.session_state.team_rival else 2))
                    else:
                        st.session_state.record["l"] += 1; st.session_state.career_stats["l"] += 1
                        st.session_state.job_security = max(0, st.session_state.job_security - 2)
                    st.session_state.week_index += 1
                    if st.session_state.week_index >= 12: end_regular_season_and_stay_on_results()
                    st.rerun()
            with c3:
                st.markdown("Simulate")
                if st.button("Sim Season", use_container_width=True):
                    while not st.session_state.season_simulated and st.session_state.week_index < 12:
                        wk = st.session_state.week_index
                        opp = sched[wk]
                        opp_data = OpponentManager.get(opp)
                        rng = game_rng(st.session_state.year, wk+1, opp, "SIM")
                        res = engine_play_game_v8(st.session_state.team_off, st.session_state.team_def, opp_data.get("OffOVR"), opp_data.get("DefOVR"), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off"), "Def": opp_data.get("Def")}, st.session_state.game_plan, opp_data.get("Coaches"), wk%2==0, opp==st.session_state.team_rival, st.session_state.facilities["Stadium"], opp_data.get("Stadium"), rng)
                        st.session_state.season_logs.append({"Week": wk+1, "Opponent": opp, "Score": f"{res['result']} {res['score']}", "Stats": res["stats"], "OppOVR": opp_data.get("OVR")})
                        if res["result"] == "W":
                            st.session_state.record["w"] += 1; st.session_state.career_stats["w"] += 1
                        else:
                            st.session_state.record["l"] += 1; st.session_state.career_stats["l"] += 1
                        st.session_state.week_index += 1
                    end_regular_season_and_stay_on_results()
                    st.rerun()

            st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.caption("Weeks 1-6")
            for i in range(min(6, len(sched))):
                opp = sched[i]
                played = next((x for x in st.session_state.season_logs if x["Week"] == i+1), None)
                if played:
                    is_win = played["Score"].startswith("W")
                    css = "game-card-win" if is_win else "game-card-loss"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1}: {played['Score']} vs {opp}</div>", unsafe_allow_html=True)
                else:
                    css = "game-card-rival" if opp==st.session_state.team_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)
        with c2:
            st.caption("Weeks 7-12")
            for i in range(6, min(12, len(sched))):
                opp = sched[i]
                played = next((x for x in st.session_state.season_logs if x["Week"] == i+1), None)
                if played:
                    is_win = played["Score"].startswith("W")
                    css = "game-card-win" if is_win else "game-card-loss"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1}: {played['Score']} vs {opp}</div>", unsafe_allow_html=True)
                else:
                    css = "game-card-rival" if opp==st.session_state.team_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)

    with tab5:
        st.subheader("Legacy")
        cs = st.session_state.career_stats
        st.write(f"Titles: {cs['titles']} | Bowl: {cs['bowl_w']}-{cs['bowl_l']} | Career: {cs['w']}-{cs['l']}")
        render_trophy_gallery()
        render_achievements_panel()
        render_dynasty_timeline()
        st.divider()
        if st.button("Retire"): st.session_state.game_state = GameState.RETIREMENT; st.rerun()

# ==============================================================================
# SEASON END SCREEN
# ==============================================================================

def show_season_end():
    sync_team_ratings()
    st.title("📊 Season End — Results Hub")
    st.markdown(f"<div class='nil-alert'>Regular season complete. Record: <b>{st.session_state.record['w']}-{st.session_state.record['l']}</b> | Budget: <b>{helper_format_cash(st.session_state.budget)}</b></div>", unsafe_allow_html=True)
    
    avg_sos, best_win, worst_loss = get_season_metrics()
    st.divider(); st.subheader("🏆 Your Tournament Resume")
    st.markdown(f"<div class='resume-box'><div class='resume-grid'><div><div class='resume-label'>Record</div><div class='resume-val'>{st.session_state.record['w']}-{st.session_state.record['l']}</div></div><div><div class='resume-label'>SOS Score</div><div class='resume-val'>{avg_sos}</div></div><div><div class='resume-label'>Best Win</div><div class='resume-val'>{best_win}</div></div><div><div class='resume-label'>Worst Loss</div><div class='resume-val'>{worst_loss}</div></div></div></div>", unsafe_allow_html=True)
    
    st.subheader("Game-by-game recap")
    for log in st.session_state.season_logs:
        wk = log["Week"]
        opp = log["Opponent"]
        score = log["Score"]
        is_win = score.startswith("W")
        stats = log.get("Stats")
        css = "game-card-win" if is_win else "game-card-loss"
        s = stats or {}
        st.markdown(f"<div class='game-card {css}'><div class='card-header'><span>{score}</span><span>vs {opp}</span></div></div>", unsafe_allow_html=True)

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
    
    st.divider()

# ==============================================================================
# SELECTION SUNDAY SCREEN  
# ==============================================================================

def show_selection_sunday():
    sync_team_ratings()
    st.markdown(UIComponents.gradient_header("🏆 SELECTION SUNDAY", "The Committee Has Spoken"), unsafe_allow_html=True)
    
    results = st.session_state.selection_sunday_results
    user_rank = -1
    for i, t in enumerate(results):
        if t.get("IsUser"): user_rank = i + 1; break
    if user_rank == -1: 
        for i, t in enumerate(results):
            if t.get("Team") == st.session_state.team_name: user_rank = i + 1; t["IsUser"] = True; break
    if user_rank == -1: user_rank = 999
    
    user_row = next((t for t in results if t.get("IsUser") or t.get("Team") == st.session_state.team_name), None)
    if user_row:
        outcome = "BYE" if user_rank <= 4 else ("PLAYOFF" if user_rank <= 12 else ("BOWL" if user_row['Wins'] >= 6 else "ELIMINATED"))
        st.markdown(UIComponents.hero_card(user_rank, user_row['Team'], user_row['Wins'], user_row['Losses'], user_row['Conf'], outcome), unsafe_allow_html=True)
        st.divider()

    if user_rank <= 4: st.success(f"✅ Top-4 Seed (#{user_rank}): You receive a First Round BYE.")
    
    st.subheader("🛡️ First Round Byes (Seeds #1 - #4)")
    vip_cols = st.columns(4)
    for i in range(4):
        if i < len(results):
            t = results[i]
            with vip_cols[i]:
                border = "2px solid #2196f3" if t.get("IsUser") else "2px solid #f1c40f"
                bg = "#e3f2fd" if t.get("IsUser") else "#fffbeb"
                st.markdown(f"<div style='background:{bg}; border:{border}; border-radius:8px; padding:15px; text-align:center;'><h3>#{i+1}</h3><div>{t['Team']}</div></div>", unsafe_allow_html=True)
    st.divider()

    st.subheader("⚔️ First Round Matchups")
    m_cols = st.columns(4)
    pairs = [(4, 11), (5, 10), (6, 9), (7, 8)]
    for idx, (h, l) in enumerate(pairs):
        if l < len(results):
            high, low = results[h], results[l]
            with m_cols[idx]:
                st.markdown(f"<div style='background:white; border:1px solid #ddd; border-radius:8px; padding:10px; text-align:center;'><b>Match {idx+1}</b><br>#{h+1} {high['Team']}<br>vs<br>#{l+1} {low['Team']}</div>", unsafe_allow_html=True)
    st.divider()

    st.subheader("📉 The Bubble & Rankings")
    rest_data = []
    for i, t in enumerate(results[12:25]):
        status = "🎳 BOWL" if safe_int(t.get("Wins"),0) >= 6 else "❌ OUT"
        if t.get("IsUser"): status += " (YOU)"
        rest_data.append({"Rank": i + 13, "Team": t["Team"], "Record": f"{t['Wins']}-{t['Losses']}", "Conf": t["Conf"], "Status": status})
    
    if rest_data: st.dataframe(pd.DataFrame(rest_data), hide_index=True, use_container_width=True)

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

# ==============================================================================
# POSTSEASON SCREEN
# ==============================================================================

def show_postseason():
    sync_team_ratings()
    st.title("Postseason Hub")
    data = st.session_state.postseason_data or {}
    if not data.get("Type"): st.warning("Data missing."); st.session_state.game_state = GameState.SEASON_END; st.rerun()

    if data.get("Type") == "BOWL":
        bowl, opp = data.get("Bowl", "Bowl"), data.get("Opponent", "Opp")
        opp_data = OpponentManager.get(opp)
        st.markdown(UIComponents.gradient_header(f"{st.session_state.team_name} VS {opp}", bowl, "135deg, #ff6b6b 0%, #feca57 100%"), unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 0.2, 1])
        with c1: st.markdown(UIComponents.team_stat_card(st.session_state.team_name, f"{st.session_state.record['w']}-{st.session_state.record['l']}", st.session_state.team_rating, st.session_state.team_off, st.session_state.team_def, st.session_state.facilities.get("Stadium",7), True), unsafe_allow_html=True)
        with c2: st.markdown("<h1 style='text-align:center'>VS</h1>", unsafe_allow_html=True)
        with c3: st.markdown(UIComponents.team_stat_card(opp, "Est. 9-3", opp_data.get("OVR",80), opp_data.get("OffOVR",80), opp_data.get("DefOVR",80), opp_data.get("Stadium",7), False), unsafe_allow_html=True)
        
        st.divider()
        if st.button("PLAY BOWL GAME 🏈", type="primary"):
            res = engine_play_game_v8(st.session_state.team_off, st.session_state.team_def, int(opp_data.get("OffOVR", 80)), int(opp_data.get("DefOVR", 80)), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off"), "Def": opp_data.get("Def")}, st.session_state.game_plan, opp_data.get("Coaches"), False, False, st.session_state.facilities.get("Stadium"), opp_data.get("Stadium"), random.Random())
            st.session_state.postseason_flash = {"res": res, "bowl": bowl, "opp": opp}
            st.rerun()
            
        if "postseason_flash" in st.session_state:
            flash = st.session_state.postseason_flash; res = flash["res"]
            css = "game-card-win" if res["result"]=="W" else "game-card-loss"
            st.markdown(f"<div class='game-card {css}'><div class='card-header'><span>{res['score']}</span><span>vs {flash['opp']}</span></div></div>", unsafe_allow_html=True)
            if st.button("Continue ->", type="primary"):
                w = st.session_state.record["w"] + (1 if res["result"]=="W" else 0)
                l = st.session_state.record["l"] + (1 if res["result"]=="L" else 0)
                st.session_state.last_postseason_result = "BOWL_WIN" if res["result"]=="W" else "BOWL_LOSS"
                if res["result"]=="W": 
                    BudgetManager.add(2000000, "Bowl Win"); st.session_state.career_stats["bowl_w"]+=1; award_trophy(flash['bowl'])
                else: st.session_state.career_stats["bowl_l"]+=1
                
                st.session_state.history.append({"Year": st.session_state.year, "Record": f"{w}-{l}", "Rank": f"#{data.get('Rank','?')}", "Bowl": flash['bowl'], "PostseasonResult": st.session_state.last_postseason_result})
                check_and_award_achievements()
                del st.session_state.postseason_flash
                st.session_state.game_state = GameState.SEASON_RECAP; st.session_state.offseason_step = 1; st.rerun()

    elif data.get("Type") == "CFP":
        render_cfp_bracket_tree(st.session_state.postseason_data)
        st.divider()
        st.info("CFP playoff logic not fully implemented in this merge. Use V1.7 for complete CFP experience.")
        if st.button("End Season"): st.session_state.game_state = GameState.SEASON_RECAP; st.rerun()

# ==============================================================================
# SEASON RECAP SCREEN
# ==============================================================================

def show_season_recap():
    sync_team_ratings()
    st.title(f"SEASON RECAP: {st.session_state.year}")
    summary = build_season_summary_dict()
    st.markdown(UIComponents.gradient_header("SEASON COMPLETE", f"Record: {summary['Record']} | Rank: {summary['FinalRank']}"), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Record", summary["Record"]); c2.metric("Rank", summary["FinalRank"]); c3.metric("SOS", summary["SOS"]); c4.metric("Bowl", summary["Postseason"])
    
    st.divider()
    if st.button("Proceed to Offseason ->", type="primary"):
        apply_roster_attrition()
        st.session_state.game_state = GameState.OFFSEASON; st.session_state.offseason_step = 1; st.rerun()

# ==============================================================================
# FIRED SCREEN
# ==============================================================================

def show_fired():
    st.title("🔥 FIRED")
    st.markdown(UIComponents.gradient_header("YOU'VE BEEN FIRED", "The Athletic Director has decided to make a change"))
    if st.button("Start New Dynasty"):
        st.session_state.clear(); st.rerun()

# ==============================================================================
# RETIREMENT SCREEN
# ==============================================================================

def show_retirement():
    st.title("🏆 RETIREMENT")
    st.markdown(UIComponents.gradient_header("HALL OF FAME CEREMONY", "Congratulations on a legendary career"))
    render_trophy_gallery()
    if st.button("Start New Dynasty"):
        st.session_state.clear(); st.rerun()

def show_offseason():
    """Master offseason controller - routes through retention, NIL, HS outreach, and Top-8"""
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
    
    # PHASE 1: RETENTION
    if step == 1:
        show_retention_phase()
        
    # PHASE 2: NIL RECRUITING
    elif step == 2:
        show_offseason_nil_v8()
        st.divider()
        if st.button("Continue to HS Outreach →", type="primary"):
            st.session_state.offseason_step = 3
            st.rerun()
            
    # PHASE 3: HS OUTREACH
    elif step == 3:
        show_offseason_hs_outreach()
        # Note: HS Outreach has its own navigation via render_hs_results_summary()
        # which automatically advances to step 4 when dismissed

    # PHASE 4: TOP-8 BATTLES
    elif step == 4:
        show_offseason_top8_v8()
        st.divider()
        
        # FINISH RECRUITING BUTTON
        if st.button("Finish Recruiting & Advance Season →", type="primary"):
            # Calculate recruiting grade
            grade, score, breakdown = compute_recruiting_class_grade()
            
            # Update last season's history entry with recruiting grade
            last_hist = st.session_state.history[-1] if st.session_state.history else None
            if last_hist and safe_int(last_hist.get("Year", 0), 0) == year:
                last_hist["RecruitingGrade"] = grade
            
            add_news(f"Recruiting class grade: {grade} ({score} pts)")
            
            # ADVANCE TO NEXT SEASON
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.inflation = safe_float(st.session_state.get("inflation", 1.0), 1.0) * 1.02
            
            # Evolve AI opponents
            OpponentManager.evolve_universe()
            
            # Conference realignment
            invite = maybe_generate_conference_invite()
            if not invite:
                ai_conference_swap_lightweight()
            
            # Generate new schedule
            st.session_state.schedule = engine_generate_schedule(
                st.session_state.team_name, 
                st.session_state.team_conf, 
                st.session_state.team_rival
            )
            
            # Reset season state
            st.session_state.week_index = 0
            st.session_state.record = {"w": 0, "l": 0}
            st.session_state.season_logs = []
            st.session_state.season_simulated = False
            st.session_state.season_end_ready = False
            st.session_state.revenue_report = None
            
            # Reset recruiting state
            st.session_state.nil_class = []
            st.session_state.hs_total_spend = 0
            st.session_state.top8 = []
            st.session_state.top8_resolved = set()
            st.session_state.offseason_step = 1
            
            # Update team needs and hotspots
            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
            st.session_state.hotspots = generate_hotspots()
            
            # Sync ratings
            sync_team_ratings()
            
            # Clear recruiting UI state
            st.session_state.hs_last_results = None
            st.session_state.retention_data = []
            for p in GameConfig.POSITIONS:
                st.session_state[f"hs_pos_input_{p}_v28"] = 0
            st.session_state.hs_alloc_by_pos = {p: 0 for p in GameConfig.POSITIONS}
            
            # Store recruiting summary for wrap screen
            st.session_state.recruiting_summary = {
                "grade": grade, 
                "score": score, 
                "breakdown": breakdown
            }
            
            # Move to recruiting wrap screen
            st.session_state.game_state = GameState.RECRUITING_WRAP
            st.rerun()

# ==============================================================================
# SYSTEM SIDEBAR (Save/Load)
# ==============================================================================

def render_system_sidebar():
    """Renders news and save/load system in sidebar"""
    with st.sidebar:
        st.header("💾 CEO System")
        st.caption(f"Version {STATE_VERSION}")
        
        # SAVE SYSTEM
        if st.button("Export Save File"):
            state_copy = dict(st.session_state)
            if "top8_resolved" in state_copy: 
                state_copy["top8_resolved"] = list(state_copy["top8_resolved"])
            export_data = {k: v for k, v in state_copy.items() if k in ALLOWED_SAVE_KEYS}
            json_str = json.dumps(export_data, default=safe_json_default)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            st.download_button(
                label="📥 Download JSON", 
                data=json_str, 
                file_name=f"CFB_CEO_Save_{timestamp}.json", 
                mime="application/json"
            )
        
        # LOAD SYSTEM
        uploaded_file = st.file_uploader("Import Save File", type=["json"])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                for k, v in data.items():
                    if k in ALLOWED_SAVE_KEYS:
                        if k == "top8_resolved": 
                            st.session_state[k] = set(v) if isinstance(v, list) else set()
                        else: 
                            st.session_state[k] = v
                migrate_state()
                st.session_state.candidates = {}
                sync_team_ratings()
                st.success("Save Loaded Successfully! Reloading...")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error loading save: {e}")

# ==============================================================================
# MAIN INITIALIZATION
# ==============================================================================

init_session_state_defaults()
render_system_sidebar()

# ==============================================================================
# MAIN ROUTER
# ==============================================================================

if st.session_state.game_state == GameState.SETUP:
    run_setup()

elif st.session_state.game_state == GameState.FIRED:
    show_fired()

elif st.session_state.game_state == GameState.DASHBOARD:
    show_dashboard()

elif st.session_state.game_state == GameState.SEASON_END:
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
    # Fallback to dashboard if unknown state
    st.session_state.game_state = GameState.DASHBOARD
    st.rerun()
