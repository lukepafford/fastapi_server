from fastapi import APIRouter, Header, Request, HTTPException, BackgroundTasks
from config import settings
from .tower import sync_tower_project
import hashlib
import hmac
import logging


router = APIRouter()


def validate_github_signature(
    secret: str, payload: bytes, github_signature: str
) -> bool:
    if not github_signature:
        return False

    secret_hmac = hmac.new(bytes(secret, "utf8"), payload, hashlib.sha1)
    digest = "sha1=" + secret_hmac.hexdigest()

    logging.info(f"digest: {digest}; github_signature: {github_signature}")
    if hmac.compare_digest(digest, github_signature):
        return True
    else:
        return False


@router.post("/ansible2_webhook")
async def ansible2_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature: str = Header(None),
):
    payload = await request.body()
    if not validate_github_signature(settings.github_secret, payload, x_hub_signature):
        raise HTTPException(status_code=403, detail="Invalid Github payload")

    background_tasks.add_task(
        sync_tower_project, settings.tower_url, settings.tower_token
    )
    return {"Status": "Valid Github Payload"}
