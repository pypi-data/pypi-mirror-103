#!/usr/bin/env python3
""" infer_playbook_limit.py
Parse through a list of changed `ansible inventory` files to determine an appropriate 
playbook_limit variable. The inferred playbook_limit is printed to stdout.
"""
import os
from typing import List
from buildtools import util

import configargparse

from buildtools import BuildToolsTemplate


class InferPlaybookLimit(BuildToolsTemplate):
    def __init__(self):
        cli_path = ['infer', 'ansible', 'playbook-limit']
        cli_descriptions = {'infer': 'Make some inference based on the provided arguments.',
                            'ansible': 'Make some inference about an Ansible project.',
                            'playbook-limit': 'Infer the --playbook-limit for an ansible project (returned to stdout).',
                            }
        summary = '''Infer the playbook-limit for an Ansible project. Parse through a list of changed `ansible 
        inventory` files, and compare it against the project's `hosts` file to determine the optimal `playbook_limit` 
        value to be passed to Ansible. The inferred `playbook_limit` is printed to stdout.'''
        super().__init__(cli_path, cli_descriptions, summary)

    def config_parser(self, parser: configargparse.ArgumentParser, parents: List[configargparse.ArgumentParser] = None):
        parser.set_defaults(func=self.run)
        parser.add_argument('source',
                            help='The path to the file that contains a list of paths (each separated by a  new line).')
        parser.add_argument('hosts',
                            help='The path to the relevant (`ini` styled) Ansible hosts file.')

    def run(self, args):
        # Do the work of actually inferring the playbook limit from the pathnames listed in 'source' file
        playbook_limit = util.infer_playbook_limit(args.source, args.hosts)

        # Print the PLAYBOOK_LIMIT to stdout
        print(",".join(list(playbook_limit)))
