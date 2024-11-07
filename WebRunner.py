#!/usr/bin/env python3

from core.core import *
from core.WebRunnerUrl import *
from core.WebRunnerRegx import *
from core.WebRunnerEmails import *
from core.WebRunnerHelp import *
from core.WebRunnerClone import *
import argparse
from bs4 import BeautifulSoup
import requests

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-u', '--url', help='Set target URL')
parser.add_argument('-a', '--user-agent', default='WebRunner v1.0', help='Set user-agent')
parser.add_argument('-t', '--threads', default='10', help='Set threads')
parser.add_argument('mode', help='Set attack mode (url,email,regx,clone)')
parser.add_argument('-h', '--help', action='store_true', help="")
parser.add_argument('-k', '--no-tls-validation', action='store_false')
parser.add_argument('-c', '--cookie', help='Set cookies to use for the requests')
parser.add_argument('--timeout', default=15, help='Time each thread waits between requests (15s by default)')
parser.add_argument('-s', '--string', help='Set string to search.')
parser.add_argument('-n', '--name', help='Set project name for clone module.')
parser.add_argument('-f', '--folder', help='Set destination folder for clone module.')
args = parser.parse_args()
ATTACK_MODE = args.mode

if ATTACK_MODE == 'url':
    URL_MODULE.main(args)
elif ATTACK_MODE == 'regx':
    REGX_MODULE.main(args)
elif ATTACK_MODE == 'email':
    EMAILS_MODULE.main(args)
elif ATTACK_MODE == 'help':
    HELP_MODULE.main()
elif ATTACK_MODE == 'clone':
    CLONE_MODULE.main(args)

# Exemplo de scraping usando BeautifulSoup
if args.url:
    headers = {'User-Agent': args.user_agent}
    response = requests.get(args.url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())  # Exibe o HTML formatado
    else:
        print(f"Erro ao acessar a URL: {response.status_code}")