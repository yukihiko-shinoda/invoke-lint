"""Paths."""
import os
from pathlib import Path

from setuptools.discovery import ConfigDiscovery
from setuptools.dist import Distribution

distribution = Distribution()
distribution.parse_config_files()
config_discovery = ConfigDiscovery(distribution)
config_discovery()
project_root = Path(config_discovery.dist.src_root or os.curdir).resolve()
SOURCE_DIRS = config_discovery.dist.packages
TASKS_PY = "tasks.py"
TEST_DIR = "tests"
PYTHON_DIRS = [*SOURCE_DIRS, TASKS_PY, TEST_DIR]
