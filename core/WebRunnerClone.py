#!/usr/bin/env python3

from core.core import *
import string
import sys
import validators
import random
import requests
from bs4 import BeautifulSoup
import os

class CLONE_OPTIONS:
    MODULE_NAME = "Clone module"
    TARGET_URL = ""
    FOLDER = "projects/"
    NAME = ""
    HELP = False

class CLONE_MODULE:

    def main(args):
        print(TerminalColor.Green + 'clone mode selected.' + TerminalColor.Reset)

        CLONE_OPTIONS.TARGET_URL = args.url
        CLONE_OPTIONS.FOLDER = args.folder
        CLONE_OPTIONS.NAME = args.name
        CLONE_OPTIONS.HELP = args.help

        Core.Banner()
        CLONE_MODULE.Banner()

        if CLONE_OPTIONS.HELP:
            CLONE_HELP.Help()

        if not CLONE_OPTIONS.NAME:
            CLONE_OPTIONS.NAME = CLONE_MODULE.RandomStrings()

        if not CLONE_OPTIONS.FOLDER:
            CLONE_OPTIONS.FOLDER = "projects/"

        if not CLONE_OPTIONS.TARGET_URL:
            print(f'{TerminalColor.Red}Target URL is required{TerminalColor.Reset}')
            sys.exit()

        if not validators.url(CLONE_OPTIONS.TARGET_URL):
            print(TerminalColor.LightRed + "Invalid URL!" + TerminalColor.Reset)
            sys.exit()

        # Cria a pasta para salvar o site, se não existir
        os.makedirs(CLONE_OPTIONS.FOLDER, exist_ok=True)
        CLONE_MODULE.clone_website(CLONE_OPTIONS.TARGET_URL, CLONE_OPTIONS.FOLDER, CLONE_OPTIONS.NAME)

    def Banner():
        print(f"""- Target: {TerminalColor.Green}{CLONE_OPTIONS.TARGET_URL}{TerminalColor.Reset}
- Attack mode: {TerminalColor.Green}{CLONE_OPTIONS.MODULE_NAME}{TerminalColor.Reset}
- Project name: {TerminalColor.Green}{CLONE_OPTIONS.NAME}{TerminalColor.Reset}
- Destination folder: {TerminalColor.Green}{CLONE_OPTIONS.FOLDER}{TerminalColor.Reset}
======================================================================================================""")

    def RandomStrings(size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def clone_website(url, folder, name):
        headers = {'User-Agent': 'WebRunner v1.0'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
            soup = BeautifulSoup(response.text, 'html.parser')

            # Salva o HTML principal
            with open(os.path.join(folder, f"{name}.html"), "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            print(TerminalColor.Green + "Website cloned successfully!" + TerminalColor.Reset)

        except requests.exceptions.RequestException as e:
            print(TerminalColor.Red + f"Error while cloning website: {e}" + TerminalColor.Reset)
            sys.exit()

class CLONE_HELP:
    def Help():
        print("""Clone websites - Help menu

Uses Clone websites mode

Usage:
  python3 WebRunner.py clone [args]

Args:
    -u, --url                set target url (required)
    -f, --folder             set destination folder 
    -n, --name               set project name 
    -h, --help               show this message

Examples:

    clone websites
    python3 WebRunner.py clone -u https://www.domain.com -n mysite
                """)
        sys.exit()