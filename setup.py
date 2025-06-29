from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geekmoon",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An OSINT tool for searching usernames across social networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/geekmoon",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'geekmoon': ['sites.json'],
    },
    install_requires=[
        "aiohttp",
        "pyppeteer",
        "beautifulsoup4",
        "dateparser",
        "Pillow",
        "exifread",
    ],
    entry_points={
        "console_scripts": [
            "geekmoon=geekmoon.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)