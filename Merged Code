"""
Build the Program: College Football CEO
VERSION 4.2 (The Ultimate UI Update)

Audit Log:
- MERGE: Combined V3.0 Logic (Hard Mode, Scheduling, Bug Fixes) with V2.9 UI Suite.
- VISUALS: Added Trading Cards (NIL), Interest Meters (Top 8), 3D Trophy Case, and Mount Rushmore.
- STABILITY: Preserved V3.0 Native Column fixes for Game Results to prevent rendering errors.
- DATA: Retained V2.3 Expanded Team Database (65+ teams).
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

STATE_VERSION = 4.0

class GameState:
    """Game state constants representing different screens/phases of the game."""
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
    """Central configuration class containing all game constants and settings."""
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

    # TROPHY TRACKING CONFIG
    TROPHY_CATEGORIES = {
        "National Championships": {"icon": "🏆", "color": "#FFD700", "empty_text": "Win the CFP", "track_key": "titles"},
        "CFP Appearances": {"icon": "⚔️", "color": "#C0C0C0", "empty_text": "Make the Playoff", "track_key": "cfp_appearances"},
        "Perfect Seasons": {"icon": "💯", "color": "#4CAF50", "empty_text": "Go 12-0", "track_key": "perfect_seasons"},
        "Bowl Victories": {"icon": "🎳", "color": "#2196F3", "empty_text": "Win a Bowl Game", "track_key": "bowl_wins"},
        "10+ Win Seasons": {"icon": "🔟", "color": "#9C27B0", "empty_text": "Win 10+ Games", "track_key": "ten_win_seasons"},
        "Conference Titles": {"icon": "🏅", "color": "#FF9800", "empty_text": "Win Your Conference", "track_key": "conf_titles"},
        "Rivalry Wins": {"icon": "⚡", "color": "#F44336", "empty_text": "Beat Your Rival", "track_key": "rivalry_wins"},
        "Top-5 Finishes": {"icon": "⭐", "color": "#00BCD4", "empty_text": "Finish in Top 5", "track_key": "top5_finishes"},
    }

    TROPHY_ICONS = {k: v["icon"] for k, v in TROPHY_CATEGORIES.items()}
    TROPHY_ICONS["Bowl Win"] = "🎳"
    TROPHY_ICONS["National Title"] = "🏆"

    LEGENDS = [
        {"Name": "Nick Saban", "Titles": 7, "Wins": 292, "Losses": 71, "BowlWins": 19},
        {"Name": "Bear Bryant", "Titles": 6, "Wins": 323, "Losses": 85, "BowlWins": 15},
        {"Name": "Bernie Bierman", "Titles": 5, "Wins": 153, "Losses": 65, "BowlWins": 8},
        {"Name": "Howard Jones", "Titles": 5, "Wins": 194, "Losses": 64, "BowlWins": 9},
        {"Name": "Frank Leahy", "Titles": 4, "Wins": 107, "Losses": 13, "BowlWins": 6},
        {"Name": "John McKay", "Titles": 4, "Wins": 127, "Losses": 40, "BowlWins": 10},
        {"Name": "Urban Meyer", "Titles": 3, "Wins": 187, "Losses": 32, "BowlWins": 12},
        {"Name": "Tom Osborne", "Titles": 3, "Wins": 255, "Losses": 49, "BowlWins": 12},
        {"Name": "Kirby Smart", "Titles": 2, "Wins": 94, "Losses": 16, "BowlWins": 9},
        {"Name": "Dabo Swinney", "Titles": 2, "Wins": 170, "Losses": 43, "BowlWins": 12},
    ]

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

    # V2.3 HARD MODE RATINGS PRESERVED
    REAL_WORLD_INIT = {
        # TIER 1 (BOSSES) - Base 98
        "Georgia": {"Prestige": 99, "Talent": 98, "Tier": 1, "Rival": "Florida"},
        "Ohio State": {"Prestige": 98, "Talent": 98, "Tier": 1, "Rival": "Michigan"},
        "Texas": {"Prestige": 97, "Talent": 98, "Tier": 1, "Rival": "Oklahoma"},
        "Oregon": {"Prestige": 96, "Talent": 97, "Tier": 1, "Rival": "Washington"},
        
        # TIER 2 (CONTENDERS) - Base 90-95
        "Alabama": {"Prestige": 94, "Talent": 95, "Tier": 1, "Rival": "Auburn"},
        "Notre Dame": {"Prestige": 93, "Talent": 93, "Tier": 1, "Rival": "USC"},
        "Penn State": {"Prestige": 91, "Talent": 92, "Tier": 1, "Rival": "Ohio State"},
        "Michigan": {"Prestige": 90, "Talent": 91, "Tier": 1, "Rival": "Ohio State"},
        "LSU": {"Prestige": 89, "Talent": 91, "Tier": 2, "Rival": "Alabama"},
        "Ole Miss": {"Prestige": 88, "Talent": 90, "Tier": 2, "Rival": "Mississippi St"},
        
        # TIER 3 (TRAPS) - Base 85-90
        "Miami": {"Prestige": 87, "Talent": 89, "Tier": 2, "Rival": "Florida St"},
        "Florida St": {"Prestige": 85, "Talent": 88, "Tier": 2, "Rival": "Miami"},
        "Tennessee": {"Prestige": 86, "Talent": 89, "Tier": 2, "Rival": "Alabama"},
        "Clemson": {"Prestige": 87, "Talent": 88, "Tier": 2, "Rival": "South Carolina"},
        "USC": {"Prestige": 84, "Talent": 88, "Tier": 2, "Rival": "Notre Dame"},
        "Oklahoma": {"Prestige": 85, "Talent": 89, "Tier": 2, "Rival": "Texas"},
        "Texas A&M": {"Prestige": 84, "Talent": 89, "Tier": 2, "Rival": "Texas"},
        "Indiana": {"Prestige": 88, "Talent": 86, "Tier": 2, "Rival": "Purdue"},
        "Utah": {"Prestige": 80, "Talent": 85, "Tier": 2, "Rival": "BYU"},
        "Kansas State": {"Prestige": 79, "Talent": 84, "Tier": 2, "Rival": "Kansas"},
        "Missouri": {"Prestige": 79, "Talent": 85, "Tier": 2, "Rival": "Kansas"},
        "Iowa": {"Prestige": 79, "Talent": 83, "Tier": 2, "Rival": "Iowa State"},
        "SMU": {"Prestige": 78, "Talent": 84, "Tier": 2, "Rival": "TCU"},
        "Boise State": {"Prestige": 78, "Talent": 84, "Tier": 2, "Rival": "Fresno St"},
        "Colorado": {"Prestige": 77, "Talent": 82, "Tier": 2, "Rival": "Nebraska"},
        "Arizona": {"Prestige": 76, "Talent": 83, "Tier": 3, "Rival": "Arizona State"},
        "Virginia Tech": {"Prestige": 75, "Talent": 80, "Tier": 3, "Rival": "UVA"},
        "Tulane": {"Prestige": 74, "Talent": 81, "Tier": 3, "Rival": "LSU"},
        "App State": {"Prestige": 72, "Talent": 79, "Tier": 3, "Rival": "Georgia Southern"},
        "UNLV": {"Prestige": 70, "Talent": 78, "Tier": 3, "Rival": "Nevada"},
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
    "last_known_team_name", "last_known_team_color", "retention_data", "trophy_stats"
}

try:
    st.set_page_config(page_title="Build the Program: College Football CEO", page_icon="🏈", layout="wide")
except Exception:
    pass

# ==============================================================================
# CSS ENHANCEMENTS
# ==============================================================================
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

/* ENHANCED CARDS */
.staff-card-enhanced { background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border: 2px solid #e0e0e0; border-radius: 12px; padding: 15px; margin-bottom: 15px; position: relative; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.staff-card-enhanced:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
.staff-card-gold { border: 2px solid #FFD700; background: linear-gradient(145deg, #FFFEF0 0%, #FFF9E6 100%); }
.staff-card-silver { border: 2px solid #C0C0C0; background: linear-gradient(145deg, #F8F8F8 0%, #EFEFEF 100%); }
.staff-card-bronze { border: 2px solid #CD7F32; background: linear-gradient(145deg, #FFF5E6 0%, #FFEACC 100%); }
.staff-headshot { width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5em; font-weight: bold; color: white; margin: 0 auto 10px; border: 3px solid #ddd; }
.staff-headshot-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); border-color: #FFD700; }
.staff-headshot-silver { background: linear-gradient(135deg, #C0C0C0 0%, #909090 100%); border-color: #C0C0C0; }
.staff-headshot-bronze { background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%); border-color: #CD7F32; }
.staff-trait-icon { position: absolute; top: 10px; right: 10px; font-size: 1.5em; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); }
.staff-tenure { background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; font-weight: bold; display: inline-block; margin-top: 5px; }

/* FACILITIES */
.facility-card { background: white; border: 2px solid #e0e0e0; border-radius: 12px; padding: 20px; text-align: center; transition: all 0.3s ease; }
.facility-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
.facility-visual { font-size: 3em; margin: 15px 0; filter: grayscale(0.3); transition: all 0.3s ease; }
.facility-card:hover .facility-visual { filter: grayscale(0); transform: scale(1.1); }
.facility-level-indicator { display: flex; justify-content: center; gap: 5px; margin: 10px 0; }
.facility-pip { width: 12px; height: 12px; border-radius: 50%; background: #e0e0e0; transition: all 0.3s ease; }
.facility-pip-active { background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); box-shadow: 0 0 8px rgba(76, 175, 80, 0.6); }
.facility-next-unlock { background: #f3e5f5; border-left: 4px solid #9c27b0; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.85em; color: #6a1b9a; }

/* NIL CARDS */
.nil-card { background: white; border: 2px solid #e0e0e0; border-radius: 12px; padding: 15px; margin-bottom: 15px; position: relative; overflow: hidden; transition: all 0.3s ease; }
.nil-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.15); }
.nil-card-tier1 { border: 3px solid #FFD700; background: linear-gradient(145deg, #FFFEF0 0%, #FFF9E6 100%); }
.nil-card-tier2 { border: 3px solid #C0C0C0; background: linear-gradient(145deg, #F8F8F8 0%, #EFEFEF 100%); }
.nil-card-tier3 { border: 3px solid #CD7F32; background: linear-gradient(145deg, #FFF5E6 0%, #FFEACC 100%); }
.nil-card-signed { opacity: 0.6; position: relative; }
.nil-card-signed::after { content: "SIGNED ✓"; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-15deg); font-size: 3em; font-weight: 900; color: #4CAF50; opacity: 0.3; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
.nil-player-name { font-size: 1.3em; font-weight: bold; margin-bottom: 5px; color: #1a1a1a; }
.nil-position-badge { position: absolute; top: 10px; right: 10px; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85em; color: white; }
.pos-QB { background: #e53935; } .pos-RB { background: #43a047; } .pos-WR { background: #1e88e5; }
.pos-OL { background: #6d4c41; } .pos-DL { background: #5e35b1; } .pos-LB { background: #f57c00; } .pos-DB { background: #00acc1; }
.nil-star-rating { font-size: 1.5em; margin: 8px 0; letter-spacing: 2px; }
.nil-tier-medal { position: absolute; top: -5px; left: 10px; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.2em; color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }
.medal-gold { background: radial-gradient(circle, #FFD700 0%, #FFA500 100%); }
.medal-silver { background: radial-gradient(circle, #C0C0C0 0%, #909090 100%); }
.medal-bronze { background: radial-gradient(circle, #CD7F32 0%, #8B4513 100%); }
.nil-price-tag { background: #ff5722; color: white; padding: 8px 15px; border-radius: 20px; display: inline-block; font-weight: bold; margin: 10px 0; box-shadow: 0 2px 8px rgba(255, 87, 34, 0.4); }
.nil-trait-badge { background: #e1bee7; color: #6a1b9a; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; display: inline-block; margin-top: 5px; }

/* MISC UI */
.interest-meter-container { background: #f5f5f5; height: 20px; border-radius: 10px; overflow: hidden; margin: 10px 0; border: 1px solid #ddd; }
.interest-meter-fill { height: 100%; transition: width 0.5s ease; background: linear-gradient(90deg, #ff9800 0%, #ff5722 100%); display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; color: white; font-size: 0.75em; font-weight: bold; }
.rivalry-indicator { background: #ffebee; border: 2px dashed #e53935; padding: 6px 10px; border-radius: 6px; font-size: 0.8em; color: #c62828; margin-top: 5px; }
.game-card-preview { background: white; border: 2px solid #e0e0e0; border-radius: 10px; padding: 15px; margin-bottom: 12px; transition: all 0.3s ease; }
.game-card-preview:hover { border-color: #2196f3; box-shadow: 0 4px 12px rgba(33, 150, 243, 0.2); }
.matchup-preview { display: grid; grid-template-columns: 1fr auto 1fr; gap: 10px; margin: 10px 0; text-align: center; }
.matchup-bar { height: 8px; border-radius: 4px; background: #e0e0e0; position: relative; overflow: hidden; }
.matchup-bar-fill { height: 100%; background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%); transition: width 0.5s ease; }
.betting-line { background: #e8f5e9; color: #2e7d32; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; display: inline-block; margin-top: 5px; }
.stat-bar-left, .stat-bar-right { height: 20px; border-radius: 10px; background: #e0e0e0; position: relative; overflow: hidden; }
.stat-bar-fill-user { height: 100%; background: linear-gradient(90deg, #2196f3 0%, #1976d2 100%); transition: width 0.5s ease; display: flex; align-items: center; justify-content: flex-end; padding-right: 5px; color: white; font-size: 0.75em; font-weight: bold; }
.stat-bar-fill-opp { height: 100%; background: linear-gradient(90deg, #f44336 0%, #d32f2f 100%); transition: width 0.5s ease; display: flex; align-items: center; justify-content: flex-start; padding-left: 5px; color: white; font-size: 0.75em; font-weight: bold; }

.rank-row { display: grid; grid-template-columns: 50px 40px 1fr 100px 90px 80px; gap: 10px; align-items: center; padding: 10px; border-bottom: 1px solid #eee; background: white; transition: all 0.2s ease; }
.rank-row:hover { background: #f5f5f5; transform: translateX(3px); }
.rank-row-user { background: #e3f2fd !important; border-left: 5px solid #2196f3; font-weight: bold; }
.conf-badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 0.7em; font-weight: bold; color: white; }
.conf-SEC { background: #8B0000; } .conf-BIG { background: #00274C; } .conf-ACC { background: #00205B; } .conf-B12 { background: #003DA5; } .conf-G5 { background: #666666; }
.record-undefeated { color: #FFD700; } .record-strong { color: #4CAF50; } .record-bubble { color: #ff9800; } .record-weak { color: #f44336; }

/* TROPHY CASE */
.trophy-shelf { background: linear-gradient(180deg, #8B4513 0%, #654321 100%); padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); position: relative; }
.trophy-shelf::after { content: ''; position: absolute; bottom: -5px; left: 10px; right: 10px; height: 5px; background: rgba(0,0,0,0.2); border-radius: 0 0 8px 8px; }
.trophy-shelf-title { color: #FFD700; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
.trophy-display { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; }
.trophy-item { background: rgba(255,255,255,0.1); border: 2px solid rgba(255,215,0,0.3); border-radius: 8px; padding: 15px 10px; text-align: center; transition: all 0.3s ease; cursor: pointer; }
.trophy-item:hover { transform: translateY(-5px) scale(1.05); background: rgba(255,255,255,0.2); border-color: rgba(255,215,0,0.6); box-shadow: 0 8px 16px rgba(255,215,0,0.4); }
.trophy-icon { font-size: 2.5em; margin-bottom: 5px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3)); }
.trophy-icon-national { font-size: 3.5em; animation: trophy-glow 2s ease-in-out infinite; }
@keyframes trophy-glow { 0%, 100% { filter: drop-shadow(0 0 10px rgba(255,215,0,0.6)); } 50% { filter: drop-shadow(0 0 20px rgba(255,215,0,1)); } }
.trophy-label { font-size: 0.75em; color: white; font-weight: bold; }
.trophy-year { font-size: 0.7em; color: rgba(255,255,255,0.7); margin-top: 3px; }
.trophy-empty { opacity: 0.3; background: rgba(255,255,255,0.05); border: 2px dashed rgba(255,255,255,0.2); }
.trophy-empty .trophy-icon { filter: grayscale(1); }

/* TIMELINE */
.timeline-container { position: relative; padding: 20px 0 20px 60px; }
.timeline-line { position: absolute; left: 30px; top: 0; bottom: 0; width: 4px; background: linear-gradient(180deg, #2196f3 0%, #1976d2 100%); }
.timeline-node { position: relative; margin-bottom: 30px; padding-left: 20px; }
.timeline-dot { position: absolute; left: -42px; top: 5px; width: 24px; height: 24px; border-radius: 50%; border: 4px solid white; box-shadow: 0 0 0 2px #2196f3; z-index: 2; }
.timeline-dot-win { background: #4CAF50; box-shadow: 0 0 0 2px #4CAF50, 0 0 12px rgba(76, 175, 80, 0.6); }
.timeline-dot-loss { background: #f44336; box-shadow: 0 0 0 2px #f44336; }
.timeline-dot-championship { background: #FFD700; box-shadow: 0 0 0 2px #FFD700, 0 0 16px rgba(255, 215, 0, 0.8); width: 32px; height: 32px; left: -46px; }
.timeline-content { background: white; border: 2px solid #e0e0e0; border-radius: 8px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.timeline-year { font-weight: bold; color: #2196f3; font-size: 1.1em; margin-bottom: 5px; }
.timeline-achievement { background: #fff3e0; color: #e65100; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; display: inline-block; margin-top: 5px; }
.era-marker { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; text-align: center; margin: 20px 0; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }

/* RETIREMENT */
.mount-rushmore { background: linear-gradient(180deg, #b0bec5 0%, #78909c 100%); padding: 30px; border-radius: 12px; margin: 20px 0; box-shadow: inset 0 4px 8px rgba(0,0,0,0.2); }
.rushmore-heads { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 20px; }
.rushmore-head { text-align: center; }
.rushmore-circle { width: 100px; height: 100px; border-radius: 50%; background: rgba(255,255,255,0.9); border: 4px solid #fff; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 2em; font-weight: bold; color: #546e7a; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }
.rushmore-circle-user { border-color: #FFD700; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: white; }
.rushmore-name { font-weight: bold; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
.highlight-slide { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
.legacy-report-card { background: #fff9c4; border: 3px solid #f57f17; border-radius: 12px; padding: 30px; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
.report-card-grade { font-size: 6em; font-weight: 900; color: #f57f17; text-shadow: 3px 3px 6px rgba(0,0,0,0.2); animation: grade-stamp 1s ease-out; }
@keyframes grade-stamp { 0% { transform: scale(0) rotate(-180deg); opacity: 0; } 70% { transform: scale(1.2) rotate(10deg); } 100% { transform: scale(1) rotate(0deg); opacity: 1; } }
.percentile-badge { background: #4caf50; color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; display: inline-block; margin-top: 15px; }

/* NEWS BOX */
.news-box { background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.news-item { padding: 6px 10px; border-bottom: 1px solid #f1f1f1; font-size: 0.9em; }
.news-item-good { border-left: 4px solid #28a745; background-color: #f0fff4; }
.news-item-bad { border-left: 4px solid #dc3545; background-color: #fff5f5; }

/* STAT COMPARISON BARS - MISSING CLASSES */
.stat-comparison { margin: 8px 0; }
.stat-label { font-size: 0.85em; color: #666; margin-bottom: 3px; }
.stat-bars-container { 
    display: grid; 
    grid-template-columns: 1fr auto 1fr; 
    gap: 8px; 
    align-items: center; 
}
.mvp-star {
    color: #FFD700;
    font-size: 1.2em;
    text-shadow: 0 0 4px rgba(255, 215, 0, 0.6);
}
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
        
        good_keys = ["win", "wins", "advances", "upgrade", "signs", "committed", "found", "promotes", "hires", "universe update"]
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

# ==============================================================================
# UI HELPER FUNCTIONS
# ==============================================================================

def get_coach_initials(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2: return f"{parts[0][0]}{parts[1][0]}"
    return name[:2].upper()

def get_staff_quality_class(rating: int) -> str:
    if rating >= 9: return "staff-card-gold"
    elif rating >= 7: return "staff-card-silver"
    elif rating >= 5: return "staff-card-bronze"
    return ""

def get_trait_icon(trait: str) -> str:
    icons = {"Recruiter": "🏃", "Tactician": "🧠", "Air Raid": "✈️", "Smashmouth": "💪", "Pro Style": "🎯", "None": ""}
    return icons.get(trait, "⭐")

def render_enhanced_staff_card(coach: dict, role: str, rating: int) -> str:
    initials = get_coach_initials(coach.get('name', 'XX'))
    quality_class = get_staff_quality_class(rating)
    headshot_class = quality_class.replace('staff-card-', 'staff-headshot-')
    trait = coach.get('trait', 'None')
    trait_icon = get_trait_icon(trait)
    tenure_years = coach.get('tenure_years', 1)
    stars = "⭐" * rating + "☆" * (10 - rating)
    
    html = f"""
    <div class='staff-card-enhanced {quality_class}'>
        {f'<div class="staff-trait-icon">{trait_icon}</div>' if trait_icon else ''}
        <div class='staff-headshot {headshot_class}'>{initials}</div>
        <div class='staff-role'>{role}</div>
        <div class='staff-name'>{coach.get('name', 'Unknown')}</div>
        <div style='margin: 8px 0;'>{stars}</div>
        <div class='staff-tenure'>Year {tenure_years}</div>
        {f"<div style='margin-top: 8px; font-size: 0.85em; color: #666;'><strong>Trait:</strong> {trait}</div>" if trait != 'None' else ''}
    </div>
    """
    return html

def get_facility_visual(facility_type: str, level: int) -> str:
    visuals = {
        "Stadium": {"icon": "🏟️", "levels": ["🏚️", "🏗️", "🏟️", "🏟️✨", "🏟️🌟", "🏟️💎", "🏟️👑", "🏟️🔥", "🏟️⚡", "🏟️🏆", "🏟️🌈"]},
        "Training": {"icon": "🏋️", "levels": ["🥉", "🥈", "🥇", "💪", "💪💪", "🏋️", "🏋️‍♂️💪", "⚡💪", "⚡⚡", "🔥⚡", "👑💪"]},
        "Marketing": {"icon": "📢", "levels": ["📣", "📢", "📢📢", "📢✨", "📣🌟", "📢💫", "📢🚀", "📢🔥", "📢⚡", "📢💎", "📢👑"]}
    }
    visual_data = visuals.get(facility_type, {"levels": ["❓"] * 11})
    return visual_data["levels"][min(level, len(visual_data["levels"]) - 1)]

def get_next_unlock(facility_type: str, current_level: int) -> str:
    unlocks = {
        "Stadium": {3: "Student Section (+1 Home Field)", 5: "Jumbotron (+1 Home Field)", 7: "Premium Suites (+2 Home Field)", 9: "National Spotlight (+2 Home Field)", 10: "Historic Venue Status"},
        "Training": {3: "Weight Room Upgrade (+2 Development)", 5: "Sports Science Lab (+2 Development)", 7: "Recovery Center (+3 Development)", 9: "Elite Performance Center (+3 Development)", 10: "Olympic-Level Facilities"},
        "Marketing": {3: "Social Media Team (+$500K Revenue)", 5: "National TV Deals (+$1M Revenue)", 7: "Brand Partnerships (+$1.5M Revenue)", 9: "Global Reach (+$2M Revenue)", 10: "Media Empire Status"}
    }
    facility_unlocks = unlocks.get(facility_type, {})
    next_level = current_level + 1
    if next_level in facility_unlocks: return f"Level {next_level}: {facility_unlocks[next_level]}"
    elif current_level >= 10: return "MAX LEVEL REACHED"
    else: return f"Level {next_level}: Continued Improvements"

def render_enhanced_facility_card(facility_type: str, current_level: int, max_level: int = 10) -> str:
    visual = get_facility_visual(facility_type, current_level)
    next_unlock = get_next_unlock(facility_type, current_level)
    pips_html = ""
    for i in range(1, max_level + 1):
        pip_class = "facility-pip facility-pip-active" if i <= current_level else "facility-pip"
        pips_html += f"<div class='{pip_class}'></div>"
    
    html = f"""
    <div class='facility-card'>
        <h3>🎯 {facility_type}</h3>
        <div class='facility-visual'>{visual}</div>
        <div style='font-size: 1.5em; font-weight: bold; margin: 10px 0;'>Level {current_level}/{max_level}</div>
        <div class='facility-level-indicator'>{pips_html}</div>
        {f"<div class='facility-next-unlock'><strong>Next:</strong> {next_unlock}</div>" if current_level < max_level else "<div style='color: #4CAF50; font-weight: bold; margin-top: 10px;'>⭐ MAXED OUT ⭐</div>"}
    </div>
    """
    return html

def get_position_color(pos: str) -> str:
    colors = {"QB": "pos-QB", "RB": "pos-RB", "WR": "pos-WR", "OL": "pos-OL", "DL": "pos-DL", "LB": "pos-LB", "DB": "pos-DB"}
    return colors.get(pos, "pos-QB")

def render_nil_prospect_card(prospect: dict, is_need: bool = False) -> str:
    tier = prospect.get('tier', 3)
    name = prospect.get('name', 'Unknown')
    pos = prospect.get('pos', 'QB')
    rating = prospect.get('rating', 75)
    ask = prospect.get('ask', 1000000)
    trait = prospect.get('trait', '⭐')
    status = prospect.get('status', 'AVAILABLE')
    
    tier_class = f"nil-card-tier{tier}"
    medal_class = ["medal-gold", "medal-silver", "medal-bronze"][tier - 1]
    tier_label = ["T1", "T2", "T3"][tier - 1]
    signed_class = " nil-card-signed" if status == "SIGNED" else ""
    full_stars = rating // 10
    stars_html = "⭐" * min(full_stars, 10)
    pos_color = get_position_color(pos)
    need_badge = "<div style='background: #ff5722; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.75em; font-weight: bold; display: inline-block; margin-top: 5px;'>🎯 TEAM NEED</div>" if is_need else ""
    ask_formatted = f"${ask/1_000_000:.1f}M" if ask >= 1_000_000 else f"${ask/1_000:.0f}K"
    
    html = f"""
    <div class='nil-card {tier_class}{signed_class}'>
        <div class='nil-tier-medal {medal_class}'>{tier_label}</div>
        <div class='nil-position-badge {pos_color}'>{pos}</div>
        <div class='nil-player-name'>{name}</div>
        <div class='nil-star-rating'>{stars_html}</div>
        <div style='font-size: 1.1em; color: #666; margin: 5px 0;'><strong>OVR:</strong> {rating}</div>
        <div class='nil-price-tag'>💰 {ask_formatted}</div>
        <div class='nil-trait-badge'>{trait}</div>
        {need_badge}
    </div>
    """
    return html

def render_nil_filter_buttons() -> str:
    html = """
    <div style='display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap;'>
        <button style='background: #FFD700; color: #333; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer;'>🥇 Tier 1</button>
        <button style='background: #C0C0C0; color: #333; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer;'>🥈 Tier 2</button>
        <button style='background: #CD7F32; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer;'>🥉 Tier 3</button>
        <button style='background: #2196f3; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer;'>🎯 Needs Only</button>
        <button style='background: #4caf50; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer;'>✅ Available</button>
    </div>
    """
    return html

def render_interest_meter(recruit: dict, chance: float, spend_by_pos: dict) -> str:
    pos = recruit.get('pos', 'QB')
    offer = recruit.get('offer', 0)
    ask = recruit.get('ask', 1_000_000)
    
    interest_pct = int(chance * 100)
    if interest_pct >= 70:
        meter_color = "linear-gradient(90deg, #4CAF50 0%, #45a049 100%)"
        status_text = "🔥 HOT"
    elif interest_pct >= 40:
        meter_color = "linear-gradient(90deg, #ff9800 0%, #ff5722 100%)"
        status_text = "🌡️ WARM"
    else:
        meter_color = "linear-gradient(90deg, #9e9e9e 0%, #757575 100%)"
        status_text = "❄️ COLD"
    
    offer_status = ""
    if offer >= ask * 1.25: offer_status = "<div style='color: #4CAF50; font-weight: bold; margin-top: 5px;'>💵 OVERPAYING (+Boost)</div>"
    elif offer >= ask: offer_status = "<div style='color: #2196f3; font-weight: bold; margin-top: 5px;'>✅ MEETS ASK</div>"
    elif offer > 0: offer_status = "<div style='color: #ff9800; font-weight: bold; margin-top: 5px;'>⚠️ BELOW ASK</div>"
    
    competing = ["Ohio State", "Alabama", "Georgia"][int(chance * 3) % 3]
    rivalry_html = f"<div class='rivalry-indicator'>⚔️ Also recruiting: <strong>{competing}</strong></div>" if interest_pct < 80 else ""
    
    html = f"""
    <div style='margin: 15px 0;'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
            <span style='font-weight: bold;'>Interest Level</span>
            <span style='font-weight: bold;'>{status_text}</span>
        </div>
        <div class='interest-meter-container'>
            <div class='interest-meter-fill' style='width: {interest_pct}%; background: {meter_color};'>{interest_pct}%</div>
        </div>
        {offer_status}
        {rivalry_html}
    </div>
    """
    return html

def get_weather_icon() -> str:
    weather = ["☀️", "⛅", "🌤️", "🌧️", "❄️", "🌨️"]
    return random.choice(weather)

def render_game_preview_card(week: int, opponent: str, opp_data: dict, user_off: int, user_def: int, is_rival: bool = False) -> str:
    opp_off = opp_data.get('OffOVR', 75)
    opp_def = opp_data.get('DefOVR', 75)
    
    user_off_advantage = user_off - opp_def
    user_def_advantage = user_def - opp_off
    point_spread = int((user_off_advantage + user_def_advantage) / 2 * 0.5)
    
    if abs(point_spread) <= 3: betting_text = "PICK 'EM"
    elif point_spread > 0: betting_text = f"You -{abs(point_spread)}"
    else: betting_text = f"{opponent} -{abs(point_spread)}"
    
    weather = get_weather_icon()
    rivalry_html = ""
    if is_rival:
        trophy_names = ["The Axe", "The Bell", "The Bucket", "The Jug", "The Boot"]
        trophy = random.choice(trophy_names)
        rivalry_html = f"<div class='rivalry-trophy'>🏆 <strong>{trophy}</strong> on the line!</div>"
    
    def create_matchup_bar(user_val: int, opp_val: int) -> str:
        total = max(1, user_val + opp_val)
        user_pct = (user_val / total) * 100
        color = "#4CAF50" if user_val > opp_val else "#f44336" if user_val < opp_val else "#ff9800"
        return f"<div class='matchup-bar'><div class='matchup-bar-fill' style='width: {user_pct}%; background: {color};'></div></div>"
    
    html = f"""
    <div class='game-card-preview'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <div style='font-weight: bold; font-size: 1.2em;'>Week {week}</div>
            <div style='font-size: 1.5em;'>{weather}</div>
        </div>
        <div style='font-size: 1.3em; font-weight: bold; margin: 10px 0; text-align: center;'>vs {opponent}</div>
        <div class='betting-line'>{betting_text}</div>
        <div style='margin-top: 15px;'>
            <div style='font-size: 0.85em; color: #666; margin-bottom: 3px;'>Your OFF vs Their DEF</div>
            <div class='matchup-preview'>
                <div style='font-weight: bold;'>{user_off}</div><div>⚔️</div><div style='font-weight: bold;'>{opp_def}</div>
            </div>
            {create_matchup_bar(user_off, opp_def)}
            <div style='font-size: 0.85em; color: #666; margin-bottom: 3px; margin-top: 10px;'>Your DEF vs Their OFF</div>
            <div class='matchup-preview'>
                <div style='font-weight: bold;'>{user_def}</div><div>🛡️</div><div style='font-weight: bold;'>{opp_off}</div>
            </div>
            {create_matchup_bar(user_def, opp_off)}
        </div>
        {rivalry_html}
    </div>
    """
    return html

def render_game_result_with_bars(week: int, opponent: str, score: str, is_win: bool, stats: dict) -> str:
    css_class = "game-card-win" if is_win else "game-card-loss"
    qb_duel = stats.get('qb_duel', [75, 75])
    off_vs_def = stats.get('off_vs_def', [75, 75])
    def_vs_off = stats.get('def_vs_off', [75, 75])
    
    qb_mvp = "⭐" if qb_duel[0] > qb_duel[1] else ""
    off_mvp = "⭐" if off_vs_def[0] > off_vs_def[1] else ""
    def_mvp = "⭐" if def_vs_off[0] > def_vs_off[1] else ""
    
    def create_stat_bar(user_val: int, opp_val: int, label: str, user_mvp: str = "") -> str:
        max_val = max(user_val, opp_val, 1)
        user_pct = (user_val / max_val) * 100
        opp_pct = (opp_val / max_val) * 100
        return f"""
        <div class='stat-comparison'>
            <div class='stat-label'>{label}</div>
            <div class='stat-bars-container'>
                <div class='stat-bar-left'><div class='stat-bar-fill-user' style='width: {user_pct}%;'>{user_val} {user_mvp}</div></div>
                <div style='font-weight: bold; color: #666;'>vs</div>
                <div class='stat-bar-right'><div class='stat-bar-fill-opp' style='width: {opp_pct}%;'>{opp_val}</div></div>
            </div>
        </div>
        """
    
    html = f"""
    <div class='game-card {css_class}'>
        <div class='card-header'><span style='font-size: 1.3em;'>{score}</span><span>vs {opponent}</span></div>
        {create_stat_bar(qb_duel[0], qb_duel[1], "🔥 QB Duel", qb_mvp)}
        {create_stat_bar(off_vs_def[0], off_vs_def[1], "⚔️ OFF vs DEF", off_mvp)}
        {create_stat_bar(def_vs_off[0], def_vs_off[1], "🛡️ DEF vs OFF", def_mvp)}
    </div>
    """
    return html

def get_conference_badge_class(conf: str) -> str:
    conf_map = {"SEC": "conf-SEC", "Big Ten": "conf-BIG", "ACC": "conf-ACC", "Big 12": "conf-B12"}
    return conf_map.get(conf, "conf-G5")

def get_record_color_class(wins: int, losses: int) -> str:
    if losses == 0 and wins >= 12: return "record-undefeated"
    elif wins >= 10: return "record-strong"
    elif wins >= 6: return "record-bubble"
    else: return "record-weak"

def render_enhanced_ranking_row(rank: int, team: str, wins: int, losses: int, conf: str, is_user: bool = False, last_rank: int = None) -> str:
    row_class = "rank-row-user" if is_user else "rank-row"
    conf_badge_class = get_conference_badge_class(conf)
    record_class = get_record_color_class(wins, losses)
    
    if rank <= 12: status = "🏆 CFP"; status_color = "#4CAF50"
    elif wins >= 6: status = "🎳 BOWL"; status_color = "#2196F3"
    else: status = "❌ OUT"; status_color = "#f44336"
    
    bubble_icon = " <span class='bubble-warning'>⚠️</span>" if 11 <= rank <= 14 else ""
    trend_arrow = ""
    if last_rank is not None:
        if last_rank > rank: trend_arrow = f"<span class='trend-arrow trend-up'>{'↑' * min(3, (last_rank - rank) // 2)}</span>"
        elif last_rank < rank: trend_arrow = f"<span class='trend-arrow trend-down'>{'↓' * min(3, (rank - last_rank) // 2)}</span>"
    
    html = f"""
    <div class='{row_class}'>
        <div class='rank-num'>#{rank}{trend_arrow}</div>
        <div><span class='conf-badge {conf_badge_class}'>{conf[:3].upper()}</span></div>
        <div class='rank-team'>{team}{bubble_icon}</div>
        <div class='rank-rec'><span class='{record_class}'><b>{wins}-{losses}</b></span></div>
        <div class='rank-status' style='color: {status_color};'>{status}</div>
    </div>
    """
    return html

def render_rankings_table_header() -> str:
    return """
    <div style='display: grid; grid-template-columns: 50px 40px 1fr 100px 90px 80px; gap: 10px; align-items: center; padding: 10px; background: #f5f5f5; font-weight: bold; border-radius: 8px 8px 0 0; margin-bottom: 5px;'>
        <div>Rank</div><div>Conf</div><div>Team</div><div>Record</div><div>Status</div>
    </div>
    """
    era_markers = ""
    for era in eras:
        era_markers += f"<div class='era-marker' style='background: linear-gradient(135deg, {era['color']} 0%, {era['color']}dd 100%);'>📅 {era['name']} ({era['start_year']}-{era['end_year']})</div>"
    
    full_html = f"<div style='margin: 20px 0;'>{era_markers}<div class='timeline-container'><div class='timeline-line'></div>{timeline_html}</div></div>"
    return full_html

def calculate_percentile(user_score: int, all_coaches: List[Dict]) -> int:
    """
    Calculate the user's percentile rank among all coaches based on career score.
    
    Args:
        user_score: User's calculated career score (Titles * 50 + Wins * 2)
        all_coaches: List of all coach dictionaries with Titles and Wins
        
    Returns:
        int: Percentile rank (0-100), where 100 is the best
    """
    scores = sorted([coach.get("Titles", 0) * 50 + coach.get("Wins", 0) * 2 for coach in all_coaches], reverse=True)
    if not scores:
        return 100
    user_position = len([s for s in scores if s > user_score])
    percentile = int(((len(scores) - user_position) / len(scores)) * 100)
    return percentile

def render_mount_rushmore(top_coaches: List[Dict], user_data: Dict, user_rank: int) -> str:
    """
    Render the Mount Rushmore display showing the top 4 coaches of all time.
    
    Args:
        top_coaches: List of top coach dictionaries
        user_data: Current user's coach data
        user_rank: User's ranking position
        
    Returns:
        str: HTML string for the Mount Rushmore display
    """
    heads_html = ""
    for i, coach in enumerate(top_coaches):
        is_user = (coach.get("Name", "").endswith("(You)"))
        circle_class = "rushmore-circle-user" if is_user else "rushmore-circle"
        if is_user:
            display = "YOU"
        else:
            name = coach.get("Name", "?")
            parts = name.split()
            display = f"{parts[0][0]}{parts[1][0]}" if len(parts) >= 2 else name[:2]
        
        heads_html += f"<div class='rushmore-head'><div class='{circle_class}'>{display}</div><div class='rushmore-name'>#{i+1} {coach.get('Name', 'Unknown')}</div><div style='color: white; font-size: 0.85em;'>{coach.get('Titles', 0)} Titles</div></div>"
    
    climber_html = ""
    if user_rank > 4:
        climber_html = f"<div style='text-align: center; margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 8px;'><div style='color: white; font-weight: bold; margin-bottom: 5px;'>THE CLIMBERS</div><div style='color: white; font-size: 1.2em;'>#{user_rank} {user_data.get('Name', 'You')}</div><div style='color: rgba(255,255,255,0.8); font-size: 0.9em;'>{user_data.get('Titles', 0)} Titles • {user_data.get('Wins', 0)} Wins</div></div>"
    
    html = f"<div class='mount-rushmore'><div style='text-align: center; color: white; font-size: 1.5em; font-weight: bold; margin-bottom: 10px;'>🗻 MOUNT RUSHMORE OF CFB COACHES 🗻</div><div class='rushmore-heads'>{heads_html}</div>{climber_html}</div>"
    return html

def generate_career_highlights(history: List[Dict], career_stats: Dict) -> List[Dict]:
    highlights = []
    championships = [h for h in history if "TITLE" in h.get("PostseasonResult", "")]
    if championships:
        first_title = championships[0]
        highlights.append({"year": first_title.get("Year"), "text": f"Won First National Championship!", "color": "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)"})
        if len(championships) >= 3:
            highlights.append({"year": championships[2].get("Year"), "text": f"Dynasty Established - 3rd National Title", "color": "linear-gradient(135deg, #4CAF50 0%, #45a049 100%)"})
    
    perfect = [h for h in history if h.get("Record", "").endswith("-0")]
    if perfect:
        highlights.append({"year": perfect[0].get("Year"), "text": f"Perfect Season! ({perfect[0].get('Record')})", "color": "linear-gradient(135deg, #2196F3 0%, #1976D2 100%)"})
    
    win_count = 0
    for h in history:
        try:
            wins = int(h.get("Record", "0-0").split('-')[0])
            win_count += wins
            if win_count >= 50 and len(highlights) < 5:
                highlights.append({"year": h.get("Year"), "text": f"Reached 50 Career Wins!", "color": "linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%)"})
                break
        except (ValueError, IndexError, AttributeError): pass
    
    for h in history:
        if "CFP" in h.get("PostseasonResult", ""):
            highlights.append({"year": h.get("Year"), "text": f"Made College Football Playoff", "color": "linear-gradient(135deg, #FF5722 0%, #E64A19 100%)"})
            break
            
    return highlights[:5]

def render_career_highlights_carousel(highlights: List[Dict]) -> str:
    if not highlights: return ""
    slides_html = ""
    for highlight in highlights:
        slides_html += f"<div class='highlight-slide' style='background: {highlight.get('color', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)')};'><div class='highlight-year'>{highlight.get('year', '????')}</div><div class='highlight-text'>{highlight.get('text', 'Achievement Unlocked!')}</div></div>"
    html = f"<div class='career-highlights-carousel'><h3 style='text-align: center; margin-bottom: 20px;'>🎬 Career Highlight Reel</h3>{slides_html}</div>"
    return html

def render_legacy_report_card(grade: str, score: int, percentile: int) -> str:
    grade_labels = {"S": "🐐 GOAT STATUS", "A": "🏛️ HALL OF FAME LEGEND", "B": "⭐ CHAMPIONSHIP COACH", "C": "✅ ACCOMPLISHED CAREER", "D": "😐 SOLID EFFORT"}
    label = grade_labels.get(grade, "Career Complete")
    html = f"<div class='legacy-report-card'><h2 style='margin-bottom: 10px;'>Legacy Report Card</h2><div class='report-card-grade'>{grade}</div><div style='font-size: 1.5em; font-weight: bold; color: #f57f17; margin: 10px 0;'>{label}</div><div style='font-size: 1.2em; color: #666; margin: 5px 0;'>Career Score: <strong>{score}</strong></div><div class='percentile-badge'>Top {100 - percentile}% of All-Time Coaches</div></div>"
    return html
def render_trophy_shelf(shelf_name: str, trophies: List[Dict], max_display: int = 8, show_empty: bool = True) -> str:
    """Render a 3D trophy shelf display with trophies organized by category."""
    category_data = GameConfig.TROPHY_CATEGORIES.get(shelf_name, {
        "icon": "🏆", 
        "color": "#FFD700", 
        "empty_text": "Earn Trophy",
        "track_key": "titles"
    })
    
    trophy_html = ""
    
    # Render earned trophies
    for trophy in trophies[:max_display]:
        year = trophy.get("Year", "????")
        icon = trophy.get("Icon", category_data["icon"])
        name = trophy.get("Name", shelf_name)
        icon_class = "trophy-icon-national" if "National" in shelf_name or "Championship" in name else "trophy-icon"
        trophy_html += f"""
        <div class='trophy-item' title='{name} - {year}'>
            <div class='{icon_class}'>{icon}</div>
            <div class='trophy-label'>{name}</div>
            <div class='trophy-year'>{year}</div>
        </div>
        """
    
    # Render empty trophy slots
    if show_empty:
        empty_count = max(0, max_display - len(trophies))
        for _ in range(empty_count):
            trophy_html += f"""
            <div class='trophy-item trophy-empty' title='{category_data["empty_text"]}'>
                <div class='trophy-icon'>{category_data["icon"]}</div>
                <div class='trophy-label'>???</div>
                <div class='trophy-year'>????</div>
            </div>
            """
    
    # Build complete shelf HTML
    html = f"""
    <div class='trophy-shelf'>
        <div class='trophy-shelf-title'>{shelf_name} ({len(trophies)})</div>
        <div class='trophy-display'>{trophy_html}</div>
    </div>
    """
    return html

# ==============================================================================
# UI COMPONENTS
# ==============================================================================

class UIComponents:
    @staticmethod
    def gradient_header(title: str, subtitle: str = "", gradient: str = "135deg, #667eea 0%, #764ba2 100%") -> str:
        subtitle_html = f"<p style='color: rgba(255,255,255,0.9); font-size: 1.2em; margin-top: 10px;'>{subtitle}</p>" if subtitle else ""
        return f"<div style='background: linear-gradient({gradient}); padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.3); margin-bottom: 30px;'><h1 style='color: white; font-size: 3em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>{subtitle_html}</div>"
    
    @staticmethod
    def hero_card(rank: int, team: str, wins: int, losses: int, conf: str, outcome_type: str) -> str:
        styles = {"BYE": {"bg": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "text": "🛡️ FIRST ROUND BYE", "icon": "🏆"}, "PLAYOFF": {"bg": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)", "text": "⚔️ PLAYOFF BOUND", "icon": "🎯"}, "BOWL": {"bg": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)", "text": "🎳 BOWL ELIGIBLE", "icon": "✅"}, "ELIMINATED": {"bg": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)", "text": "❌ SEASON OVER", "icon": "💔"}}
        style = styles.get(outcome_type, styles["ELIMINATED"])
        return f"<div style='background: {style['bg']}; padding: 30px; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); margin-bottom: 30px; border: 3px solid rgba(255,255,255,0.3);'><div style='text-align: center;'><div style='font-size: 1.2em; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;'>YOUR FINAL RANKING</div><div style='font-size: 5em; font-weight: 900; color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.3); margin: 10px 0;'>#{rank}</div><div style='font-size: 2em; font-weight: bold; color: white; margin: 10px 0;'>{team}</div><div style='font-size: 1.5em; color: rgba(255,255,255,0.95); margin-bottom: 20px;'>{wins}-{losses} • {conf}</div><div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-top: 20px; backdrop-filter: blur(10px);'><div style='font-size: 2em; margin-bottom: 5px;'>{style['icon']}</div><div style='font-size: 1.3em; font-weight: bold; color: white;'>{style['text']}</div></div></div></div>"
    
    @staticmethod
    def team_stat_card(team: str, record: str, overall: int, offense: int, defense: int, stadium: int, is_user: bool = False) -> str:
        color, bg_color, side = ("#2196F3", "rgba(33, 150, 243, 0.1)", "left") if is_user else ("#f44336", "rgba(244, 67, 54, 0.1)", "right")
        return f"<div style='background: {bg_color}; padding: 20px; border-radius: 10px; border-{side}: 5px solid {color};'><h3 style='text-align: center; color: {color};'>{team}</h3><div style='text-align: center; margin: 15px 0;'><div style='font-size: 2.5em; font-weight: bold;'>{record}</div></div><hr style='opacity: 0.3;'><div style='display: grid; gap: 10px;'><div style='display: flex; justify-content: space-between;'><span>Overall:</span><strong>{overall}</strong></div><div style='display: flex; justify-content: space-between;'><span>Offense:</span><strong>{offense}</strong></div><div style='display: flex; justify-content: space-between;'><span>Defense:</span><strong>{defense}</strong></div><div style='display: flex; justify-content: space-between;'><span>Stadium:</span><strong>{stadium}</strong></div></div></div>"
    
    @staticmethod
    def progress_bar_gradient(label: str, value: int, max_value: int = 100, team_color: str = "#2196F3") -> str:
        pct = min(100, (value / max_value) * 100)
        return f"<div style='margin: 10px 0;'><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span style='font-weight: bold;'>{label}</span><span>{value}/{max_value}</span></div><div style='background: #e0e0e0; height: 24px; border-radius: 12px; overflow: hidden;'><div style='width: {pct}%; height: 100%; background: {team_color}; transition: width 0.3s ease;'></div></div></div>"
    def star_rating(rating: int, max_stars: int = 10) -> str:
        return "⭐" * rating + "☆" * (max_stars - rating)

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
    """
    Manages team budget operations including spending, revenue, and validation.
    All operations interact with st.session_state.budget.
    """
    
    @staticmethod
    def get_current() -> int:
        """Get current budget amount from session state."""
        return safe_int(st.session_state.get("budget", 0), 0)
    
    @staticmethod
    def spend(amount: int, description: str, show_toast: bool = True) -> bool:
        """
        Spend budget on an item with validation.
        
        Args:
            amount: Amount to spend
            description: Description of purchase for notifications
            show_toast: Whether to show success toast notification
            
        Returns:
            bool: True if successful, False if insufficient funds
        """
        amount = safe_int(amount, 0)
        if not validate_budget_input(amount, BudgetManager.get_current(), description):
            return False
        st.session_state.budget = BudgetManager.get_current() - amount
        clamp_budget()
        if show_toast:
            safe_toast(f"Spent {helper_format_cash(amount)} on {description}")
        return True
    
    @staticmethod
    def add(amount: int, description: str, show_toast: bool = True) -> None:
        """
        Add money to budget.
        
        Args:
            amount: Amount to add
            description: Description of income source
            show_toast: Whether to show notification toast
        """
        amount = safe_int(amount, 0)
        st.session_state.budget = BudgetManager.get_current() + amount
        clamp_budget()
        if show_toast and amount > 0:
            safe_toast(f"Received {helper_format_cash(amount)}: {description}")
        if description:
            add_news(description)
    
    @staticmethod
    def calculate_revenue(tier: int, marketing_level: int, inflation: float) -> int:
        """
        Calculate annual revenue based on tier, marketing, and conference multipliers.
        
        Args:
            tier: School tier (1=Elite, 2=High, 3=Mid, 4=Low)
            marketing_level: Marketing department level (adds 1.5M per level)
            inflation: Inflation multiplier for year
            
        Returns:
            int: Total calculated revenue
        """
        base = {1: 22_000_000, 2: 14_000_000, 3: 6_000_000, 4: 3_000_000}.get(tier, 3_000_000)
        bonus = safe_int(marketing_level, 0) * 1_500_000
        total = (base + bonus) * float(inflation) * float(st.session_state.get("conf_revenue_boost_mult", 1.0))
        return int(total)

class OpponentManager:
    """
    Manages opponent team data and ensures consistency across game sessions.
    """
    
    @staticmethod
    def get(team_name: str) -> dict:
        """
        Get or create opponent data for a given team.
        
        Args:
            team_name: Name of the opponent team
            
        Returns:
            dict: Opponent data dictionary with ratings and stats
        """
        if "opponents_db" not in st.session_state:
            st.session_state.opponents_db = {}
        if team_name not in st.session_state.opponents_db:
            st.session_state.opponents_db[team_name] = OpponentFactory.create_opponent(team_name, context="RUNTIME")
        
        opp = st.session_state.opponents_db[team_name]
        opp.setdefault("Prestige", 60)
        opp.setdefault("OVR", 75)
        
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
        
        movers = []
        for team, data in st.session_state.opponents_db.items():
            base_ovr = safe_int(data.get("OVR", 75), 75)
            wins = int((base_ovr / 105) * 12) + random.randint(-3, 3) 
            wins = max(0, min(12, wins))
            
            old_pres = safe_int(data.get("Prestige", 60), 60)
            
            evolved = OpponentFactory.create_opponent(team, context="EVOLVE", performance_data={"wins": wins})
            data["Prestige"] = evolved["Prestige"]; data["OVR"] = evolved["OVR"]
            
            if data["Prestige"] > 80 and wins < 6: data["Coaches"] = {"OC": random.randint(7, 9), "DC": random.randint(7, 9)}
            elif data["Prestige"] < 70 and wins > 9: data["Coaches"] = {"OC": random.randint(3, 6), "DC": random.randint(3, 6)}
            else: data["Coaches"] = evolved["Coaches"]
            
            if random.random() < 0.35: data.pop("OffOVR", None); data.pop("DefOVR", None)
            
            diff = data["Prestige"] - old_pres
            if abs(diff) >= 3:
                movers.append(f"{team} ({'+' if diff>0 else ''}{diff})")
        
        if movers:
            report = ", ".join(movers[:3])
            add_news(f"Universe Report: {report}")

class OpponentFactory:
    @staticmethod
    def create_opponent(team_name: str, context: str = "INIT", performance_data: dict = None) -> dict:
        is_elite = team_name in GameConfig.CONFERENCES.get("SEC", []) or team_name in GameConfig.CONFERENCES.get("Big Ten", []) or team_name in GameConfig.CONFERENCES.get("ACC", [])
        if team_name in GameConfig.REAL_WORLD_INIT:
            d = GameConfig.REAL_WORLD_INIT[team_name]
            pres, ovr = d["Prestige"], d["Talent"]
        else:
            pres, ovr = (78, 79) if is_elite else (60, 70) 
        
        if context == "EVOLVE" and performance_data:
            wins = performance_data.get("wins", 6)
            if wins >= 10: pres = min(99, pres + 3)
            elif wins <= 4: pres = max(20, pres - 3)
            ovr = int(pres * 0.9) + random.randint(-3, 3)
        elif context == "RUNTIME":
            try:
                uc = st.session_state.get("team_conf", "G5")
                if uc in ["G5", "MAC", "Pac-12", "Indep"]:
                    u_ovr = st.session_state.get("team_rating", 75)
                    u_win = st.session_state.get("record", {}).get("w", 0)
                    boost = random.randint(10, 15) if (u_ovr >= 82 or u_win >= 8) else (random.randint(6, 10) if (u_ovr >= 78 or u_win >= 6) else 0)
                    if boost > 0: ovr = min(88, ovr + boost)
            except (KeyError, AttributeError):
                # Skip if conference data not available
                pass
        
        if is_elite or pres >= 90: c_min, c_max, s_min, s_max = 9, 10, 10, 11
        elif pres >= 85: c_min, c_max, s_min, s_max = 9, 10, 9, 11
        elif pres >= 75: c_min, c_max, s_min, s_max = 7, 9, 7, 9
        else: c_min, c_max, s_min, s_max = 5, 8, 5, 8 
        
        return {
            "Prestige": pres, "OVR": ovr,
            "Off": random.choice(GameConfig.SCHEMES["Offense"]), "Def": random.choice(GameConfig.SCHEMES["Defense"]),
            "Coaches": {"OC": random.randint(c_min, c_max), "DC": random.randint(c_min, c_max)},
            "Stadium": random.randint(s_min, s_max)
        }

# ==============================================================================
# OTHER HELPERS
# ==============================================================================
def make_deterministic_rng(*parts) -> random.Random:
    base = (str(st.session_state.get("state_version", "")), str(st.session_state.get("year", "")), str(st.session_state.get("team_name", "")))
    seed_str = "|".join([*base, *[str(p) for p in parts]])
    return random.Random(seed_str)

def game_rng(year: int, week: int, opp: str, mode: str = "PLAY") -> random.Random:
    """
    Create a deterministic random number generator for game simulation.
    
    Args:
        year: Current game year
        week: Current week number
        opp: Opponent team name
        mode: Game mode (e.g., "PLAY", "SIM")
        
    Returns:
        random.Random: Seeded random number generator for reproducible results
    """
    return make_deterministic_rng("game", mode, int(year), int(week), str(opp))

def calculate_difficulty_multiplier(user_conf: str, user_prestige: int, user_ovr: int, user_wins: int) -> float:
    """
    Calculate difficulty multiplier for lower-tier teams (Cinderella Tax).
    
    Teams from weaker conferences face tougher opponents when they perform well,
    making it harder to maintain success (simulating real playoff committee bias).
    
    Args:
        user_conf: User's conference name
        user_prestige: Team prestige rating (0-100)
        user_ovr: Team overall rating (0-99)
        user_wins: Current season wins
        
    Returns:
        float: Difficulty multiplier (1.0 - 1.35), applied to opponent strength
    """
    mult = 1.0
    # G5 teams face increased difficulty when successful
    if user_conf in ["G5", "MAC", "Pac-12", "Indep"]:
        if user_ovr >= 85:
            mult += 0.20
        elif user_ovr >= 80:
            mult += 0.15
        elif user_ovr >= 75:
            mult += 0.10
        if user_wins >= 10:
            mult += 0.08
        elif user_wins >= 8:
            mult += 0.05
        if user_prestige >= 80:
            mult += 0.05
    # Elite P5 teams get slight boost
    elif user_conf in ["SEC", "Big Ten"] and user_prestige >= 90:
        mult += 0.05
    return min(1.35, mult)

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
    """
    Calculate College Football Playoff committee ranking score.
    
    Simulates the real CFP committee's bias toward power conferences and
    penalizes G5 teams with any losses.
    
    Args:
        team_name: Team name (currently unused but kept for interface)
        wins: Number of wins
        losses: Number of losses
        conf: Conference name
        sos_score: Strength of schedule score
        
    Returns:
        int: Committee score used for ranking teams
    """
    score = (wins * 105) - (losses * 115) + (sos_score * 3.0)
    # Power conference bonuses
    if conf in ["SEC", "Big Ten"]:
        score += 140
    elif conf in ["ACC", "Big 12"]:
        score += 80
    # G5 penalty for any loss
    if conf in ["G5", "MAC", "Indep"] and losses > 0:
        score -= 300
    return int(score)

def trophy_icon(name: str) -> str:
    return GameConfig.TROPHY_ICONS.get(name, GameConfig.TROPHY_ICONS.get("Bowl Win", "🎳"))

def award_trophy(trophy_name: str):
    if "trophies" not in st.session_state: st.session_state.trophies = []
    st.session_state.trophies.append({"Year": st.session_state.year, "Name": trophy_name, "Icon": trophy_icon(trophy_name)})
    
    # Update trophy stats
    if "trophy_stats" not in st.session_state: initialize_trophy_tracking()
    
    if "National" in trophy_name or "Championship" in trophy_name:
        st.session_state.trophy_stats["titles"] += 1
    if "Bowl" in trophy_name:
        st.session_state.trophy_stats["bowl_wins"] += 1

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

def normalize_shares(shares: dict):
    """
    Normalize position budget shares to percentages summing to 100%.
    
    Args:
        shares: Dictionary mapping positions to budget amounts
        
    Returns:
        dict: Normalized percentages for each position
    """
    def _val(pos):
        try:
            return max(0.0, float(shares.get(pos, 0.0)))
        except (ValueError, TypeError):
            return 0.0
    
    total = sum(_val(p) for p in GameConfig.POSITIONS)
    if total <= 0:
        return {p: 100.0/len(GameConfig.POSITIONS) for p in GameConfig.POSITIONS}
    return {p: (_val(p)/total)*100.0 for p in GameConfig.POSITIONS}

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
        safe_toast("🏆 Achievement Unlocked: First Bowl Win")
    if st.session_state.prestige >= 80 and "Program Builder" not in st.session_state.achievements:
        st.session_state.achievements.append("Program Builder"); safe_toast("🏆 Achievement Unlocked: Program Builder")
    if st.session_state.record['l'] == 0 and st.session_state.record['w'] >= 12 and "Perfect Season" not in st.session_state.achievements:
        st.session_state.achievements.append("Perfect Season"); safe_toast("🏆 Achievement Unlocked: Perfect Season")
    
    # Trophy Stats Tracking
    if "trophy_stats" not in st.session_state: initialize_trophy_tracking()
    
    # CFP Appearances
    if st.session_state.get("last_postseason_result", "").startswith("CFP"):
        st.session_state.trophy_stats["cfp_appearances"] += 1
    
    # Perfect Seasons
    if st.session_state.record['l'] == 0 and st.session_state.record['w'] >= 12:
        st.session_state.trophy_stats["perfect_seasons"] += 1
    
    # 10+ Win Seasons
    if st.session_state.record['w'] >= 10:
        st.session_state.trophy_stats["ten_win_seasons"] += 1

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
            html += f"<div class='{cls}'><div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'><span>{m.get('t1')}</span><span class='bracket-score'>{m.get('s1','')}</span></div><div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'><span>{m.get('t2')}</span><span class='bracket-score'>{m.get('s2','')}</span></div></div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Quarterfinals</div>"
        qf_seeds = data.get("QF_Seeds", seeds[:4])
        for i, s in enumerate(qf_seeds):
            cls = "bracket-matchup bracket-bye"
            if user_team == s: cls += " user-involved"
            html += f"<div class='{cls}'><div class='bracket-team'><span><span class='bracket-seed'>{i+1}</span>{s}</span></div><div style='text-align:center;color:#666;font-size:0.85em;margin-top:8px;'>BYE</div></div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Semifinals</div>"
        html += "<div class='bracket-matchup' style='opacity:0.4;text-align:center;padding:20px;color:#999;'>TBD</div>" * 2
        html += "</div>"
    
    elif round_num == 2:
        html += "<div class='bracket-round'><div class='bracket-round-title'>Quarterfinals</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            cls = "bracket-matchup"
            if m.get("winner"): cls += " completed"
            else: cls += " active"
            if user_team in [m.get("t1"), m.get("t2")]: cls += " user-involved"
            html += f"<div class='{cls}'><div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'><span><span class='bracket-seed'>{seed_map.get(m.get('t1'),'?')}</span>{m.get('t1')}</span><span class='bracket-score'>{m.get('s1','')}</span></div><div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'><span><span class='bracket-seed'>{seed_map.get(m.get('t2'),'?')}</span>{m.get('t2')}</span><span class='bracket-score'>{m.get('s2','')}</span></div></div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Semifinals</div>"
        html += "<div class='bracket-matchup' style='opacity:0.6;text-align:center;padding:20px;color:#999;'>Awaiting QF</div>" * 2
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>Championship</div>"
        html += "<div class='bracket-matchup' style='opacity:0.3;text-align:center;padding:30px;color:#999;'>🏆</div></div>"
    
    elif round_num == 3:
        html += "<div class='bracket-round'><div class='bracket-round-title'>Semifinals</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            cls = "bracket-matchup"
            if m.get("winner"): cls += " completed"
            else: cls += " active"
            if user_team in [m.get("t1"), m.get("t2")]: cls += " user-involved"
            html += f"<div class='{cls}'><div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'><span><span class='bracket-seed'>{seed_map.get(m.get('t1'),'?')}</span>{m.get('t1')}</span><span class='bracket-score'>{m.get('s1','')}</span></div><div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'><span><span class='bracket-seed'>{seed_map.get(m.get('t2'),'?')}</span>{m.get('t2')}</span><span class='bracket-score'>{m.get('s2','')}</span></div></div>"
        
        html += "</div><div class='bracket-round'><div class='bracket-round-title'>National Championship</div>"
        html += "<div class='bracket-matchup active' style='padding:30px;text-align:center;'><div style='font-size:2em;'>🏆</div><div style='color:#666;margin-top:10px;'>Awaiting Semifinals</div></div></div>"
    
    elif round_num == 4:  # Final
        html += "<div class='bracket-round'><div class='bracket-round-title'>National Championship</div>"
        seed_map = data.get("SeedMap", {})
        for m in matches:
            cls = "bracket-matchup"
            if m.get("winner"): cls += " completed"
            else: cls += " active"
            if user_team in [m.get("t1"), m.get("t2")]: cls += " user-involved"
            html += f"<div class='{cls}' style='min-width:300px;'><div style='text-align:center;font-size:1.5em;margin-bottom:10px;'>🏆</div><div class='bracket-team {'winner' if m.get('winner')==m.get('t1') else 'loser' if m.get('winner') else ''}'><span><span class='bracket-seed'>{seed_map.get(m.get('t1'),'?')}</span>{m.get('t1')}</span><span class='bracket-score'>{m.get('s1','')}</span></div><div class='bracket-team {'winner' if m.get('winner')==m.get('t2') else 'loser' if m.get('winner') else ''}'><span><span class='bracket-seed'>{seed_map.get(m.get('t2'),'?')}</span>{m.get('t2')}</span><span class='bracket-score'>{m.get('s2','')}</span></div></div>"
        html += "</div>"

    elif round_num == 5: # Champion
         html += "<div class='bracket-round'><div class='bracket-round-title'>National Champions</div>"
         html += "<div class='bracket-matchup completed' style='padding:30px;text-align:center;border:4px solid #FFD700;background:#FFF9C4'><div style='font-size:3em;'>🏆</div><div style='font-weight:900;font-size:1.5em;margin-top:10px;color:#B7791F'>CHAMPION</div></div></div>"
    
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def init_playoff_bracket(user_rank, user_team_name):
    results = st.session_state.get("selection_sunday_results", []) or []
    top12 = [t.get("Team") for t in results[:12] if t.get("Team")]
    while len(top12) < 12: top12.append("FCS East")
    seen = set()
    for i in range(len(top12)):
        nm = top12[i]
        if nm in seen: top12[i] = "FCS East"
        else: seen.add(nm)
    seed_map = {tm: idx for idx, tm in enumerate(top12, start=1)}
    try:
        ur = int(user_rank)
    except (ValueError, TypeError):
        ur = 999
    if 1 <= ur <= 12:
        target_idx = ur - 1; top12[target_idx] = user_team_name; seed_map[user_team_name] = ur
        for i in range(len(top12)):
            if i != target_idx and top12[i] == user_team_name: top12[i] = "FCS East"
    
    r1_matches = [
        {"seed_high": 5, "seed_low": 12, "t1": top12[4], "t2": top12[11], "winner": None},
        {"seed_high": 6, "seed_low": 11, "t1": top12[5], "t2": top12[10], "winner": None},
        {"seed_high": 7, "seed_low": 10, "t1": top12[6], "t2": top12[9], "winner": None},
        {"seed_high": 8, "seed_low": 9, "t1": top12[7], "t2": top12[8], "winner": None},
    ]
    return {"Type": "CFP", "Round": 1, "Seeds": top12, "QF_Seeds": top12[:4], "Matches": r1_matches, "UserAlive": True, "Rank": int(ur), "SeedMap": seed_map}

def initialize_trophy_tracking():
    if "trophy_stats" not in st.session_state:
        st.session_state.trophy_stats = {
            "titles": 0, "cfp_appearances": 0, "perfect_seasons": 0, "bowl_wins": 0,
            "ten_win_seasons": 0, "conf_titles": 0, "rivalry_wins": 0, "top5_finishes": 0
        }

def organize_trophies_by_category(all_trophies: List[Dict]) -> Dict[str, List[Dict]]:
    categories = {cat: [] for cat in GameConfig.TROPHY_CATEGORIES.keys()}
    for trophy in all_trophies:
        name = trophy.get("Name", "")
        if "National" in name or "Championship" in name: categories["National Championships"].append(trophy)
        elif "CFP" in name or "Playoff" in name: categories["CFP Appearances"].append(trophy)
        elif "Bowl" in name: categories["Bowl Victories"].append(trophy)
        elif "Perfect" in name: categories["Perfect Seasons"].append(trophy)
        elif "Conference" in name: categories["Conference Titles"].append(trophy)
    return categories

def categorize_season(record: str, postseason: str) -> str:
    try:
        wins, losses = map(int, record.split('-'))
        if "TITLE" in postseason or "CHAMPIONSHIP" in postseason:
            return "championship"
        elif wins >= 10:
            return "win"
        else:
            return "loss"
    except (ValueError, AttributeError):
        return "loss"

def detect_era_boundaries(history: List[Dict]) -> List[Dict]:
    if len(history) < 3: return []
    eras = []
    current_era = None
    for i, season in enumerate(history):
        category = categorize_season(season.get("Record", "0-0"), season.get("PostseasonResult", ""))
        if category == "championship":
            if current_era and current_era["type"] != "dynasty": eras.append(current_era)
            current_era = {"name": "Dynasty Peak", "type": "dynasty", "start_year": season.get("Year"), "end_year": season.get("Year"), "color": "#FFD700"}
        elif current_era is None:
            current_era = {"name": "The Rebuild", "type": "rebuild", "start_year": season.get("Year"), "end_year": season.get("Year"), "color": "#2196F3"}
        else:
            current_era["end_year"] = season.get("Year")
    if current_era: eras.append(current_era)
    return eras

def render_timeline_node(season: Dict, category: str) -> str:
    year = season.get("Year", "????")
    record = season.get("Record", "?-?")
    rank = season.get("Rank", "NR")
    bowl = season.get("Bowl", "None")
    result = season.get("PostseasonResult", "")
    
    dot_class = "timeline-dot"
    if category == "championship": dot_class += " timeline-dot-championship"
    elif category == "win": dot_class += " timeline-dot-win"
    else: dot_class += " timeline-dot-loss"
    
    achievements = []
    if "TITLE" in result or "CHAMPIONSHIP" in result: achievements.append("<span class='timeline-achievement'>🏆 National Champs</span>")
    if "CFP" in result: achievements.append("<span class='timeline-achievement'>⚔️ CFP Appearance</span>")
    if record.endswith("-0"): achievements.append("<span class='timeline-achievement'>💯 Perfect Season</span>")
    
    achievements_html = " ".join(achievements) if achievements else ""
    
    html = f"""
    <div class='timeline-node'>
        <div class='{dot_class}'></div>
        <div class='timeline-content'>
            <div class='timeline-year'>Year {year}</div>
            <div class='timeline-record'><strong>{record}</strong> • Rank {rank}</div>
            <div style='font-size: 0.85em; color: #666; margin-top: 5px;'>{bowl}</div>
            {achievements_html}
        </div>
    </div>
    """
    return html

def render_dynasty_timeline_infographic(history: List[Dict], max_years: int = 20) -> str:
    if not history: return "<p style='text-align: center; color: #999;'>No dynasty history yet. Start your legend!</p>"
    history = sorted(history, key=lambda x: x.get("Year", 0))
    eras = detect_era_boundaries(history)
    timeline_html = ""
    for season in history[-max_years:]:
        category = categorize_season(season.get("Record", "0-0"), season.get("PostseasonResult", ""))
        timeline_html += render_timeline_node(season, category)
    
    era_markers = ""
    for era in eras:
        era_markers += f"<div class='era-marker' style='background: linear-gradient(135deg, {era['color']} 0%, {era['color']}dd 100%);'>📅 {era['name']} ({era['start_year']}-{era['end_year']})</div>"
    
    full_html = f"<div style='margin: 20px 0;'>{era_markers}<div class='timeline-container'><div class='timeline-line'></div>{timeline_html}</div></div>"
    return full_html

# ==============================================================================
# ENGINE & STATE
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
    
    # UPDATED V2.3: Force 2 Hard Money Games for G5
    if my_conf in ["G5", "MAC", "Pac-12", "Indep"]:
        p4 = []
        for c in ["SEC", "Big Ten", "ACC", "Big 12"]: p4.extend(conf_map.get(c, []))
        # Filter for top tier opponents
        elite_opps = [t for t in p4 if GameConfig.REAL_WORLD_INIT.get(t, {}).get("Prestige", 0) >= 85]
        avail = [t for t in elite_opps if t != my_team and t not in schedule]
        
        if avail:
            num = 2 # Force 2 hard games
            money_games = rng.sample(avail, min(num, len(avail)))
            
            # Remove weakest non-rivals
            sched_ovr = []
            for o in schedule:
                ov = 60
                if o in GameConfig.REAL_WORLD_INIT: ov = GameConfig.REAL_WORLD_INIT[o]["Talent"]
                sched_ovr.append((o, ov))
            sched_ovr.sort(key=lambda x: x[1]) # Sort by weakest
            
            final_schedule = []
            replaced_count = 0
            
            # Keep rival, replace weak teams
            for team, _ in sched_ovr:
                if team == rival:
                    final_schedule.append(team)
                elif replaced_count < len(money_games):
                    final_schedule.append(money_games[replaced_count])
                    replaced_count += 1
                else:
                    final_schedule.append(team)
            
            schedule = final_schedule
            rng.shuffle(schedule)
            # Ensure rival is last
            if rival in schedule:
                schedule.remove(rival)
                schedule.append(rival)
                
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
    """
    Main game simulation engine that calculates game outcome based on team stats and game factors.
    
    Args:
        my_off: User's offensive rating
        my_def: User's defensive rating
        opp_off: Opponent's offensive rating
        opp_def: Opponent's defensive rating
        staff: User's coaching staff dictionary
        schemes: User's offensive and defensive schemes
        opp_schemes: Opponent's schemes
        game_plan: User's game plan ("Aggressive", "Conservative", "Balanced")
        opp_coaches: Opponent coaching stats
        is_home: Whether user is playing at home
        is_rival: Whether this is a rivalry game
        my_stadium_level: User's stadium level (affects home field advantage)
        opp_stadium_level: Opponent's stadium level
        rng: Optional random number generator for deterministic results
        
    Returns:
        dict: Game result with score, win/loss, and stats
    """
    rng = rng or random.Random()
    
    # V1.8: Cinderella Tax - Apply difficulty multiplier for lower-tier teams
    try:
        diff_mult = calculate_difficulty_multiplier(
            st.session_state.get("team_conf", "G5"),
            st.session_state.get("prestige", 60),
            st.session_state.get("team_rating", 75),
            st.session_state.get("record", {}).get("w", 0)
        )
        opp_off = int(opp_off * diff_mult)
        opp_def = int(opp_def * diff_mult)
    except (KeyError, ValueError, TypeError):
        # If difficulty calculation fails, use original opponent ratings
        pass

    # Calculate team edges (offense vs defense matchups)
    my_edge, opp_edge = (my_off - opp_def)*0.75, (opp_off - my_def)*0.75
    
    # Scheme bonuses/penalties based on matchups
    sb_my, sb_opp = 0.0, 0.0
    if GameConfig.OFF_COUNTERED_BY.get(schemes.get("Off")) == opp_schemes.get("Def"):
        sb_my -= 2.5  # User's offense is countered
        sb_opp += 1.0
    if GameConfig.DEF_COUNTERS.get(opp_schemes.get("Def")) == schemes.get("Off"):
        sb_my += 2.5  # User's offense counters their defense
        sb_opp -= 1.0
    
    # Coaching bonuses (coordinator quality differential)
    my_c = (get_tier_bonus(safe_int(staff.get("OC",{}).get("off",3))) - 
            get_tier_bonus(safe_int(opp_coaches.get("DC",5))))*1.2
    opp_c = (get_tier_bonus(safe_int(opp_coaches.get("OC",5))) - 
             get_tier_bonus(safe_int(staff.get("DC",{}).get("def",3))))*1.2
    
    # Head coach trait bonuses
    hc_t = staff.get("HC", {}).get("trait", "None")
    if hc_t == "Tactician":
        my_c += 0.9  # Tactician trait gives game boost
    elif hc_t == "Recruiter":
        my_c += 0.25  # Recruiter trait gives small game boost
    
    # Scheme specialist coordinator bonus
    if staff.get("OC", {}).get("trait") == schemes.get("Off"):
        sb_my += 1.0  # OC specialist in user's offensive scheme
    
    # Home field advantage
    hf = home_field_points(my_stadium_level) if is_home else 0.0
    opp_hf = home_field_points(opp_stadium_level) if not is_home else 0.0
    
    # Variance multipliers
    var = 1.35 if is_rival else 1.0  # Rivalry games more unpredictable
    if game_plan == "Aggressive":
        var *= 1.25  # Aggressive increases variance
    elif game_plan == "Conservative":
        var *= 0.85  # Conservative reduces variance
    
    # Calculate expected scores (clamped between 10-50)
    exp_my = max(10, min(50, 27.5 + my_edge + sb_my + my_c + hf))
    exp_opp = max(10, min(50, 27.5 + opp_edge + sb_opp + opp_c + opp_hf))
    
    # Generate actual scores using gaussian distribution
    ms = int(round(rng.gauss(exp_my, 5.5 * var)))
    os = int(round(rng.gauss(exp_opp, 5.5 * var)))
    
    # Handle ties (slightly favor user)
    if ms == os:
        ms += rng.choice([0, 3, 7])
        os += rng.choice([0, 0, 3])
    
    # Clamp scores to realistic range (0-70)
    ms, os = max(0, min(70, ms)), max(0, min(70, os))
    
    # Build stats dictionary for display
    stats = {
        "qb_duel": [int(st.session_state.roster["QB"]), int(opp_off)],
        "off_vs_def": [int(my_off), int(opp_def)],
        "def_vs_off": [int(my_def), int(opp_off)],
        "staff": ["?","?"],
        "raw_roster": int((my_off+my_def)/2)
    }
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

def sync_team_ratings():
    """
    Synchronize team offensive, defensive, and overall ratings based on current roster, staff, and facilities.
    Updates st.session_state with calculated ratings.
    """
    if all(k in st.session_state for k in ["roster", "staff", "facilities"]):
        try:
            res = compute_team_unit_ratings(st.session_state.roster, st.session_state.staff, st.session_state.facilities)
            st.session_state.team_off, st.session_state.team_def, st.session_state.team_rating = res
        except (KeyError, ValueError, TypeError) as e:
            # If rating computation fails, keep existing ratings
            pass

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
    except (AttributeError, KeyError):
        # Skip if team name/color not available
        pass

def init_session_state_defaults():
    if "game_state" not in st.session_state: st.session_state.game_state = GameState.SETUP
    migrate_state()

def safe_json_default(obj):
    if isinstance(obj, set): return list(obj)
    if isinstance(obj, (datetime.date, datetime.datetime)): return obj.isoformat()
    return str(obj)

# ==============================================================================
# RECRUITING FUNCTIONS (Moved Up to Fix NameError)
# ==============================================================================

def generate_retention_demands() -> List[Dict]:
    demands = []
    targets = random.sample(GameConfig.POSITIONS, 3)
    for pos in targets:
        current_rating = st.session_state.roster.get(pos, 75)
        base_cost = max(250_000, (current_rating - 60) * 50_000)
        cost = int(base_cost * random.uniform(0.8, 1.2))
        demands.append({"pos": pos, "rating": current_rating, "cost": cost, "status": "PENDING"})
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
            try:
                allocated += int(float(shares_or_alloc.get(p, 0) or 0))
            except (ValueError, TypeError):
                # Skip invalid allocation values
                pass
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
    chance = 0.18 + (max(40, min(99, prestige)) - 60) * 0.004 + (scout - 5) * 0.02
    if hc_trait == "Recruiter": chance += 0.05
    pos = recruit["pos"]; spend = float(spend_by_pos.get(pos, 0.0))
    chance += min(0.20, spend / 10_000_000)
    return max(0.05, min(0.80, chance))

def compute_recruiting_class_grade():
    """
    Calculate the recruiting class grade based on NIL signings, top 8 commits, and gems found.
    
    Returns:
        tuple: (grade, score, breakdown) where:
            - grade: Letter grade (A+, A, B, C, D, F)
            - score: Numeric score based on tier points, top8 commits, and gems
            - breakdown: Dictionary with detailed scoring breakdown
    """
    # Get recruiting data from session state
    nil = st.session_state.get("nil_class", [])
    top8 = st.session_state.get("top8", [])
    stars = st.session_state.get("stars", [])
    
    # Initialize counters
    tier_counts = {}
    tier_points = 0
    
    # Calculate NIL tier points
    for p in nil:
        if p.get("status") == "SIGNED":
            tier = int(p.get("tier", 3))
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
            tier_points += {1: 12, 2: 7, 3: 3}.get(tier, 3)
    
    # Calculate top 8 commits points
    top8_commits = [r for r in top8 if r.get("status") == "COMMITTED"]
    top8_points = len(top8_commits) * 10
    
    # Calculate gem points
    gem_count = 0
    for s in stars:
        if "(GEM)" in str(s.get("name", "")):
            gem_count += 1
    gem_points = gem_count * 6
    
    # Calculate total score and assign grade
    score = tier_points + top8_points + gem_points
    if score >= 70:
        grade = "A+"
    elif score >= 55:
        grade = "A"
    elif score >= 42:
        grade = "B"
    elif score >= 30:
        grade = "C"
    elif score >= 18:
        grade = "D"
    else:
        grade = "F"
    
    # Build breakdown dictionary
    breakdown = {
        "score": score,
        "nil_signed": sum(tier_counts.values()),
        "tier_counts": tier_counts,
        "top8_commits": len(top8_commits),
        "gems_found": gem_count,
        "points": {
            "nil": tier_points,
            "top8": top8_points,
            "gems": gem_points
        }
    }
    
    return grade, score, breakdown

# ==============================================================================
# VIEW FUNCTIONS (Offseason Controller Logic)
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
    
    if st.button("Dismiss & Continue to Top-8 →", type="primary", key="dismiss_hs_summary"):
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
    if render_hs_results_summary(): 
        return

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
        
        with st.container(border=True):
            # Header
            st.markdown(f"### {pos} {r['name']} ({r['rating']}) {r.get('trait', '')}")
            st.caption(f"💰 Asking Price: {helper_format_cash(ask)}")
            
            c1, c2 = st.columns([2, 1])
            
            with c1:
                # INTEREST METER
                chance = top8_commit_chance(
                    r,
                    {pos: float(r.get("offer", 0) or 0)},
                    st.session_state.staff,
                    st.session_state.prestige
                )
                st.markdown(render_interest_meter(r, chance, {}), unsafe_allow_html=True)
            
            with c2:
                # Offer slider
                row_budget = int(st.session_state.get("budget", 0) or 0)
                max_offer = max(0, min(row_budget, max(ask * 2, 250_000)))
                default_offer = int(r.get("offer", 0) or 0)
                default_offer = max(0, min(default_offer, max_offer))
                
                offer = st.slider(
                    "Your Offer",
                    0, max_offer, default_offer,
                    step=250_000,
                    key=f"offer_{rid}"
                )
                r["offer"] = int(offer)
            
            st.divider()
            
            # Display status or pitch button
            if r.get("status") == "COMMITTED":
                st.success("✅ COMMITTED")
            elif r.get("status") == "LOST":
                st.error("❌ LOST")
            else:
                disabled = already or r["offer"] <= 0
                if st.button("Make Pitch", key=f"pitch_{rid}", disabled=disabled, use_container_width=True, type="primary"):
                    if not validate_budget_input(r["offer"], BudgetManager.get_current(), f"recruit {r['name']}"):
                        st.error("Cannot afford this offer!")
                    else:
                        chance = top8_commit_chance(r, {pos: float(r.get("offer", 0) or 0)}, st.session_state.staff, st.session_state.prestige)
                        if random.random() < chance:
                            BudgetManager.spend(r["offer"], f"Top-8 commit: {r['name']}")
                            st.session_state.roster[pos] = max(st.session_state.roster[pos], r["rating"])
                            r["status"] = "COMMITTED"
                            st.session_state.top8_resolved.add(rid)
                            add_news(f"{st.session_state.team_name} lands Top-8 {pos} {r['name']} ({r['rating']})!")
                            sync_team_ratings()
                            safe_toast(f"✅ COMMITTED: {r['name']}")
                            st.rerun()
                        else:
                            r["status"] = "LOST"
                            st.session_state.top8_resolved.add(rid)
                            add_news(f"{r['name']} commits elsewhere. Lost recruit.")
                            safe_toast(f"❌ LOST: {r['name']}")
                            st.rerun()
    st.divider()
    if st.button("Finish Top-8 & Continue →", type="primary"):
        st.session_state.offseason_step = 5
        st.rerun()

# ==============================================================================
# MAIN VIEW CONTROLLERS
# ==============================================================================

def run_setup():
    st.title("🏆 Build the Program: CEO")
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
        # V2.9 NEW: Initialize Trophy Tracking if missing
        st.session_state.trophy_stats = {
            "titles": 0, "cfp_appearances": 0, "perfect_seasons": 0, "bowl_wins": 0,
            "ten_win_seasons": 0, "conf_titles": 0, "rivalry_wins": 0, "top5_finishes": 0
        }
        for p in GameConfig.POSITIONS: st.session_state[f"hs_pos_input_{p}_v28"] = 0
        add_news(f"{team} hires {st.session_state.staff['HC']['name']} as HC.")
        st.session_state.game_state = GameState.DASHBOARD
        st.rerun()

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
        
        # Staff Chemistry Bonus
        traits = [st.session_state.staff.get(r, {}).get('trait', 'None') for r in ["HC", "OC", "DC", "Scout"]]
        has_chemistry = len(set(traits) - {'None'}) >= 3
        if has_chemistry:
            st.markdown("<div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);border:3px solid #ff9800;padding:15px;border-radius:12px;text-align:center;margin:15px 0;font-weight:bold;color:#e65100;box-shadow:0 4px 12px rgba(255,152,0,0.3);'>✨ STAFF CHEMISTRY ACTIVE ✨<br><span style='font-size:0.9em;font-weight:normal;'>Your diverse coaching staff provides bonus recruiting!</span></div>", unsafe_allow_html=True)
            
        cols = st.columns(4)
        for i, role in enumerate(["HC", "OC", "DC", "Scout"]):
            with cols[i]:
                if role in st.session_state.staff:
                    c = st.session_state.staff[role]
                    if 'tenure_years' not in c: c['tenure_years'] = 1
                    
                    st.markdown(render_enhanced_staff_card(c, role, role_rating(c,role)), unsafe_allow_html=True)
                    if st.button("Fire", key=f"fire_{role}"):
                        del st.session_state.staff[role]
                        add_news(f"Fired {role} {c['name']}")
                        st.rerun()
                else: 
                    st.warning(f"{role} VACANT")
                    if st.button(f"Promote GA (Free)", key=f"quick_ga_{role}"):
                        ga = generate_ga_coach(role)
                        st.session_state.staff[role] = ga
                        add_news(f"Promoted {ga['name']} to {role}")
                        st.rerun()
        
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
        st.markdown("### 🏗️ Program Facilities")
        st.caption("Invest in your program's infrastructure to boost recruiting, development, and revenue")
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(render_enhanced_facility_card("Marketing", st.session_state.facilities["Marketing"]), unsafe_allow_html=True)
            if st.button("Upgrade Marketing ($1M)", key="um", use_container_width=True):
                if BudgetManager.spend(1000000, "Upgrade Marketing"):
                    st.session_state.facilities["Marketing"] += 1; st.rerun()
        with c2:
            st.markdown(render_enhanced_facility_card("Training", st.session_state.facilities["Training"]), unsafe_allow_html=True)
            if st.button("Upgrade Training ($3M)", key="ut", use_container_width=True):
                if BudgetManager.spend(3000000, "Upgrade Training"):
                    st.session_state.facilities["Training"] += 1; st.rerun()
        with c3:
            st.markdown(render_enhanced_facility_card("Stadium", st.session_state.facilities["Stadium"]), unsafe_allow_html=True)
            if st.button("Upgrade Stadium ($10M)", key="us", use_container_width=True):
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
            is_rival = (opp == st.session_state.team_rival)
            
            # V2.9: ENHANCED PREVIEW CARD
            st.markdown(render_game_preview_card(wk + 1, opp, opp_data, st.session_state.team_off, st.session_state.team_def, is_rival), unsafe_allow_html=True)
            st.divider()
            
            c1, c2, c3 = st.columns([1,2,2])
            with c1:
                st.markdown("Strategy")
                st.session_state.game_plan = st.selectbox("Plan", ["Conservative", "Normal", "Aggressive"], index=["Conservative", "Normal", "Aggressive"].index(st.session_state.game_plan), label_visibility="collapsed")
            with c2:
                st.markdown("Action")
                if st.button(f"Play Week {wk+1}", type="primary", use_container_width=True, key=f"play_wk_{wk}"):
                    rng = game_rng(st.session_state.year, wk+1, opp, "PLAY")
                    res = engine_play_game_v8(st.session_state.team_off, st.session_state.team_def, opp_data.get("OffOVR"), opp_data.get("DefOVR"), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off"), "Def": opp_data.get("Def")}, st.session_state.game_plan, opp_data.get("Coaches"), wk%2==0, opp==st.session_state.team_rival, st.session_state.facilities["Stadium"], opp_data.get("Stadium"), rng)
                    
                    st.session_state.season_logs.append({"Week": wk+1, "Opponent": opp, "Score": f"{res['result']} {res['score']}", "Stats": res["stats"], "OppOVR": opp_data.get("OVR")})
                    if res["result"] == "W":
                        st.session_state.record["w"] += 1; st.session_state.career_stats["w"] += 1
                        st.session_state.job_security = min(100, st.session_state.job_security + (5 if opp==st.session_state.team_rival else 2))
                        # V2.9 Track Rivalry
                        if is_rival: st.session_state.trophy_stats["rivalry_wins"] += 1
                    else:
                        st.session_state.record["l"] += 1; st.session_state.career_stats["l"] += 1
                        st.session_state.job_security = max(0, st.session_state.job_security - 2)
                    
                    st.session_state.week_index += 1
                    if st.session_state.week_index >= 12: end_regular_season_and_stay_on_results()
                    st.rerun()
            with c3:
                st.markdown("Simulate")
                if st.button("Sim Season", use_container_width=True, key="sim_season_main"):
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
                        time.sleep(0.01) # Stabilization
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
                    st.markdown(render_game_result_with_bars(i+1, played['Opponent'], played['Score'], is_win, played.get('Stats', {})), unsafe_allow_html=True)
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
                    st.markdown(render_game_result_with_bars(i+1, played['Opponent'], played['Score'], is_win, played.get('Stats', {})), unsafe_allow_html=True)
                else:
                    css = "game-card-rival" if opp==st.session_state.team_rival else "game-card-pending"
                    st.markdown(f"<div class='game-card {css}'>Week {i+1} vs {opp}</div>", unsafe_allow_html=True)

    with tab5:
        st.subheader("🏛️ Dynasty Overview")
        cs = st.session_state.career_stats
        
        m1, m2, m3 = st.columns(3)
        m1.metric("National Titles", cs['titles'])
        m2.metric("Career Record", f"{cs['w']}-{cs['l']}")
        m3.metric("Bowl Record", f"{cs['bowl_w']}-{cs['bowl_l']}")
        st.caption(f"Legacy Score: {calculate_saban_score(cs, st.session_state.prestige)}")
        st.divider()
        
        # ENHANCED TROPHY CASE
        st.subheader("🏆 Trophy Gallery")
        initialize_trophy_tracking()
        all_trophies = st.session_state.get("trophies", [])
        categorized = organize_trophies_by_category(all_trophies)
        
        priority_shelves = ["National Championships", "CFP Appearances", "Perfect Seasons", "Bowl Victories", "10+ Win Seasons"]
        for shelf_name in priority_shelves:
            trophies = categorized.get(shelf_name, [])
            st.markdown(render_trophy_shelf(shelf_name, trophies, max_display=8, show_empty=True), unsafe_allow_html=True)
            
        st.divider()
        st.subheader("📅 Dynasty Timeline")
        st.markdown(render_dynasty_timeline_infographic(st.session_state.history, max_years=20), unsafe_allow_html=True)
        st.divider()
        
        if st.button("🚪 Retire from Coaching", type="secondary"):
            st.session_state.game_state = GameState.RETIREMENT
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
        wk = log["Week"]
        opp = log["Opponent"]
        score = log["Score"]
        is_win = score.startswith("W")
        stats = log.get("Stats")
        opp_ovr = log.get("OppOVR", "?")
        
        # V3.0 FIX: Native columns
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**Week {wk} vs {opp} ({opp_ovr})**")
                st.markdown(f"### {score}")
                st.markdown("✅ WIN" if is_win else "❌ LOSS")
            with col2:
                if stats:
                    s_grid = pd.DataFrame([
                        {"Metric": "🔥 QB Duel", "Value": f"{stats['qb_duel'][0]} vs {stats['qb_duel'][1]}"},
                        {"Metric": "⚔️ OFF vs DEF", "Value": f"{stats['off_vs_def'][0]} vs {stats['off_vs_def'][1]}"},
                        {"Metric": "🛡️ DEF vs OFF", "Value": f"{stats['def_vs_off'][0]} vs {stats['def_vs_off'][1]}"},
                    ])
                    st.dataframe(s_grid, hide_index=True, use_container_width=True)

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

def show_selection_sunday():
    sync_team_ratings()
    st.markdown(UIComponents.gradient_header("🏆 SELECTION SUNDAY", "The Committee Has Spoken"), unsafe_allow_html=True)
    
    # ENHANCED RANKINGS
    st.subheader("📊 Complete Committee Rankings")
    st.markdown(render_rankings_table_header(), unsafe_allow_html=True)
    
    results = st.session_state.selection_sunday_results
    
    # Show Top 25
    for i, t in enumerate(results[:25]):
        rank = i + 1
        is_user = t.get("IsUser", False) or t.get("Team") == st.session_state.team_name
        st.markdown(render_enhanced_ranking_row(rank, t["Team"], t["Wins"], t["Losses"], t["Conf"], is_user), unsafe_allow_html=True)
    
    # Find user if not in top 25
    user_rank = next((i+1 for i, t in enumerate(results) if t.get("IsUser") or t.get("Team") == st.session_state.team_name), 999)
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
    if not data.get("Type"): st.warning("Data missing."); st.session_state.game_state = GameState.SEASON_END; st.rerun()

    if data.get("Type") == "BOWL":
        bowl, opp = data.get("Bowl", "Bowl"), data.get("Opponent", "Opp")
        opp_data = OpponentManager.get(opp)
        st.markdown(UIComponents.gradient_header(f"{st.session_state.team_name} VS {opp}", bowl, "135deg, #ff6b6b 0%, #feca57 100%"), unsafe_allow_html=True)
        
        # ENHANCED TALE OF THE TAPE
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
            # V3.0 FIX: Native columns for Bowl result too
            with st.container(border=True):
                st.markdown(f"**Final Score: {res['score']}**")
                s = res.get("stats", {})
                if s:
                    c1, c2 = st.columns(2)
                    c1.write(f"Total Offense: {s['off_vs_def'][0]} vs {s['off_vs_def'][1]}")
                    c2.write(f"Total Defense: {s['def_vs_off'][0]} vs {s['def_vs_off'][1]}")

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
        # FIXED LOGIC: V2.5 Dedicated Round 5 Handler
        render_cfp_bracket_tree(st.session_state.postseason_data)
        st.divider()
        user_match = None
        matches = data.get("Matches", [])
        round_num = int(data.get("Round", 1))
        user_alive = data.get("UserAlive", True)
        
        if not user_alive:
            st.error("💔 You have been eliminated from the College Football Playoff")
            if st.button("Continue to Season Recap"):
                st.session_state.game_state = GameState.SEASON_RECAP
                st.rerun()
            return
            
        if round_num == 5:
             st.balloons()
             st.success("🏆🏆🏆 NATIONAL CHAMPIONS! 🏆🏆🏆")
             if st.button("Finish Season & Celebrate", type="primary"):
                 st.session_state.game_state = GameState.SEASON_RECAP
                 st.rerun()
             return

        for m in matches:
            if m.get("t1") == st.session_state.team_name or m.get("t2") == st.session_state.team_name: user_match = m; break

        if not user_match and round_num == 1:
            st.success("✅ FIRST ROUND BYE: You automatically advance to the Quarterfinals.")
            if st.button("Simulate Opening Round & Advance", type="primary"):
                data.setdefault("History", []).append(copy.deepcopy(matches))
                seed_map = st.session_state.postseason_data.get("SeedMap", {})
                for m in matches:
                    t1, t2 = m.get("t1"), m.get("t2"); o1 = st.session_state.opponents_db.get(t1, {"OVR": 82}).get("OVR", 82); o2 = st.session_state.opponents_db.get(t2, {"OVR": 82}).get("OVR", 82)
                    p = o1 / max(1.0, (o1 + o2)); winner = t1 if random.random() < p else t2
                    s_win = int(random.gauss(34, 7)); s_loss = int(random.gauss(20, 7))
                    if s_win <= s_loss: s_win = s_loss + 3 
                    if winner == t1: m["s1"], m["s2"] = s_win, s_loss
                    else: m["s1"], m["s2"] = s_loss, s_win
                    m["winner"] = winner
                    
                seeds = data.get("Seeds", []); new_matches = []
                if len(seeds) >= 4:
                    winners = [m["winner"] for m in matches]
                    qf_seeds = data.get("QF_Seeds", seeds[:4])
                    if len(winners) >= 4:
                         new_matches = [
                            {"t1": qf_seeds[0], "t2": winners[3], "winner": None}, # 1 vs 8/9
                            {"t1": qf_seeds[3], "t2": winners[0], "winner": None}, # 4 vs 5/12
                            {"t1": qf_seeds[2], "t2": winners[1], "winner": None}, # 3 vs 6/11
                            {"t1": qf_seeds[1], "t2": winners[2], "winner": None}, # 2 vs 7/10
                         ]

                st.session_state.postseason_data["Round"] = 2; st.session_state.postseason_data["Matches"] = new_matches; st.rerun()

        elif user_match and not user_match.get("winner"):
            opp = user_match["t2"] if user_match["t1"] == st.session_state.team_name else user_match["t1"]
            opp_data = OpponentManager.get(opp)
            
            st.subheader(f"🏈 CFP Matchup: {st.session_state.team_name} vs {opp}")
            c1, c2, c3 = st.columns([1, 0.2, 1])
            with c1: st.markdown(UIComponents.team_stat_card(st.session_state.team_name, f"{st.session_state.record['w']}-{st.session_state.record['l']}", st.session_state.team_rating, st.session_state.team_off, st.session_state.team_def, st.session_state.facilities.get("Stadium", 7), True), unsafe_allow_html=True)
            with c2: st.markdown("<h1 style='text-align:center'>VS</h1>", unsafe_allow_html=True)
            with c3: st.markdown(UIComponents.team_stat_card(opp, "Opponent", opp_data.get("OVR", 88), opp_data.get("OffOVR", 88), opp_data.get("DefOVR", 88), opp_data.get("Stadium", 9), False), unsafe_allow_html=True)

            if st.button("PLAY PLAYOFF GAME 🏈", type="primary"):
                rng = game_rng(st.session_state.year, 20, opp, mode="PLAY")
                res = engine_play_game_v8(st.session_state.team_off, st.session_state.team_def, int(opp_data.get("OffOVR", 80)), int(opp_data.get("DefOVR", 80)), st.session_state.staff, st.session_state.my_schemes, {"Off": opp_data.get("Off", "Pro Style"), "Def": opp_data.get("Def", "Man Coverage")}, st.session_state.game_plan, opp_data.get("Coaches", {"OC": 5, "DC": 5}), is_home=False, is_rival=False, my_stadium_level=st.session_state.facilities.get("Stadium", 7), opp_stadium_level=opp_data.get("Stadium", 9), rng=rng)
                
                try:
                    my_s, opp_s = [int(x) for x in str(res.get("score","0-0")).split("-")]
                except (ValueError, IndexError):
                    # Default to 0-0 if score parsing fails
                    my_s, opp_s = 0, 0
                if user_match.get("t1") == st.session_state.team_name: user_match["s1"], user_match["s2"] = my_s, opp_s
                else: user_match["s1"], user_match["s2"] = opp_s, my_s

                # Simulate other games
                for m in matches:
                    if m is not user_match:
                        t1, t2 = m.get("t1"), m.get("t2")
                        if not t1 or not t2: continue
                        o1 = st.session_state.opponents_db.get(t1, {"OVR": 82}).get("OVR", 82); o2 = st.session_state.opponents_db.get(t2, {"OVR": 82}).get("OVR", 82)
                        p = o1 / max(1.0, (o1 + o2)); winner = t1 if random.random() < p else t2
                        s_win = int(random.gauss(34, 7)); s_loss = int(random.gauss(20, 7))
                        if s_win <= s_loss: s_win = s_loss + 3 
                        if winner == t1: m["s1"], m["s2"] = s_win, s_loss
                        else: m["s1"], m["s2"] = s_loss, s_win
                        m["winner"] = winner

                if res["result"] == "W":
                    user_match["winner"] = st.session_state.team_name
                    add_news(f"{st.session_state.team_name} advances in the CFP!"); safe_toast("VICTORY! Advancing...")
                    BudgetManager.add(5_000_000, "CFP Round Bonus")
                    st.rerun() 
                else:
                    user_match["winner"] = opp
                    st.session_state.postseason_data["UserAlive"] = False
                    st.session_state.last_postseason_result = "CFP_LOSS"
                    add_news(f"{st.session_state.team_name} is eliminated by {opp}."); st.error(f"Eliminated by {opp}")
                    st.rerun()

        elif user_match and user_match.get("winner"):
             st.success("✅ Round Complete!")
             if st.button("Advance to Next Round →", type="primary"):
                 winners = [m["winner"] for m in matches]
                 new_matches = []
                 if len(winners) >= 2:
                     for i in range(0, len(winners), 2):
                         if i+1 < len(winners):
                             new_matches.append({"t1": winners[i], "t2": winners[i+1], "winner": None})
                 
                 if not new_matches and round_num >= 4:
                      # If this was the Championship, move to Round 5 (Victory Lap)
                      if user_alive:
                          st.session_state.last_postseason_result = "TITLE"
                          st.session_state.career_stats["titles"] += 1
                          BudgetManager.add(50_000_000, "NATIONAL CHAMPIONSHIP!")
                          award_trophy("National Title")
                          st.session_state.history.append({"Year": st.session_state.year, "Record": "CHAMPS", "Rank": "#1", "Bowl": "National Title", "PostseasonResult": "TITLE"})
                          st.session_state.postseason_data["Round"] = 5
                          st.rerun()
                      else:
                          st.session_state.game_state = GameState.SEASON_RECAP
                          st.rerun()
                 else:
                     st.session_state.postseason_data["Matches"] = new_matches
                     st.session_state.postseason_data["Round"] = round_num + 1
                     st.rerun()

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
    
    # --- V2.6: Universe Report (Show this once per offseason start) ---
    if "offseason_report_shown" not in st.session_state or st.session_state.get("offseason_report_year") != year:
        OpponentManager.evolve_universe()
        st.session_state.offseason_report_shown = True
        st.session_state.offseason_report_year = year

    step = safe_int(st.session_state.get("offseason_step", 1), 1)
    
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
        # V2.7 FIX: Do not call render_hs_results_summary here explicitly
        # It is handled inside show_offseason_hs_outreach logic

    elif step == 4:
        show_offseason_top8_v8()
        st.divider()
        if st.button("Finish Recruiting & Advance Season →", type="primary"):
            grade, score, breakdown = compute_recruiting_class_grade()
            last_hist = st.session_state.history[-1] if st.session_state.history else None
            if last_hist and safe_int(last_hist.get("Year", 0), 0) == year:
                last_hist["RecruitingGrade"] = grade
            
            add_news(f"Recruiting class grade: {grade} ({score} pts)")
            st.session_state.year += 1
            st.session_state.tenure += 1
            st.session_state.inflation = safe_float(st.session_state.get("inflation", 1.0), 1.0) * 1.02
            
            invite = maybe_generate_conference_invite()
            if not invite: ai_conference_swap_lightweight()
            
            st.session_state.schedule = engine_generate_schedule(
                st.session_state.team_name, 
                st.session_state.team_conf, 
                st.session_state.team_rival
            )
            st.session_state.week_index = 0
            st.session_state.record = {"w": 0, "l": 0}
            st.session_state.season_logs = []
            st.session_state.season_simulated = False
            st.session_state.season_end_ready = False
            st.session_state.revenue_report = None
            st.session_state.nil_class = []
            st.session_state.hs_total_spend = 0
            st.session_state.top8 = []
            st.session_state.top8_resolved = set()
            st.session_state.offseason_step = 1
            st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
            st.session_state.hotspots = generate_hotspots()
            sync_team_ratings()
            st.session_state.hs_last_results = None
            st.session_state.retention_data = []
            for p in GameConfig.POSITIONS:
                st.session_state[f"hs_pos_input_{p}_v28"] = 0
            st.session_state.hs_alloc_by_pos = {p: 0 for p in GameConfig.POSITIONS}
            st.session_state.recruiting_summary = {
                "grade": grade, "score": score, "breakdown": breakdown
            }
            st.session_state.game_state = GameState.RECRUITING_WRAP
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

def show_fired():
    st.title("🔥 FIRED")
    st.markdown(UIComponents.gradient_header("YOU'VE BEEN FIRED", "The Athletic Director has decided to make a change"), unsafe_allow_html=True)
    if st.button("Start New Dynasty"):
        st.session_state.clear(); st.rerun()

def show_retirement():
    st.markdown(UIComponents.gradient_header("HALL OF FAME CEREMONY", "Congratulations on a legendary career"), unsafe_allow_html=True)
    
    # 1. Career Stats Summary
    st.subheader("🐐 The GOAT Debate")
    my_stats = {
        "Name": f"{st.session_state.get('ad_name','You')} (You)", 
        "Titles": st.session_state.career_stats['titles'],
        "Wins": st.session_state.career_stats['w'],
        "Losses": st.session_state.career_stats['l'],
        "BowlWins": st.session_state.career_stats['bowl_w']
    }
    
    # Combine with legends
    all_coaches = GameConfig.LEGENDS + [my_stats]
    all_coaches.sort(key=lambda x: (x["Titles"], x["Wins"]), reverse=True)
    user_rank = next((i+1 for i, c in enumerate(all_coaches) if c["Name"] == my_stats["Name"]), 99)
    
    # Calculate final grade
    score = (my_stats["Titles"] * 50) + (my_stats["Wins"] * 2) + (my_stats["BowlWins"] * 5)
    if score > 500: grade = "S"; st.balloons()
    elif score > 300: grade = "A"; st.balloons()
    elif score > 150: grade = "B"; st.snow()
    elif score > 80: grade = "C"; st.snow()
    else: grade = "D"
    
    # V2.9: MOUNT RUSHMORE
    top_4 = all_coaches[:4]
    percentile = calculate_percentile(score, all_coaches)
    st.markdown(render_mount_rushmore(top_4, my_stats, user_rank), unsafe_allow_html=True)
    st.divider()
    
    # V2.9: CAREER HIGHLIGHTS
    highlights = generate_career_highlights(st.session_state.history, st.session_state.career_stats)
    st.markdown(render_career_highlights_carousel(highlights), unsafe_allow_html=True)
    st.divider()
    
    # V2.9: LEGACY REPORT CARD
    st.markdown(render_legacy_report_card(grade, score, percentile), unsafe_allow_html=True)
    st.divider()
    
    # All-Time Rankings Table
    st.subheader("📊 All-Time Coaching Rankings")
    table_data = []
    for i, c in enumerate(all_coaches):
        table_data.append({
            "Rank": i+1,
            "Coach": c["Name"],
            "Nat'l Titles": c["Titles"],
            "Career Wins": c["Wins"],
            "Bowl Wins": c["BowlWins"]
        })
    st.dataframe(pd.DataFrame(table_data), hide_index=True, use_container_width=True)
    
    st.divider()
    render_trophy_gallery("🏆 Your Trophy Case")
    
    if st.button("Start New Dynasty", type="primary"):
        st.session_state.clear()
        st.rerun()
# ==============================================================================
# MAIN ROUTER & SAVE SYSTEM
# ==============================================================================

def render_system_sidebar():
    with st.sidebar:
        st.header("💾 CEO System")
        st.caption(f"Version {STATE_VERSION}")
        if st.button("Export Save File"):
            state_copy = dict(st.session_state)
            if "top8_resolved" in state_copy:
                state_copy["top8_resolved"] = list(state_copy["top8_resolved"])
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
        
        render_news_box()

# --- V2.6: Auto-Scroll Fix ---
st.markdown("""
<script>
    var body = window.parent.document.querySelector(".main");
    body.scrollTop = 0;
</script>
""", unsafe_allow_html=True)

# Initialize the session state and render the system sidebar
init_session_state_defaults()
render_system_sidebar()

# ---
# Function definitions for each game state must be declared beforehand and **not nested** inside any conditional blocks.
# Run `run_setup()` inside the `if` block and **keep function declarations separate.**
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
    # If the game state is invalid or missing, default back to the dashboard.
    st.session_state.game_state = GameState.DASHBOARD
    st.rerun()
