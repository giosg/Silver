import json
from notifications.hostinfo import HostInfo, HostService

def is_ports_list_changed(portsinfo, tabledata):
    for i in portsinfo.keys():
        if not(i in tabledata.keys() and portsinfo[i]==tabledata[i]):
            return True
        else: 
            return False


def is_hostinfo_changed(hostinfo: HostInfo):
    try:
        with open('/secscan/results/previous_results.json') as previous, open('/secscan/results/current_results.json') as current:
            data_prev=json.load(previous)
            data_current=json.load(current)
            if hostinfo.address.exploded not in data_prev.keys():
                return True
            elif len(hostinfo.services) != len(data_prev[hostinfo.address.exploded]):
                return True
            elif is_ports_list_changed(data_current[hostinfo.address.exploded], data_prev[hostinfo.address.exploded]):
                return True
            else:
                return False
    except :
        return True