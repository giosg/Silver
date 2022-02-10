from slack_sdk.webhook import WebhookClient
from notifications.slack_block import get_notification_template_slack_block
from notifications.hostinfo import HostInfo
from typing import List, NoReturn
from settings import SETTINGS

MAX_SLACK_BLOCK_COUNT_ALLOWED = 50

def send_report_to_slack(slack_client: WebhookClient, hosts: List[HostInfo]) -> NoReturn:
  blocks = get_notification_template_slack_block(hosts)
  c_begin, c_end = 0, MAX_SLACK_BLOCK_COUNT_ALLOWED
  while c_begin < len(blocks):
    slack_client.send(blocks=blocks[c_begin:c_end])
    c_begin += MAX_SLACK_BLOCK_COUNT_ALLOWED
    c_end += MAX_SLACK_BLOCK_COUNT_ALLOWED

def notify(hosts: List[HostInfo]) -> NoReturn:
  if SETTINGS.SLACK_WEBHOOK:
    slack_client = WebhookClient(SETTINGS.SLACK_WEBHOOK)
    send_report_to_slack(slack_client, hosts)