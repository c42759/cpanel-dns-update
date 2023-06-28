#!/bin/python3

import os

cpanel_address = os.environ.get('CPANEL_ADDRESS')
username = os.environ.get('CPANEL_USERNAME')
password = os.environ.get('CPANEL_PASSWORD')

domain = os.environ.get('DOMAIN')
record = os.environ.get('RECORD')
ttl = int(os.environ.get('TTL'))

every = int(os.environ.get('EVERY'))
