import os, sys, re
import settings
from datetime import datetime
from nslookup import Nslookup as nslookup

def log(message, error):
    path = '{parent_dir}/logs/{filename}.log'.format(
        parent_dir = os.path.dirname(os.path.realpath(__file__)),
        filename = datetime.now().strftime('%d-%m-%Y')
    )
    open(path, 'a').write(message + '\n')
    if error == 0: print(message)
    else: sys.exit(message)

def getIPv4():
    ipv4 = os.popen("curl -s 'https://ip4.seeip.org'").read()
    if not ipv4: log('[-] ERROR: Unable to reach IPv4 API', 1)
    else: return ipv4

# Horodatage de l'opération
timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
log('{timestamp} :'.format(timestamp=timestamp), 0)

# Vérification de l'adresse IP publique portée par le serveur
public_ip = getIPv4()
log('[+] Public IP address is {public_ip}'.format(public_ip=public_ip), 0)

# Vérification de l'enregistrement DNS
dns_lookup = nslookup(dns_servers=[settings.dns_server]).dns_lookup(settings.domain).answer[0]
log('[+] DNS record for {domain} is {ip}'.format(
    domain = settings.domain,
    ip = dns_lookup
), 0)

# Mise à jour de la zone DNS
if not public_ip == dns_lookup:
    for domain in settings.dns_records:
        log('[+] Updating {domain}'.format(domain=domain), 0)
        request = 'http://www.ovh.com/nic/update?system=dyndns&hostname={domain}&myip={ip}'.format(
            domain = domain,
            ip = public_ip
        )
        os.popen('curl -u {username}:{password} "{request}"'.format(
            username = settings.dynhost_creds['username'],
            password = settings.dynhost_creds['password'],
            request = request
        )).read()
else: log('[+] DNS zone for {domain} is up to date'.format(domain=settings.domain), 1)

log('[+] DNS zone for {domain} was updated'.format(domain=settings.domain), 0)