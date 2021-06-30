from slack_sdk.webhook import WebhookClient
from notifications.slack_block import get_notification_template_slack_block
from notifications.hostinfo import HostInfo
from typing import List, NoReturn
from settings import SETTINGS

def send_report_to_slack(slack_client: WebhookClient, hosts: List[HostInfo]) -> NoReturn:
  slack_client.send(blocks=get_notification_template_slack_block(hosts))

def notify(hosts: List[HostInfo]) -> NoReturn:
  if SETTINGS.SLACK_WEBHOOK:
    slack_client = WebhookClient(SETTINGS.SLACK_WEBHOOK)
    send_report_to_slack(slack_client, hosts)