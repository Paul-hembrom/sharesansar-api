from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sharesansar-api",
    version="0.3.0",  # Bump version
    author="Paul Hembrom",
    author_email="your.email@example.com",  # Update with your real email
    description="An API for Nepali stock data from ShareSansar for NEPSE Market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Paul-hembrom/sharesansar-api",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.3.0",
        "beautifulsoup4>=4.9.0",
        "lxml>=4.6.0"
    ],
    keywords="nepal, stocks, sharesansar, finance, trading, nepal-stock-exchange, nepse",
    project_urls={
        "Bug Reports": "https://github.com/Paul-hembrom/sharesansar-api/issues",
        "Source": "https://github.com/Paul-hembrom/sharesansar-api",
    },
)