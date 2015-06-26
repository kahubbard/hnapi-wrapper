#!/usr/bin/python

from sseclient import SSEClient
import json
import sys
import pygerduty

pager = pygerduty.PagerDuty('test subscribe', '7b162cbac5d14faa9ccba8fb91968a68')

messages = SSEClient('https://popping-heat-7885.firebaseio.com/.json')
for message in messages:
    msg_data = json.loads(message.data)
    if msg_data is None or message.event is 'keep-alive':
        continue
    elif 'sbumitted' in msg_data['path']:
        #data format {u'path': u'/sbumitted/2', u'data': u'vonnegut'}
        pager.create_event('7b162cbac5d14faa9ccba8fb91968a68', 'hubb comment', 'trigger', msg_data)
