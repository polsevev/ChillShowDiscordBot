import discord
import os
from discord.ext import commands


client = discord.Client()

GUILD = os.getenv('Rolf\'s bot testing')
guildID = 0
bot = commands.Bot(command_prefix='$')


roleChannelID = 824001207436836875
emojis = ["😀", "😃"]

changeRoleMessageBrief = "Change the message of the setRole channel"
changeRoleMessageFull = "Change the message of setRole by typing the new message inside \" \" after the command"

pingBrief = "Ping the bot"
pingFull = "Ping the bot and it will respond with pong if online"

announceBrief = "Will create an anouncement in the anouncement channel"
announceFull = "Will make an announcement with them essage inside \"MESSAGE HERE\" after the command"




@bot.command(brief = changeRoleMessageBrief, description=changeRoleMessageFull)
async def changeRoleMessage(ctx, arg):
    channel = bot.get_channel(roleChannelID)
    await channel.purge(limit=int(100))
    message = await channel.send(arg)
    for emoji in emojis:
        await message.add_reaction(emoji)



@bot.command()
async def ping(ctx):
    print(ctx.message.author)
    await ctx.send("pong")

@bot.event
async def on_ready():
    roleChannel = bot.get_channel(roleChannelID)
    messages = await roleChannel.history(limit=10).flatten()
    if (len(messages) < 1):
        message = await roleChannel.send("React with 😀 To be added to Role1, React with 😃 to be added to Role2")
        for emoji in emojis:
            await message.add_reaction(emoji)
    print("Bot is ready")



@bot.command(brief=announceBrief, description=announceFull)
async def announce(ctx, arg1):
    anounceChannel = bot.get_channel(823988506158170125)
    await anounceChannel.send(arg1)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == roleChannelID:
        guild = bot.get_guild(payload.guild_id)
        member = payload.member
        if str(payload.emoji) == "😀":
            role = discord.utils.find(lambda r : r.name == "Role1", guild.roles)
            await member.add_roles(role)
        elif str(payload.emoji) == "😃":
            role = discord.utils.find(lambda r: r.name == "Role2", guild.roles)
            await member.add_roles(role)
        else:
            print("Smack")
    print(payload.user_id)
    print(str(payload.emoji))

@bot.event
async def on_raw_reaction_remove(payload):
    if(payload.channel_id == roleChannelID):
        guild = bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        if str(payload.emoji) == "😀":
            role = discord.utils.find(lambda r : r.name == "Role1", guild.roles)
            if(role == "error"):
                print("Couldn't find role")
            else:
                await member.remove_roles(role)
        elif str(payload.emoji) == "😃":
            role = discord.utils.find(lambda r: r.name == "Role2", guild.roles)
            if (role == "error"):
                print("Couldn't find role")
            else:
                await member.remove_roles(role)
        else:
            print("Smack")
    print(payload.user_id)
    print(str(payload.emoji))


bot.run("ODIzOTgyODY2NTkzMzQ5NzI0.YFov2A.YXez7kDPcE9bdQ5Em840Ny08qqw")
