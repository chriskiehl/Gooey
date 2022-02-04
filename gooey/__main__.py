'''
Delegates arguments to the main Gooey runner.

For use when run directly from command line with the -m (module) flag:

  e.g. $ python -m gooey

'''

from gooey.cli import main

if __name__ == '__main__':
    main()
