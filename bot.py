#!/usr/bin/env python3

import json
import random

from twitchio.ext import commands


with open('botConfig.json') as json_file:
    botConfig = json.load(json_file)


#env
irc_token=botConfig['irc_token']
client_id=botConfig['client_id']
nick=botConfig['nick']
prefix=botConfig['prefix']
initial_channels=botConfig['initial_channels']
token=botConfig['token']

commandCooldown = 30
commandCooldownRate = 4

bot = commands.Bot(
    irc_token=irc_token,
    client_id=client_id,
    nick=nick,
    prefix=prefix,
    initial_channels=initial_channels,
    token=token
)


@bot.command(name='ping')
@commands.cooldown(commandCooldownRate,commandCooldown,commands.Bucket.user)
async def ping(ctx):
    message = "Pong"
    print(f'Message: {message}')
    await ctx.send(message)

@bot.command(name='help')
async def help(ctx):
    print(f'{ctx.author.name} used "{prefix}help" in {ctx.message.channel}')
    Arn = '@KeBaBeeeN'
    X3l = '@iamx___'
    message = f'Contact us at {Arn} / {X3l}'
    print(f'Message: {message}')
    await ctx.send(message)

@bot.command(name='penis')
async def penis(ctx):
    size = random.randint(3,20)
    print(f'{ctx.author.name} used "{prefix}help" in {ctx.message.channel}')
    message = f'{ctx.author.name}, your schlong is {size}cm long.'
    print(f'Message: {message}')
    await ctx.send(message)

if __name__ == "__main__":
    print("Starting bot now")
    bot.run()