import requests
import time
import random
import string
from colorama import Fore, Style, init
import sys
import re

init(autoreset=True)

class RobloxUsernameChecker:
    def __init__(self):
        # Settings
        self.username_length = 4
        self.delay = 0.2
        self.max_retries = 3
        self.retry_delay = 2
        self.timeout = 10
        self.use_special_chars = True
        self.use_numbers = True
        self.output_file = "valid_usernames.txt"
        
        # Allowed characters
        self.allowed_special_chars = ['_']
        self.base_chars = string.ascii_lowercase
        self.update_allowed_chars()
        
        # Statistics
        self.valid_count = 0
        self.total_checked = 0
        self.unknown_count = 0
        self.start_time = 0
        self.recent_usernames = set()
        self.max_recent = 1000

        # Error handling
        self.consecutive_errors = 0
        self.max_consecutive_errors = 10

    def update_allowed_chars(self):
        """Updates allowed characters based on settings"""
        chars = self.base_chars
        if self.use_numbers:
            chars += string.digits
        if self.use_special_chars:
            chars += ''.join(self.allowed_special_chars)
        self.all_chars = chars

    def save_valid_username(self, username):
        """Saves valid username to file"""
        with open(self.output_file, 'a') as f:
            f.write(username + '\n')

    def generate_valid_username(self) -> str:
        """Generates valid usernames following Roblox rules"""
        while True:
            # Ensures first character is a letter
            first_char = random.choice(string.ascii_lowercase)
            
            # Generates the rest of the username
            rest = []
            for _ in range(self.username_length - 1):
                char = random.choice(self.all_chars)
                
                # Avoids consecutive underscores
                if self.use_special_chars and char == '_' and rest and rest[-1] == '_':
                    char = random.choice(self.base_chars + (string.digits if self.use_numbers else ''))
                
                rest.append(char)
            
            username = first_char + ''.join(rest)
            
            # Ensures it doesn't end with underscore
            if self.use_special_chars and username.endswith('_'):
                username = username[:-1] + random.choice(self.base_chars + (string.digits if self.use_numbers else ''))
            
            # Checks if recently generated
            if username not in self.recent_usernames:
                self.recent_usernames.add(username)
                if len(self.recent_usernames) > self.max_recent:
                    self.recent_usernames.pop()
                return username

    def check_username(self, username: str) -> bool:
        """Checks username availability with robust error handling"""
        url = "https://auth.roblox.com/v1/usernames/validate"
        params = {
            "request.username": username,
            "request.birthday": "2000-01-01"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate"
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                    headers=headers
                )
                
                # Rate limit handling
                if response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 10))
                    self.print_message(f"Rate limit reached. Waiting {wait_time}s...", "warning")
                    time.sleep(wait_time)
                    continue
                
                # Server error handling
                if response.status_code >= 500:
                    self.print_message(f"Server error ({response.status_code}). Retrying...", "warning")
                    time.sleep(self.retry_delay)
                    continue
                    
                data = response.json()
                code = data.get("code")
                
                # Known responses handling
                if code == 0:
                    return True
                elif code in (1, 5):  # 1 and 5 indicate taken username
                    return False
                elif code == 2:
                    self.print_message(f"Censored: {username}", "error")
                    return False
                else:
                    # Unknown responses handling
                    self.unknown_count += 1
                    self.print_message(f"Unknown response (code: {code}) for: {username}", "warning")
                    
                    # Progressive delay for consecutive errors
                    if self.unknown_count % 5 == 0:
                        extra_delay = min(30, self.unknown_count * 2)
                        self.print_message(f"Too many consecutive errors. Waiting {extra_delay}s...", "error")
                        time.sleep(extra_delay)
                    
                    return False
                    
            except Exception as e:
                self.print_message(f"Error (attempt {attempt + 1}/{self.max_retries}): {str(e)}", "warning")
                time.sleep(self.retry_delay * (attempt + 1))
        
        self.print_message(f"Permanent failure: {username}", "error")
        return False

    def print_message(self, message: str, msg_type: str = "info"):
        """Displays colored messages according to type"""
        colors = {
            "success": Fore.GREEN + Style.BRIGHT,
            "error": Fore.RED + Style.BRIGHT,
            "warning": Fore.YELLOW,
            "info": Fore.LIGHTBLACK_EX,
            "header": Fore.CYAN + Style.BRIGHT,
            "stats": Fore.MAGENTA + Style.BRIGHT
        }
        print(colors.get(msg_type, "") + message)

    def print_header(self):
        """Displays the header"""
        header = f"""
        {Fore.CYAN + Style.BRIGHT}╔════════════════════════════════════════╗
        {Fore.CYAN + Style.BRIGHT}║                                        ║
        {Fore.CYAN + Style.BRIGHT}║    {Fore.WHITE + Style.BRIGHT}Roblox Username Sniper    {Fore.CYAN + Style.BRIGHT}║
        {Fore.CYAN + Style.BRIGHT}║                                        ║
        {Fore.CYAN + Style.BRIGHT}╚════════════════════════════════════════╝
        """
        print(header)
        print(f"{Fore.CYAN + Style.BRIGHT}• Length: {self.username_length} characters")
        print(f"{Fore.CYAN + Style.BRIGHT}• Numbers: {'Enabled' if self.use_numbers else 'Disabled'}")
        print(f"{Fore.CYAN + Style.BRIGHT}• Underscore: {'Enabled' if self.use_special_chars else 'Disabled'}")
        print(f"{Fore.CYAN + Style.BRIGHT}• Delay: {self.delay}s")
        print(f"{Fore.CYAN + Style.BRIGHT}• Mode: {'4 letters' if self.username_length == 4 else 'Custom'}")
        print(f"{Fore.CYAN + Style.BRIGHT}• Output file: {self.output_file}")
        print(f"{Fore.YELLOW}\nPress Ctrl+C to stop execution\n")

    def show_stats(self):
        """Displays formatted statistics"""
        elapsed = time.time() - self.start_time
        speed = self.total_checked / max(elapsed, 1)
        
        stats = f"""
        {Fore.MAGENTA + Style.BRIGHT}Total Checked: {self.total_checked}
        {Fore.MAGENTA + Style.BRIGHT}Valid Names: {self.valid_count}
        {Fore.MAGENTA + Style.BRIGHT}Unknown Errors: {self.unknown_count}
        {Fore.MAGENTA + Style.BRIGHT}Speed: {speed:.1f} checks/sec
        """
        print(stats)

    def run(self):
        """Runs the username checker"""
        self.print_header()
        self.start_time = time.time()
        
        # Clear/create output file
        open(self.output_file, 'w').close()
        
        try:
            while True:
                username = self.generate_valid_username()
                available = self.check_username(username)
                self.total_checked += 1
                
                if available:
                    self.valid_count += 1
                    self.print_message(f"Available: {username}", "success")
                    self.save_valid_username(username)
                else:
                    self.print_message(f"Unavailable: {username}", "info")
                
                # Update stats every 20 checks
                if self.total_checked % 20 == 0:
                    self.show_stats()
                
                time.sleep(self.delay)
                
        except KeyboardInterrupt:
            elapsed = time.time() - self.start_time
            print(f"\n{Fore.YELLOW + Style.BRIGHT}Session Summary:")
            print(f"{Fore.YELLOW}• Total checked: {self.total_checked}")
            print(f"{Fore.YELLOW}• Valid names found: {self.valid_count}")
            print(f"{Fore.YELLOW}• Unknown errors: {self.unknown_count}")
            print(f"{Fore.YELLOW}• Total time: {elapsed:.1f} seconds")
            print(f"{Fore.CYAN + Style.BRIGHT}\nThank you for using Roblox Username Checker Pro!")
            print(f"{Fore.CYAN}Valid usernames saved to: {self.output_file}")

