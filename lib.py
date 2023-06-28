#!/bin/python3

import re
import json
import base64
import pycpanel

from urllib import request


def public_ip() -> str:
    html = str(request.urlopen('http://checkip.dyndns.com').read())

    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    match = reg.search(html)

    return match.group()


def get_auth_header(username: str, password: str) -> str:
    enc_user_pw = base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')

    return f'Basic {enc_user_pw}'


class PyCpanel(pycpanel.conn):
    def cpanel_api(self, module, function, user, version=2, params: dict = None, api='json-api/cpanel'):
        generic = {'cpanel_jsonapi_user': user,
                   'cpanel_jsonapi_module': module,
                   'cpanel_jsonapi_func': function,
                   'cpanel_jsonapi_apiversion': version}

        if params is not None:
            params.update(generic)

        elif params is None:
            params = generic

        r = self.__session__.get(self.hostname + api, params=params, verify=self.verify)

        if r.status_code == 403:
            pycpanel.unauthorised()

        if api == 'json-api/cpanel':
            if version == 1:
                return json.loads(r.text)['data']

            return json.loads(r.text)['cpanelresult']['data']

        return r.text
