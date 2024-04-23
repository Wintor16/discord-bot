import discord
from discord import app_commands
from discord.ext import commands
import random
import sqlite3

# Constants
DECK = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
BOT_TOKEN = 'MTIzMTY1MzMyNTg1MDY3MzI0Mg.GtpjaA.Ko6S5hb83UEWKWiMgfnWpyUGO8CtqltOwV6Zww'

# SQLite database file name
DB_FILE = 'economy.db'
# Starting balance for new players
START_MONEY = 1000
# Initialize Discord client with commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    try:
        synced=await bot.tree.sync()
        print(f"synced{len(synced)}command(s)")
    except Exception as e:
        print(e)
# Helper function to calculate the total value of a hand
def calculate_hand_value(hand):
    total_value = sum(hand)
    if total_value > 21 and 11 in hand:
        total_value -= 10
    return total_value

# Helper function to deal a new hand
def deal_hand():
    random.shuffle(DECK)
    return [DECK.pop(), DECK.pop()]

# Helper function to create the SQLite table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players
                      (user_id INTEGER PRIMARY KEY, balance INTEGER)''')
    conn.commit()
    conn.close()
38
# Helper function to get a player's balance from the database
def get_balance(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM players WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        return None

# Helper function to update a player's balance in the database
def update_balance(user_id, new_balance):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO players (user_id, balance) VALUES (?, ?)", (user_id, new_balance))
    conn.commit()
    conn.close()

# Main Blackjack game logic
class BlackjackGame:
    def __init__(self, player, bet_amount):
        self.player = player
        self.bet_amount = bet_amount
        self.player_hand = deal_hand()
        self.dealer_hand = deal_hand()
    def hit(self):
        self.player_hand.append(DECK.pop())
    def stand(self):
        while calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(DECK.pop())
    def get_player_hand_value(self):
        return calculate_hand_value(self.player_hand)
    def get_dealer_hand_value(self):
        return calculate_hand_value(self.dealer_hand)

@bot.event
async def on_message(message):
    if message.author.name == "wintor16" and "kurumi galp" in message.content.lower():
        await message.channel.send("wintor galp <3")
    if message.author.name== "wintor16" and "miyav" in message.content.lower():
        await message.channel.send("*~headpats*")

    # Eğer mesaj, komutlarla alakalıysa diğer eventlerin işlenmesi için bu satırı ekleyin.
    await bot.process_commands(message)
# Command to start a new Blackjack game
@bot.command(name="blackjack", aliases=['bj'])
async def blackjack(ctx, bet_amount: int):
    create_table()
    user_id = ctx.author.id
    balance = get_balance(user_id)

    if balance is None or balance <= 0:
        await ctx.send(f'{ctx.author.mention}, oynayacak kadar bakiyen yok')
        return
    if bet_amount <= 0:
        await ctx.send('geçersiz sayı lütfen pozitif bir sayı gir')
        return
    if bet_amount > balance:
        await ctx.send('yeteri kadar bakiyen yok')
        return
    game = BlackjackGame(ctx.author.mention, bet_amount)
    await ctx.send(f'{game.player}, elin: {game.player_hand}')

    while game.get_player_hand_value() < 21:
        await ctx.send(f'{game.player}, kalmakmı çekmek mi istiyorsun (`hit` yada `stand` yaz)')
        def check(m):
            return m.author == ctx.author and m.content.lower() in ['hit', 'stand']
        try:
            reply = await bot.wait_for('message', check=check, timeout=60)
        except TimeoutError:
            await ctx.send('çok fazla bekledin. oyun sonlandı')
            return

        if reply.content.lower() == 'hit':
            game.hit()
            await ctx.send(f'{game.player}, elin: {game.player_hand}')
        else:
            break
    game.stand()
    
    await ctx.send(f'kumarbaz onurun eli: {game.dealer_hand}')
    player_value = game.get_player_hand_value()
    dealer_value = game.get_dealer_hand_value()
    if player_value > 21:
        await ctx.send(f'patladın {game.bet_amount} kredi kaybettin.')
        balance -= game.bet_amount
    elif dealer_value > 21 or player_value > dealer_value:
        await ctx.send(f'tebrikler!!!! {game.bet_amount} kredi kazandın!')
        balance += game.bet_amount
    elif dealer_value == player_value:
        await ctx.send('berabere paranı geri aldın.')
    else:
        await ctx.send(f'kumarbaz onur kazandı {game.bet_amount} kredi kaybettin.')
        balance -= game.bet_amount
    # Ensure the balance doesn't go below 0
    if balance < 0:
        balance = 0
    update_balance(user_id, balance)
    await ctx.send(f'bakiyen: {balance} kredi.')

# Command to start money for first-time users
@bot.command(name='startmoney',aliases=['sm'])
async def start_money(ctx):
    create_table()
    user_id = ctx.author.id
    balance = get_balance(user_id)
    if balance is not None:
        await ctx.send(f'{ctx.author.mention}, bu komudu kullanamazsın zaten paran var')
        return
    update_balance(user_id, START_MONEY)
    await ctx.send(f'{ctx.author.mention}, başlangıç paran: {START_MONEY} kredi.')

# Command to check my balance
@bot.command(name='balance',aliases=['bal'])
async def my_balance(ctx):
    create_table()
    user_id = ctx.author.id
    balance = get_balance(user_id)
    if balance is None:
        balance = START_MONEY
        update_balance(user_id, balance)
    await ctx.send(f'{ctx.author.mention}, şuanki bakiyen: {balance} kredi.')

# Command to give currency to a selected user
@bot.command(name='givemoney' or 'gm')
@commands.has_permissions(administrator=True)
async def give_currency(ctx, user: discord.Member, amount: int):
    create_table()

    if amount <= 0:
        await ctx.send('hatalı giriş lütfen pozitif bir sayı gir.')
        return

    balance = get_balance(user.id)
    if balance is None:
        balance = 0

    balance += amount
    update_balance(user.id, balance)

    await ctx.send(f'{user.mention} kullanıcısına {ctx.author.mention} tarafından {amount} kadar kredi verildi . {user.mention} yeni bakiyen: {balance} kredi.')

@bot.command(name='yazitura', aliases=['yazıtura', 'coinflip', 'cf'])
async def coin_flip(ctx, bet_amount: int, *, choice: str = 'Yazı'):
    create_table()

    user_id = ctx.author.id
    balance = get_balance(user_id)

    if balance is None or balance <= 0:
        await ctx.send(f'{ctx.author.mention}, oynayacak kadar bakiyen yok')
        return

    if bet_amount <= 0:
        await ctx.send('geçersiz sayı lütfen pozitif bir sayı gir')
        return

    if bet_amount > balance:
        await ctx.send('yeteri kadar bakiyen yok')
        return

    choices = ['yazı', 'tura']
    choice = choice.lower()  # Make the choice lowercase

    if choice not in choices:
        await ctx.send('hatalı seçim lütfen "Yazı" veya "Tura" yaz.')
        return

    result = random.choice(choices)

    await ctx.send(f'{ctx.author.mention} Yazı Tura: **{result.capitalize()}**')

    if result == choice:
        await ctx.send(f'Tebrikler, kazandınız! {bet_amount} kredi kazandınız.')
        balance += bet_amount
    else:
        await ctx.send(f'Üzgünüm, kaybettiniz! {bet_amount} kredi kaybettiniz.')
        balance -= bet_amount

    update_balance(user_id, balance)

    await ctx.send(f'bakiyeniz: {balance} kredi.')
   

# Remove the default help command to avoid conflict with slash command help
bot.remove_command('help')

# Run the Discord bot
bot.run(BOT_TOKEN)