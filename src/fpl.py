import fpl.program
import fpl.binary_operators
import fpl.unary_operators
import fpl.jump

import argparse
import sys

def main():
    args = parse_arguments()
    program = fpl.program.Program()
    if args.program:
        program.run_file(args.program)
    elif args.command:
        program.run_code(args.command)
    else:
        for line in sys.stdin:
            program.run_code(line)

def parse_arguments():
    parser = argparse.ArgumentParser(description='fpl interpreter')
    parser.add_argument(
            'program', nargs='?',
            help='fpl script to run')
    parser.add_argument(
            '-c', '--command',
            help='run a script from the command line')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
