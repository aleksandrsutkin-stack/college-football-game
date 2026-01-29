"""
UI Components Module
Extracted UI rendering functions from App.py for better code organization.
This module contains all UI-related helper functions with proper input validation.
"""

from typing import Dict, List, Optional


def validate_dict(value, default=None):
    """Validate that a value is a dict, return default if not."""
    if default is None:
        default = {}
    return value if isinstance(value, dict) else default


def validate_numeric(value, default=0, min_val=None, max_val=None):
    """Validate and clamp a numeric value."""
    try:
        value = float(value)
        if min_val is not None:
            value = max(min_val, value)
        if max_val is not None:
            value = min(max_val, value)
        return value
    except (ValueError, TypeError):
        return default


def validate_string(value, default=""):
    """Validate that a value is a string."""
    return str(value) if value is not None else default


# ==============================================================================
# UI HELPER FUNCTIONS
# ==============================================================================

def get_coach_initials(name: str) -> str:
    """Extract initials from coach name."""
    name = validate_string(name, "XX")
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}"
    return name[:2].upper()


def get_staff_quality_class(rating: int) -> str:
    """Get CSS class based on staff rating."""
    rating = int(validate_numeric(rating, 0, 0, 10))
    if rating >= 9:
        return "staff-card-gold"
    elif rating >= 7:
        return "staff-card-silver"
    elif rating >= 5:
        return "staff-card-bronze"
    return ""


def get_trait_icon(trait: str) -> str:
    """Get emoji icon for coach trait."""
    trait = validate_string(trait, "None")
    icons = {
        "Recruiter": "🏃",
        "Tactician": "🧠",
        "Air Raid": "✈️",
        "Smashmouth": "💪",
        "Pro Style": "🎯",
        "None": ""
    }
    return icons.get(trait, "⭐")


def get_position_color(pos: str) -> str:
    """Get CSS class for position color."""
    pos = validate_string(pos, "QB")
    colors = {
        "QB": "pos-QB",
        "RB": "pos-RB",
        "WR": "pos-WR",
        "OL": "pos-OL",
        "DL": "pos-DL",
        "LB": "pos-LB",
        "DB": "pos-DB"
    }
    return colors.get(pos, "pos-QB")


def get_conference_badge_class(conf: str) -> str:
    """Get CSS class for conference badge."""
    conf = validate_string(conf, "G5")
    conf_map = {
        "SEC": "conf-SEC",
        "Big Ten": "conf-BIG",
        "ACC": "conf-ACC",
        "Big 12": "conf-B12"
    }
    return conf_map.get(conf, "conf-G5")


def get_record_color_class(wins: int, losses: int) -> str:
    """Get CSS class based on win-loss record."""
    wins = int(validate_numeric(wins, 0, 0))
    losses = int(validate_numeric(losses, 0, 0))
    
    if losses == 0 and wins >= 12:
        return "record-undefeated"
    elif wins >= 10:
        return "record-strong"
    elif wins >= 6:
        return "record-bubble"
    else:
        return "record-weak"


# ==============================================================================
# UI RENDERING FUNCTIONS
# ==============================================================================

def render_enhanced_staff_card(coach: dict, role: str, rating: int) -> str:
    """Render an enhanced staff card with validation."""
    coach = validate_dict(coach)
    role = validate_string(role, "Coach")
    rating = int(validate_numeric(rating, 5, 0, 10))
    
    initials = get_coach_initials(coach.get('name', 'XX'))
    quality_class = get_staff_quality_class(rating)
    headshot_class = quality_class.replace('staff-card-', 'staff-headshot-')
    trait = validate_string(coach.get('trait', 'None'))
    trait_icon = get_trait_icon(trait)
    tenure_years = int(validate_numeric(coach.get('tenure_years', 1), 1, 1))
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


def render_interest_meter_safe(recruit: dict, chance: float, spend_by_pos: dict = None) -> str:
    """
    Render an interest meter for a recruit with full input validation.
    This is a validated version that can be used independently.
    """
    # Input validation
    recruit = validate_dict(recruit)
    chance = validate_numeric(chance, 0.0, 0.0, 1.0)
    
    pos = validate_string(recruit.get('pos', 'QB'))
    offer = validate_numeric(recruit.get('offer', 0), 0, 0)
    ask = validate_numeric(recruit.get('ask', 1_000_000), 1_000_000, 1)
    
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
    if offer >= ask * 1.25:
        offer_status = "<div style='color: #4CAF50; font-weight: bold; margin-top: 5px;'>💵 OVERPAYING (+Boost)</div>"
    elif offer >= ask:
        offer_status = "<div style='color: #2196f3; font-weight: bold; margin-top: 5px;'>✅ MEETS ASK</div>"
    elif offer > 0:
        offer_status = "<div style='color: #ff9800; font-weight: bold; margin-top: 5px;'>⚠️ BELOW ASK</div>"
    
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


def render_nil_prospect_card_safe(prospect: dict, is_need: bool = False) -> str:
    """
    Render a NIL prospect card with full input validation.
    This is a validated version that can be used independently.
    """
    prospect = validate_dict(prospect)
    
    tier = int(validate_numeric(prospect.get('tier', 3), 3, 1, 3))
    name = validate_string(prospect.get('name', 'Unknown'))
    pos = validate_string(prospect.get('pos', 'QB'))
    rating = int(validate_numeric(prospect.get('rating', 75), 75, 0, 99))
    ask = validate_numeric(prospect.get('ask', 1000000), 1000000, 0)
    trait = validate_string(prospect.get('trait', '⭐'))
    status = validate_string(prospect.get('status', 'AVAILABLE'))
    
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


# ==============================================================================
# UI COMPONENT CLASS
# ==============================================================================

class UIComponentsHelper:
    """
    Static helper class for UI component generation with validation.
    """
    
    @staticmethod
    def progress_bar_gradient_safe(label: str, value: int, max_value: int = 100, team_color: str = "#2196F3") -> str:
        """Render a progress bar with full input validation."""
        label = validate_string(label, "Progress")
        value = int(validate_numeric(value, 0, 0))
        max_value = int(validate_numeric(max_value, 100, 1))
        team_color = validate_string(team_color, "#2196F3")
        
        pct = min(100, (value / max_value) * 100)
        
        return f"""
        <div style='margin: 10px 0;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                <span style='font-weight: bold;'>{label}</span>
                <span>{value}/{max_value}</span>
            </div>
            <div style='background: #e0e0e0; height: 24px; border-radius: 12px; overflow: hidden;'>
                <div style='width: {pct}%; height: 100%; background: {team_color}; transition: width 0.3s ease;'></div>
            </div>
        </div>
        """


# Export commonly used functions
__all__ = [
    'validate_dict',
    'validate_numeric',
    'validate_string',
    'get_coach_initials',
    'get_staff_quality_class',
    'get_trait_icon',
    'get_position_color',
    'get_conference_badge_class',
    'get_record_color_class',
    'render_enhanced_staff_card',
    'render_interest_meter_safe',
    'render_nil_prospect_card_safe',
    'UIComponentsHelper',
]
