import shutil
import psutil
import signal
import pickle

from os import execl, kill, path, remove
from sys import executable
import pytz
import time

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from . import dispatcher, updater, botStartTime, AUTHORIZED_CHATS
from .helper.ext_utils import fs_utils
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .helper.config import editor
from .helper.config.subproc import killAll
from .helper.config import sync
from .helper.config.dynamic import configList, DYNAMIC_CONFIG
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, anime, stickers, search, delete, speedtest, usage

now=datetime.now(pytz.timezone('America/Toronto'))

@run_async
def stats(update: Update, context: CallbackContext):
    currentTime = get_readable_time((time.time() - botStartTime))
    current = now.strftime('%Y/%m/%d %I:%M:%S %p')
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>Bot Uptime ⌚:</b> {currentTime}\n' \
            f'<b>Start Time ⌚:</b> {current}\n' \
            f'<b>Total disk space🗄️:</b> {total}\n' \
            f'<b>Used 🗃️:</b> {used}  ' \
            f'<b>Free 🗃️:</b> {free}\n\n' \
            f'📇Data Usage📇\n<b>Uploaded :</b> {sent}\n' \
            f'<b>Downloaded:</b> {recv}\n\n' \
            f'<b>CPU 🖥️:</b> {cpuUsage}% ' \
            f'<b>RAM ⛏️:</b> {memory}% ' \
            f'<b>Disk 🗄️:</b> {disk}%'
    sendMessage(stats, context.bot, update)


@run_async
def start(update: Update, context: CallbackContext):
    start_string = f'''
mirrors files to shared drive. 
courtesy of @ori001. 
/{BotCommands.HelpCommand} for a list of available commands.
'''
    sendMessage(start_string, context.bot, update)

@run_async
def chat_list(update, context: CallbackContext):
    chatlist =''
    chatlist += '\n'.join(str(id) for id in AUTHORIZED_CHATS)
    sendMessage(f'<b>Authorized List:</b>\n{chatlist}\n', context.bot, update)

@run_async
def restart(update: Update, context: CallbackContext):
    restart_msg = sendMessage('Restarting, Please Wait...', context.bot, update)
    LOGGER.info(f'Restarting the Bot...')
    fs_utils.clean_all()
    killAll()
    if DYNAMIC_CONFIG:
        time.sleep(3)
        restart_msg.edit_text(f'Syncing to Google Drive...')
        sync.handler(configList)
        restart_msg.edit_text(f'Sync Completed!\n{configList}')
    if not DYNAMIC_CONFIG:
        time.sleep(5)
    # Save restart message info in order to reply to it after restarting
    restart_msg_dat = f"{restart_msg.chat_id} {restart_msg.message_id}"
    open('restart_msg.txt', 'wt').write(restart_msg_dat)
    execl(executable, executable, "-m", "tgchizu")


@run_async
def ping(update: Update, context: CallbackContext):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping...", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update: Update, context: CallbackContext):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update: Update, context: CallbackContext):
    help_string = f'''
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
/{BotCommands.SpeedCommand}: Check Internet Speed of the Host
/{BotCommands.DeleteCommand} Delete files in Google Drive matching the given string
/{BotCommands.ConfigCommand} Edit 'config.env' file
'''
    sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart_message.txt'):
        restart_msg_dat = open('restart_message.txt', 'rt').read().split(' ')
        bot.editMessageText(text='Sync Completed!\nRestarted Successfully!',
                            chat_id=restart_msg_dat[0], message_id=restart_msg_dat[1])
        LOGGER.info('Restarted Successfully!')
        remove('restart_message.txt')

    start_handler = CommandHandler(BotCommands.StartCommand, start)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart, filters=CustomFilters.owner_filter)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    authlist_handler = CommandHandler(BotCommands.AuthListCommand, chat_list, filters=CustomFilters.owner_filter | CustomFilters.authorized_user)
    config_handler = editor.handler
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    dispatcher.add_handler(authlist_handler)
    dispatcher.add_handler(config_handler)
    updater.start_polling()
    LOGGER.info("Bot Started!")
    updater.idle()
    fs_utils.clean_all()
    killAll()


main()
