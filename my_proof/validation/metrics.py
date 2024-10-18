import math
from typing import Dict

import math

def recalculate_evaluation_metrics(decrypted_data: dict) -> dict:
    encrypted_browsing_data_array = decrypted_data.get('browsingDataArray', [])
    
    url_count = len(encrypted_browsing_data_array)
    time_spent_list = []
    action_counts_list = []
    cookie_counts_list = []
    total_actions = 0
    total_time_spent = 0  # In seconds
    total_cookies = 0
    
    for entry in encrypted_browsing_data_array:
        # Handle time spent
        time_spent_ms = entry.get('timeSpent', 0)
        time_spent_sec = time_spent_ms / 1000.0  # Convert milliseconds to seconds
        time_spent_sec_int = math.floor(time_spent_sec)  # Floor for consistency
        time_spent_list.append(time_spent_sec_int)
        total_time_spent += time_spent_sec_int
        
        # Handle actions
        actions = entry.get('actions', {})
        action_count = len(actions)
        action_counts_list.append(action_count)
        total_actions += action_count
        
        # Handle cookies
        cookies_count = entry.get('cookies', 0)
        cookie_counts_list.append(cookies_count)
        total_cookies += cookies_count
    
    # Calculate points: (URL count + total actions) * 10 + total time spent + total cookies
    points = math.floor((url_count + total_actions) * 10 + total_time_spent + total_cookies)
    
    calculated_metrics = {
        'url_count': url_count,
        'timeSpent': time_spent_list,
        'actions': action_counts_list,
        'cookies': cookie_counts_list,
        'points': points
    }
    print("calculated_metrics :",calculated_metrics)
    
    return calculated_metrics

def verify_evaluation_metrics(calculated_metrics: dict, given_metrics: dict) -> bool:
    calculated_points = calculated_metrics.get('points', 0)
    given_points = given_metrics.get('points', 0)
    points_match = (calculated_points == given_points)
    
    metrics_match = (
        calculated_metrics.get('url_count', 0) == given_metrics.get('url_count', 0) and
        calculated_metrics.get('timeSpent', []) == given_metrics.get('timeSpent', []) and
        calculated_metrics.get('actions', []) == given_metrics.get('actions', []) and
        calculated_metrics.get('cookies', []) == given_metrics.get('cookies', [])
    )
    
    authenticity = points_match and metrics_match
    return authenticity
