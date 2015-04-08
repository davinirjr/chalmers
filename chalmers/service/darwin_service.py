"""
Install a launchd rule to run at boot 
"""
from __future__ import unicode_literals, print_function

import logging
from subprocess import check_output, CalledProcessError
import sys

from chalmers import errors
launchd_label = "org.continuum.chalmers"

log = logging.getLogger('chalmers.service')

def get_launchd():
    try:
        return check_output(['launchctl', 'list', launchd_label])
    except OSError as err:
        raise errors.ChalmersError("Could not access program 'launchctl' required for osx service install")
    except CalledProcessError as err:
        if err.returncode == 1:
            # launchd_label was not found
            return None
        raise


def add_launchd():
    try:
        chalmers_script = sys.argv[0]
        command = ['launchctl', 'submit', '-l', launchd_label, '--',
                   sys.executable, chalmers_script, 'start', '--all']
        log.info("Running command: %s" % ' '.join(command))
        output = check_output(command).strip()
        log.info("launchctl: %s" % output)
    except OSError as err:
        raise errors.ChalmersError("Could not access program 'launchctl' required for osx service install")
    except CalledProcessError as err:
        if err.returncode == 1:
            # launchd_label was not found
            raise errors.ChalmersError("Chalmers service is already installed")
        raise


def install(args):
    """Create a launchd plist and load as a global daemon"""

    if args.system is not False:
        raise  errors.ChalmersError("--system is not yet implemented for osx. "
                                    "Run 'sudo su - USERNAME -c \"chalmers install service\"' ")

    log.info("Adding chalmers launchd plist")
    add_launchd()
    log.info("All chalmers programs will now run on boot")

def uninstall(args):
    """Uninstall launchd plist for chalmers"""

    log.info("Removing chalmers plist from launchd")
    try:
        command = ['launchctl', 'remove', launchd_label]
        log.info("Running command: %s" % ' '.join(command))
        output = check_output(command).strip()
    except CalledProcessError as err:
        if err.returncode == 1:
            raise errors.ChalmersError("Chalmers service is not installed")
        raise
    else:
        log.info("Chalmers service has been removed")

def status(args):
    """Check if chalmers will be started at reboot"""

    launchd_lines = get_launchd()
    if launchd_lines:
        log.info("Chalmers is setup to start on boot")
    else:
        log.info("Chalmers will not start on boot")

