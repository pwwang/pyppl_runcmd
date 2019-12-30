# pyppl_runcmd

Allowing to run local command before and after each process for PyPPL

## Installation
```shell
pip install pyppl_runcmd
```

## Usage

```python
pXXX.config.runcmd_pre = "bedtools --version"
# if bedtools is not installed, error will be raised.
pXXX.config.runcmd_post = "# some cleanup code"
```

Note: This is different from setting prescript or postscript in runner configurations:

1. These commands are only running locally. The commands set in runner configuration are running with the given runner.
2. These commands are only running by each process. The commands set in runner configuration are running by each job.
