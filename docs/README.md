# How Plugins work?

First, livebio loads all python files with .plugin.py at the end as modules, storing them in a dictionary, so it is easy to find plugins.
While loading, it checks each file for:
- Plugin Metadata (\_\_plugin__ dictionary)
- gather Coroutine
- postprocess Coroutine

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
__plugin__ = {
              "name": "awesome_plugin", # You should use your plugin's filename without .plugin.py as a name
              "author": "You",
              "version": "1.0",
              "link": "https://github.com/LaptopCat/livebio-plugins/"
             }
             
awesome_plugin = Config.plugins.awesome_plugin

async def gather():
  return "I am awesome!"
 
async def postprocess():
  if awesome_plugin.postprocess:
    return "I am really, really awesome!"
```
Now, let's break this code down.

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

gather() gets called whenever the plugin is generating a new bio.

postprocess() gets called after each full generation so plugins can possibly reduce text if it is too long or do anything else.

Now, let's add some logging to this plugin:
```python
from config import Config
from helpers import console
__plugin__ = {
              "name": "awesome_plugin", # You should use your plugin's filename without .plugin.py as a name
              "author": "You",
              "version": "1.0",
              "link": "https://github.com/LaptopCat/livebio-plugins/"
             }
print = console.print    
awesome_plugin = Config.plugins.awesome_plugin

async def gather():
  console.log("\[awesome_plugin] Data got gathered!")
  return "I am awesome!"
 
async def postprocess():
  if awesome_plugin.postprocess:
    print("\[awesome_plugin] Data got postprocessed!")
    return "I am really, really awesome!"
```
console is an [rich.console.Console](https://rich.readthedocs.io/en/stable/reference/console.html#rich.console.Console) object.
Using it for logging/printing is recommended. It also supports styles and [more](https://rich.readthedocs.io/en/stable/console.html).
Following this style of logging/printing is also recommended
```
\[PLUGIN_NAME] TEXT
```
to keep consistency between plugins and livebio.
