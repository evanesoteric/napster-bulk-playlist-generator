from datetime import datetime
import time

import sys
import os
home_dir = os.path.expanduser('~')

# setup logging
import logging
logging.basicConfig(filename=f'{home_dir}/napster.log',
    filemode='a+',
    format='%(asctime)s %(levelname)-8s "%(message)s"',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M')

import string
import random
import re

import json
import requests
from bs4 import BeautifulSoup


# for use in headers
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
user_agent_header = {'User-agent': user_agent}

api_default_username = ''  # napster API fallback
api_default_password = ''  # napster API fallback

# import accounts
try:
    with open('accounts.txt', 'r') as f:
        accounts = f.read().splitlines()
        accounts = list(filter(None, accounts))
except FileNotFoundError:
    logging.error('[config] No account.txt file found. Exiting!')
    sys.exit()
except Exception as e:
    logging.critical(f'[config] Error: {e}. Exiting!')
    sys.exit(e)


# import albums
try:
    with open('albums.txt', 'r') as f:
        albums = f.read().splitlines()
        albums = list(filter(None, albums))
except FileNotFoundError:
    logging.error('[config] No albums.txt file found. Exiting!')
    sys.exit()
except Exception as e:
    logging.critical('Error: ' + e + '. Exiting!')
    sys.exit(1)


# import playlist names
try:
    with open('playlist_names.txt', 'r') as f:
        playlist_names = f.read().splitlines()
        playlist_names = list(filter(None, playlist_names))
except FileNotFoundError:
    logging.error('[config] No playlist_names.txt file found. Exiting!')
    sys.exit()
except Exception as e:
    logging.critical('Error: ' + e + '. Exiting!')
    sys.exit(1)
