import asyncio
from typing import Any, AsyncContextManager, AsyncGenerator, AsyncIterator, Awaitable, Callable, Coroutine, Generator, Iterable, Iterator, TypeVar, Union


def iter_over_async(ait: AsyncIterator[Any], asyncEventLoop: asyncio.AbstractEventLoop = asyncio.get_event_loop()) -> Iterator[Any]:
    """This function will take an async iterator and return a sync iterator that will iterate over the async iterator."""
    ait = ait.__aiter__()

    async def get_next():
        try:
            obj = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None
    while True:
        done, obj = asyncEventLoop.run_until_complete(get_next())
        if done:
            break
        yield obj


def sync_generator(asyncGen, asyncEventLoop=asyncio.get_event_loop()):
    """This function will take an async generator and return a sync generator that will iterate over the async generator."""
    return iter_over_async(asyncGen, asyncEventLoop)
