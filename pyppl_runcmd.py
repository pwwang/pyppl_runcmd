"""Add annotation to PyPPL processes"""
import cmdy
from pyppl.plugin import hookimpl
from pyppl.logger import Logger
from pyppl.config import config

__version__ = "0.0.3"

logger = Logger(plugin='runcmd') # pylint: disable=invalid-name

config.config.runcmd_failfast = True
config.config.runcmd_pre = ''
config.config.runcmd_post = ''

@hookimpl
def logger_init(logger):  # pylint: disable=redefined-outer-name
    """Add log levels"""
    logger.add_level('CMDOUT')
    logger.add_level('CMDERR', 'ERROR')

@hookimpl
def proc_init(proc):
    """Add config for process"""
    proc.add_config('runcmd_failfast', default=True)
    proc.add_config('runcmd_pre', default='', runtime='ignore')
    proc.add_config('runcmd_post', default='', runtime='ignore')


def _runcmd(cmd, proc):
    """Run a command"""
    cmdstr = proc.template(cmd,
                           **proc.envs).render(dict(proc=proc, args=proc.args))
    logger.info('Running command from pyppl_runcmd ...', proc=proc.id)
    logger.debug('  ' + cmdstr, proc=proc.id)
    cmd = cmdy.bash(c=cmdstr, _raise=False).iter
    for line in cmd:
        logger.cmdout(line, proc=proc.id)

    cmd.wait()
    if cmd.rc == 0:
        return True
    for line in cmd.stderr.splitlines():
        logger.cmderr(line, proc=proc.id)
    return False


@hookimpl
def proc_prerun(proc):  # pylint: disable=inconsistent-return-statements
    """Run pre-command"""
    if proc.config.runcmd_pre:
        ret = _runcmd(proc.config.runcmd_pre, proc)
        if proc.config.runcmd_failfast and not ret:
            logger.error(
                "Process will not be running due to failure of pre-command.")
            return False


@hookimpl
def proc_postrun(proc, status):
    """Run post-command"""
    if status == 'succeeded' and proc.config.runcmd_post:
        _runcmd(proc.config.runcmd_post, proc)
