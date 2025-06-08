# the fastest 
import asyncio
import aiohttp
import random
import string
from datetime import datetime

# Configuration
NAMES = 10
LENGTH = 5
FILE = 'valid.txt'
BIRTHDAY = '1999-04-20'
CONCURRENCY = 50  # Number of concurrent requests
REQUEST_TIMEOUT = 5
DELAY = 0  # Can be 0 with async!

# Color formatting
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    GRAY = '\033[90m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

found = 0
lock = asyncio.Lock()

def generate_username():
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=LENGTH))

async def check_username(session, username):
    global found
    url = f'https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday={BIRTHDAY}'
    
    try:
        async with session.get(url, timeout=REQUEST_TIMEOUT) as response:
            if response.status == 200:
                data = await response.json()
                code = data.get('code')
                
                if code == 0:
                    async with lock:
                        if found < NAMES:
                            found += 1
                            print(f"{bcolors.OKBLUE}[{found}/{NAMES}] [+] Found Username: {username}{bcolors.ENDC}")
                            with open(FILE, 'a') as f:
                                f.write(f"{username}\n")
                            return True
                else:
                    print(f'{bcolors.FAIL}[-] {username} is taken{bcolors.ENDC}')
    except Exception as e:
        print(f'{bcolors.WARNING}[!] Error checking {username}: {str(e)}{bcolors.ENDC}')
    return False

async def worker(session, queue):
    while found < NAMES:
        username = generate_username()
        await queue.put(username)
        await check_username(session, username)
        await asyncio.sleep(DELAY)

async def main():
    print(f"{bcolors.HEADER}=== Async Roblox Username Checker ==={bcolors.ENDC}")
    print(f"{bcolors.BOLD}Finding {NAMES} valid {LENGTH}-character usernames{bcolors.ENDC}")
    print(f"Concurrent requests: {CONCURRENCY}\n")
    
    # Clear output file
    open(FILE, 'w').close()
    
    connector = aiohttp.TCPConnector(limit=CONCURRENCY)
    async with aiohttp.ClientSession(connector=connector) as session:
        queue = asyncio.Queue()
        workers = [asyncio.create_task(worker(session, queue)) for _ in range(CONCURRENCY)]
        
        try:
            await asyncio.gather(*workers)
        except asyncio.CancelledError:
            print(f"{bcolors.WARNING}\n[!] Cancelling tasks...{bcolors.ENDC}")
        finally:
            for task in workers:
                task.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
            
    print(f"{bcolors.OKBLUE}[!] Finished - Found {found} valid usernames{bcolors.ENDC}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{bcolors.FAIL}\n[!] Script interrupted{bcolors.ENDC}")
