import os

LANGUAGE = "he-IL"  # או "en-US" בהתאם לשפה הרצויה

SEARCH_FOLDERS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Music")
]

# הגדרות לוגינג
LOG_LEVEL = "INFO" # INFO, DEBUG, WARNING, ERROR, CRITICAL
LOG_FILE = "assistant.log"