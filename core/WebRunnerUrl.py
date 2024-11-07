#!/usr/bin/env python3

from core.core import *
import requests
import validators
import sys
import concurrent.futures
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

class URL_OPTIONS:
    MODULE_NAME = "URL extractor"
    TARGET_URL = ""
    THREADS = 10
    USER_AGENT = "WebRunner v1.0"
    NO_TLS_VALIDATION = True
    COOKIE = ""
    HELP = False
    TIMEOUT = 15
    URLS = []

class URL_MODULE:
    def main(args):
        print(TerminalColor.Green + 'url extractor mode selected.' + TerminalColor.Reset)

        URL_OPTIONS.TARGET_URL = args.url
        URL_OPTIONS.THREADS = args.threads
        URL_OPTIONS.USER_AGENT = args.user_agent
        URL_OPTIONS.NO_TLS_VALIDATION = args.no_tls_validation
        URL_OPTIONS.HELP = args.help
        URL_OPTIONS.COOKIE = args.cookie
        URL_OPTIONS.TIMEOUT = int(args.timeout)

        if URL_OPTIONS.HELP:
            URL_HELP.Help()

        if not URL_OPTIONS.TARGET_URL:
            print(TerminalColor.Red + "Target URL is required!" + TerminalColor.Reset)
            print(f"{TerminalColor.Orange}Example: 'python3 WebRunner.py url -u http://www.domain.com'{TerminalColor.Reset}")
            print(f"{TerminalColor.Orange}Type 'python3 WebRunner.py url -h' for commands{TerminalColor.Reset}")
            sys.exit()

        if not validators.url(URL_OPTIONS.TARGET_URL):
            print(TerminalColor.LightRed + "Invalid URL!" + TerminalColor.Reset)
            sys.exit()

        Core.Banner()
        URL_MODULE.Banner()

        try:
            print(f'[{TerminalColor.Blue}!{TerminalColor.Reset}] {TerminalColor.Orange}Checking connection for {URL_OPTIONS.TARGET_URL}{TerminalColor.Reset}')
            headers = {"User-Agent": URL_OPTIONS.USER_AGENT, "Cookie": URL_OPTIONS.COOKIE}

            res = requests.get(
                URL_OPTIONS.TARGET_URL,
                headers=headers,
                allow_redirects=False,
                timeout=URL_OPTIONS.TIMEOUT,
                verify=not URL_OPTIONS.NO_TLS_VALIDATION
            )
            print(f'[{TerminalColor.Green}+{TerminalColor.Reset}] {TerminalColor.Green}Connection OK!{TerminalColor.Reset}')

        except requests.exceptions.Timeout:
            print(f"{TerminalColor.Red}Timeout for {URL_OPTIONS.TARGET_URL}{TerminalColor.Reset}")
            sys.exit()
        except requests.exceptions.SSLError:
            print(f"{TerminalColor.Red}SSL verification error! Add -k arg to ignore.{URL_OPTIONS.TARGET_URL}{TerminalColor.Reset}")
            print(f"{TerminalColor.Orange}Type 'python3 WebRunner.py url -h' for commands{TerminalColor.Reset}")
            sys.exit()
        except requests.exceptions.TooManyRedirects:
            print(f"{TerminalColor.Red}Too many redirects for {URL_OPTIONS.TARGET_URL}{TerminalColor.Reset}")
            sys.exit()
        except requests.exceptions.ConnectionError as e:
            print(f"{TerminalColor.Red}Connection error: {e}{TerminalColor.Reset}")
            sys.exit()
        except KeyboardInterrupt:
            print(f'{TerminalColor.Red}Process terminated, Ctrl C!{TerminalColor.Reset}')
            sys.exit()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        URL_TASK.Threads()

    def Banner():
        Message = f"""- Target: {TerminalColor.Green}{URL_OPTIONS.TARGET_URL}{TerminalColor.Reset}
- Attack mode: {TerminalColor.Green}{URL_OPTIONS.MODULE_NAME}{TerminalColor.Reset}
- User-agent: {TerminalColor.Green}{URL_OPTIONS.USER_AGENT}{TerminalColor.Reset}"""

        if URL_OPTIONS.COOKIE:
            Message = f"""{Message}
- Cookie: {TerminalColor.Green}{URL_OPTIONS.COOKIE}{TerminalColor.Reset}"""

        if not URL_OPTIONS.NO_TLS_VALIDATION:
            Message = f"""{Message}
- TLS Validation: {TerminalColor.Green}{URL_OPTIONS.NO_TLS_VALIDATION}{TerminalColor.Reset}"""
        
        print(f"""{Message}
======================================================================================================""")

