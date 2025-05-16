# Discord Bot with Economy and Games

A feature-rich Discord bot that implements an economy system and various casino-style games. This bot was developed as a personal project to demonstrate Python programming skills and Discord bot development.

## Features

### Economy System
- Virtual currency system with balance tracking
- SQLite database for persistent storage
- Starting balance of 1000 credits for new users
- Balance checking and management commands

### Games
1. **Blackjack**
   - Classic casino blackjack implementation
   - Betting system with credit management
   - Interactive gameplay with hit/stand options

2. **Coin Flip (Yazı/Tura)**
   - Simple coin flip game
   - Betting system
   - Support for both Turkish and English commands

### Administrative Features
- Admin commands for currency management
- Custom response triggers for specific users

## Commands

### Economy Commands
- `!startmoney` or `!sm` - Get starting balance (1000 credits)
- `!balance` or `!bal` - Check your current balance
- `!givemoney` or `!gm` - [Admin] Give credits to a user

### Game Commands
- `!blackjack <amount>` or `!bj <amount>` - Play blackjack with specified bet
- `!yazitura <amount> <choice>` or `!cf <amount> <choice>` - Play coin flip
  - Choices: "Yazı" or "Tura"

## Setup

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install discord.py
   ```
3. Create a Discord bot and get your bot token from the [Discord Developer Portal](https://discord.com/developers/applications)
4. Replace `BOT_TOKEN` in `main.py` with your bot token
5. Run the bot:
   ```bash
   python main.py
   ```

## Technical Details

- Built with Python 3.x
- Uses discord.py library
- SQLite database for data persistence
- Implements Discord's slash commands and traditional prefix commands

## Database Structure

The bot uses a SQLite database (`economy.db`) with the following structure:
- Table: `players`
  - `user_id` (INTEGER PRIMARY KEY)
  - `balance` (INTEGER)

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Author

[Your Name] - Developer 