from setuptools import setup, find_packages
from collections import OrderedDict

long_description="""
This is a minimal engine for the Battlehack20 game.
It lacks the secure of the original engine, but makes up for it
by running 30 times faster.
Read more at the Battlehack website: https://bh2020.battlecode.org.
"""

setup(name='battlehack20-minimal',
      version="1.0.2",
      description='Battlehack 2020 fancy viewer.',
      author='cooljoseph',
      long_description=long_description,
      author_email='camacho.joseph@gmail.com',
      url="https://bh2020.battlecode.org",
      license='GNU General Public License v3.0',
      packages=find_packages(),
      project_urls=OrderedDict((
          ('Code', 'https://github.com/programjames/battlehack2020/battlehack20-minimalengine'),
          ('Documentation', 'https://github.com/programjames/battlehack2020/battlehack20-minimalengine')
      )),
      install_requires=[],
      python_requires='>=3, <3.8',
      zip_safe=False,
      include_package_data=True
)
