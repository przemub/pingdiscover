# pingdiscover

A simple ping discovery tool using [aioping](https://github.com/stellarbit/aioping). The output is very similar to `nmap -sn subnet`.

## Usage

```
usage: pingdiscover.py [-h] --concurrency CONCURRENCY [--timeout TIMEOUT]
                       [--verbose]
                       subnet

Perform a ping-based concurrent network scan

positional arguments:
  subnet                The subnet to scan in format network address + mask,
                        for example 192.168.0.0/16.

optional arguments:
  -h, --help            show this help message and exit
  --concurrency CONCURRENCY
                        number of concurrent hosts that are pinged at the same
                        time
  --timeout TIMEOUT     number of seconds after giving up on pinging a host
                        (default 5 s)
  --verbose, -v         increase output verbosity
```

### Example output

```
[prem@prem pingdiscover]$ docker run --rm -it pingdiscover 192.168.1.0/24 --concurrency 30 --timeout 1
192.168.1.1 responded after 0.0079 ms
192.168.1.102 responded after 0.0072 ms
Scanned subnet 192.168.1.0/24 in 9.14 s. 2 hosts are up, 252 hosts are down.
```

## Requirements
* Python 3.7+
* aioping

## Run

You can run pingdiscover.py using your system interpreter (`python pingdiscover.py`) once you install the requirements (`make system`).

There are also several virtual environments you can use.

### venv
```bash
make venv
python pingdiscover.py --help
exit # once you're done
```

### Docker
```bash
make docker
docker run --rm -it pingdiscover --help
```

### Conda
```bash
make conda
python pingdiscover.py --help
exit # once you're done
```
