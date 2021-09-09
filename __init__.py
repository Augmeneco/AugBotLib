from datetime import datetime
import requests as req
import json
from typing import Iterable, Any, Tuple

CONFIG = None

def load_config():
    with open('config.json') as f:
        CONFIG = json.load(f)

def log_print(text, type='info'):
    print('[' + datetime.now().strftime("%H:%M:%S") + '] ' + text)

def tg_api(method, token=CONFIG['tg_token'], **parameters):
    url = 'https://api.telegram.org/bot' + token + '/' + method

    r = req.post(url, params=parameters).json()
    # if file == None:
    #     r = req.post(url, params=parameters, headers=headers).json()
    # else:
    #     r = req.post(url, params=parameters, headers=headers, files={'file': file}).json()
    
    if not r['ok']:
        log_print('TG ERROR #{}: "{}"'.format(r['error_code'],
                                              r['description']))
                                             #r['parameters']))
        return None

    return r['result']

def vk_api(method, token=CONFIG['vk_token'], **parameters):
    url = 'https://api.vk.com/method/' + method
    parameters['access_token'] = token
    if 'v' not in parameters:
        parameters['v'] = '5.103'

    # if method.split('.')[1][:3] == 'get':
    r = req.post(url, params=parameters)

    result = r.json()

    # print(result)

    if 'error' in result:
        log_print('VK ERROR #{}: "{}"\nPARAMS: {}'.format(result['error']['error_code'],
                                                          result['error']['error_msg'],
                                                          result['error']['request_params']))
        return None

    return result['response']

def signal_first(it:Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    iterable = iter(it)
    yield True, next(iterable)
    for val in iterable:
        yield False, val

def signal_last(it:Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var

    