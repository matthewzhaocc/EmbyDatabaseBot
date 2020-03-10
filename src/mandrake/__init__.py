"""gets the bot and runs it"""
from mandrake.config import Config
import mandrake.bot

def run(config_file):
    """starts the bot from config file"""
    mandrake.bot.run(Config.from_file(config_file))
