from mandrake.config import Config
import mandrake.bot

def run(configFile):
    mandrake.bot.run(Config.from_file(configFile))