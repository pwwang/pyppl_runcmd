import pytest
import cmdy
import pyppl_runcmd
from pathlib import Path
from pyppl import Proc
from pyppl.config import config
from pyppl.logger import logger, LEVEL_GROUPS

# def test_setup():
# 	pyppl_runcmd.setup(config)
# 	assert config.config.runcmd_pre == ''
# 	assert config.config.runcmd_post == ''
# 	assert config.config.runcmd_failfast is True

def test_logger_init():
	pyppl_runcmd.logger_init(logger)
	assert 'CMDOUT' in LEVEL_GROUPS['INFO']
	assert 'CMDERR' in LEVEL_GROUPS['ERROR']

def test_proc_init():
	pProcInit = Proc()
	pyppl_runcmd.proc_init(pProcInit)
	assert pProcInit.config.runcmd_pre == ''
	assert pProcInit.config.runcmd_post == ''
	assert pProcInit.config.runcmd_failfast is True

def test_runcmd(caplog):
	pRuncmd = Proc()

	ret = pyppl_runcmd._runcmd('__nosuchcmd__', pRuncmd)
	assert ret is False
	assert 'command not found' in caplog.text
	caplog.clear()

	ret = pyppl_runcmd._runcmd('ls ' + Path(__file__).parent.resolve().as_posix(), pRuncmd)
	assert ret is True
	assert Path(__file__).name in caplog.text

def test_prerun(caplog):
	pPreRun = Proc()
	pPreRun.config.runcmd_pre = '__nosuchcmd__'
	ret = pyppl_runcmd.proc_prerun(pPreRun)
	assert ret is False
	assert 'Process will not be running due to failure of pre-command.' in caplog.text
	caplog.clear()

	pPreRun.config.runcmd_failfast = False
	ret = pyppl_runcmd.proc_prerun(pPreRun)
	assert ret is None
	assert 'Process will not be running due to failure of pre-command.' not in caplog.text

def test_postrun(caplog):
	pPostRun = Proc()
	pPostRun.config.runcmd_post = 'ls ' + Path(__file__).parent.resolve().as_posix()
	pyppl_runcmd.proc_postrun(pPostRun, 'succeeded')
	assert Path(__file__).name in caplog.text
