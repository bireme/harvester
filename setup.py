from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

README_FILEPATH = os.path.join(here, 'README.txt')
#CHANGES_FILEPATH = os.path.join(here, 'CHANGES.txt')

README = open(README_FILEPATH).read()
#CHANGES = open(CHANGES_FILEPATH).read()

requirements = ['pyoai', 'argparse']
additional_files = [README_FILEPATH]


setup(name='harvester', version='0.0.0',
      packages=find_packages(),
      long_description=README,
      author="BIREME/OPAS/OMS",
      author_email="desenvolvedores@listas.bireme.br",
      url="http://reddes.bvsalud.org/",
      download_url='https://github.com/rafaelnovello/harvester',
      license="LGPL v2.1 (http://www.gnu.org/licenses/lgpl-2.1.txt)",
      install_requires=requirements,
      description='Harvester is an OAI-PMH client to save the harvest result in file system like a xml file.',
      data_files=additional_files,
    )
