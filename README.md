# AWS Discord integration
This bot will allow you to start a Minecraft server given a custom AMI that will start a minecraft server on port 25565 (can be changed in terraform).

## Requirnments 
1. AWS CLI installed with configured access to AWS for terraform and boto3
2. A machine to run the discord bot (I am using a raspberry pi)
3. Python

### Notes
I only intended this for my own use so if you want to use this, you will have to change a few things:

- Not only are AMIs region locked but the AMI I have will be deleted after I am done with this project. You will need to create your own AMI with a Minecraft server and openJDK intalled. You'll want to create a system service that will auto start the server every time the instance starts.
  
- When you create an AMI, on the EBS, you should turn off delete on termination. That way when terraform destory is run it will not destroy your game files.
  
- You will need to create your own AWS key pair to ssh into the instance and update the key_name attribute in main.tf.
  
- Setup a [discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) and set its token to an environment variable called "DISCORD_TOKEN"


### Possible up coming changes and updates
- Could futher expand on Terraform or use Ansible to create an AMI that will set up, download and automate everything for you.
- A way to automatically create and send a key pair to access the server

### Licence
MIT License
