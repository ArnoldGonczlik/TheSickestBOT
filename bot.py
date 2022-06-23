#!/usr/bin/env python3

import json
import time
from datetime import timedelta

from twitchio.ext import commands, routines
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


with open('botConfig.json') as json_file:
    botConfig = json.load(json_file)


#env
irc_token=botConfig['irc_token']
client_id=botConfig['client_id']
nick=botConfig['nick']
prefix=botConfig['prefix']
initial_channels=botConfig['initial_channels']
token=botConfig['token']

traderTuples = []
startTime = time.time()

bot = commands.Bot(
    irc_token=irc_token,
    client_id=client_id,
    nick=nick,
    prefix=prefix,
    initial_channels=initial_channels,
    token=token
)


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send("Pong")


@routines.routine(minutes=5)
async def getValues():
    global traderTuples
    traderTuples = getTupleListOfTrader()
    global startTime
    startTime = time.time()


@bot.command(name='traders')
async def traders(ctx, trader=None):
    print(f'{ctx.author.name} used "{prefix}traders {trader}" in {ctx.message.channel}')
    global traderTuples
    if not traderTuples:
        traderTuples = getTupleListOfTrader()
    if trader:
        for item in traderTuples:
            if item[0] == trader.lower():
                traderName = item[0].capitalize()
                traderTimer = traderTimeReCalculate(item[1])
                await ctx.send(f'{traderName}: {traderTimer}')
    else:
        for item in traderTuples:
            traderName = item[0].capitalize()
            traderTimer = traderTimeReCalculate(item[1])
            await ctx.send(f'{traderName}: {traderTimer}')


@bot.command(name='keycards')
async def keycards(ctx):
    print(f'{ctx.author.name} used "{prefix}keycards" in {ctx.message.channel}')
    global traderTuples
    if not traderTuples:
        traderTuples = getTupleListOfTrader()

    keycardTraderList = [x for x in traderTuples if x[0] in ("therapist", "mechanic")]
    #message = f'{keycardTraderList[0][0].capitalize()}: {keycardTraderList[0][1]}, {keycardTraderList[1][0].capitalize()}: {keycardTraderList[1][1]}'
    for item in keycardTraderList:
        await ctx.send(f'{item[0].capitalize()}: {item[1]}')


@bot.command(name='help')
async def help(ctx):
    print(f'{ctx.author.name} used "{prefix}help" in {ctx.message.channel}')
    emailArn = 'me@arnoldg.no'
    emailX3l = 'me@x3l51.com'
    await ctx.send(f'Contact us at {emailArn} / {emailX3l}')


def traderTimeReCalculate(traderTime):
    if traderTime.lower() == 'right now':
        return traderTime.capitalize()

    traderTimeHours = int(traderTime.split(":")[0] )
    traderTimeMinutes = int(traderTime.split(":")[1] )
    traderTimeSeconds = int(traderTime.split(":")[2] )
    traderTimeSecondsTotal = int((traderTimeHours * 60 * 60) + (traderTimeMinutes * 60) + traderTimeSeconds)

    currentTime = time.time()
    global startTime
    diffTime = currentTime - startTime
    startTime = time.time()

    updatedTraderTime = int(traderTimeSecondsTotal - diffTime)
    if updatedTraderTime <= 0:
        return 'right now'
    
    traderTime = "{:0>8}".format(str(timedelta(seconds=updatedTraderTime)))

    return traderTime


def createDriverObj():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(
        chrome_options=options,
        executable_path=ChromeDriverManager().install()
    )

    return driver


def getAndParse(driver, url):
    driver.get(url)

    # THIS PIECE OF SHIT PIECE OF SOFTWARE
    time.sleep(1)

    page_source = driver.page_source
    tree = html.fromstring(page_source)

    return tree


def getTraderInfo(traderNames, traderTimers):

    traderTimersClean = []

    for item in traderTimers:
        if item == "right now" or item[0].isdigit():
            traderTimersClean.append(item)

    traderTuples = []

    for i, item in enumerate(traderNames):
        traderTuples.append((item, traderTimersClean[i]))

    return traderTuples


def getTupleListOfTrader():
    url = "https://eft-ammo.com/traders-reset-timers"
    driver = createDriverObj()
    tree = getAndParse(driver, url)
    traderNames = tree.xpath('//p[@class="chakra-text css-dqrf28"]/text()')
    traderTimers = tree.xpath('//p[@class="chakra-text css-1mnskd6"]/text()')
    traderTuples = getTraderInfo(traderNames, traderTimers)

    driver.quit()

    return traderTuples


if __name__ == "__main__":
    getValues.start()

    print("Starting bot now")
    bot.run()