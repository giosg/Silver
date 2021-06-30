import ipaddress
from typing import Union, List, Optional

class HostService:
  def __init__(self, name: str, port: int, definition: str, is_vuln: bool, appendix: Optional[str] = None):
    self.name = name
    self.port = port
    self.definition = definition
    self.is_vuln = is_vuln
    self.appendix = appendix

class HostInfo:
  def __init__(self, address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address], services: List[HostService]):
    self.address = address
    self.services = services
