'''
'''
from __future__ import unicode_literals, print_function

from chalmers.program import Program

def main(args):

    for prog in Program.find_for_user():
        print('prog', prog.data['name'])
        exit_message = prog.data.get('exit_message', 'Stopped')
        text_status = 'Running' if prog.is_running else exit_message
        print('%s, %s' % (prog.data['name'], text_status))


def add_parser(subparsers):
    parser = subparsers.add_parser('list',
                                      help='List registered commands',
                                      description=__doc__)

    parser.set_defaults(main=main)
