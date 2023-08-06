from setuptools import setup
from factodiagrams import __version__ as current_version

setup(
  name='factodiagrams',
  version=current_version,
  description='Visualization of prime factorization',
  url='https://github.com/nguyenlouis/number-factorization-diagrams',
  author='Bouthayna Hayou, Juliette Lidoine, Louis Nguyen, Sidy Sow.',
  author_email='bouthayna.hayou@etu.umontpellier.fr , juliette.lidoine@etu.umontpellier.fr',
  license='MIT',
  packages=['factodiagrams','factodiagrams.preprocess', 'factodiagrams.vis'],
  zip_safe=False
)