# DiscordBot
1. [Commands](https://github.com/ondrasalek/Onderik_discord_bot#commands-help-command)
   1. [Admin](https://github.com/ondrasalek/Onderik_discord_botd#admin)
   2. [Everyone](https://github.com/ondrasalek/Onderik_discord_bot#everyone)
      - [Info](https://github.com/ondrasalek/Onderik_discord_bot#info)
      - [Music](https://github.com/ondrasalek/Onderik_discord_bot#music)
## Commands `.help <command>`
### Admin
#### Server
COMMAND | ABOUT command | Arguments
------------- | ------------- | -------------
`.set_autorole <role>` | Setting auto role | `<role name / id / @mention>` & `"now"`
`.set_botlog <channel>` | Setting channel BotLog | `<channel name / id / #mention>` & `"now"`
`.set_guild_url <url>` | Setting url link to server | `"<url>"` & `"now"`
`.set_msg_private <message>` | Setting Private welcome message (max 255 chars) | `"<message>"` & `"now"`
`.set_msg_welcome <message>` | Setting Channel Welcome message (max 255 chars) | `"<message>"` & `"now"`
`.set_msg_bye <message>` | Setting Channel Bye message (max 255 chars) | `"<message>"` & `"now"`
. | . | .
`.clear <number>` | Delete number of messages (max 333) | `<number>` (1-333)

### Everyone
#### Info
COMMANDS | ABOUT command | Arguments
------------- | ------------- | -------------
`.info_bot` | Info about BOT | .
`.info_channel` | Info about Channel | .
`.info_server` | Info about Server | .
`.info_role` | Info about Role | .
`.info_role <role>` | List of members if Role | `<role name / id / @mention>`
`.info_user` | Info about You | .
`.info_user <user>` | Info about Member | `<user name / nick / id / @mention>`

#### Music
COMMANDS | ABOUT command | Arguments
------------- | ------------- | -------------
`.play` | Play song | `<URL / name / author...>`
`.pause` | Pause | .
`.resume` | Resume | .
`.stop` | Stop | .


[TOP](https://github.com/ondrasalek/Onderik_discord_bot#discordbot)
