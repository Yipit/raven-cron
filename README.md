Cron-Sentry : error reporting for cron commands
================================================

This is a fork of https://github.com/mediacore/raven-cron. Why the fork?
-------------------------------------------

The original project, raven-cron, didn't preserve stdout neither stderr; it means that if a program outputs anything and exits sucessfully, original raven-cron ignores *all* output.

Another problem is that it doesn't work with commands that accept options, definitively a bug. A [pull request was sent to them](https://github.com/mediacore/raven-cron/pull/4) to support options, but they never said anything, so this fork is currently being maintained by Yipit.


This fork started with the following patches:

* Add support to command options (commit 75ade6d920cbb9f0e84575ca3ed8b568f945727d).
* Preserve stdout and stderr (commit a604f3e0a104ab018fd1c9b35fe989fdd0834a4b).
* Python 3 support, added by @Ian-Foote (commit a0b74c504e748a821fd07236204c52439cc1b1e9).

After the patches above, the project was renamed to Cron-Sentry so that it can become an independent project (get new features, more bugfixes, new PyPI package).

----


Cron-Sentry is a command-line wrapper that reports errors to
[Sentry](http://getsentry.com) if the script exits with an exit status other
than zero.

Install
-------

`pip install cron-sentry`

Usage
-----

```
usage: cron-sentry [-h] [--dsn SENTRY_DSN] [--version] cmd [cmd ...]

Wraps commands and reports failing ones to Sentry.

Positional arguments:
  cmd               The command to run

Optional arguments:
  -h, --help        show this help message and exit
  --dsn SENTRY_DSN  Sentry server address
  --version         show program's version number and exit

The Sentry server address can also be specified through
the SENTRY_DSN environment variable (and the --dns option can be omitted).
```

Example
-------

`crontab -e`
```
SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
cron-sentry my-process --arg arg2
```

License
-------

Original copyright 2013 to MediaCore Technologies (MIT license).
Copyright 2015 to Yipit Inc. (MIT license).
