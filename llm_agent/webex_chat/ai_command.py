from webex_bot.models.command import Command
from webexteamssdk.models.cards.actions import OpenUrl
from webex_bot.formatting import quote_info, quote_warning
from webex_bot.models.response import response_from_adaptive_card
from webexteamssdk.models.cards import (
    Colors,
    TextBlock,
    FontWeight,
    FontSize,
    Column,
    AdaptiveCard,
    ColumnSet,
    Image,
    ImageSize,
    Fact,
    FactSet,
)

from logging_config.main import setup_logging
from webex_chat.chat_api_client import send_message_to_chat_api

logger = setup_logging()


OPENAI_ICON = "https://github.com/fbradyirl/fbradyirl.github.io/raw/master/static/img/OpenAI_logo-100x70-rounded.png"
CARD_CALLBACK_MORE_INFO = "help"


class AiCommand(Command):
    def __init__(self):
        super().__init__(
            command_keyword="my-buddy",
            help_message="Interact with an AI based on OpenAI's GPT-3.",
            chained_commands=[AiMoreInfoCallback()],
        )

    def execute(self, message, attachment_actions, activity):
        logger.info(f"Got message prompt from user: {message}. Reviewing ")
        response = send_message_to_chat_api(message=message)
        logger.info(f"OpenAI response: {response}")
        return [quote_info(response)]


class AiMoreInfoCallback(Command):
    def __init__(self):
        super().__init__(
            card_callback_keyword=CARD_CALLBACK_MORE_INFO,
            delete_previous_message=False,
        )

    def execute(self, message, attachment_actions, activity):
        bot_version_info = "Ask me something 🤙"

        bot_facts = []

        heading = TextBlock(
            "LLM my-buddy",
            weight=FontWeight.BOLDER,
            wrap=True,
            size=FontSize.LARGE,
        )
        subtitle = TextBlock(
            bot_version_info,
            wrap=True,
            size=FontSize.SMALL,
            color=Colors.LIGHT,
        )

        image = Image(url=OPENAI_ICON, size=ImageSize.AUTO)

        header_column = Column(items=[heading, subtitle], width=2)
        header_image_column = Column(
            items=[image],
            width=1,
        )

        max_tokens_info_textblock = TextBlock(
            "I'm an AI that can connect to network devices and run commands.",
            wrap=True,
            size=FontSize.SMALL,
            color=Colors.LIGHT,
        )

        temp_info_textblock = TextBlock(
            "**I'm here to help**",
            wrap=True,
            size=FontSize.SMALL,
            color=Colors.LIGHT,
        )

        card = AdaptiveCard(
            body=[
                ColumnSet(columns=[header_column, header_image_column]),
                FactSet(facts=bot_facts),
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                temp_info_textblock,
                                max_tokens_info_textblock,
                            ],
                            width=2,
                        )
                    ]
                ),
            ],
            actions=[
                OpenUrl(url="https://platform.openai.com", title="openai.com")
            ],
        )

        return response_from_adaptive_card(card)
