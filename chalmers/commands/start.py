'''
Start a program.  
The program must be defined with the chalmers 'run' command first

example:

    chalmers start server1
'''
from __future__ import unicode_literals, print_function

from argparse import RawDescriptionHelpFormatter
import logging
import sys

from chalmers.program import Program
from chalmers.program_manager import ProgramManager
from clyent import print_colors


log = logging.getLogger('chalmers.start')


def main(args):

    if args.all:
        programs = list(Program.find_for_user())
    else:
        programs = [Program(name) for name in args.names]

    print("Starting programs %s" % ', '.join([p.name for p in programs]))
    print()
    if args.daemon:
        for prog in programs:
            if not prog.is_running:
                prog.start(args.daemon)

        for prog in programs:
            print("Starting program %-25s ... " % (prog.name[:25]), end='')
            sys.stdout.flush()
            err = prog.wait_for_start()
            if err:
                print_colors('[{=ERROR!c:red} ]')
            else:

                print_colors('[  {=OK!c:green}  ]')

    else:
        mgr = ProgramManager(exit_on_first_failure=True, use_color=args.color)

        for prog in programs:
            mgr.dispatch_start(prog.name)


        for process in mgr.processes:
            process.join()


def restart_main(args):

    if args.all:
        programs = Program.find_for_user()
    else:
        programs = [Program(name) for name in args.names]

    for prog in programs:
        prog.restart()



def add_parser(subparsers):
    parser = subparsers.add_parser('start',
                                      help='Start a program',
                                      description=__doc__,
                                      formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('names', nargs='*', metavar='PROG',
                        help='Names of the programs to start')
    parser.add_argument('-w', '--wait', '--no-daemon', action='store_false', dest='daemon',
                        help='Wait for program to exit')
    parser.add_argument('-d', '--daemon', action='store_true', dest='daemon', default=True,
                        help='Run program as daemon')
    parser.add_argument('-a', '--all', action='store_true',
                        help='start all programs')

    parser.set_defaults(main=main)

    parser = subparsers.add_parser('restart',
                                      help='Restart a program',
                                      description=__doc__)

    parser.add_argument('names', nargs='*', metavar='PROG',
                        help='Names of the programs to start')
    parser.add_argument('-a', '--all', action='store_true',
                        help='start all programs')

    parser.set_defaults(main=restart_main)
