__author__ = 'sf713420'

"""
def configuration(parent_package="", top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('PBR_utilities', parent_package, top_path)

    config.add_subpackage('jim_substraction')

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
"""

from setuptools import setup

setup(name='jim_substraction',
      version='0.1',
      description='Trying installing jim_substraction',
      url='https://github.com/zxh2135645/PBR_utilities',
      author='James (Xinheng) Zhang',
      author_email='zxh2135645@gmail.com',
      license='ucsf-henrylab',
      packages=['jim_substraction'],
      zip_safe=False)