import secrets
from typing import Optional

from fastapi import FastAPI, Form, HTTPException

app = FastAPI(title="MOSIP Native SSO Backend")

TOKEN_EXCHANGE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"
ACCESS_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:access_token"


@app.post("/oauth/token")
async def token_exchange(
    grant_type: str = Form(...),
    subject_token: str = Form(...),
    subject_token_type: str = Form(...),
    requested_token_type: str = Form(ACCESS_TOKEN_TYPE),
    audience: Optional[str] = Form(None),
    resource: Optional[str] = Form(None),
    scope: Optional[str] = Form(None),
    actor_token: Optional[str] = Form(None),
    actor_token_type: Optional[str] = Form(None),
):
    if grant_type != TOKEN_EXCHANGE_GRANT_TYPE:
        raise HTTPException(
            status_code=400,
            detail="Unsupported grant_type for this endpoint.",
        )

    expires_in = 3600
    access_token = secrets.token_urlsafe(48)

    return {
        "access_token": access_token,
        "issued_token_type": requested_token_type,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "scope": scope or "",
        "subject_token_type": subject_token_type,
        "audience": audience,
        "resource": resource,
        "actor_token_present": bool(actor_token and actor_token_type),
        "subject_token_received": bool(subject_token),
    }
