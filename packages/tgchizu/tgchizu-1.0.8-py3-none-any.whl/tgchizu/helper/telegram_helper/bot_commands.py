class _BotCommands:
    def __init__(self):
        self.StartCommand = 'start'
        self.MirrorCommand = 'mirr'
        self.UnzipMirrorCommand = 'unzipmirr'
        self.TarMirrorCommand = 'tarmirror'
        self.CancelMirrorCommand = 'cancel'
        self.CancelAllCommand = 'cancelall'
        self.ListCommand = 'list'
        self.StatusCommand = 'status'
        self.AuthorizeCommand = 'autho'
        self.UnAuthorizeCommand = 'unauth'
        self.AuthListCommand = 'authlist'
        self.PingCommand = 'ping'
        self.RestartCommand = 'restart'
        self.StatsCommand = 'stats'
        self.HelpCommand = 'help'
        self.LogCommand = 'log'
        self.CloneCommand = 'clone'
        self.WatchCommand = 'watch'
        self.SpeedCommand = 'speedtest'
        self.UsageCommand = 'usage'
        self.TarWatchCommand = 'tarwatch'
        self.DeleteCommand = 'delete'
        self.ConfigCommand = 'config'
        /{BotCommands.StartCommand} Start the bot
/{BotCommands.MirrorCommand} Mirror the provided link to Google Drive
/{BotCommands.UnzipMirrorCommand} Mirror the provided link and if the file is in archive format, it is extracted and then uploaded to Google Drive
/{BotCommands.TarMirrorCommand} Mirror the provided link and upload in archive format (.tar) to Google Drive
/{BotCommands.CloneCommand} Clone folders in Google Drive (owned by someone else) to your Google Drive
/{BotCommands.WatchCommand} Mirror through 'youtube-dl' to Google Drive
/{BotCommands.TarWatchCommand} Mirror through 'youtube-dl' and upload in archive format (.tar) to Google Drive
/{BotCommands.CancelMirrorCommand} Reply with this command to the source message, and the download will be cancelled
/{BotCommands.CancelAllCommand} Cancels all running tasks (downloads, uploads, archiving, unarchiving)
/{BotCommands.StatusCommand} Shows the status of all downloads and uploads in progress
/{BotCommands.ListCommand} Searches the Google Drive folder for any matches with the search term and presents the search results in a Telegraph page
/{BotCommands.AuthorizeCommand} Authorize a group chat or, a specific user to use the bot
/{BotCommands.UnAuthorizeCommand} Unauthorize a group chat or, a specific user to use the bot
/{BotCommands.PingCommand} Ping the bot
/{BotCommands.RestartCommand} Restart the bot
/{BotCommands.StatsCommand} Shows the stats of the machine that the bot is hosted on
/{BotCommands.HelpCommand}: To get the help message
/{BotCommands.LogCommand} Sends the log file of the bot and the log file of 'aria2c' daemon (can be used to analyse crash reports, if any)
/{BotCommands.UsageCommand}: To see Heroku Dyno Stats (Owner only).


BotCommands = _BotCommands()
