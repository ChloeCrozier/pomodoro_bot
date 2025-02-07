import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
import random
import os

load_dotenv()

BOT_TOKEN = os.getenv("POMO_DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("Ahoy! I am Buddy Bot!")

if BOT_TOKEN:
    bot.run(BOT_TOKEN)
else:
    print("Error: Bot token not found. Please check your .env file.")
