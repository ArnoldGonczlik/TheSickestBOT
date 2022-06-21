#!/usr/bin/env python3

import time
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# python -m pip install lxml, selenium, webdriver-manager


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


def getTraderInfo(tree, traderNames, traderTimers):

    traderTimersClean = []

    for item in traderTimers:
        if item == "right now" or item[0].isdigit():
            traderTimersClean.append(item)

    traderTuples = []

    for i, item in enumerate(traderNames):
        traderTuples.append((item, traderTimersClean[i]))

    return traderTuples


def getTupleListOfTrader():
    url             = "https://eft-ammo.com/traders-reset-timers"
    driver          = createDriverObj()
    tree            = getAndParse(driver, url)
    traderNames     = tree.xpath('//p[@class="chakra-text css-dqrf28"]/text()')
    traderTimers    = tree.xpath('//p[@class="chakra-text css-1mnskd6"]/text()')
    traderTuples    = getTraderInfo(tree,traderNames, traderTimers)

    driver.quit()

    return traderTuples


if __name__ == "__main__":
    traderTuples = getTupleListOfTrader()
    print(traderTuples)
