import fpl.program
import fpl.operators
import fpl.error

import argparse
import sys
import os.path

def main():
    args = parse_arguments()
    program = fpl.program.Program(args.path, args.debug, args.limit)
    try:
        if args.program:
            program.run_file(args.program)
        elif args.command:
            program.run_code(args.command)
        else:
            for line in sys.stdin:
                program.run_code(line)
    except fpl.error.Error as e:
        print('Error occurred: ' + str(e))
        print('Backtrace: ' + str(program.backtrace()))
    except Exception as e:
        print('Python exception occurred while running')
        print('Backtrace: ' + str(program.backtrace()))
        raise e

def parse_arguments():
    parser = argparse.ArgumentParser(description='fpl interpreter')
    parser.add_argument(
            'program', nargs='?',
            help='fpl script to run')
    parser.add_argument(
            '-c', '--command',
            help='run a script from the command line')
    parser.add_argument(
            '-d', '--debug', action='store_true',
            help='run in debug mode (prints tokens as they are read, prints stack)')
    parser.add_argument(
            '-p', '--path',
            help='fpl runtime path. Defaults to ./_fpl_runtime')
    parser.add_argument(
            '-l', '--limit', type=int,
            help='limit the number of commands to run. Set to < 1 to disable')
    args = parser.parse_args()
    if not args.path:
        args.path = '_fpl_runtime'
    if not args.limit:
        args.limit = 1000 #TODO remove this later
    if args.program:
        args.program = os.path.abspath(args.program)
    return args

if __name__ == '__main__':
    main()
