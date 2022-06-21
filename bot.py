from twitchio.ext import commands
import json

with open('TheSickestBOT/botConfig.json') as json_file:
    botConfig = json.load(json_file)

#env
irc_token=botConfig['irc_token']
client_id=botConfig['client_id']
nick=botConfig['nick']
prefix=botConfig['prefix']
initial_channels=botConfig['initial_channels']
token=botConfig['token']

bot = commands.Bot(
    irc_token=irc_token,
    client_id=client_id,
    nick=nick,
    prefix=prefix,
    initial_channels=initial_channels,
    token=token
)

@bot.command(name='test')
async def test(ctx):
    print('Test')
    await ctx.send('test passed!')

if __name__ == "__main__":
    bot.run()