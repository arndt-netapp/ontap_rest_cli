#!/usr/bin/env python3

################################################################################
#
# Example code using the ONTAP REST API CLI passthrough (ontap_rest_cli)
#
# This sample code implements example code for various types of commands run
# via the ONTAP REST API CLI passthrough interface. 
#
# Requirements:
#   1. Python 3.5 or higher.
#   2. The netapp-ontap Python package as described at:
#      https://pypi.org/project/netapp-ontap/
#      Note: Use module version 9.8.0 or higher, even with ONTAP 9.7!
#   3. ONTAP 9.7 or higher.
#
# Run "./ontap_rest_cli.py -h" to see usage and examples.
#
################################################################################

import sys
import logging
from argparse import ArgumentParser
from getpass import getpass

# Import the required netap_ontap modules.
from netapp_ontap import utils
from netapp_ontap import config as NaConfig
from netapp_ontap.host_connection import HostConnection as NaHostConnection
from netapp_ontap.error import NetAppRestError
from netapp_ontap.resources import CLI as NaCLI


# Get example - retrieving storage efficiency savings for volumes.
def rest_get():
    cmd = "volume show"
    query_args = {
        "vserver": "vs1",
        "fields": "size,used,sis-space-saved",
    }
    try:
        response = NaCLI().execute(cmd, **query_args)
    except NetAppRestError:
        print("Error running Rest CLI get call")
        raise
    output = response.http_response.json()
    for record in output["records"]:
        print(record)


# Post example - create a new efficiency policy.
def rest_post():
    cmd = "volume efficiency policy create"
    body_args = {
        "vserver": "vs1",
        "policy": "AlwaysOn",
        "schedule": "5min",
        "qos-policy": "background",
    }
    try:
        response = NaCLI().execute(cmd, body=body_args)
    except NetAppRestError:
        print("Error running Rest CLI post call")
        raise
    output = response.http_response.json()
    print(output)


# Patch example - update the volume efficiency policy for a volume.
def rest_patch():
    cmd = "volume efficiency modify"
    query_args = {
        "vserver": "vs1",
        "volume": "clitestvol",
    }
    body_args = {
        "policy": "AlwaysOn",
    }
    try:
        response = NaCLI().execute(cmd, body=body_args, **query_args)
    except NetAppRestError:
        print("Error running Rest CLI patch call")
        raise
    output = response.http_response.json()
    print(output)


# Delete example - delete an efficiency policy.
def rest_delete():
    cmd = "volume efficiency policy delete"
    body_args = {
        "vserver": "vs1",
        "policy": "AlwaysOn",
    }
    try:
        response = NaCLI().execute(cmd, body=body_args)
    except NetAppRestError:
        print("Error running Rest CLI delete call")
        raise
    output = response.http_response.json()
    print(output)


# Parse the command line
parser = ArgumentParser(
    usage="%(prog)s [options] [operation]...",
    description="Examples of GET, POST, PATCH, and DELETE ONTAP REST API CLI passthrough operations."
)
parser.add_argument(
    '-c', '--cluster', nargs='?', required=True,
    help='cluster name or IP'
)
parser.add_argument(
    '-u', '--username', nargs='?', default='admin',
    help='username to connect with (default: %(default)s)'
)
parser.add_argument(
    '-p', '--password', nargs='?',
    help='password for username'
)
parser.add_argument(
    '-d', '--debug', action='store_true',
    help='Use debug mode for API calls'
)
parser.add_argument(
    'operation', nargs='?', default='GET',
    choices=['GET', 'POST', 'PATCH', 'DELETE'],
    help='One of GET, POST, PATCH, or DELETE (default: %(default)s)',
)
args = parser.parse_args()
if not args.password:
    args.password = getpass()

# Setup the REST API connection to ONTAP.
# Using verify=False to ignore that we may see self-signed SSL certificates.
NaConfig.CONNECTION = NaHostConnection(
    host = args.cluster,
    username = args.username,
    password = args.password,
    verify = False,
    poll_timeout = 120,
)

# Configure debug mode if required.
if args.debug:
    # Uncomment these for additional ONTAP REST API debugging.
    logging.basicConfig(level=logging.DEBUG)
    utils.DEBUG = 1
    utils.LOG_ALL_API_CALLS = 1

# Call the appropriate operation.
if args.operation == "GET":
    rest_get()
if args.operation == "POST":
    rest_post()
if args.operation == "PATCH":
    rest_patch()
if args.operation == "DELETE":
    rest_delete()
