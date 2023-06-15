import discord
import responses
import os
from discord.ext import commands
import boto3

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
    ec2 = boto3.client('ec2', region_name="us-west-1")
    # filter used to list only servers related to discord bot
    ec2_tag_filter = [{"Name":"tag:discord_bot", "Values":["True"]}]

    # help
    @bot.command()
    async def help(ctx):
        await ctx.send("List of commands: \n!help - gives list of commands \
                       \n!list_server - list servers and their status \n!start_server - starts server")
    
    # list servers 
    @bot.command()
    async def list_server(ctx):
        # use boto3 to describe all ec2 instances with the tag discord_bot
        ec2_list = ec2.describe_instances(Filters=ec2_tag_filter)
        #response
        response = "Type | Name | Password | IP | State\n"
        for reservation in ec2_list.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                # dictionary comprehention of tags
                Tags = {tag.get("Key"): tag.get("Value") for tag in instance.get("Tags", [])}
                # check instance termination
                if instance.get("State", {}).get('Name') != "terminated":
                    response += "{0} | {1} | {2} | {3}:{4} | {5}\n".format(Tags.get("Name"),
                                                                       Tags.get("server_name"),
                                                                       Tags.get("password"),
                                                                       instance.get("PublicIpAddress", {}),
                                                                       Tags.get("port"),
                                                                       instance.get("State", {}).get("Name"))
        print("Listing servers...")
        await ctx.send(response)

    # start server ( given server name )
    @bot.command()
    async def start_server(ctx, server_name=None):
        if server_name == None :
            await ctx.send("Please specify a server name. (Ex: `start_server minecraft`) \
                           \nType `list_server` to list available servers")
        else:
            await ctx.send(str(server_name))
        # use boto3 to start the specified instance, will need check for correct name
        

    # on start up
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    bot.run(TOKEN)