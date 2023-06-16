# Author: cation1
import discord
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
                       \n!list_server - list servers and their status \n!start_server (server name) - starts server \
                       \n!stop_server (server name)- stops server")
    
    # list servers 
    @bot.command()
    async def list_server(ctx):
        # use boto3 to describe all ec2 instances with the tag discord_bot
        ec2_list = ec2.describe_instances(Filters=ec2_tag_filter)
        #response
        response = "Type | Name | Password | IP | State \n"
        for reservation in ec2_list.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                # dictionary comprehention of tags
                Tags = {tag.get("Key"): tag.get("Value") for tag in instance.get("Tags", [])}
                # check instance termination
                if instance.get("State", {}).get('Name') != "terminated":
                    response += "{0} | {1} | {2} | {3}:{4} | {5} | {6}\n".format(Tags.get("Name"),
                                                                       Tags.get("server_name"),
                                                                       Tags.get("password"),
                                                                       instance.get("PublicIpAddress", {}),
                                                                       Tags.get("port"),
                                                                       instance.get("State", {}).get("Name"), 
                                                                       instance.get("Status", {}).get("Name"))
        print("Listing servers...")
        await ctx.send(response)

    # start server ( given server name )
    @bot.command()
    async def start_server(ctx, server_name=None):
        # restart filter
        start_server_filter = []
        start_server_filter += ec2_tag_filter
        # check input
        if server_name:
            # filter down to ec2 state
            start_server_filter.append({"Name":"tag:server_name", "Values":[server_name]})
            ec2_list = ec2.describe_instances(Filters=start_server_filter)
            for reservation in ec2_list.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    ec2_state = instance.get("State", {}).get("Name")
                    # ec2 state cases
                    match ec2_state:
                        case "running":
                            response = f"{server_name} is already running."
                        case "stopping":
                            response = f"{server_name} is shutting down."
                        case "rebooting":
                            response = f"{server_name} is rebooting"
                        case "stopped":
                            ec2.start_instances(InstanceIds=[instance.get('InstanceId')])
                            response = f"{server_name} is off, please wait for a few minutes for it to start."
                            print("Starting a server")
            
        else:
            print("Invalid input")
            response = "Please specify a server name. (Ex: `!start_server minecraft`) \
                           \nType `!list_server` to list available servers"
        await ctx.send(response)
    
    # stop server ( given server name )
    @bot.command()
    async def stop_server(ctx, server_name=None):
        # restart filter
        stop_server_filter = []
        stop_server_filter += ec2_tag_filter
        # check input
        if server_name:
            # filter down to ec2 state
            stop_server_filter.append({"Name":"tag:server_name", "Values":[server_name]})
            ec2_list = ec2.describe_instances(Filters=stop_server_filter)
            for reservation in ec2_list.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    ec2_state = instance.get("State", {}).get("Name")
                    # ec2 state cases
                    match ec2_state:
                        case "running":
                            response = f"{server_name} is shutting down."
                            ec2.stop_instances(InstanceIds=[instance.get('InstanceId')])
                            print("stoppping a server")
                        case "stopping":
                            response = f"{server_name} is already shutting down."
                        case "rebooting":
                            response = f"{server_name} is rebooting"
                        case "stopped":
                            response = f"{server_name} is already off"
            
        else:
            print("Invalid input")
            response = "Please specify a server name. (Ex: `!stop_server minecraft`) \
                           \nType `!list_server` to list available servers"
        await ctx.send(response)
    

    # on start up
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    bot.run(TOKEN)
