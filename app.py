#!/bin/python3
from urllib.error import HTTPError

import config
import urllib3
import logging

from time import sleep
from lib import public_ip
from lib import PyCpanel

urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        ip = public_ip()
    except HTTPError:
        logging.info(f'Error while getting current IP...')
        logging.info(f'Sleeping for {config.every} seconds...')
        sleep(config.every)
        exit()

    logging.info(f'Detected ip is: {ip}')

    server = PyCpanel(hostname=config.cpanel_address,
                      username=config.username,
                      password=config.password,
                      ssl=True,
                      verify=False,
                      check_conn=False)

    logging.info(f'Retrieving DNS Records...')
    dns_data = server.cpanel_api(module='ZoneEdit',
                                 function='fetchzone',
                                 user=config.username,
                                 params={'domain': config.domain})
    logging.info(f'Retrieving DNS Records...Done!')

    # print(json.dumps(finalData, indent=2))

    for entry in dns_data:
        if entry['status'] == 1:
            for record in entry['record']:
                record_name = record.get('name', None)
                record_type = record.get('type', None)
                record_address = record.get('address', None)

                if record_name \
                        and record_name.startswith(config.domain) \
                        and record_type == config.record:
                    if record_address != ip:
                        logging.info(f'Detected IP from DNS Record: {record_address}')

                        logging.info(f'Updating DNS Record with the new IP...')
                        server.cpanel_api(module='ZoneEdit',
                                          function='edit_zone_record',
                                          user=config.username,
                                          params={'Line': record['Line'],
                                                  'domain': config.domain,
                                                  'name': record_name,
                                                  'type': record_type,
                                                  'address': ip,
                                                  'ttl': config.ttl,
                                                  'class': record['class']})
                        logging.info(f'Updating DNS Record with the new IP...Done!')

    logging.info(f'Sleeping for {config.every} seconds...')
    sleep(config.every)