class URL_TASK:
    def Threads():
        try:
            headers = {"User-Agent": URL_OPTIONS.USER_AGENT, "Cookie": URL_OPTIONS.COOKIE}
            r = requests.get(
                URL_OPTIONS.TARGET_URL,
                headers=headers,
                allow_redirects=False,
                timeout=URL_OPTIONS.TIMEOUT,
                verify=not URL_OPTIONS.NO_TLS_VALIDATION
            )
            soup = BeautifulSoup(r.text, 'html.parser')
            urls = []

            for tag in soup.find_all(['a', 'script']):
                attr = 'href' if tag.name == 'a' else 'src'
                link = tag.get(attr)
                if link:
                    if 'http' in link:
                        urls.append(link)
                        URL_OPTIONS.URLS.append(link)
                    else:
                        build_url = f"{URL_OPTIONS.TARGET_URL}/{link}"
                        formatted_url = build_url.replace('//', '/').replace(':/', '://')
                        urls.append(formatted_url)
                        URL_OPTIONS.URLS.append(formatted_url)

            check_urls = list(dict.fromkeys(urls))

            print(f"[{TerminalColor.Blue}!{TerminalColor.Reset}] {TerminalColor.Orange}Looking for URLs...{TerminalColor.Reset}")
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(URL_OPTIONS.THREADS)) as executor:
                future_to_url = {executor.submit(URL_TASK.ExtractURLs, url): url for url in check_urls}

                for future in concurrent.futures.as_completed(future_to_url):
                    future.result()

            for url in list(dict.fromkeys(URL_OPTIONS.URLS)):
                if validators.url(url):
                    print(f"[{TerminalColor.Green}+{TerminalColor.Reset}] {TerminalColor.Green}{url}{TerminalColor.Reset}")

        except KeyboardInterrupt:
            print(f'{TerminalColor.Red}Process terminated, Ctrl C!{TerminalColor.Reset}')
            sys.exit()
        except Exception:
            pass

    @staticmethod
    def ExtractURLs(url=""):
        try:
            headers = {"User-Agent": URL_OPTIONS.USER_AGENT, "Cookie": URL_OPTIONS.COOKIE}
            r = requests.get(url, headers=headers, allow_redirects=False, timeout=URL_OPTIONS.TIMEOUT, verify=not URL_OPTIONS.NO_TLS_VALIDATION)
            soup = BeautifulSoup(r.text, 'html.parser')

            for tag in soup.find_all(['a', 'script']):
                attr = 'href' if tag.name == 'a' else 'src'
                link = tag.get(attr)
                if link:
                    if 'http' in link:
                        URL_OPTIONS.URLS.append(link)
                    else:
                        build_url = f"{URL_OPTIONS.TARGET_URL}/{link}"
                        formatted_url = build_url.replace('//', '/').replace(':/', '://')
                        URL_OPTIONS.URLS.append(formatted_url)

        except KeyboardInterrupt:
            print(f'{TerminalColor.Red}Process terminated, Ctrl C!{TerminalColor.Reset}')
            sys.exit()
        except Exception:
            pass

class URL_HELP:
    def Help():
        print("""URL Extractor - Help menu

Uses URL Extractor mode

Usage:
  python3 WebRunner.py url [args]

Args:
    -u, --url                set target URL (required)
    -a, --user-agent         set user agent, default is 'WebRunner v1.0'
    -c, --cookie             set cookie for HTTP requests
    -t, --threads            set number of threads
    -k, --no-tls-validation  skip SSL validation
    --timeout                set timeout for HTTP requests
    -h, --help               show this message

Examples:

    URL extractor
    python3 WebRunner.py url -u https://www.domain.com
                """)
        sys.exit()