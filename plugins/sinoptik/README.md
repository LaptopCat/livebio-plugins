# sinoptik.plugin.py
Adds weather from sinoptik.ua as an emoji

# Installing
## Prerequisites
You must have livebio installed (obviously)

You must also have the requests python library installed:
```bash
pip install requests
```
## 1. Download the plugin
You can download the plugin from [here](https://laptopcat.github.io/livebio-plugins/plugins/sinoptik/sinoptik.plugin.py).

After downloading, place it to your plugins folder.
## 2. Configure the plugin
First, add a sinoptik field to the plugins field in your existing config:
```python
{
  "telegram": {
    "app": {
      "id": int(4664),
      "hash": str("Askfdweikltrjhwelkjth")
    },
    "auth": {
      "mode": mode_enum("file"), # "string" or "file"
      "string": str("isadfiuowehtkwhetkj")
    }
  },
  "script": {
    "splitter": str("|"),
    "template": str("i use livebio btw"),
    "delay": int(20),
    "max_length": int(70)
  },
  "plugins": {
    "sinoptik": {
      "path": str("/погода-москва"),
      "base_url": str("https://sinoptik.ua"), # default is "https://sinoptik.ua" 
      "postprocess": False, # default is False
      "delay": int(600), # default is 600
      "default": "⛅" # default is ⛅
    }
  }
}
```
Make it have the path, base_url, postprocess, delay and default fields.

Config Reference:
```yaml
path: The path on sinoptik.ua. For example: /погода-москва
base_url: base url for requests. should always be "https://sinoptik.ua"
postprocess: whether the plugin should remove the emoji if the generated data is too long
delay: delay in seconds between each weather request. Default and recommended is 600 (10 minutes) as this data does not change often
default: the default emoji/text to use if weather is not cached (usually on first bio change)
```
