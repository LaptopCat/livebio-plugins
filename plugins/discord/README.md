# discord.plugin.py
Adds your discord rich presence.
# Installing
## Prerequisites
You must have livebio installed (obviously)

You must also have the websockets python library installed:
```bash
python -m pip install websockets
```
(replace python with python3 on linux)
## 1. Download the plugin
You can download the plugin from [here](https://laptopcat.github.io/livebio-plugins/plugins/discord/discord.plugin.py).

After downloading, place it to your plugins folder.

## 2. Create the necessary Discord stuff
## 2.1 Create a Discord bot
A Discord bot is needed to receive presence data in a Discord ToS-compliant way.

To create a Discord bot, go to this [page](https://discord.com/developers/applications) (You may need to login with your Discord account)

When you are on the page, click on the "New Application" button on the right corner of your screen (Name it anything you want)

After creating an application, go to the "Bot" section on the left side of your screen.

Then, click on "Add Bot" on the right side of your screen. (It may ask you for your 2FA code)

If you get an error saying "Too many users have this name", you should go to the "Application" tab on the left side of your screen and change the name to something more unique.

Now, when the bot is created, copy the token and write it down somewhere (It is used to access the bot so you shouldn't share it with anyone)

After that, scroll down a bit until you find "Privileged Gateway Intents"

In there, enable "Presence Intent" (You may also want to uncheck the "Public Bot" option)
## 2.2 Create a Guild
First, open Discord. Then, in the left bar with guilds, find the + and click on it.
Fill in the stuff with anything you want, doesn't matter.
Then, go to settings, find Advanced (Behavior), enable Developer Mode.

Open the member sidebar and find yourself. Right click on yourself and copy the ID. Write it down somewhere.

## 2.3 Add the Bot to your Guild
Go back to this [page](https://discord.com/developers/applications).

Find your application and click on it. Then, click on "OAuth" on the left side of the screen and on "URL Generator".

Then, select "Bot" and copy the generated URL.

Next, go to the generated URL and select your guild that you created and add the bot.
## 3. Configure the plugin
First, add a discord field to the plugins field in your existing config:
```python
  "plugins": {
    "discord": {
      "token": str("Your Discord bot token"),
      "user": int(User ID),
    }
  }
```
Make it have the token, guild and pass_custom fields.

Config Reference:
<blockquote><details><summary>token</summary>
Your discord bot token. (String)
</details>
</blockquote>

<blockquote><details><summary>user</summary>
Your discord user id. (Integer)
</details>
</blockquote>

<blockquote><details><summary>pass_custom</summary>
  <i>Optional</i><br>
Whether your custom status should be used as an activity. Defaults to False (Boolean)
</details>
</blockquote>

<blockquote><details><summary>gateway_url</summary>
 <i>Optional</i><br>
What URL should the plugin connect to. Defaults to wss://gateway.discord.gg/?v=10&encoding=json (String)
</details>
</blockquote>

<blockquote><details><summary>activity_parser</summary>
 <i>Optional</i><br>
A function which parses the activities you get from discord's gateway into a list. Defaults to 
  
lambda strings,activities: [[strings[i['type']], i["details"] if i['type']==1 else (i['name'] if i['type']!=4 else i['state'])] if i.get('id')!='spotify:1' else [strings[i["type"]], i["state"], i["details"]] for i in activities]
</details>
</blockquote>

<blockquote><details><summary>activity_selector</summary>
 <i>Optional</i><br>
A function which selects an activity to display from activities parsed by activity_parser. Defaults to 
  
lambda activities, config: (activities[1] if len(activities)>1 else activities[0]) if config.pass_custom is True else (activities[1] if activities[0][0]==config.get_logstring("activities")[4] else activities[0])
</details>
</blockquote>
