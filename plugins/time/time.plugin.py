# livebio-tg plugin
__plugin__ = {"name": "time", "author": "LaptopCat", "version": "1.1", "link": "https://github.com/LaptopCat/livebio-plugins/blob/main/plugins/time/README.md"} # plugin manifest
from datetime import datetime
from pytz import timezone
from config import Config
time = Config.plugins.time
time.time_formatting = getattr(time, "time_formatting", "%H:%M")
time.postprocess = getattr(time, "postprocess", False)
time.timezone = getattr(time, "timezone", None)
tz = timezone(time.timezone)

async def gather(): # This function is called to give back the string that needs to be added
  return datetime.now(tz).strftime(time.time_formatting)


async def postprocess(generated, old):
  if time.postprocess:
    if generated < Config.script.max_length:
      return ""

def setup(*args, **kwargs):
  ...
