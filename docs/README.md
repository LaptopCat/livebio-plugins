# How Plugins work?

First, livebio loads all python files with .plugin.py at the end as modules, storing them in a dictionary, so it is easy to find plugins.
While loading, it checks each file for:
- Plugin Metadata (\_\_plugin__ dictionary)
- gather Coroutine
- postprocess Coroutine
- setup function

When generating the bio, it uses a regex string (```\{%plugin:(.*?)%\}```) to find all plugins in the template.
Then, livebio calls gather() of each plugin and adds it all together. It also adds the splitter between each plugin output.
If the plugin name inside of the template has UNSPLIT at the end, no splitter will be added.

After generating the bio, it calls postprocess(generated_bio, plugin_generated_string) of each plugin and changes:
- If postprocess returns None, it does not change the plugin generated string.
- If postprocess returns "", it removes the plugin generated string.
- If postprocess returns any other string, it changes the old plugin generated string to that.

# Creating Plugins

First, make a (plugin_name).plugin.py file inside of the ./plugins/ directory.

Next, you should define the required things.
```python
from config import Config
from helpers import console
# Both are livebio modules, no need to install them as they are a part of livebio
__plugin__ = {
              "name": "awesome_plugin", # You should use your plugin's filename without .plugin.py as a name
              "author": "You",
              "version": "1.0",
              "link": "https://github.com/LaptopCat/livebio-plugins/"
             }
             
awesome_plugin = Config.plugins.awesome_plugin

async def gather():
  # The code that is here runs when generating the bio string
  # You can return None or "" to not generate anything
  console.log("\[awesome-plugin] gather() was called")
  return "I am awesome!"
 
async def postprocess(generated, old):
  # The code that is here runs after the whole bio string is generated
  # It allows plugins to give edits according to the generated string and the old output
  # Two arguments get passed to this function: generated - The generated string; old - The old string made by the plugin
  # Keep in mind that this only gets called if gather() is ran successfully and actually returns something
  if awesome_plugin.postprocess:
    console.log("\[awesome-plugin] running postprocessing")
    return "I am really, really awesome!"

def setup(event):
  # The code that is here runs in a separate thread when the plugin is added
  # For example: you can run a task here like in the discord plugin or sinoptik plugin
  # It also gets a threading.Event passed to it which gets set when livebio stops
  console.log("\[awesome-plugin] plugin was added") # this message is unnecessary as livebio prints messages itself when a plugin is loaded
```

You can use the config by importing Config from config.

The Config is an object with the config from config.py

The plugin will load the config from the "awesome_plugin" field in the "plugins" field of the config.

Example config for your plugin:
```python
{
  "telegram": {
    "app": {
      "id": int(4664),
      "hash": str("asafasf")
    },
    "auth": {
      "mode": mode_enum("string"),
      "string": str("asdfasfas")
    }
  },
  "script": {
    "splitter": "|",
    "template": str("{%plugin:awesome_plugin%}{%plugin:awesome_pluginUNSPLIT%} your text"),
    # Produces "I am really, really awesome! | I am really, really awesome! your text
    "delay": int(20),
    "max_length": int(70)
  },
  "plugins": {
    "awesome_plugin": {
      "postprocess": boolean(True)
    }
  }
}
```

console is a [rich.console.Console](https://rich.readthedocs.io/en/stable/reference/console.html#rich.console.Console) object.
Using it for logging/printing is recommended. It also supports styles and [more](https://rich.readthedocs.io/en/stable/console.html).
Following this style of logging/printing is also recommended
```
\[PLUGIN_NAME] TEXT
```
to keep consistency between plugins and livebio.
