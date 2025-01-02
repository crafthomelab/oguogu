import json
import os

with open(os.path.join(os.path.dirname(__file__), 'OGUOGU.json'), 'r') as f:
    content = json.load(f)

OGUOGU_EVENT_ABI = content['abi']
