#!/usr/bin/env python

from graviteeio_cli.cli import main

if __name__ == '__main__':
    try:
        # This is because click uses decorators, and pylint doesn't catch that
        # pylint: disable=no-value-for-parameter
        main()
    except RuntimeError as e:
        import sys
        print('{0}'.format(e))
        sys.exit(1)
    except Exception as e:
        if 'ASCII' in str(e):
            print('{0}'.format(e))
            print(__doc__)
