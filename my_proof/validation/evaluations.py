import my_proof.utils.constants as constants 
from my_proof.utils.defs import is_valid_url
import math
import hashlib

def sigmoid(x, k=constants.K, x0=constants.X0):
    """
    Applies the sigmoid function to the normalized score.
    Parameters:
        - x: Normalized input score between 0 and 1.
        - k: Steepness of the curve.
        - x0: Midpoint of the sigmoid curve.
    """
    z = k * (x - x0)
    return 1 / (1 + math.exp(-z))

def evaluate_quality(browsing_data):
    """
    Evaluates the quality of the browsing data.
    """
    quality_score = 0
    max_quality_score = constants.MAX_QUALITY_SCORE
    weights = {
        'time_spent': 40,  # Increased weight for time spent
        'completeness': 10,
        'action_engagement': 10
    }

    total_entries = len(browsing_data)
    valid_time_entries = 0
    completeness_issues = 0
    action_engagement_score = 0

    for entry in browsing_data:
        # Completeness
        if not constants.REQUIRED_FIELDS.issubset(entry.keys()):
            completeness_issues += 1
            continue  # Skip incomplete entries

        # URL validation
        if not is_valid_url(entry['url']):
            completeness_issues += 1
            continue  # Skip invalid URLs

        # Time Spent Validation per URL
        time_spent = entry['timeSpent']
        if constants.MIN_TIME_SPENT_MS <= time_spent <= constants.MAX_TIME_SPENT_MS:
            valid_time_entries += 1
        else:
            pass  # Do not count towards valid entries

        # Action Engagement
        if entry['listOfActions']:
            action_engagement_score += 1

    # Time Spent Score
    if total_entries > 0:
        time_spent_ratio = valid_time_entries / total_entries
        quality_score += time_spent_ratio * weights['time_spent']

    # Completeness Score
    completeness_ratio = (total_entries - completeness_issues) / total_entries if total_entries > 0 else 0
    quality_score += completeness_ratio * weights['completeness']

    # Action Engagement Score
    action_engagement_ratio = action_engagement_score / total_entries if total_entries > 0 else 0
    quality_score += action_engagement_ratio * weights['action_engagement']

    return min(quality_score, max_quality_score)/100 #normalize the value


def evaluate_authenticity(browsing_data):
    """
    Evaluates the authenticity of the browsing data based on human-like behavior.
    """
    authenticity_score = constants.MAX_AUTHENTICITY_SCORE
    total_entries = len(browsing_data)
    short_visits = 0
    long_visits_without_actions = 0

    for entry in browsing_data:
        time_spent = entry.get('timeSpent', 0)
        actions = entry.get('listOfActions', [])

        # Count short visits (timeSpent < MIN_TIME_SPENT_MS)
        if time_spent < constants.MIN_TIME_SPENT_MS:
            short_visits += 1

        # Penalize long durations without actions (timeSpent > LONG_DURATION_THRESHOLD_MS)
        if time_spent > constants.LONG_DURATION_THRESHOLD_MS and not actions:
            long_visits_without_actions += 1

    # Calculate penalties
    # Penalty for short visits (proportion of short visits)
    if total_entries > 0:
        short_visit_ratio = short_visits / total_entries
        short_visit_penalty = short_visit_ratio * 20  # Up to 20 points penalty
        authenticity_score -= short_visit_penalty

    # Penalty for long visits without actions
    long_visit_penalty = long_visits_without_actions * 10  # 10 points penalty per occurrence
    authenticity_score -= long_visit_penalty

    # Ensure the score does not go negative
    authenticity_score = max(authenticity_score, 0)

    return authenticity_score/100 #normalize the value


def compute_overall_score(quality_score, authenticity_score):
    """
    Combines the quality and authenticity scores into an overall score.
    """
    overall_score = quality_score + authenticity_score
    return min(overall_score, 1)

def evaluate_hash(browsing_data):

    pass