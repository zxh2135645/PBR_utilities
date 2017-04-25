__author__ = 'sf713420'

from jim_substraction.jim_substraction import run_workflow
import sys

if __name__ == '__main__':

    msid = sys.argv[1]
    run_workflow(msid)
