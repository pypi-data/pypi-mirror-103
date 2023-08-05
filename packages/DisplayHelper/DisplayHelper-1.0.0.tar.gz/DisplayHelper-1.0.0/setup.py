from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DisplayHelper",
    version='1.0.0',
    url='https://gitlab.zoios.net/112-online/alarmdisplay-helper',
    license='CC BY-NC-ND 4.0',
    maintainer='mzimmer',
    maintainer_email='mzimmer@zoios.net',
    description='Python REST-Api for the Alarmdisplay software from 112-Online.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Feuerwehr, 112-Online, Alarmdisplay',
    packages=find_packages(exclude=('tests')),
    entry_points = {
        "console_scripts": [
            "hilt = DisplayHelper.__main__:main"
        ]
    },
    python_requires='>=3',
    install_requires='Flask'
)