def clear_screen():
    """Clears the console screen"""
    print("\033c", end="")

def validate_input(prompt, default, value_type):
    """Validates and converts user input"""
    while True:
        try:
            user_input = input(prompt)
            if not user_input:
                return default
            return value_type(user_input)
        except ValueError:
            print(f"{Fore.RED}Invalid input! Using default: {default}")

def main():
    clear_screen()
    checker = RobloxUsernameChecker()
    
    print(f"{Fore.CYAN + Style.BRIGHT}⚙ Settings")
    try:
        checker.username_length = validate_input(
            f"{Fore.WHITE}Username length [default: {checker.username_length}]: ",
            checker.username_length,
            int
        )
        
        checker.delay = validate_input(
            f"{Fore.WHITE}Delay between checks [default: {checker.delay}s]: ",
            checker.delay,
            float
        )
        
        use_special = input(f"{Fore.WHITE}Enable underscore (_) [Y/n]: ").lower()
        checker.use_special_chars = use_special not in ('n', 'no')
        
        use_numbers = input(f"{Fore.WHITE}Include numbers [Y/n]: ").lower()
        checker.use_numbers = use_numbers not in ('n', 'no')
        
        custom_file = input(f"{Fore.WHITE}Custom output file [default: {checker.output_file}]: ").strip()
        if custom_file:
            checker.output_file = custom_file
        
        checker.update_allowed_chars()
        
        clear_screen()
        print(f"{Fore.GREEN + Style.BRIGHT}Starting checker...")
        checker.run()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation canceled by user")

if __name__ == "__main__":
    main()
