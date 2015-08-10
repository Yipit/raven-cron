Cron-Sentry: error reporting to [Sentry](https://getsentry.com/) of commands run via cron
================================================

Cron-Sentry is a python command-line wrapper that reports errors to [Sentry](http://getsentry.com) (using [raven](https://github.com/getsentry/raven-python)) if the called script exits with a status other than zero.

Install
-------

`pip install cron-sentry`

Usage
-----

```
usage: cron-sentry [-h] [--dsn SENTRY_DSN] [--version] cmd [cmd ...]

Wraps commands and reports those that fail to Sentry.

Positional arguments:
  cmd               The command to run

Optional arguments:
  -h, --help        show this help message and exit
  --dsn SENTRY_DSN  Sentry server address
  --version         show program's version number and exit

The Sentry server address can also be specified through
the SENTRY_DSN environment variable (and the --dsn option can be omitted).
```

Example
-------

`crontab -e`
```
SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
@reboot cron-sentry ./my-process -q
```


License
-------

This project started life as [raven-cron](https://github.com/mediacore/raven-cron) by MediaCore Technologies.

Original copyright 2013 to MediaCore Technologies (MIT license).
Copyright 2015 to Yipit Inc. (MIT license).
