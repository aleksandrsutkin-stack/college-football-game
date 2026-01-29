"""
Data Helpers Module
Extracted data processing functions from App.py for better code organization.
This module contains all data transformation and calculation functions with proper input validation.
"""

from typing import List, Dict, Optional, Tuple
import random


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


def validate_dict(value, default=None):
    """Validate that a value is a dict."""
    if default is None:
        default = {}
    else:
        # Create new instance to avoid mutable default issues
        default = dict(default)
    return value if isinstance(value, dict) else default


def validate_list(value, default=None):
    """Validate that a value is a list."""
    if default is None:
        default = []
    else:
        # Create new instance to avoid mutable default issues
        default = list(default)
    return value if isinstance(value, list) else default


# ==============================================================================
# DATA PROCESSING FUNCTIONS
# ==============================================================================

def compute_team_needs(position_ratings: Dict[str, int], positions: List[str] = None) -> List[str]:
    """
    Compute the 3 weakest positions for a team.
    
    Args:
        position_ratings: Dictionary mapping position to rating
        positions: List of valid positions (defaults to common positions)
    
    Returns:
        List of 3 weakest position names
    """
    if positions is None:
        positions = ["QB", "RB", "WR", "OL", "DL", "LB", "DB"]
    
    position_ratings = validate_dict(position_ratings)
    
    # Ensure all positions have a rating
    ratings = {pos: int(validate_numeric(position_ratings.get(pos, 50), 50, 0, 99)) 
               for pos in positions}
    
    # Sort by rating (lowest first)
    sorted_positions = sorted(ratings.items(), key=lambda x: x[1])
    
    # Return top 3 weakest positions
    return [pos for pos, _ in sorted_positions[:3]]


