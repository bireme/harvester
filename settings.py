import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__)) + '/xml/'
REGEX_DATE = '\d{4}-\d{2}-\d{2}'
STR_DATE = '%Y-%m-%d'
DATE_EX = '2011-04-30'

# Providers constant allows to harvest a list of OAI providers 
# with -g or --go option
PROVIDERS = (
            ('Name', 'URL'),
            ('Name', 'URL'),
)
