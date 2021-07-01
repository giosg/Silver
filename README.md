<h1 align="center">
  <br>
  <a href="https://github.com/s0md3v/Silver"><img src="https://i.ibb.co/bv3rqXs/silver.png" alt="Silver"></a>
  <br>
  Silver - giosg-flavoured edition
  <br>
</h1>

<h4 align="center">Mass Vulnerability Scanner</h4>

<p align="center">
  <a href="https://github.com/s0md3v/Silver/releases">
    <img src="https://img.shields.io/github/release/s0md3v/Silver.svg">
  </a>
  <a href="https://github.com/s0md3v/Silver/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/Silver.svg">
  </a>
</p>

### Introduction

masscan is fast, nmap can fingerprint software and vulners is a huge vulnerability database. Silver is a front-end that allows
complete utilization of these programs by parsing data, spawning parallel processes, caching vulnerability data for faster
scanning over time and much more.

![demo](https://i.ibb.co/nPK8yD8/Untitled.png)

### Features

- Resumable scanning
- Slack notifications
- Multi-core utilization
- Supports: IPs, CIDR & hostnames
- Vulnerability data caching
- Smart Shodan integration* - disabled in giosg edition by now

*\*Shodan integration is optional but when linked, Silver can automatically use Shodan to retrieve service and vulnerability data if a host has a lot of ports open to save resources.
Shodan credits used per scan by Silver can be throttled. The minimum number of ports to trigger Shodan can be configured as well.*

### Setup

#### Downloading Silver

`git clone https://github.com/giosg/Silver`

### Requirements

#### External Programs

- [nmap](https://nmap.org/)
- [masscan](https://github.com/robertdavidgraham/masscan)

```ShellSession
apt update && apt install -y masscan nmap tmux python3 python3-pip
```

#### Python libraries

- psutil
- requests
- jinja2
- slack_sdk
- python-dotenv

Required Python libraries can be installed by executing `pip3 install -r requirements.txt` in `Silver` directory.

#### Configuration

Slack WebHook, Shodan API key and limits can be configured by editing respective variables in `/core/memory.py`

#### Setting up Slack notifications

- Create an incoming webhook, https://example.slack.com/apps/manage/custom-integrations
- Copy the incoming webhook url and export / provide on the CLI the env var SLACK_WEBHOOK containing that URL.

### Usage

#### Before you start

:warning: Run Silver as root and with `python3` i.e. with `sudo python3 silver.py <your input>`

:warning: Silver scans all TCP ports by default i.e. ports `0-65535`. Use `--quick` switch to only scan top ~1000 ports.

#### Running as cron

Most probably you'd like to run the app as cron to have e.g. daily reports.  
This way, do as follows:

1. Create a directory `/secscan`
1. Clone the repo there `git clone -C /secscan https://github.com/giosg/Silver`
1. Create auto update cron config in `/etc/cron.d/silver_autoupdate` (notice the empty newline in the end, that is on purpose!)

    ```cron
    # Seek for updates from github for silver dir each 10m
    */10 * * * * root /usr/bin/git -C /secscan/Silver pull && /usr/bin/pip3 install -r /secscan/Silver/requirements.txt

    ```

1. Create the scanning configuration in `/etc/cron.d/perform_silver_scan`

    ```cron
    SLACK_WEBHOOK="https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXXXXXXXXXXXX"
    # Perform the security scan on schedule each day
    0 8 * * * root /usr/bin/python3 /secscan/Silver/silver.py -i /secscan/targets.txt -C /secscan/results --cleanup-results --rate 2000 --vuln-cache-file /secscan/Silver/db/vulners_cache.json

    ```

1. Now put the IPs or subnets to scan to the `/secscan/targets.txt` and create directory `mkdir /secscan/results`
1. Enjoy the results in your slack channel
