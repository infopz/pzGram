import threading
import traceback

from .Objects import *
from .Useful import notafunction as nf
from .Useful import *
from .Exceptions import *


class Bot:
    def __init__(self, bot_key):
        self.key = bot_key
        self.offset = 0
        # Bot Informations
        self.id = None
        self.username = None
        self.name = None
        # Bot Functions
        self.processAll = nf
        self.processMessage = nf
        self.startFunc = nf
        self.endFunc = nf
        # Bot Settings
        self.acceptEdited = False
        self.acceptOlder = False
        self.APITimeout = 100
        # Others
        self.timers = dict()
        self.commands = {"start": default_start, "help": default_help}
        print(time_for_log() + "Bot Created")

    def run(self):
        # Check bot key and receive bot information
        try:
            bot_data = api_request(self.key, 'getMe')
        except ApiError:
            # If raise ApiError means that the token is not valid
            print(time_for_log() + "ApiKey Error: Token is not valid")
            print(time_for_log() + "Shutdown...")
            return
        self.id = bot_data["id"]
        self.username = bot_data["username"]
        self.name = bot_data["first_name"]
        if len(self.timers):
            # For each timer create a different thread
            for t in self.timers:
                threading.Thread(target=self.run_timer, args=(self.timers[t], t), daemon=True).start()
        # Call start function before starting the bot
        call(self.startFunc, {"bot": self})
        print(time_for_log() + "Bot Started")
        try:
            self.run_bot()
        except KeyboardInterrupt:
            print(time_for_log() + "Shutdown...")
            call(self.endFunc, {"bot": self})

    def run_bot(self):
        while True:
            updates = self.get_updates()
            for i in updates:
                # Create a thread for each update
                threading.Thread(target=self.run_update, args=(i,), daemon=True).start()

    def get_updates(self):
        while True:
            param = {
                "offset": self.offset,
                "timeout": self.APITimeout
            }
            # Create a local timeout, just in case of breaking connection
            local_timeout = self.APITimeout + 2
            try:
                updates = api_request(self.key, "getUpdates", param, local_timeout)
            except RequestsError:
                # If connection error, retry in 5 seconds
                print(time_for_log() + "ConnectionError: can't reach Telegram servers. Retry in 5s")
                time.sleep(5)
                continue
            # If the returned array contains at least 1 update
            if len(updates):
                # Increase the offset
                self.offset = updates[-1]["update_id"] + 1
                return updates

    def run_update(self, update):
        # If the update contains a Message
        if "message" in update:
            message = Message(self.key, update["message"])
            chat = message.chat
            possibile_args = {"message": message, "chat": chat, "bot": self}
            # Call processAll function passing all the possible args
            # If Function return something, stop running this update
            if call(self.processAll, possibile_args):
                return
            if message.type == "command":
                try:
                    call(self.commands[message.command], possibile_args)
                except KeyError:
                    # If command is not in list, send message with /help
                    call(command_not_found, possibile_args)
                    return
            else:  # For every message that is not a command
                call(self.processMessage, possibile_args)

    def set_commands(self, command_dict):
        # Used to avoid overwring of default start and help if not included
        for i in command_dict:
            self.commands[i] = command_dict[i]

    def run_timer(self, timer_function, delay):
        while True:
            timer_function()  # TODO: Manage Exception
            time.sleep(calc_new_delay(delay))
