import os

# BASE PATH
BASE_PATH = os.getcwd()

# LOGS PATH
LOG_FOLDER_PATH = os.path.join(BASE_PATH, 'logs')
SCRAPER_LOG_CONFIG = '_scraper'
SCRAPER_LOG_FILENAME = 'scraper_log'

# DATA PATH
DATA_PATH = os.path.join(BASE_PATH, 'data')
CSV_FILENAME = 'data_extracted.csv'

# CONSTANTS FOR WEBPAGES
MAIN_WEBPAGE = "https://news.ycombinator.com/"

# QUESTIONS
QUESTION_1 = """Filter all previous entries with more than five words in the title ordered by the number of comments first"""
QUESTION_2 = """Filter all previous entries with less than or equal to five words in the title ordered by points"""
