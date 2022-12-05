# Cerberus

CLI utility for Twitter to take the most recent direct message and validate it for being a likely spam message.

## Methodology

This utility checks the most recently received direct message and checks its attributes with those of known spam accounts. If it matches, the direct message will be deleted.

## Installation

Cerberus can be ran directly through the `cli.py` file in `/cerberus`. [Tweepy](https://www.tweepy.org) is a required dependency. Cerberus takes four arguments. The command for checking the most recent direct message can be seen below:

```
python cerberus/cli.py check --consumer-key <consumer key> --consumer-secret <consumer secret> --access-token <access token> --access-token-secret <access token secret>
```

The four arguments can obtained through the [Twitter Developer panel](https://developer.twitter.com). The access token and access token secret must be created with access to direct messages, and for the tool to delete direct messages, the project it's in needs to have Elevated access.