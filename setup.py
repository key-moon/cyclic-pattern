from setuptools import setup

setup(
    name="cyclic-pattern",
    packages=["cyclicpattern"],
    version="0.0.2",
    
    license="MIT",

    install_requires=[],

    author="keymoon",

    url="https://github.com/key-moon/cyclic-pattern",

    description="CLI Tools / Python library to generate and search pattern strings useful for finding offsets in Binary Exploitation.",
    entry_points={
        "console_scripts": [
            "pattern = cyclicpattern.cli:main",
        ]
    }
)
