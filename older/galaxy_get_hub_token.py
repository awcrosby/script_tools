#! /usr/bin/env python

"""
Add ansible config galaxy token (access token)
as an environment variable, run script, and
get bearer token which allows access to the api.

Usage:
export ANSIBLE_CFG_TOKEN=xxxxxxxxxxxxxxxx
HUB_BEARER_TOKEN=$(python galaxy_get_hub_token.py)
curl -H "Authorization: Bearer ${HUB_BEARER_TOKEN}" https://console.redhat.com/api/automation-hub/

"""

import os
import requests

ANSIBLE_CFG_TOKEN = os.getenv("ANSIBLE_CFG_TOKEN")
AUTH_URL = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
API_URL = "https://console.redhat.com/api/automation-hub/"

assert ANSIBLE_CFG_TOKEN

# send refresh token, (ansible config token) to auth url to get bearer token
r = requests.post(
        url=AUTH_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": "cloud-services",
            "refresh_token": ANSIBLE_CFG_TOKEN,
        })
hub_bearer_token = r.json()["id_token"]

# check bearer token can access the api
r = requests.get(
    url = API_URL,
    headers = {"Authorization": f"Bearer {hub_bearer_token}"}
)
assert "v3" in r.json()["available_versions"].keys()

# output the bearer token
print(hub_bearer_token)
