import re
import subprocess
from hashlib import sha1
from os import remove, path

from core.utils import load_json

def parse_result(ip, nmapfile):
	result = {}
	result[ip] = {}
	with open(nmapfile, 'r') as file:
		for line in file:
			match = re.search(r'<port protocol="\w+" portid="(\d+)"><state state="([^"]+)" reason="[^"]+" reason_ttl="\d+"/><service name="([^"]*)"( product="([^"]*)")?( version="([^"]*)")?.*?>.*?(<cpe>([^<]*))?', line)
			if match:
				port = match.group(1)
				result[ip][port] = {}
				result[ip][port]['state'] = match.group(2)
				result[ip][port]['service'] = match.group(3)
				result[ip][port]['software'] = match.group(5)
				result[ip][port]['version'] = match.group(7)
				result[ip][port]['cpe'] = match.group(9)
				if not match.group(7) and match.group(9):
					if match.group(9).count(':') > 3:
						result[ip][port]['version'] = match.group(9).split(':')[-1]
	return result

def pymap(ip, ports, exclude, workdir, cleanup):
	ports = ','.join([str(port) for port in sorted(ports)])
	nmapfile = path.join(workdir, "nmap-{}-{}.xml".format(
			ip,
			sha1(
				(ip+ports).encode('utf8')
			).hexdigest()
		)
	)
	if ip not in exclude:
		subprocess.getoutput('nmap -Pn -sT -oX %s -sV %s -p%s' % (nmapfile, ip, ports))
		result = parse_result(ip, nmapfile)
		if cleanup:
			remove(nmapfile)
		return result
	else:
		return 'cached'
