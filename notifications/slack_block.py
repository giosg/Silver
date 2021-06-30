import slack_sdk
from typing import List
from notifications.hostinfo import HostInfo, HostService
from datetime import datetime
from collections import namedtuple

CIRCLES = {
  "VULN": ":red_circle:",
  "NOT_VULN": ":large_green_circle:",
  "UNKNOWN": ":large_orange_circle:"
}


def __get_service_field_section(service: HostService) -> dict:
  vuln = "VULN" if service.is_vuln else "NOT_VULN"
  if service.is_vuln is None:
    vuln = "UNKNOWN"
  return {
	  "type": "mrkdwn",
		"text": "{vulnerability_level_mark} Port: *{port}*\nService: *{service_name}*\nVersion: *{service_version}*\n".format_map(
      {
        "vulnerability_level_mark": CIRCLES[vuln],
        "port": service.port,
        "service_name": service.name,
        "service_version": service.definition
      }
    )
	}

def __get_host_field_section(hostinfo: HostInfo) -> list:
  blocks = [
    {
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Host scanned: *{ip}*\nFound *{port_qty}* ports, of those:".format_map(
          {
            "ip": hostinfo.address.exploded,
            "port_qty": len(hostinfo.services)
          }
        )
      }
		}
  ]
  for i in range(0, len(hostinfo.services), 2):
    fields = []
    fields.append(
      __get_service_field_section(hostinfo.services[i])
    )
    if i+1 < len(hostinfo.services):
      fields.append(
      __get_service_field_section(hostinfo.services[i+1])
      )
    blocks.append(
		  {
			  "type": "section",
			  "fields": fields
		  }
    )
  return blocks

def get_notification_template_slack_block(hosts: List[HostInfo]) -> list:
  blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Host scan report {} :male-detective::skin-tone-2: ".format(datetime.now().strftime("%a %b %d %H:%M:%S %Y")),
				"emoji": True
			}
		}
  ]
  for host in hosts:
    blocks = blocks + __get_host_field_section(host)
  print(blocks)
  return blocks