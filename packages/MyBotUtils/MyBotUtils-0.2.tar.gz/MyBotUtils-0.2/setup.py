import setuptools

requirements = [
    "discord.py>=1.6",
    "toml",
    "asyncpg",
    "aioredis",
    "aiohttp",
]

setuptools.setup(
    name="MyBotUtils",
    version="0.2",
    author="Megan",
    author_email="obama@gmail.com",
    description="Simple discord.py bot utils for personal use",
    long_description="This literally only exists so I dont have to git pull everytime I update something",
    url="https://github.com/aaaMeganaaa/botbase",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=requirements
)