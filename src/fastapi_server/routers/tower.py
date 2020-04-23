import requests


def sync_tower_project(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return requests.post(url, headers=headers, data="{}",)
