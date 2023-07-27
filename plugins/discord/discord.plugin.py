# livebio-tg plugin
__plugin__ = {"name": "discord", "author": "LaptopCat", "version": "1.4", "link": "https://github.com/LaptopCat/livebio-plugins/blob/main/plugins/discord/README.md"} # plugin manifest
from config import Config
from websockets import connect
from json import loads, dumps
from helpers import console
discord = Config.plugins.discord
print=console.print
from asyncio import run, create_task, sleep
heartbeat = 0
activity = []
activities = []
def activity_parser(strings, activities):
  result = []
  for i in activities:
      result2 = [strings[i["type"]], i["name"]]
      if i.get('id') == "spotify:1":
        result2.append(i["state"])
        result2.append(i["details"])
      else:
        if i['type'] == 1:
          result2.append(i["details"])
        elif i["type"] == 4:
          result2.append(i["state"])
        else:
          result2.append(i["name"])
      result.append(result2)
  return result
def activity_selector(activities, config):
    if len(activities) != 0:
        if config.pass_custom:
            if len(activities) > 1:
                return activities[1]
            else:
                return activities[0]
        else:
            if activities[0][0] == config.get_logstring("activities")[4]:
                return activities[1]
            else:
                return activities[0]
discord.activity_selector = getattr(discord, "activity_selector", activity_selector)
discord.activity_parser = getattr(discord, "activity_parser", activity_parser)
discord.logstrings = getattr(discord, "logstrings", None)
discord.gateway_url = getattr(discord, "gateway", "wss://gateway.discord.gg/?v=10&encoding=json")
discord.pass_custom = getattr(discord, "pass_custom", False)
default_logstrings = {
        "ready": "\[discord] Client is up! Running as [bold blue]{}#{}[/bold blue]",
        "reconnecting": "\[discord] Reconnecting to gateway",
        "activities": ["Playing", "Streaming", "Listening to", "Watching", "", "Competing in"],
        "by": "by"
}
def logstring(name):
  return getattr(discord.logstrings, name, default_logstrings[name])
discord.get_logstring = logstring
async def send_message(ws, opcode, data={}):
    await ws.send(dumps({"op": opcode, "d": data}))

async def heartbeats(ws, event):
    while not event.is_set():
      try:
        await send_message(ws, 1)
        await sleep(heartbeat)
      except:
        return
async def handle_message(ws, msg, event):
    global heartbeat, activities
    if msg["op"] == 10:
        heartbeat = msg["d"]["heartbeat_interval"]/1000
        create_task(heartbeats(ws, event))
        await send_message(ws, 2, {"token": discord.token, "properties": {
                    "os": "linux",
                    "browser": "firefox",
                    "device": "pc"
                }, "presence": {
                    "activities": [],
                    "status": "online",
                    "since": 91879201,
                    "afk": False
                },
                "intents": 256})
    elif msg["op"] == 1:
        await send_message(ws, 11)
    elif msg["op"] == 0:
        if msg["t"] == "READY":
            user = msg["d"]["user"]
            console.log(logstring("ready").format(user['username'], user['discriminator']))
        elif msg["t"] == "PRESENCE_UPDATE":
            data = msg["d"]
            if data["user"]["id"] == str(discord.user):
              activities = data["activities"]
              activities = discord.activity_parser(discord.logstrings.activities, activities)
    elif msg["op"] == "7" or msg["op"] == 9:
        console.log(logstring("reconnecting") + " (Opcode {})".format(msg["op"]))
        return "RECONNECT"
async def main(event):
  async for ws in connect(discord.gateway_url):
      try:
            while not event.is_set():
                msg = loads(await ws.recv())
                if await handle_message(ws, msg, event) == "RECONNECT":
                    await ws.close()
            return
      except Exception as e:
        console.log(logstring("reconnecting") + " ({}: {})".format(type(e).__name__, str(e)))

async def gather(): # This function is called to give back the string that needs to be added
  global actname, doing, activity
  if len(activities)<1:
    return ""
  actname = ""
  doing = ""
  activity = discord.activity_selector(activities, discord)
  if activity is None:
    return ""
  try:
      actname = activity[2]
      doing = activity[0]
      if doing == "":
        action = actname
      else:
        if len(activity) == 4:
          action = f'{doing} {activity[3]} {logstring("by")} {activity[2]}'
        else:
          action = f"{doing} {actname}"
  except:
      action = ""
  return action


async def postprocess(generated, old):
    generated = str(generated)
    action = None
    complete = False
    phase = 0
    if len(activity) == 4:
      while complete is False:
        if len(generated) < Config.script.max_length:
          return action
          complete = True
        if phase == 0:
          action = f'{doing} {activity[2]} - {activity[3]}'
          generated=generated.replace(old,action,1)
          phase = 1
        elif phase == 1:
          old = str(action)
          action = f'{doing} {activity[3]} {logstring("by")} {activity[2].split(", ")[0].split("; ")[0]}'
          generated=generated.replace(old,action,1)
          phase = 2
        elif phase == 2:
          old = str(action)
          action = f'{doing} {activity[2].split(", ")[0].split("; ")[0]} - {activity[3]}'
          generated=generated.replace(old,action,1)
          phase = 3
        elif phase == 3:
          old = str(action)
          action = f'{doing} {activity[1]}'
          generated=generated.replace(old,action,1)
          phase = 4
        elif phase == 4:
          old = str(action)
          action = ""
          generated=generated.replace(old,action,1)
          phase = 5
        else:
          return action
    elif doing != logstring("activities")[4] and actname != "":
      while complete is False:
        if len(generated) < Config.script.max_length:
          return action
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
def setup(event):
  run(main(event))
