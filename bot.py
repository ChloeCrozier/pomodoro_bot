import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

BOT_TOKEN = os.getenv("POMO_DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Timer modes
TIMER_MODES = {
    "work": 1 * 60,  # 25 minutes
    "short_break": 5 * 60,  # 5 minutes
    "long_break": 15 * 60  # 15 minutes
}

class StudySession:
    def __init__(self):
        self.participants = set()
        self.current_mode = "work"
        self.timer_task = None
        self.session_active = False
        self.session_message = None

    async def start_timer(self, ctx, mode_duration):
        self.session_active = True
        minutes = mode_duration // 60
        await ctx.send(f"Starting {self.current_mode.replace('_', ' ')} for {minutes} minutes!")

        try:
            for remaining in range(mode_duration, 0, -1):
                if not self.session_active:
                    break
                await asyncio.sleep(1)
            if self.session_active:
                await ctx.send(f"Time's up! {self.current_mode.replace('_', ' ')} completed.")
        except asyncio.CancelledError:
            await ctx.send("Timer was paused or cancelled.")

study_session = StudySession()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def start_session(ctx):
    if study_session.session_active:
        await ctx.send("A session is already active.")
        return

    study_session.participants.add(ctx.author)
    study_session.current_mode = "work"

    # Send session start message and allow reactions
    study_session.session_message = await ctx.send(
        f"Study session started by {ctx.author.mention}! React to join.")

    await study_session.session_message.add_reaction("✅")  # Checkmark reaction

    # Start timer for work period
    study_session.timer_task = bot.loop.create_task(study_session.start_timer(ctx, TIMER_MODES[study_session.current_mode]))

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot or reaction.message != study_session.session_message:
        return

    if reaction.emoji == "✅":  # Checkmark emoji
        study_session.participants.add(user)
        await reaction.message.channel.send(f"{user.mention} joined the session!")

@bot.command()
async def end_session(ctx):
    if not study_session.session_active:
        await ctx.send("No active session to end.")
        return

    study_session.session_active = False
    study_session.participants.clear()
    if study_session.timer_task:
        study_session.timer_task.cancel()
        study_session.timer_task = None
    await ctx.send("Session ended and metrics reset.")

@bot.command()
async def pause(ctx):
    if not study_session.session_active:
        await ctx.send("No active session to pause.")
        return

    study_session.session_active = False
    if study_session.timer_task:
        study_session.timer_task.cancel()
        study_session.timer_task = None
    await ctx.send("Session paused.")

@bot.command()
async def unpause(ctx):
    if study_session.session_active:
        await ctx.send("Session is already active.")
        return

    study_session.session_active = True
    await ctx.send(f"Resuming {study_session.current_mode.replace('_', ' ')}.")
    study_session.timer_task = bot.loop.create_task(study_session.start_timer(ctx, TIMER_MODES[study_session.current_mode]))

@bot.command()
async def set_time(ctx, mode: str, minutes: int):
    if mode not in TIMER_MODES:
        await ctx.send("Invalid mode. Choose from work, short_break, or long_break.")
        return

    TIMER_MODES[mode] = minutes * 60
    await ctx.send(f"{mode.replace('_', ' ').title()} duration set to {minutes} minutes.")

@bot.command()
async def reset(ctx):
    if not study_session.session_active:
        await ctx.send("No active session to reset.")
        return

    study_session.timer_task.cancel()
    await ctx.send("Timer reset. Starting current mode duration again.")
    study_session.timer_task = bot.loop.create_task(study_session.start_timer(ctx, TIMER_MODES[study_session.current_mode]))

if BOT_TOKEN:
    bot.run(BOT_TOKEN)
else:
    print("Error: Bot token not found. Please check your .env file.")