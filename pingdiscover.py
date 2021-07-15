import argparse
import asyncio
import time

from ipaddress import IPv4Network, IPv4Address
from socket import AddressFamily

import aioping


def main():
    """
    The synchronous part of the program, which parses the arguments,
    prepares the futures and starts the actual ping scan asynchronously.
    """
    # Create an arguments parser
    parser = argparse.ArgumentParser(
        description="Perform a ping-based concurrent network scan"
    )
    parser.add_argument(
        "subnet",
        type=IPv4Network,
        help="The subnet to scan in format network address + mask, "
             "for example 192.168.0.0/16.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        help="number of concurrent hosts that are pinged at the same time",
        required=True,
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="number of seconds after giving up on pinging a host "
             "(default 5 s)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="increase output verbosity",
        action="store_true",
    )

    args = parser.parse_args()

    async def main_routine():
        start = time.time()

        semaphore = asyncio.Semaphore(args.concurrency)
        futures = [
            scan_host(host, semaphore, args.timeout, args.verbose)
            for host in args.subnet.hosts()
        ]
        results = await asyncio.gather(*futures)

        elapsed = time.time() - start
        responded_count = sum(1 for result in results if result is True)
        timed_out_count = sum(1 for result in results if result is False)

        print(
            f"Scanned subnet {args.subnet} in {elapsed:.2f} s."
            f"{responded_count} hosts are up, {timed_out_count} hosts are down."
        )

    # Start the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_routine())


async def scan_host(
    host: IPv4Address,
    semaphore: asyncio.Semaphore,
    timeout: int,
    verbose: bool,
):
    """
    Locks the "semaphore" and tries to ping "host" with timeout "timeout" s. 
    Prints out the result of the ping to the standard output.
    """
    async with semaphore:
        try:
            delay = await aioping.ping(
                str(host), timeout, family=AddressFamily.AF_INET
            )
            print(f"{host} responded after {delay:.4f} ms")
            return True
        except TimeoutError:
            if verbose:
                print(f"{host} has not responded")
            return False
        except OSError as error:
            if verbose:
                print(
                    f"Ping to host {host} failed for the following reason: {error}"
                )
            return False


if __name__ == "__main__":
    main()

