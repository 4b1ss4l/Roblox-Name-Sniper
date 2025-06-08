# 🇧🇷
# Roblox Username Sniper🎯

A powerful Python script to find available Roblox usernames with customizable settings and robust error handling.

## Features

- **Customizable username generation**:
  - Set username length (default: 4 characters)
  - Toggle number inclusion (0-9)
  - Toggle underscore (_) special character
  - Adjust delay between checks

- **Intelligent checking**:
  - Follows Roblox username rules
  - Avoids consecutive underscores
  - Ensures proper starting/ending characters
  - Prevents duplicate checks

- **Robust error handling**:
  - Automatic retry mechanism
  - Rate limit detection
  - Progressive delay for consecutive errors
  - Server error recovery

- **Statistics tracking**:
  - Total checks performed
  - Valid names found
  - Unknown errors encountered
  - Checks per second

- **Output**:
  - Colored console output
  - Saves valid usernames to text file
  - Real-time statistics display

## Requirements

- Python 3.6+
- Required packages:
  - `requests`
  - `colorama`

Install dependencies with:
```bash
pip install requests colorama
```

## Usage

1. Run the script:
```bash
python roblox.py
```

2. Configure settings when prompted:
   - Username length
   - Delay between checks
   - Special character (_) usage
   - Number inclusion
   - Custom output filename

3. The script will:
   - Generate valid usernames
   - Check availability against Roblox
   - Save available usernames to file
   - Display real-time statistics

4. Press `Ctrl+C` to stop execution and view summary.

## Configuration

All settings can be configured at runtime:
- `username_length`: Length of usernames to generate
- `delay`: Seconds between API requests
- `use_special_chars`: Enable/disable underscore
- `use_numbers`: Enable/disable numbers
- `output_file`: File to save valid usernames

## Output

Valid usernames are saved to `valid_usernames.txt` by default (configurable).

Sample output:
```
Available: xkay
Unavailable: user1
Censored: badword
```

## Error Handling

The script handles:
- Rate limiting (automatic wait)
- Server errors (retry mechanism)
- Network issues (retry with delay)
- Unknown responses (tracking and reporting)

## Performance

The script maintains optimal performance while respecting Roblox's API limits:
- Adjustable delay prevents rate limiting
- Progressive backoff for errors
- Recent username tracking prevents duplicates

## License

This project is open source. Feel free to modify and distribute.

## Disclaimer

This script is for educational purposes only. Use responsibly and respect Roblox's Terms of Service.
