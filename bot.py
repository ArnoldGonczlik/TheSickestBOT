#!/usr/bin/env python3

import json
import time

from twitchio.ext import commands, routines
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


with open('botConfig.json') as json_file:
    botConfig = json.load(json_file)

# env
irc_token = botConfig['irc_token']
client_id = botConfig['client_id']
nick = botConfig['nick']
prefix = botConfig['prefix']
initial_channels = botConfig['initial_channels']
token = botConfig['token']

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


@routines.routine(minutes=1)
async def getValues():
    traderTuples = getTupleListOfTrader()
    fetchTime = time.time()

    print("I JUST RAN")


@bot.command(name='traders')
async def traders(ctx):
    traderTuples = getTupleListOfTrader()
    for item in traderTuples:
        await ctx.send(f'{item[0]}: {item[1]}')


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

    print("Fetching complete")

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
    bot.run()

    traderTuples = getTupleListOfTrader()
    fetchTime = time.time()
