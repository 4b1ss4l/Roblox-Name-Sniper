import requests
import time
import random
import string
from colorama import Fore, Style, init
import logging
import traceback

init(autoreset=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='username_checker.log'
)
logger = logging.getLogger(__name__)

CONFIG = {
    "USERNAME_LENGTH": 5,
    "DELAY": 0.5,
    "MAX_RETRIES": 3,
    "RETRY_DELAY": 5,
    "API_TIMEOUT": 10
}

def generate_username():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(CONFIG["USERNAME_LENGTH"]))

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=2000-01-01"
    try:
        response = requests.get(url, timeout=CONFIG["API_TIMEOUT"])
        response.raise_for_status()
        data = response.json()

        code = data.get("code")
        if code == 0:
            logger.info(f"VALID: {username}")
            print(Fore.GREEN + f"VALID: {username}" + Style.RESET_ALL)
            with open("valid.txt", "a") as f:
                f.write(username + "\n")
            return True
        elif code == 1:
            logger.info(f"TAKEN: {username}")
            print(Fore.LIGHTBLACK_EX + f"TAKEN: {username}" + Style.RESET_ALL)
        elif code == 2:
            logger.info(f"CENSORED: {username}")
            print(Fore.RED + f"CENSORED: {username}" + Style.RESET_ALL)
        else:
            logger.warning(f"UNKNOWN CODE {code}: {username}")
            print(Fore.YELLOW + f"UNKNOWN CODE ({code}): {username}" + Style.RESET_ALL)

    except Exception as e:
        logger.error(f"ERROR checking {username}: {str(e)}\n{traceback.format_exc()}")
        print(Fore.RED + f"API ERROR: {username}: {str(e)}" + Style.RESET_ALL)
        raise

    return False

def run_checker():
    retry_count = 0
    while retry_count < CONFIG["MAX_RETRIES"]:
        try:
            username = generate_username()
            if check_username(username):
                retry_count = 0
            time.sleep(CONFIG["DELAY"])
            
        except requests.exceptions.RequestException as e:
            retry_count += 1
            logger.error(f"Connection error (attempt {retry_count}/{CONFIG['MAX_RETRIES']}): {str(e)}")
            print(Fore.RED + f"CONNECTION FAILED. Retry {retry_count} in {CONFIG['RETRY_DELAY']}s..." + Style.RESET_ALL)
            time.sleep(CONFIG["RETRY_DELAY"])
            
        except KeyboardInterrupt:
            logger.info("Script stopped by user")
            print(Fore.YELLOW + "\nScript stopped by user" + Style.RESET_ALL)
            return False
            
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
            print(Fore.RED + f"CRITICAL ERROR: {str(e)}" + Style.RESET_ALL)
            time.sleep(CONFIG["RETRY_DELAY"])
            retry_count += 1

    return retry_count >= CONFIG["MAX_RETRIES"]

def main():
    print(Fore.CYAN + "=== Roblox Username Checker ===" + Style.RESET_ALL)
    print(Fore.CYAN + f"Generating {CONFIG['USERNAME_LENGTH']}-letter usernames..." + Style.RESET_ALL)
    
    while True:
        failure = run_checker()
        if failure:
            print(Fore.RED + "Maximum retries reached. Restarting in 10 seconds..." + Style.RESET_ALL)
            time.sleep(10)
        else:
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}\n{traceback.format_exc()}")
        print(Fore.RED + f"FATAL ERROR: {str(e)}" + Style.RESET_ALL)
    finally:
        print(Fore.CYAN + "Script ended" + Style.RESET_ALL)
