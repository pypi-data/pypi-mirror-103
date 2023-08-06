"""
The PDA ("main" class) for the :mod:`royalnet_telethon` frontend.
"""

from __future__ import annotations
import royalnet.royaltyping as t

import logging
import royalnet.engineer as engi
import enum
import discord as d

from .bullet.projectiles import DiscordMessageReceived, DiscordMessageEdited, DiscordMessageDeleted

log = logging.getLogger(__name__)


class DiscordpyPDAMode(enum.Enum):
    """
    .. todo:: Document this.
    """

    GLOBAL = enum.auto()
    CHANNEL = enum.auto()
    USER = enum.auto()
    CHANNEL_USER = enum.auto()


class DiscordpyPDAImplementation(engi.ConversationListImplementation):
    """
    .. todo:: Document this.
    """

    @property
    def namespace(self):
        return "discordpy"

    def __init__(self, name: str, bot_token: str,
                 mode: DiscordpyPDAMode = DiscordpyPDAMode.CHANNEL_USER):

        super().__init__(name=name)

        self.mode: DiscordpyPDAMode = mode
        """
        The mode to use for mapping dispensers.
        """

        self.bot_token: str = bot_token
        """
        .. todo:: Document this.
        """

        self.client: d.Client = d.Client()
        """
        .. todo:: Document this.        
        """

    def _register_events(self):
        """
        .. todo:: Document this.
        """

        self.log.info("Registering Discord.py events...")
        self.log.debug("Registering on_message...")
        self.client.on_message = self._on_message
        self.log.debug("Registering on_message_edit...")
        self.client.on_message_edit = self._on_message_edit
        self.log.debug("Registering on_message_delete...")
        self.client.on_message_delete = self._on_message_delete

    def _determine_key(self, message: d.Message):
        """
        .. todo:: Document this.
        """

        if self.mode == DiscordpyPDAMode.GLOBAL:
            return None
        elif self.mode == DiscordpyPDAMode.USER:
            author: d.User = message.author
            return author.id
        elif self.mode == DiscordpyPDAMode.CHANNEL:
            channel: t.Union[d.DMChannel, d.TextChannel] = message.channel
            return channel.id
        elif self.mode == DiscordpyPDAMode.CHANNEL_USER:
            author: d.User = message.author
            channel: t.Union[d.DMChannel, d.TextChannel] = message.channel
            return author.id, channel.id
        else:
            raise TypeError("Invalid mode")

    async def _on_message(self, message: d.Message):
        """
        .. todo:: Document this.
        """

        await self.put(
            key=self._determine_key(message=message),
            projectile=DiscordMessageReceived(event=message)
        )

    async def _on_message_edit(self, message: d.Message):
        """
        .. todo:: Document this.
        """

        await self.put(
            key=self._determine_key(message=message),
            projectile=DiscordMessageEdited(event=message)
        )

    async def _on_message_delete(self, message: d.Message):
        """
        .. todo:: Document this.
        """

        await self.put(
            key=self._determine_key(message=message),
            projectile=DiscordMessageDeleted(event=message)
        )

    async def run(self) -> t.NoReturn:
        await self.client.login(token=self.bot_token)
        await self.client.connect(reconnect=True)


__all__ = (
    "DiscordpyPDAImplementation",
)
