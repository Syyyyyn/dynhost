import os, sys
import settings
from datetime import datetime
from nslookup import Nslookup as nslookup

def log(message, error):
    if os.path.exists('./logs'):
        log_file = '{parent_dir}/logs/{filename}.log'.format(
            parent_dir = os.path.dirname(os.path.realpath(__file__)),
            filename = datetime.now().strftime('%d-%m-%Y')
        )
        open(log_file, 'a').write(message + '\n')
    if error == 0: print(message)
    else: sys.exit(message)

def getIPv4():
    ipv4 = os.popen("curl -s 'https://ip4.seeip.org'").read()
    if not ipv4: log('[-] ERROR: Unable to reach IPv4 API. Please check your Internet connection or firewall policy.', 1)
    else: return ipv4

# Date stamping the operation
timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
log('{timestamp} :'.format(timestamp=timestamp), 0)

# Error handling
if settings.zone == '': log('[-] ERROR: Invalid parameter (zone) in settings.py. Please check your settings and try again.', 1)
if len(settings.nameservers) == 0: log('[-] WARNING: Invalid parameter (nameserver) in settings.py. Public DNS 1.1.1.1 and 1.0.0.1 will be used as default nameservers.', 0)
for nameserver in settings.nameservers:
    if nameserver == '': log('[-] ERROR: Invalid parameter (nameserver) in settings.py. Please check your settings and try again.', 1)
if settings.dynhost_creds['username'] == '': log('[-] ERROR: Invalid parameter (dynhost_creds:username) in settings.py. Please check your settings and try again.', 1)
if settings.dynhost_creds['password'] == '': log('[-] ERROR: Invalid parameter (dynhost_creds:password) in settings.py. Please check your settings and try again.', 1)
if len(settings.dns_records) == 0: log('[-] ERROR: Invalid parameter (dns_records) in settings.py. Please check your settings and try again.', 1)
for record in settings.dns_records:
    if record == '': log('[-] ERROR: Invalid parameter (dns_records) in settings.py. Please check your settings and try again.', 1)

# Get server's public IP address
public_ip = getIPv4()
log('[+] Public IP address is {public_ip}'.format(public_ip=public_ip), 0)

# Resolve domain name IP address
log('[+] Resolving {zone}'.format(zone=settings.zone), 0)
nslookup_response = None
if settings.nameservers == '':
    if not nslookup(dns_servers=['1.1.1.1', '1.0.0.1']).dns_lookup(settings.zone).answer: log('[-] ERROR: Could not resolve {zone} (EMPTY_RESPONSE).'.format(zone=settings.zone), 1)
    else: nslookup_response = nslookup(dns_servers=['1.1.1.1', '1.0.0.1']).dns_lookup(settings.zone).answer[0]
else:
    if not nslookup(dns_servers=settings.nameservers).dns_lookup(settings.zone).answer: log('[-] ERROR: Could not resolve {zone} (EMPTY_RESPONSE).'.format(zone=settings.zone), 1)
    else: nslookup_response = nslookup(dns_servers=['1.1.1.1', '1.0.0.1']).dns_lookup(settings.zone).answer[0]
log('[+] Current IP address for {zone} is {ip}'.format(zone=settings.zone, ip=nslookup_response), 0)

# Update DNS zone
if not public_ip == nslookup_response:
    for record in settings.dns_records:
        request = 'http://www.ovh.com/nic/update?system=dyndns&hostname={record}&myip={ip}'.format(record=record, ip=public_ip)
        response = os.popen('curl -su {username}:{password} "{request}"'.format(
            username = settings.dynhost_creds['username'],
            password = settings.dynhost_creds['password'],
            request = request
        )).read()
        if 'good' in response: log('[+] Updating {record}'.format(record=record), 0)
        if 'nohost' in response: log('[-] WARNING: No record found for {record}'.format(record=record), 0)
        if '401 Authorization Required' in response: log('[-] ERROR: Wrong credentials. Please check your settings and try again.'.format(record=record), 1)
else: log('[+] DNS zone for {zone} is up to date'.format(zone=settings.zone), 1)

# It made it to the end, congrats
log('[+] DNS zone for {zone} was updated'.format(zone=settings.zone), 0)