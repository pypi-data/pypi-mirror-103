import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stonky-bot",
    version="0.0.4",
    author="Moris Doratiotto",
    author_email="moris.doratiotto@gmail.com",
    description="A python crypto trading bot for Kraken",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mortafix/Stonky",
    packages=setuptools.find_packages(),
    install_requires=[
        "krakenex",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    keywords=["bot", "trading", "crypto", "kraken"],
    package_data={
        "stonky": [
            "utils.py",
            "strategies/mean_trend.py",
            "strategies/loss_rebuy.py",
        ]
    },
    entry_points={"console_scripts": ["stonky=stonky.stonky:main"]},
)
