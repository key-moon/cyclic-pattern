from setuptools import setup

setup(
    name="cyclic-pattern",
    packages=["pattern"],
    version="0.0.1",
    
    license="MIT",

    install_requires=[],

    author="keymoon",

    url="https://github.com/key-moon/cyclic-pattern",

    description="CLI Tools / Python library to generate and search pattern strings useful for finding offsets in Binary Exploitation.",
    entry_points={
        "console_scripts": [
            "pattern = pattern.cli:main",
        ]
    }
)
