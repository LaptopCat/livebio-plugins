# livebio-tg plugin
__plugin__ = {"name": "discord", "author": "LaptopCat", "version": "1.1", "link": "https://github.com/LaptopCat/livebio-plugins/blob/main/plugins/discord/README.md"} # plugin manifest
from config import Config
from websockets import connect
from json import loads, dumps
from helpers import console
discord = Config.plugins.discord
print=console.print
from asyncio import run, create_task, sleep
heartbeat = 0
session = ""
url = ""
seq = 0
Activities = ["Playing", "Streaming", "Listening to", "Watching", "", "Competing in"]
activity = []
activities = []
async def send_message(ws, opcode, data={}):
    await ws.send(dumps({"op": opcode, "d": data}))

async def heartbeats(ws, event):
    while not event.is_set():
        await send_message(ws, 1)
        await sleep(heartbeat)
async def handle_message(ws, msg, event):
    global heartbeat, session, url, seq, activities
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
                "intents": 1<<8})
    elif msg["op"] == 1:
        await send_message(ws, 11)
    elif msg["op"] == 0:
        seq = msg["s"]
        if msg["t"] == "READY":
            session = msg["d"]["session_id"]
            url = msg["d"]["resume_gateway_url"]
            user = msg["d"]["user"]
            console.log(f"\[discord] Client is up! Running as [bold blue]{user['username']}#{user['discriminator']}[/bold blue]")
        elif msg["t"] == "PRESENCE_UPDATE":
            data = msg["d"]
            if data["user"]["id"] == str(discord.user):
              activities = data["activities"]
              activities = [[Activities[i['type']], i["details"] if i['type']==1 else (i['name'] if i['type']!=4 else i['state'])] if i.get('id')!='spotify:1' else [Activities[i["type"]], i["state"], i["details"]] for i in activities]
    elif msg["op"] == "7" or msg["op"] == 9:
        console.log(f"\[discord] Reconnecting to gateway")
        await reconnect(event)
        return "RECONNECT"
async def main(event):
      try:
        async with connect("wss://gateway.discord.gg/?v=10&encoding=json") as ws:
            while not event.is_set():
                msg = loads(await ws.recv())
                if await handle_message(ws, msg, event) == "RECONNECT":
                    await ws.close()
            await ws.close()
      except:
        console.log(f"\[discord] Reconnecting to gateway")
        await reconnect(event)

async def reconnect(event):
    try:
        async with connect(url) as ws:
            await send_message(ws, 6, {"token": discord.token, "session_id": session, "seq": seq})
            while not event.is_set():
                msg = loads(await ws.recv())
                if await handle_message(ws, msg, event) == "RECONNECT":
                    await ws.close()
            await ws.close()
    except:
        console.log(f"\[discord] Reconnecting to gateway")
        await reconnect(event)
async def gather(): # This function is called to give back the string that needs to be added
  global actname, doing, activity
  if len(activities)<1:
    return ""
  actname = ""
  doing = ""
  activity = (activities[1] if len(activities)>1 else activities[0]) if discord.pass_custom is True else (activities[1] if activities[0][0]=="" else activities[0])
  try:
      actname = activity[1]
      doing = activity[0]
      if doing == "":
        action = actname
      else:
        if len(activity) == 3:
          action = f'{doing} {activity[2]} by {activity[1]}'
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
    if len(activity) == 3:
      while complete is False:
        if len(generated) < Config.script.max_length:
          return action
          complete = True
        if phase == 0:
          action = f'{doing} {activity[1]} - {activity[2]}'
          generated=generated.replace(old,action,1)
          phase = 1
        elif phase == 1:
          old = str(action)
          action = f'{doing} {activity[2]} by {activity[1].split(", ")[0].split("; ")[0]}'
          generated=generated.replace(old,action,1)
          phase = 2
        elif phase == 2:
          old = str(action)
          action = f'{doing} {activity[1].split(", ")[0].split("; ")[0]} - {activity[2]}'
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
