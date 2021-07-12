Cron-Sentry: error reporting to `Sentry <https://getsentry.com/>`__ of commands run via cron
============================================================================================

Cron-Sentry is a python command-line wrapper that reports errors to `Sentry <http://getsentry.com>`__ (using `raven <https://github.com/getsentry/raven-python>`__)
if the called script exits with a status other than zero.

Install
-------

``pip install cron-sentry``

Usage
-----

::

    $ cron-sentry --help
    usage: cron-sentry [-h] [--dsn SENTRY_DSN] [-M STRING_MAX_LENGTH] [--quiet] [--report-all] [--version] cmd [arg ...]

    Wraps commands and reports those that fail to Sentry.

    positional arguments:
      cmd                   The command to run

    optional arguments:
      -h, --help            show this help message and exit
      --dsn SENTRY_DSN      Sentry server address
      -M STRING_MAX_LENGTH, --string-max-length STRING_MAX_LENGTH, --max-message-length STRING_MAX_LENGTH
                            The maximum characters of a string that should be sent
                            to Sentry (defaults to 4096)
      -q, --quiet           Suppress all command output
      --version             show program's version number and exit
      --report-all          Report to Sentry even if the task has succeeded
      --output-all          Send all stderr/stdout to stdout regardless of max
                            message length

    The Sentry server address can also be specified through the SENTRY_DSN
    environment variable (and the --dsn option can be omitted).

It's possible to send extra information to Sentry via environment
variables (prefix them with ``CRON_SENTRY_EXTRA_``), such as:

::

    $ export CRON_SENTRY_EXTRA_env=production
    $ cron-sentry my-program

Example
-------

``$ crontab -e``

::

    SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
    0 4 * * * cron-sentry my-process --arg arg2

Notes
-----

- If your command outputs Unicode, you may need to signal to python that stdin/stdout/stderr are UTF-8 encoded:

::

    PYTHONIOENCODING=utf-8
    SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
    0 4 * * * cron-sentry my-process --arg arg2

License
-------

This project started life as `raven-cron <https://github.com/mediacore/raven-cron>`__ by MediaCore Technologies.

Original copyright 2013 to MediaCore Technologies (MIT license).
Copyright 2015 to Yipit Inc. (MIT license).
