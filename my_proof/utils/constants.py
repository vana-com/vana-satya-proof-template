# Time thresholds (in milliseconds)
MIN_TIME_SPENT_MS = 2000          # Minimum time spent on a page (2 seconds)
MAX_TIME_SPENT_MS = 7200000       # Maximum time spent on a page (2 hours)

# Completeness
REQUIRED_FIELDS = {'url', 'timeSpent', 'listOfActions'}

# Authenticity thresholds
LONG_DURATION_THRESHOLD_MS = 300000  # 5 minutes (300,000 ms) without actions

# Scoring weights
MAX_QUALITY_SCORE = 60
MAX_AUTHENTICITY_SCORE = 40

# Labeling thresholds based on overall score
HIGH_QUALITY_THRESHOLD = 80
MODERATE_QUALITY_THRESHOLD = 50

# Sigmoid Function Parameters
X0 = 0.5  # Midpoint of the sigmoid curve
K = 5     # Steepness of the curve