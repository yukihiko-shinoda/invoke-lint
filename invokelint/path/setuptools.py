"""Call Setuptools API to list packages."""
import os
from pathlib import Path
from typing import cast, List

from setuptools.discovery import ConfigDiscovery
from setuptools.dist import Distribution


class Setuptools:
    """To access dist."""

    def __init__(self) -> None:
        distribution = Distribution()
        distribution.parse_config_files()
        self.config_discovery = ConfigDiscovery(distribution)
        self.config_discovery()

    @property
    def packages(self) -> List[str]:
        return cast(List[str], self.config_discovery.dist.packages)

    @property
    def project_root(self) -> Path:
        return Path(self.config_discovery.dist.src_root or os.curdir).resolve()
