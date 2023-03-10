# livebio-tg plugin
__plugin__ = {"name": "sinoptik", "author": "LaptopCat", "version": "1.0", "link": "https://github.com/LaptopCat/livebio-plugins/blob/main/plugins/sinoptik/README.md"} # plugin manifest
from requests import Session
from time import sleep
from config import Config
from helpers import console
sinoptik = Config.plugins.sinoptik
session = Session()
weather = ""
url = sinoptik.base_url + sinoptik.path

def setup(event):
  global weather
  items = {
        "d": 
            {"000": "☀", "100": "🌤", "110": "🌦", "111": "🌦🌨", "112": "🌤🌨", "120": "🌦", "121": "🌦🌨", "122": "🌤🌨", "130": "🌦", "131": "🌦🌨", "132": "🌤🌨", "140": "🌦⚡", 
             "141": "🌦🌨", "142": "🌤🌨", "200": "⛅", "210": "🌦", "211": "🌦🌨", "212": "⛅🌨", "220": "🌦", "221": "🌦🌨", "222": "⛅🌨", "230": "🌦", "231": "🌦🌨", 
             "232": "⛅🌨", "240": "🌦⚡", "241": "🌦🌨", "242": "⛅🌨", "300": "🌥", "310": "🌦", "311": "🌦🌨", "312": "🌥🌨", "320": "🌦", "321": "🌦🌨", "322": "🌥🌨", 
             "330": "🌦", "331": "🌦🌨", "332": "🌥🌨", "340": "🌦⚡", "341": "🌦🌨", "342": "🌥🌨", "400": "☁", "410": "🌧", "411": "🌨🌧", "412": "🌨", "420": "🌧", "421": "🌨🌧", 
             "422": "🌨", "430": "🌧", "431": "🌨🌧", "432": "🌨", "440": "⛈", "441": "🌨🌧", "442": "🌨", "500": "🌤"}, 
        "n": 
            {"000": "🌙", "100": "🌙☁", "110": "🌙🌧", "111": "🌙🌨🌧", "112": "🌙🌨", "120": "🌙🌧", "121": "🌙🌨🌧", "122": "🌙🌨", "130": "🌙🌧", "131": "🌙🌨🌧", 
             "132": "🌙🌨", "140": "🌙⚡", "141": "🌙🌨🌧", "142": "🌙🌨", "200": "🌙☁", "210": "🌙🌧", "211": "🌙🌧🌨", "212": "🌙🌨", "220": "🌙🌧", "221": "🌙🌧🌨", 
             "222": "🌙🌨", "230": "🌙🌧", "231": "🌙🌧🌨", "232": "🌙🌨", "240": "🌙⛈", "241": "🌙🌧🌨", "242": "🌙🌨", "300": "🌙☁", "310": "🌙🌧", "311": "🌙🌧🌨", 
             "312": "🌙🌨", "320": "🌙🌧", "321": "🌙🌧🌨", "322": "🌙🌨", "330": "🌙🌧", "331": "🌙🌧🌨", "332": "🌙🌨", "340": "🌙⛈", "341": "🌙🌧🌨", "342": "🌙🌨", 
             "400": "☁", "410": "🌧", "411": "🌨🌧", "412": "🌨", "420": "🌧", "421": "🌨🌧", "422": "🌨", "430": "🌧", "431": "🌨🌧", "432": "🌨", "440": "🌧⚡", "441": "🌨🌧", 
             "442": "🌨", "500": "🌙☁"}
              }
  while not event.is_set():
        weather = session.get(url).text.split('bd1c')[1].split("weatherIcoS")[1].split("cur")[1].split("/s/")[1].split(".gif")[0]
        weather = items[weather[0]][weather[1:]]
        console.log("\[sinoptik] Cached weather to {}".format(weather))
        sleep(sinoptik.delay)

async def gather(): # This function is called to give back the string that needs to be added
  value = weather
  if value.strip() == "":
    value = sinoptik.default
  return value


async def postprocess(generated, old):
  if sinoptik.postprocess is True:
    if generated < Config.script.max_length:
      return ""
