#!/usr/bin/env python
###
# (C) Copyright (2012-2015) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library
standard_library.install_aliases()
import sys

PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)
if PY2:
    if PYTHON_VERSION < (2, 7, 9):
        raise Exception('Must use Python 2.7.9 or later')
elif PYTHON_VERSION < (3, 4):
    raise Exception('Must use Python 3.4 or later')

import hpOneView as hpov
from pprint import pprint


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print('EULA display needed')
            con.set_eula('no')
    except Exception as e:
        print('EXCEPTION:')
        print(e)


def login(con, credential):
    # Login with givin credentials
    try:
        con.login(credential)
    except:
        print('Login failed')


def add_network(net, name, minbw, maxbw, vlan, vtype, purpose, slink, private):

    # Invert the smart link boolean value
    slink = not slink
    maxbw = int(maxbw * 1000)
    minbw = int(minbw * 1000)

    if vtype != 'Tagged':
        vlan = 0

    enet = net.create_enet_network(name=name,
                                   vlanId=vlan,
                                   purpose=purpose,
                                   smartLink=slink,
                                   privateNetwork=private,
                                   ethernetNetworkType=vtype,
                                   typicalBandwidth=minbw,
                                   maximumBandwidth=maxbw)

    print('\nCreated Ethernet Network\n')
    print('{0:<15}\t{1:<15}\t{2:<15}\t{3:<15}\t{4:<15}\t{5:<15}'.format('NAME', 'VLAN', 'TYPE', 'PURPOSE', 'SMART LINK', 'PRIVATE'))
    print('{0:<15}\t{1:<15}\t{2:<15}\t{3:<15}\t{4:<15}\t{5:<15}'.format('-------', '-------', '-------', '-------', '----------', '-------'))
    print('{0:<15}\t{1:<15}\t{2:<15}\t{3:<15}\t{4:<15}\t{5:<15}'.format(enet['name'], enet['vlanId'],
          enet['ethernetNetworkType'], enet['purpose'], str(enet['smartLink']), str(enet['privateNetwork'])))


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define new ethernet network

    Usage: ''')
    parser.add_argument('-a', dest='host', required=True,
                        help='''
    HPE OneView Appliance hostname or IP address''')
    parser.add_argument('-u', dest='user', required=False,
                        default='Administrator',
                        help='''
    HPE OneView Username''')
    parser.add_argument('-p', dest='passwd', required=True,
                        help='''
    HPE OneView Password''')
    parser.add_argument('-c', dest='cert', required=False,
                        help='''
    Trusted SSL Certificate Bundle in PEM (Base64 Encoded DER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-j', dest='domain', required=False,
                        default='Local',
                        help='''
    HPE OneView Authorized Login Domain''')
    parser.add_argument('-n', dest='network_name', required=True,
                        help='''
    Name of the network''')
    parser.add_argument('-b', dest='prefered_bandwidth', type=float,
                        required=False, default=2.5,
                        help='''
    Typical bandwidth between .1  and 20 Gb/s''')
    parser.add_argument('-m', dest='max_bandwidth', type=float, required=False,
                        default=10,
                        help='''
    Maximum bandwidth between .1 and 20 Gb/s''')
    parser.add_argument('-v', dest='vlan', required=False,
                        help='''
    VLAN ID''')
    parser.add_argument('-z', dest='vlan_type',
                        choices=['Tagged', 'Untagged', 'Tunnel'],
                        required=False, default='Tagged',
                        help='''
    VLAN Type''')
    parser.add_argument('-o', dest='purpose', choices=['FaultTolerance',
                        'General', 'Management', 'VMMigration'],
                        required=False, default='General',
                        help='''
    A description to attach to a network to help categorize the purpose of
    the  network''')
    parser.add_argument('-s', dest='slink', required=False,
                        action='store_true',
                        help='''
    DISABLE Smart Link''')
    parser.add_argument('-x', dest='private', required=False,
                        action='store_true',
                        help='''
    ENABLE Private Network''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    net = hpov.networking(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    if args.vlan_type == 'Tagged' and not args.vlan:
        print('Error, you must specify a VLAN ID for a Tagged network')
        sys.exit()

    if args.prefered_bandwidth < .1 or args.prefered_bandwidth > 20:
        print('Error, prefered bandwidth must be between .1 and 20 Gb/s')
        sys.exit()
    if args.max_bandwidth < .1 or args.max_bandwidth > 20:
        print('Error, max bandwidth must be between .1 and 20 Gb/s')
        sys.exit()
    if args.prefered_bandwidth > args.max_bandwidth:
        print('Error, prefered bandwidth must be less than or equal '
              'to the maximum bandwidth')
        sys.exit()

    add_network(net, args.network_name, args.prefered_bandwidth,
                args.max_bandwidth, args.vlan, args.vlan_type,
                args.purpose, args.slink, args.private)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
