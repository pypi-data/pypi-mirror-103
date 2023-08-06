from setuptools import setup
from multiplication_table import __version__ as current_version

setup(
  name='multiplication_table',
  version=current_version,
  description='Visualisation of the modular multiplication table',
  url='https://github.com/goujilinouhaila-coder/Multiplication_table.git',
  author='SOBOLAK Valérian, GOUJILI Nouhaila, SENE Assane, BERRANDOU Assia',
  author_email="valerian.sobolak@etu.umontpellier.fr, nouhaila.goujili@etu.umontpellier.fr, assane.sene@etu.umontpellier.fr, assia.berrandou@etu.umontpellier.fr",
  license='M1 MIND/BIOSTAT',
  packages=['multiplication_table', 'multiplication_table.process_math',
            'multiplication_table.process_vis'],
  zip_safe=False
)
