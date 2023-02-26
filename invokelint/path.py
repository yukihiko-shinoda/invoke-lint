"""Paths."""
import os
from pathlib import Path

from setuptools.discovery import ConfigDiscovery
from setuptools.dist import Distribution

config_discovery = ConfigDiscovery(Distribution())
config_discovery()
project_root = Path(config_discovery.dist.src_root or os.curdir).resolve()
SOURCE_DIRS = config_discovery.dist.packages
TASKS_PY = "tasks.py"
TEST_DIR = "tests"
PYTHON_DIRS = [*SOURCE_DIRS, TASKS_PY, TEST_DIR]
