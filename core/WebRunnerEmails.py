from core.core import *
import requests
import sys
import concurrent.futures
import urllib3
import validators
import re
urllib3.disable_warnings()

class EMAILS_OPTIONS:
    MODULE_NAME="Emails search module"
    TARGET_URL=""
    USER_AGENT=""
    NO_TLS_VALIDATION=True
    COOKIE=""
    HELP=False
    TIMEOUT=15
    THREADS=10
    EMAILS=[]

class EMAILS_MODULE:
    def main(args):
        print(TerminalColor.Green + 'emails search mode selected.' + TerminalColor.Reset)

        EMAILS_OPTIONS.TARGET_URL = args.url
        EMAILS_OPTIONS.USER_AGENT = args.user_agent
        EMAILS_OPTIONS.NO_TLS_VALIDATION = args.no_tls_validation
        EMAILS_OPTIONS.HELP = args.help
        EMAILS_OPTIONS.COOKIE = args.cookie
        EMAILS_OPTIONS.TIMEOUT = int(args.timeout)

        if EMAILS_OPTIONS.HELP:
            EMAIL_HELP.Help()

        if not EMAILS_OPTIONS.TARGET_URL:
            print(TerminalColor.Red + "target url is required!" + TerminalColor.Reset)
            print(f"{TerminalColor.Orange}example: python3 WebRunner.py email -u http://www.domain.com{TerminalColor.Reset}")
            print(f"{TerminalColor.Orange}Type 'python3 WebRunner.py email -h' for commands{TerminalColor.Reset}")
            sys.exit()

        if not validators.url(EMAILS_OPTIONS.TARGET_URL):
            print(TerminalColor.LightRed + "Invalid url!" + TerminalColor.Reset)
            sys.exit()

        Core.Banner()
        EMAILS_MODULE.Banner()

        try:
            print(f'[{TerminalColor.Blue}!{TerminalColor.Reset}] {TerminalColor.Orange}Checking connection for {EMAILS_OPTIONS.TARGET_URL}{TerminalColor.Reset}')
            headers = {"User-Agent": f"{EMAILS_OPTIONS.USER_AGENT}", "cookie": EMAILS_OPTIONS.COOKIE}

            res = requests.get(EMAILS_OPTIONS.TARGET_URL, headers=headers, allow_redirects=False, timeout=EMAILS_OPTIONS.TIMEOUT, verify=EMAILS_OPTIONS.NO_TLS_VALIDATION)
            print(f'[{TerminalColor.Green}+{TerminalColor.Reset}]{TerminalColor.Green} Connection OK!{TerminalColor.Reset}')

        except requests.exceptions.Timeout:
            print(f"{TerminalColor.Red}Timeout for {EMAILS_OPTIONS.TARGET_URL}{TerminalColor.Reset}")
            sys.exit()
        except requests.exceptions.SSLError:
            print(f"{TerminalColor.Red}SSL verification error! add -k arg to ignore.{EMAILS_OPTIONS.TARGET_URL}{TerminalColor.Reset}")
            print(f"{TerminalColor.Orange}Type 'python3 WebRunner.py email -h' for commands{TerminalColor.Reset}")
            sys.exit()
        except requests.exceptions.TooManyRedirects:
            print(f"{TerminalColor.Red}Too many redirects for {EMAILS_OPTIONS.TARGET_URL}{TerminalColor.Reset}")
            sys.exit()
        except requests.exceptions.ConnectionError as e:
            print(f"{TerminalColor.Red}Connection error: {e}{TerminalColor.Reset}")
            sys.exit()
        except KeyboardInterrupt:
            print(f'{TerminalColor.Red}Process terminated, Ctrl C!{TerminalColor.Reset}')
            sys.exit()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        EMAILS_TASK.Threads()

    def Banner():
        Message = f"""- Target: {TerminalColor.Green}{EMAILS_OPTIONS.TARGET_URL}{TerminalColor.Reset}
- Attack mode: {TerminalColor.Green}{EMAILS_OPTIONS.MODULE_NAME}{TerminalColor.Reset}
- User-agent: {TerminalColor.Green}{EMAILS_OPTIONS.USER_AGENT}{TerminalColor.Reset}"""

        if EMAILS_OPTIONS.COOKIE:
            Message += f"\n- Cookie: {TerminalColor.Green}{EMAILS_OPTIONS.COOKIE}{TerminalColor.Reset}"

        if not EMAILS_OPTIONS.NO_TLS_VALIDATION:
            Message += f"\n- TLS Validation: {TerminalColor.Green}{EMAILS_OPTIONS.NO_TLS_VALIDATION}{TerminalColor.Reset}"
        
        print(f"{Message}\n======================================================================================================")


class EMAILS_TASK:
    def Threads():
        try:
            headers = {"User-Agent": f"{EMAILS_OPTIONS.USER_AGENT}", "cookie": EMAILS_OPTIONS.COOKIE}
            r = requests.get(EMAILS_OPTIONS.TARGET_URL, headers=headers, allow_redirects=False, timeout=EMAILS_OPTIONS.TIMEOUT, verify=EMAILS_OPTIONS.NO_TLS_VALIDATION)

            # Extrair URLs da página usando regex
            tag_a = re.findall(r'href=["\'](http[s]?://[^\s"\'<>]+)', r.text)
            tag_scripts = re.findall(r'src=["\'](http[s]?://[^\s"\'<>]+)', r.text)

            urls = set(tag_a + tag_scripts)
            urls.add(EMAILS_OPTIONS.TARGET_URL)

            print(f"[{TerminalColor.Blue}!{TerminalColor.Reset}] {TerminalColor.Orange}Looking for emails...{TerminalColor.Reset}")
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(EMAILS_OPTIONS.THREADS)) as executor:
                future_to_url = {executor.submit(EMAILS_TASK.Search, url): url for url in urls}

                for future in concurrent.futures.as_completed(future_to_url):
                    future.result()

            for email in list(dict.fromkeys(EMAILS_OPTIONS.EMAILS)):
                if validators.email(email):
                    print(f"[{TerminalColor.Green}+{TerminalColor.Reset}] {TerminalColor.Green}{email}{TerminalColor.Reset}")

        except KeyboardInterrupt:
            print(f'{TerminalColor.Red}Process terminated, Ctrl C!{TerminalColor.Reset}')
            sys.exit()
        except:
            pass

    def Search(URL=""):
        try:
            headers = {"User-Agent": f"{EMAILS_OPTIONS.USER_AGENT}", "cookie": EMAILS_OPTIONS.COOKIE}
            r = requests.get(URL, headers=headers, allow_redirects=False, timeout=EMAILS_OPTIONS.TIMEOUT, verify=EMAILS_OPTIONS.NO_TLS_VALIDATION)
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', r.text)
            EMAILS_OPTIONS.EMAILS.extend(emails)

        except KeyboardInterrupt:
            print(f'{TerminalColor.Red}Process terminated, Ctrl C!{TerminalColor.Reset}')
            sys.exit()
        except:
            pass


class EMAIL_HELP:
    def Help():
        print("""Email Extractor - Help menu

Uses Email Extractor mode

Usage:
  python3 WebRunner.py email [args]

Args
    -u, --url                set target url (required)
    -a, --user-agent         set user agent, by default (WebRunner v1.0)
    -c, --cookie             set cookie for http requests
    -t, --threads            set threads
    -k, --no-tls-validation  not ssl check
        --timeout            set timeout for http requests
    -h, --help               show this message

Examples:

    email extractor
    python3 WebRunner.py email -u https://www.domain.com
                """)
        sys.exit()