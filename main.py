import os
import pytz
from datetime import datetime, timedelta
import requests


TOKEN = os.environ['TOKEN']
HOST = os.environ.get('HOST', 'https://whatsapp.turn.io')

# Get the date range in the UTC timezone, for this
# example we're looking at messages sent & received in the last 24 hours
today = datetime.utcnow().replace(tzinfo=pytz.utc)
yesterday = today - timedelta(hours=24)

# Request a cursor from the API for the given date range
# and specify the scrubbing rules we want
cursor_response = requests.post(url=f'{HOST}/v1/data/messages/cursor', headers={
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.v1+json'
  }, json={
    "from": yesterday.isoformat(),
    "until": today.isoformat(),
    "ordering": "asc",
    "page_size": 100
  })

  # Request a cursor and unpack it
cursor_data = cursor_response.json()
cursor = cursor_data['cursor']
cursor_expires_at = cursor_data['expires_at']

print(f"Cursor expires at {cursor_expires_at}")

# Request any data for the given cursor
first_page_response = requests.get(url=f'{HOST}/v1/data/messages/cursor/{cursor}', headers={
  'Authorization': f'Bearer {TOKEN}',
  'Accept': 'application/vnd.v1+json',
})
first_page_data = first_page_response.json()

messages = first_page_data['data']
# if there are more than 1 pages, the `paging` payload
# will inform you of that.
paging = first_page_data['paging']

# inbound messages follow the WABiz API format and
# have the contacts and messages keys
#
# outbound messages following the API format for sending
# and do not have those keys.
#
# Will use that as a simple filter to only work with
# messages that have been sent to a recipient via WhatsApp
# and which have a card_uuid set
outbound_messages_with_card_uuid = filter(
  lambda m: 'messages' not in m and m['_vnd']['v1']['card_uuid'], messages)

# helper function to find a single card for a UUID
def find_card(uuid):
  return requests.get(url=f'{HOST}/v1/cards/{uuid}', 
  headers={
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.v1+json'
  }).json()

# helper function to just retrieve the label values
# for a given card
def get_labels_for_card(card):
  for card_number_tag in card['card_number_tags']:
    number_tag = card_number_tag['number_tag']
    yield number_tag['value']

# helper function to print a card summary for a message
def print_card_summary(message):
  # get the recipient
  to = m['to']
  # get the UUID
  card_uuid = m['_vnd']['v1']['card_uuid']
  # find the card
  card = find_card(card_uuid)
  # get the labels and the title
  card_labels = "\", \"".join(get_labels_for_card(card))
  card_title = card['title']
  # print a summary
  if card_labels:
    print(f'"{to}" received the card "{card_title}" with labels: "{card_labels}"')
  else:
    print(f'"{to}" received the card "{card_title}" without labels')

# Loop over the messages send
for m in outbound_messages_with_card_uuid:
  print_card_summary(m)
