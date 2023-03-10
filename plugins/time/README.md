# time.plugin.py
Adds current time (supports timezones)

# Installing
## Prerequisites
You must have livebio installed (obviously)

You must also have the pytz python library installed:
```bash
pip install pytz
```
## 1. Download the plugin
You can download the plugin from [here](https://laptopcat.github.io/livebio-plugins/plugins/time/time.plugin.py).

After downloading, place it to your plugins folder.
## 2. Configure the plugin
First, add a time field to the plugins field in your existing config:
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
    "time": {
      "time_formatting": str("%H:%M"), # Default - %H:%M
      "timezone": str("Pacific/Tarawa"), # Default - None
      "postprocess": False # default - False
    }
  }
}
```
Make it have the time_formatting, timezone and postprocess fields.

Config Reference:
```yaml
time_formatting: How the plugin needs to format the time. Default is %H:%M (HOUR:MINUTE)
timezone: The timezone used for getting current time. Can be None if you want to use system timezone. See available timezones below
postprocess: Whether the plugin should remove its output if the generated string is too long.
```
You can find available timezones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). You should use the TZ database name in the config.
