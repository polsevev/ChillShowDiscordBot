import discord
import os
from discord.ext import commands



client = discord.Client()

GUILD = os.getenv('Rolf\'s bot testing')
guildID = 0
bot = commands.Bot(command_prefix='$')


roleChannelID = 824001207436836875
channelGuild = 823983756993888277
emojis = ["\U0001F49C", "\U0001F49A", "\U0001F5A4","\U0001FAD0","\U0001F499", "\U0001F338", "\U0001F90D", "\U0001F7EA", "\U0001F7E9", "\U0001F49B"]
roleNames = ["Purple", "Green", "Black", "Blue", "Cyan", "Pink", "White", "Dark Purple", "Light Green", "Yellow"]
roleId = []

changeRoleMessageBrief = "Change the message of the setRole channel"
changeRoleMessageFull = "Change the message of setRole by typing the new message inside \" \" after the command"

pingBrief = "Ping the bot"
pingFull = "Ping the bot and it will respond with pong if online"

announceBrief = "Will create an anouncement in the anouncement channel"
announceFull = "Will make an announcement with them essage inside \"MESSAGE HERE\" after the command"

standardRoleMessage = ""



@bot.command(brief = changeRoleMessageBrief, description=changeRoleMessageFull)
@commands.has_permissions(administrator=True)
async def resetRoleMessage(ctx):
    roleChannel = bot.get_channel(roleChannelID)
    messages = await roleChannel.history(limit=10).flatten()
    for message in messages:
        await message.delete()
    message = await roleChannel.send(standardRoleMessage)
    for emoji in emojis:
        await message.add_reaction(emoji)



@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def say(ctx, arg):
    await ctx.send(arg)


@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    print(ctx.message.author)
    await ctx.send("pong")

@bot.command()
@commands.has_permissions(administrator=True)
async def addRoleMessage(ctx, arg):
    roleChannel = bot.get_channel(roleChannelID)
    message = await roleChannel.send(arg)
    for emoji in emojis:
        await message.add_reaction(emoji)

@bot.event
async def on_ready():
    roleChannel = bot.get_channel(roleChannelID)
    messages = await roleChannel.history(limit=10).flatten()

    for x in roleNames:
        role = discord.utils.find(lambda r : r.name == x, bot.get_guild(channelGuild).roles)
        roleId.append(role.id)

    global standardRoleMessage
    standardRoleMessage = (
            f"To choose color, please react with the following emoji for the specified color: \n"
            f":purple_heart:  = <@&{roleId[0]}>\n"
            f":green_heart:  = <@&{roleId[1]}>\n"
            f":black_heart:  = <@&{roleId[2]}>\n"
            f":blueberries:  = <@&{roleId[3]}>\n"
            f":blue_heart:  = <@&{roleId[4]}>\n"
            f":cherry_blossom:  = <@&{roleId[5]}>\n"
            f":white_heart:  = <@&{roleId[6]}>\n"
            f":purple_square:  = <@&{roleId[7]}>\n"
            f":green_square:  = <@&{roleId[8]}>\n"
            f":yellow_heart:  = <@&{roleId[9]}>\n"
        )
    if (len(messages) < 1):
        message = await roleChannel.send(standardRoleMessage)
        for emoji in emojis:
            await message.add_reaction(emoji)
    print("Bot is ready")

@bot.command(brief=announceBrief, description=announceFull)
@commands.has_permissions(administrator=True)
async def announce(ctx, arg1):
    anounceChannel = bot.get_channel(823988506158170125)
    await anounceChannel.send(arg1)



@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == roleChannelID:
        guild = bot.get_guild(payload.guild_id)
        member = payload.member
        for x in range(0, len(emojis)):
            if(str(payload.emoji)) == emojis[x]:
                print("It was true")
                role = guild.get_role(roleId[x])
                await member.add_roles(role)
    print(payload.user_id)
    print(str(payload.emoji))

@bot.event
async def on_raw_reaction_remove(payload):
    if(payload.channel_id == roleChannelID):
        guild = bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        for x in range(0, len(emojis)):
            if(str(payload.emoji)) == emojis[x]:
                print("It was true")
                role = role = guild.get_role(roleId[x])
                await member.remove_roles(role)
                print("role removed")



bot.run("")

