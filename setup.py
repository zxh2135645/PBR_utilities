__author__ = 'sf713420'

def configuration(parent_package="", top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('PBR_utilities', parent_package, top_path)

    config.add_subpackage('jim_substraction')

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())