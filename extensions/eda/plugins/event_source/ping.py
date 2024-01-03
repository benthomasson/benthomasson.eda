"""
ping.py

Arguments:
---------
    dest: The destination address to ping.

Example:
-------
    - benthomasson.eda.ping:
        dest: example.com
        count: 5
        delay: 1
        timeout: 10
"""

import asyncio
import aioping
from typing import Any


async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:
    """Generate events with an increasing index i with a limit."""
    delay = args.get("delay", 1)
    dest = args.get("dest")
    timeout = args.get("timeout", 10)
    count = args.get("count", 0)

    i = 0

    while True:
        if count and i >= count:
            break
        try:
            duration = await aioping.ping(dest, timeout=timeout)
            await queue.put({"pong":
                             {"duration": duration,
                              "dest": dest,
                              "seq": i}})
        except TimeoutError:
            await queue.put({"timeout": {"timeout": timeout,
                                         "dest": dest,
                                         "seq": i}})
        await asyncio.sleep(delay)
        i += 1


if __name__ == "__main__":
    # MockQueue if running directly

    class MockQueue:
        """A fake queue."""

        async def put(self: "MockQueue", event: dict) -> None:
            """Print the event."""
            print(event)  # noqa: T201

    asyncio.run(main(MockQueue(), {"dest": "127.0.0.1", "count": 1}))
