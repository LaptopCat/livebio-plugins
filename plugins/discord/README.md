# discord.plugin.py
Adds your discord rich presence.
## Installing
### 1. Download the plugin
You can download the plugin from [here]().
If you are using replit, you should download [this]() version of the plugin and [this]() script.

Place both of them in your plugins folder.
### 2.1 Create a Discord bot

To create a Discord bot, go to this [page](https://discord.com/developers/applications) (You may need to login with your Discord account)

When you are on the page, click on the "New Application" button on the right corner of your screen (Name it anything you want)

After creating an application, go to the "Bot" section on the left side of your screen.

Then, click on "Add Bot" on the right side of your screen. (It may ask you for your 2FA code)

If you get an error saying "Too many users have this name", you should go to the "Application" tab on the left side of your screen and change the name to something more unique.

Now, when the bot is created, copy the token and write it down somewhere (It is used to access the bot so you shouldn't share it with anyone)

After that, scroll down a bit until you find "Privileged Gateway Intents"

In there, enable "Presence Intent" and "Server Members Intent" (You may also want to uncheck the "Public Bot" option)
