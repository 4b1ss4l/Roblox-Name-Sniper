# Roblox Username Sniper 🎯

A Python script to check the availability of Roblox usernames.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- Generates random usernames with configurable length (default: 5 characters)
- Checks username availability against Roblox's API
- Option to include/exclude numbers in usernames
- Retry mechanism for failed API requests
- Real-time statistics display
- Saves valid usernames to `valid.txt`
- Configurable delay between requests

## Requirements

- Python 3.7+
- `requests` library
- `colorama` library

## Installation

1. Clone this repository or download the script
2. Install the required dependencies:
   ```bash
   pip install requests colorama
   ```

## Configuration

Edit the `CONFIG` dictionary at the top of the script to customize:

```python
CONFIG = {
    "USERNAME_LENGTH": 4,          # Length of usernames to generate
    "DELAY": 0.0,                  # Delay between checks (in seconds)
    "MAX_API_RETRIES": 5,          # Maximum retry attempts for failed API calls
    "RETRY_DELAY": 2,              # Delay between retry attempts (in seconds)
    "API_TIMEOUT": 10,             # API request timeout (in seconds)
    "INCLUDE_NUMBERS": True        # Whether to include numbers in usernames
}
```

## Usage

Run the script:
```bash
python roblox.py
```

The script will:
1. Generate random usernames
2. Check their availability
3. Display results in real-time (green for available, gray for taken)
4. Save available usernames to `valid.txt`

Press `Ctrl+C` to stop the script and see final statistics.

## Output

- `VALID: username` - Username is available (saved to valid.txt)
- `INVALID: username` - Username is taken
- `FAILED: username` - API request failed after retries
- `CENSURED: username` - The username generated violates Roblox policies
- Statistics shown every 50 checks

## Notes

- Use responsibly and respect Roblox's terms of service
- Excessive requests may lead to IP rate limiting
- The script includes delays and retries to be more reliable

## License

MIT License - Feel free to modify and distribute.
