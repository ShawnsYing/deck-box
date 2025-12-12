from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deck-box",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A card deck game for task management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/deck-box",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "emoji>=1.6.1",
    ],
    entry_points={
        'console_scripts': [
            'deck-box=deck_box.main:cli',
        ],
    },
)