from setuptools import setup, find_packages

setup(
    name='toTrello',
    version='0.0.5',
    packages=["trello_tool"],
    entry_points={
        "console_scripts": ['toTrello = trello_tool.__main__:main']
    },
    install_requires=[
        "requests==2.25.1"
    ],
    url='https://github.com/LogosFu/trello-tool',
    license='GNU General Public License v3.0',
    author='LogosFu',
    author_email='logosfu@gmail.com',
    description='publish work flow to trello'
)