def normalize_shares(shares: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize budget share percentages to sum to 100%.
    
    Args:
        shares: Dictionary of position to allocation percentage
        
    Returns:
        Normalized dictionary where values sum to 100%
    """
    shares = validate_dict(shares)
    
    # Handle empty dictionary case
    if not shares:
        return {}
    
    def _val(d: dict, k: str) -> float:
        """Safely extract float value from dict."""
        try:
            return float(d.get(k, 0))
        except (ValueError, TypeError):
            return 0.0
    
    total = sum(_val(shares, k) for k in shares.keys())
    
    # Prevent division by zero
    if total <= 0:
        # Equal distribution if all zeros
        num_keys = len(shares)
        if num_keys == 0:
            return {}
        return {k: 100.0 / num_keys for k in shares.keys()}
    
    # Normalize to 100%
    return {k: (_val(shares, k) / total) * 100 for k in shares.keys()}


def calculate_percentile(user_score: int, all_coaches: List[Dict]) -> int:
    """
    Calculate the user's percentile rank among all coaches based on career score.
    
    Args:
        user_score: User's calculated career score
        all_coaches: List of all coach dictionaries with scoring data
        
    Returns:
        int: Percentile rank (0-100), where 100 is the best
    """
    all_coaches = validate_list(all_coaches)
    user_score = int(validate_numeric(user_score, 0, 0))
    
    if not all_coaches:
        return 100
    
    # Calculate scores for all coaches
    scores = []
    for coach in all_coaches:
        coach = validate_dict(coach)
        titles = int(validate_numeric(coach.get("Titles", 0), 0, 0))
        wins = int(validate_numeric(coach.get("Wins", 0), 0, 0))
        score = titles * 50 + wins * 2
        scores.append(score)
    
    scores = sorted(scores, reverse=True)
    
    # Find user's position
    user_position = len([s for s in scores if s > user_score])
    
    # Calculate percentile
    percentile = int(((len(scores) - user_position) / len(scores)) * 100)
    return percentile


def calculate_committee_score(wins: int, losses: int, sos: float, conf: str, 
                              best_win_rank: int = 999, worst_loss_rank: int = 999) -> float:
    """
    Calculate CFP committee ranking score.
    
    Args:
        wins: Number of wins
        losses: Number of losses  
        sos: Strength of schedule (0-100)
        conf: Conference name
        best_win_rank: Rank of best win (lower is better)
        worst_loss_rank: Rank of worst loss
        
    Returns:
        float: Committee score (higher is better)
    """
    wins = int(validate_numeric(wins, 0, 0))
    losses = int(validate_numeric(losses, 0, 0))
    sos = validate_numeric(sos, 50, 0, 100)
    best_win_rank = int(validate_numeric(best_win_rank, 999, 1, 999))
    worst_loss_rank = int(validate_numeric(worst_loss_rank, 999, 1, 999))
    
    # Base score from record
    base_score = (wins * 100) - (losses * 150)
    
    # Strength of schedule bonus
    sos_bonus = (sos / 100) * 50
    
    # Quality wins bonus (lower rank = better win)
    quality_win_bonus = max(0, (100 - best_win_rank) / 10)
    
    # Bad loss penalty (lower rank = worse loss)
    bad_loss_penalty = 0
    if losses > 0 and worst_loss_rank > 50:
        bad_loss_penalty = (worst_loss_rank - 50) / 5
    
    # Power conference bonus
    power_conferences = ["SEC", "Big Ten", "ACC", "Big 12"]
    conf_bonus = 25 if conf in power_conferences else 0
    
    # Calculate final score
    score = base_score + sos_bonus + quality_win_bonus - bad_loss_penalty + conf_bonus
    
    return score


def calculate_saban_score(titles: int, wins: int, bowl_wins: int, prestige: int) -> int:
    """
    Calculate legacy score using Saban formula.
    
    Args:
        titles: National championships
        wins: Career wins
        bowl_wins: Bowl game victories
        prestige: Team prestige rating
        
    Returns:
        int: Legacy score
    """
    titles = int(validate_numeric(titles, 0, 0))
    wins = int(validate_numeric(wins, 0, 0))
    bowl_wins = int(validate_numeric(bowl_wins, 0, 0))
    prestige = int(validate_numeric(prestige, 0, 0, 100))
    
    score = (titles * 50) + (wins * 2) + (bowl_wins * 5) + (prestige * 0.5)
    
    return int(score)


def compute_recruiting_class_grade(total_rating: int, num_recruits: int) -> Tuple[str, str]:
    """
    Grade a recruiting class based on total rating and number of recruits.
    
    Args:
        total_rating: Sum of all recruit ratings
        num_recruits: Number of recruits in class
        
    Returns:
        Tuple of (grade letter, grade description)
    """
    total_rating = int(validate_numeric(total_rating, 0, 0))
    num_recruits = int(validate_numeric(num_recruits, 1, 1))
    
    # Calculate average rating
    avg_rating = total_rating / num_recruits
    
    # Grade thresholds
    if avg_rating >= 90:
        return "A+", "Elite Class"
    elif avg_rating >= 85:
        return "A", "Excellent Class"
    elif avg_rating >= 80:
        return "A-", "Strong Class"
    elif avg_rating >= 75:
        return "B+", "Good Class"
    elif avg_rating >= 70:
        return "B", "Solid Class"
    elif avg_rating >= 65:
        return "B-", "Average Class"
    elif avg_rating >= 60:
        return "C+", "Below Average"
    elif avg_rating >= 55:
        return "C", "Weak Class"
    elif avg_rating >= 50:
        return "C-", "Poor Class"
    elif avg_rating >= 45:
        return "D", "Very Poor Class"
    else:
        return "F", "Failed Class"


def categorize_season(record: str, postseason_result: str) -> str:
    """
    Categorize a season as championship, win, or loss.
    
    Args:
        record: Win-loss record (e.g., "12-1")
        postseason_result: Postseason outcome description
        
    Returns:
        str: Category ("championship", "win", or "loss")
    """
    record = str(record) if record else "0-0"
    postseason_result = str(postseason_result) if postseason_result else ""
    
    # Championship season
    if "TITLE" in postseason_result.upper() or "CHAMPIONSHIP" in postseason_result.upper():
        return "championship"
    
    # Parse record
    try:
        parts = record.split('-')
        if len(parts) >= 2:
            wins = int(parts[0])
            losses = int(parts[1])
            
            # Winning season: 8+ wins or bowl victory
            if wins >= 8 or "WON" in postseason_result.upper():
                return "win"
    except (ValueError, IndexError):
        pass
    
    return "loss"


def role_rating(coach: Dict, role: str) -> int:
    """
    Get coach rating for a specific role.
    
    Args:
        coach: Coach dictionary with ratings
        role: Role name (HC/OC/DC/Scout)
        
    Returns:
        int: Rating for that role (0-10)
    """
    coach = validate_dict(coach)
    role = str(role) if role else "HC"
    
    # Map role to rating key
    role_key_map = {
        "HC": "rating",
        "OC": "rating",
        "DC": "rating",
        "Scout": "rating"
    }
    
    rating_key = role_key_map.get(role, "rating")
    rating = int(validate_numeric(coach.get(rating_key, 5), 5, 0, 10))
    
    return rating


# Export commonly used functions
__all__ = [
    'validate_numeric',
    'validate_dict',
    'validate_list',
    'compute_team_needs',
    'normalize_shares',
    'calculate_percentile',
    'calculate_committee_score',
    'calculate_saban_score',
    'compute_recruiting_class_grade',
    'categorize_season',
    'role_rating',
]
