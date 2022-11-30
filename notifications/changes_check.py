import json  
from notifications.hostinfo import HostInfo, HostService

known_hosts = []

def is_ports_list_changed(portsinfo,tabledata):
    for i in portsinfo:
        if not(i.port in tabledata.keys() and i.name == tabledata[i.port]['software'] and i.definition == tabledata[i.port]['version']):
            return True
        else: 
            return False


def is_hostinfo_changed(hostinfo: HostInfo):
    with open('host_table.json') as jsonFile:
        data = json.load(jsonFile)
        if hostinfo.address.exploded not in data.keys():
            return True          
        elif len(hostinfo.services) != len(data[hostinfo.address.exploded]):
            return True
        elif is_ports_list_changed(hostinfo.services,data[hostinfo.address.exploded]):
            return True       
        else: 
            return False


if __name__ == "__main__":
    is_hostinfo_changed()

    