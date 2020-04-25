from fastapi import APIRouter, Header, Request, HTTPException, BackgroundTasks, Depends
from config import settings
from .tower import sync_tower_project
import hashlib
import hmac
import logging


router = APIRouter()


invalid_header_message = "Invalid header: X-HUB-SIGNATURE"


async def validate_github_signature(
    request: Request, x_hub_signature: str = Header(None)
) -> None:
    if not x_hub_signature:
        raise HTTPException(status_code=403, detail=invalid_header_message)

    payload = await request.body()

    secret_hmac = hmac.new(bytes(settings.github_secret, "utf8"), payload, hashlib.sha1)
    digest = "sha1=" + secret_hmac.hexdigest()

    logging.info(f"digest: {digest}; x_hub_signature: {x_hub_signature}")
    if not hmac.compare_digest(digest, x_hub_signature):
        raise HTTPException(status_code=403, detail=invalid_header_message)


@router.post(
    "/ansible2_webhook",
    responses={403: {"description": invalid_header_message}},
    dependencies=[Depends(validate_github_signature)],
)
async def ansible2_webhook(background_tasks: BackgroundTasks,):
    background_tasks.add_task(
        sync_tower_project, settings.tower_url, settings.tower_token
    )
    return {"Status": "Valid Github Payload"}
