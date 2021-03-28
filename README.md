# dynhost

A python module for OVH DynHost update

## Getting started

### Prerequisites

This application requires Python3 :

```
$ apt install python3 python3-pip
```

You also need to install `nslookup` module for Python3 (more about this module at https://pypi.org/project/nslookup/):

```
$ pip3 install nslookup
```

### Installation

**Cloning the repository**

```
$ git clone https://github.com/Syyyyyn/dynhost.git
```

**Configure**

Edit `settings.py` with your informations :

```python
domain = 'exemple.com'
dns_server = '1.1.1.1'
dynhost_creds = {
    'username': 'exemple.com-dynhost',
    'password': 'P@ssw0rd'
}
dns_records = ['exemple.com', 'www.exemple.com', 'mail.exemple.com']
```

It is higly recommanded to change the permissions of this file in order to protect sensitive informations :

```
$ chmod 740 settings.py
```

## Quick use

```
$ python3 dynhost.py
```

## Logs

The application will automatically output logs to the console as follwed :

```
$ python3 dynhost.py
---
28-03-2021 12:46:58 :
[+] Public IP address is 67.129.182.203
[+] DNS record for exemple.com is 107.180.40.145
[+] Updating exemple.com
[+] Updating www.exemple.com
[+] Updating mail.exemple.com
[+] DNS zone for exemple.com was updated
```

If you wish to keep track of these actions, simply create a `logs` folder in the same directory as `dynhost.py`.

**Enable logs**

```
$ mkdir logs
```

**Disable logs**

```
$ rm -r logs/
```