from .tower import sync_tower_project
from fastapi_server.config import settings


def test_sync_tower_project():
    res = sync_tower_project(settings.tower_url, settings.tower_token,)
    assert res.status_code == 202
