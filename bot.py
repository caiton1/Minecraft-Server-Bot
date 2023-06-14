import discord
import responses
import os
from discord.ext import commands

async def send_messages(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents().default()
    intents.message_content = True
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
    

    @bot.command()
    async def help(ctx):
        await ctx.send("'skill issue'")
    
    @bot.command()
    async def list_server(ctx):
        await ctx.send("no")

    @bot.command()
    async def start_server(ctx, server_name=None):
        await ctx.send("none")

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
    ''''
    @bot.event
    async def on_message(message):
        if message.author == bot.use
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_messages(message, user_message, is_private=True)
        else:
            await send_messages(message, user_message, is_private=False)

    '''

    bot.run(TOKEN)