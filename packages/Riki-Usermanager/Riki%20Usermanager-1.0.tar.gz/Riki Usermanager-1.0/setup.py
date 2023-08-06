from setuptools import find_packages, setup
from pathlib import Path

setup(
    name="Riki Usermanager",
    version="1.0",
    description="User Manager utilities for the Riki",
    author="Arseny Poga",
    author_email="pogaa1@nku.edu",
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=Path("README.md").read_text(),
    )
