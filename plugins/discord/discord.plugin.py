# livebio-tg plugin
__plugin__ = {"name": "discord", "author": "LaptopCat", "version": "1.0", "link": "https://github.com/LaptopCat/livebio-plugins/blob/main/plugins/discord/README.md"} # plugin manifest
from discord import Client, Intents, VoiceClient
from config import Config
from threading import Thread
from helpers import console
discord = Config.plugins.discord

VoiceClient.warn_nacl = False
intents = Intents.default()
intents.presences = True
intents.members = True
dclient = Client(intents=intents)
guild = None


async def gather(): # This function is called to give back the string that needs to be added
  if guild == None:
    return ""
  global actname, doing, activity
  usr = guild.get_member(int(discord.user))
  actname = ""
  doing = ""
  activity = usr.activity
  try:
      actname = activity.name
      doing = activity.type
      doing = str(doing)
      doing = doing.replace("ActivityType.", "").replace("listening", "Listening to")
      if doing == "custom":
        if discord.pass_custom == False:
          action = ""
        else:
          action = actname
      else:
        if actname == "Spotify" and doing == "Listening to":
          action = f'{doing} {activity.title} by {activity.artist}'
        else:
          doing = doing[0].upper() + doing[1:len(doing)]
          action = f"{doing} {actname}"
  except AttributeError:
      action = ""
  return action



@dclient.event
async def on_ready():
  global guild
  guild = dclient.get_guild(int(discord.guild))
  console.log("\[discord] Client is up! Running as [bold blue]{}[/bold blue]".format(dclient.user))

async def postprocess(generated, old):
    generated = str(generated)
    if actname == "Spotify" and doing == "Listening to":
      complete = False
      phase = 0
      while complete is False:
        if len(generated) < Config.script.max_length:
          complete = True
        if phase == 0:
          action = f'{doing} {activity.artist} - {activity.title}'
          generated=generated.replace(old,action,1)
          phase = 1
        elif phase == 1:
          old = str(action)
          action = f'{doing} {activity.title} by {activity.artist.split(",")[0]}'
          generated=generated.replace(old,action,1)
          phase = 2
        elif phase == 2:
          old = str(action)
          action = f'{doing} {activity.artist.split(",")[0]} - {activity.title}'
          generated=generated.replace(old,action,1)
          phase = 3
        elif phase == 3:
          old = str(action)
          action = f'{doing} Spotify'
          generated=generated.replace(old,action,1)
          phase = 4
        elif phase == 4:
          old = str(action)
          action = ""
          generated=generated.replace(old,action,1)
          phase = 5
        else:
          return action
    elif doing != "" and actname != "" and doing != "custom":
      while complete is False:
        if len(generated) <= Config.script.max_length:
          complete = True
        if phase == 0:
          action = f'{doing} {actname}'
          generated=generated.replace(old,action,1)
          phase = 1
        elif phase == 1:
          old = str(action)
          action = f'{doing}'
          generated=generated.replace(old,action,1)
          phase = 2
        elif phase == 2:
          old = str(action)
          action = ""
          generated=generated.replace(old,action,1)
          phase = 3
        else:
          return action


def run_client():
  dclient.run(discord.token, log_handler=None, log_level=50)
thread=Thread(target=run_client).start()