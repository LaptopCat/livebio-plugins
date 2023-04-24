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

  "plugins": {
    "sinoptik": {
      "path": str("/погода-москва")
    }
  }
```

Config Reference:
<blockquote><details><summary>path</summary>
Which path on the website should be used to get weather info. (String)
</details>
</blockquote>

<blockquote><details><summary>base_url</summary>
<i>Optional</i><br>
Base URL for requests (String). Defaults to https://sinoptik.ua
</details>
</blockquote>

<blockquote><details><summary>delay</summary>
  <i>Optional</i><br>
How much time should pass between each weather cache in seconds (Integer). Defaults to 600.
</details>
</blockquote>

<blockquote><details><summary>default</summary>
 <i>Optional</i><br>
Default string to use as weather if weather not cached yet/caching failed (String). Defaults to ⛅ 
</details>
</blockquote>

<blockquote><details><summary>parser</summary>
 <i>Optional</i><br>
A function which parses the page data you get into a string. Defaults to 
  
lambda text: text.split('bd1c')[1].split("weatherIcoS")[1].split("cur")[1].split("/s/")[1].split(".gif")[0]
</details>
</blockquote>

<blockquote><details><summary>postprocess</summary>
 <i>Optional</i><br>
Whether the plugin should remove weather output if generated bio is bigger than Config.script.max_length. Defaults to False
</details>
</blockquote>

<blockquote><details><summary>logstrings</summary>
<i>Optional</i><br>
Dictionary of strings that are logged to the console or used somewhere to generate the bio. Default logstrings are <a href="https://github.com/LaptopCat/livebio-plugins/blob/main/plugins/sinoptik/sinoptik.plugin.py#L17">on line 17 of sinoptik.plugin.py</a>
</details>
</blockquote>
