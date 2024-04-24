"""
This module provides functionality for interacting with Webex Teams.

The main class is `WebexBotManager`, which encapsulates the logic for creating a bot and sending notifications.

This module is based on the idea from: https://github.com/fbradyirl/webex_bot
"""

import logging
from webexteamssdk import WebexTeamsAPI
from webex_bot.webex_bot import WebexBot
from llm_agent.webex_chat.ai_command import AiCommand
from llm_agent.config.global_settings import (
    WEBEX_APPROVED_USERS_MAIL,
    WEBEX_TEAMS_ACCESS_TOKEN,
)

logging.getLogger().setLevel(logging.ERROR)


def get_webex_room_id(webex_api: WebexTeamsAPI) -> str:
    """
    Retrieve the ID of the first room that contains the specified username in its title.

    TODO: This is a hacky way, only works if there is only one room with the boot
    """
    all_rooms = webex_api.rooms.list()
    room_id = [room.id for room in all_rooms]
    return room_id[0]


class WebexBotManager:
    """
    This class encapsulates the logic for creating a Webex bot and sending notifications.
    """

    def __init__(self):

        self.bot = self._create_bot()
        self.webex_api = self._initialize_webex_api()
        self._add_commands()

    def _create_bot(self) -> WebexBot:
        """
        Create a new Webex bot.

        :return: The created Webex bot.
        """
        return WebexBot(
            teams_bot_token=WEBEX_TEAMS_ACCESS_TOKEN,
            approved_users=[WEBEX_APPROVED_USERS_MAIL],
            bot_name="my-buddy",
            include_demo_commands=False,
        )

    def _initialize_webex_api(self) -> WebexTeamsAPI:
        """
        Get the Webex API object.

        :return: The Webex API object.
        """
        return WebexTeamsAPI(access_token=WEBEX_TEAMS_ACCESS_TOKEN)

    def _add_commands(self) -> None:
        self.bot.commands.clear()
        self.bot.add_command(AiCommand())
        self.bot.help_command = AiCommand()

    def send_notification(self, message: str) -> None:
        """
        Send a message to a specified room.

        :param message: The message to send.
        """
        room_id = get_webex_room_id(self.webex_api)
        self.webex_api.messages.create(roomId=room_id, markdown=message)

    def run(self):
        """
        Start the bot process.
        """
        self.bot.run()


if __name__ == "__main__":
    webex_bot_manager = WebexBotManager()
    webex_bot_manager.run()
