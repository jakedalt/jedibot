import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
ENVIRONMENT = os.getenv('ENVIRONMENT')
DD_KEY = os.getenv('DD_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
SCHEMA = os.getenv('SCHEMA')
TABLE = os.getenv('TABLE')





