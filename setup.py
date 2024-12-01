from setuptools import setup, find_packages

setup(
    name="browser_amnesia",
    version="1.0.0",
    description="A tool to uninstall browsers and delete their data on macOS.",
    author="A. Aurelions",
    author_email="aaurelions@gmail.com",
    packages=find_packages(),
    py_modules=["browser_amnesia", "browser_amnesia_gui"],
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "browser_amnesia=browser_amnesia:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
    ]
)