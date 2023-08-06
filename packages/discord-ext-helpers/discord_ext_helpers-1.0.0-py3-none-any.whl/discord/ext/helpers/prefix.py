from re import compile, Pattern
from typing import Callable
from functools import lru_cache

from discord import Message
from discord.ext.commands import Bot


@lru_cache(maxsize=None)  # TODO: work out why i get an error when importing functools' regular cache
def _get_prefix_regex(bot: Bot, force_space: bool) -> Pattern:
    return compile(r"^<@!?" + str(bot.user.id) + (r"> " if force_space else r"(> |>)"))

def when_mentioned_or_coro(coro: Callable, force_space: bool = False) -> Callable:
    """Generate an async function allowing the use of a coroutine as the prefix or when the bot is mentioned.

    Args:
        coro (Callable): The custom prefix async function.
        force_space (bool): Whether to force having a space after the mention.
    """

    async def get_prefix(bot: Bot, message: Message) -> str:
        """Get the bot's prefix."""

        pattern = _get_prefix_regex(bot, force_space)

        print(pattern, message.content)

        if match := pattern.match(message.content):
            return match.group()

        return await coro(bot, message)

    return get_prefix
