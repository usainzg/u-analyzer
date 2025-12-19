"""Setup configuration for u-analyzer."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="u-analyzer",
    version="0.1.0",
    description="A fitness data analyzer for comparing and analyzing workout data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="U-Analyzer Contributors",
    url="https://github.com/usainzg/u-analyzer",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "fitparse>=1.2.0",
        "gpxpy>=1.5.0",
        "lxml>=4.9.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
