import sys
from getpass import getuser
from os import getenv, path, SEEK_END
from raven import Client
from subprocess import Popen, PIPE, call
from tempfile import TemporaryFile
from argparse import ArgumentParser, REMAINDER
from sys import argv
from time import time
from .version import VERSION


# More info:
# * https://github.com/getsentry/sentry/blob/b44cdaa27e1ba3f27d217f7f7f45efaa5e742d0f/src/sentry/conf/server.py#L742-L744
# * https://github.com/getsentry/sentry/blob/5d6b0fef0f4446128730d9c1f5940e7f071a4509/src/sentry/utils/safe.py#L68-L76
# the value is 4094 because of `_size += 2` in the code linked above
DEFAULT_MAX_MESSAGE_LENGTH = 4094


parser = ArgumentParser(
    description='Wraps commands and reports those that fail to Sentry.',
    epilog=('The Sentry server address can also be specified through ' +
            'the SENTRY_DSN environment variable ' +
            '(and the --dsn option can be omitted).'),
    usage='cron-sentry [-h] [--dsn SENTRY_DSN] [-M MAX_MESSAGE_LENGTH] [--quiet] [--version] cmd [arg ...]',
)
parser.add_argument(
    '--dsn',
    metavar='SENTRY_DSN',
    default=getenv('SENTRY_DSN'),
    help='Sentry server address',
)

parser.add_argument(
    '-M', '--max-message-length',
    type=int,
    default=DEFAULT_MAX_MESSAGE_LENGTH,
    help='The maximum characters of a string that should be sent to Sentry (defaults to {0})'.format(DEFAULT_MAX_MESSAGE_LENGTH),
)
parser.add_argument(
    '-q', '--quiet',
    action='store_true',
    default=False,
    help='suppress all command output'
)
parser.add_argument(
    '--version',
    action='version',
    version=VERSION,
)
parser.add_argument(
    'cmd',
    nargs=REMAINDER,
    help='The command to run',
)

def update_dsn(opts):
    """Update the Sentry DSN stored in local configs

    It's assumed that the file contains a DSN endpoint like this:
    https://public_key:secret_key@app.getsentry.com/project_id

    It could easily be extended to override all settings if there
    were more use cases.
    """

    homedir = path.expanduser('~%s' % getuser())
    home_conf_file = path.join(homedir, '.cron-sentry')
    system_conf_file = '/etc/cron-sentry.conf'

    conf_precedence = [home_conf_file, system_conf_file]
    for conf_file in conf_precedence:
        if path.exists(conf_file):
            with open(conf_file, "r") as conf:
                opts.dsn = conf.read().rstrip()
            return

def run(args=argv[1:]):
    opts = parser.parse_args(args)

    # Command line takes precendence, otherwise check for local configs
    if not opts.dsn:
        update_dsn(opts)

    if opts.cmd:
        # make cron-sentry work with both approaches:
        #
        #     cron-sentry --dsn http://dsn -- command --arg1 value1
        #     cron-sentry --dsn http://dsn command --arg1 value1
        #
        # see more details at https://github.com/Yipit/cron-sentry/pull/6
        if opts.cmd[0] == '--':
            cmd = opts.cmd[1:]
        else:
            cmd = opts.cmd
        runner = CommandReporter(
            cmd=cmd,
            dsn=opts.dsn,
            max_message_length=opts.max_message_length,
            quiet=opts.quiet
        )
        sys.exit(runner.run())
    else:
        sys.stderr.write("ERROR: Missing command parameter!\n")
        parser.print_usage()
        sys.exit(1)


class CommandReporter(object):
    def __init__(self, cmd, dsn, max_message_length, quiet=False):
        self.dsn = dsn
        self.command = cmd
        self.max_message_length = max_message_length
        self.quiet = quiet

    def run(self):
        start = time()

        with TemporaryFile() as stdout:
            with TemporaryFile() as stderr:
                exit_status = call(self.command, stdout=stdout, stderr=stderr)

                last_lines_stdout = self._get_last_lines(stdout)
                last_lines_stderr = self._get_last_lines(stderr)

                if exit_status > 0:
                    elapsed = int((time() - start) * 1000)
                    self.report_fail(exit_status, last_lines_stdout, last_lines_stderr, elapsed)

                if not self.quiet:
                    sys.stdout.write(last_lines_stdout)
                    sys.stderr.write(last_lines_stderr)

                return exit_status

    def report_fail(self, exit_status, last_lines_stdout, last_lines_stderr, elapsed):
        if self.dsn is None:
            return

        message = "Command \"%s\" failed" % (self.command,)

        client = Client(dsn=self.dsn, string_max_length=-1)

        client.captureMessage(
            message,
            data={
                'logger': 'cron',
            },
            extra={
                'command': self.command,
                'exit_status': exit_status,
                'last_lines_stdout': last_lines_stdout,
                'last_lines_stderr': last_lines_stderr,
            },
            time_spent=elapsed
        )

    def _get_last_lines(self, buf):
        buf.seek(0, SEEK_END)
        file_size = buf.tell()
        if file_size < self.max_message_length:
            buf.seek(0)
            last_lines = buf.read().decode('utf-8')
        else:
            buf.seek(-(self.max_message_length - 3), SEEK_END)
            last_lines = u'...' + buf.read().decode('utf-8')
        return last_lines
