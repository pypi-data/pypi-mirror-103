from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='syrup',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/xqk/syrup',
    license='MIT',
    author='xqk',
    author_email='xiaqiankun@outlook.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "fastapi==0.63.0",
        "uvicorn==0.13.4",
        "PyYaml==5.4.1",
        "PyPika==0.48.1",
        "asyncpg==0.22.0",
        "aiosqlite==0.17.0",
        "pytz==2021.1",
        "aiohttp==3.7.4.post0",
        "astroid==2.5.3",
        "pylint==2.7.4",
        "Quart==0.14.1",
        "sanic==21.3.4",
        "asynctest==0.13.0",
        "iso8601==0.1.14",
        "Mako==1.1.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)