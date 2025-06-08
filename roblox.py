import requests
import time
import random
import string
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG = {
    "USERNAME_LENGTH": 4,
    "DELAY": 0.0,
    "MAX_API_RETRIES": 5,
    "RETRY_DELAY": 2,
    "API_TIMEOUT": 10,
    "INCLUDE_NUMBERS": True
}

def generate_username():
    characters = string.ascii_lowercase
    if CONFIG["INCLUDE_NUMBERS"]:
        characters += string.digits
    return ''.join(random.choice(characters) for _ in range(CONFIG["USERNAME_LENGTH"]))

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=2000-01-01"
    
    for attempt in range(CONFIG["MAX_API_RETRIES"]):
        try:
            response = requests.get(url, timeout=CONFIG["API_TIMEOUT"])
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                print(Fore.GREEN + f"VALID: {username}")
                with open("valid.txt", "a") as f:
                    f.write(username + "\n")
                return True
            else:
                print(Fore.LIGHTBLACK_EX + f"INVALID: {username}")
                return False
                
        except requests.exceptions.RequestException as e:
            if attempt < CONFIG["MAX_API_RETRIES"] - 1:
                print(Fore.YELLOW + f"Retry {attempt+1}/{CONFIG['MAX_API_RETRIES']} for {username}")
                time.sleep(CONFIG["RETRY_DELAY"])
            else:
                print(Fore.RED + f"FAILED: {username} after {CONFIG['MAX_API_RETRIES']} attempts")
                return False
                
    return False

def main():
    print(Fore.CYAN + "=== Roblox Username Availability Checker ===")
    print(Fore.CYAN + f"Checking {CONFIG['USERNAME_LENGTH']}-char usernames...")
    print(Fore.CYAN + f"Numbers {'included' if CONFIG['INCLUDE_NUMBERS'] else 'excluded'}")
    
    valid_count = 0
    total_checked = 0
    start_time = time.time()
    
    try:
        while True:
            username = generate_username()
            if check_username(username):
                valid_count += 1
                
            total_checked += 1
            elapsed = time.time() - start_time
            
            # Mostrar estatísticas a cada 50 verificações
            if total_checked % 50 == 0:
                rate = total_checked / elapsed if elapsed > 0 else 0
                print(Fore.MAGENTA + 
                      f"Checked: {total_checked} | " +
                      f"Valid: {valid_count} | " +
                      f"Rate: {rate:.2f} checks/sec")
            
            time.sleep(CONFIG["DELAY"])
            
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        rate = total_checked / elapsed if elapsed > 0 else 0
        print(Fore.YELLOW + "\n" + "=" * 50)
        print(Fore.CYAN + "Final statistics:")
        print(Fore.CYAN + f"Total checked: {total_checked}")
        print(Fore.CYAN + f"Valid usernames: {valid_count}")
        print(Fore.CYAN + f"Average rate: {rate:.2f} checks/sec")
        print(Fore.YELLOW + "Script stopped by user")
    except Exception as e:
        print(Fore.RED + f"UNEXPECTED ERROR: {str(e)}")
    finally:
        print(Fore.CYAN + "Script ended")

if __name__ == "__main__":
    main()
