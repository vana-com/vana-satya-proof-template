import my_proof.utils.constants as constants

def label_browsing_behavior(overall_score):
    """
    Labels the browsing behavior based on the overall score.
    """
    if overall_score >= constants.HIGH_QUALITY_THRESHOLD:
        return "High Quality, Authentic Browsing"
    elif overall_score >= constants.MODERATE_QUALITY_THRESHOLD:
        return "Moderate Quality, Some Authentic Traits"
    else:
        return "Low Quality, Potentially Non-Human Browsing"
