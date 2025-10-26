from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="sharesansar-api",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A yfinance-like API for Nepali stock data from ShareSansar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sharesansar-api",
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
    install_requires=requirements,
    keywords="nepal, stocks, sharesansar, finance, trading, nepal-stock-exchange",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/sharesansar-api/issues",
        "Source": "https://github.com/yourusername/sharesansar-api",
    },
)