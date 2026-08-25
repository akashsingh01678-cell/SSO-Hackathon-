# SSO-Hackathon-

## Backend (Phase 1)

This repository now includes a minimal FastAPI backend with an OAuth 2.0 Token Exchange endpoint (RFC 8693-style request fields).

### Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Token exchange endpoint

- **Method:** `POST`
- **Path:** `/oauth/token`
- **Content-Type:** `application/x-www-form-urlencoded`
- **Required fields:**
  - `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`
  - `subject_token`
  - `subject_token_type`

Example request:

```bash
curl -X POST http://127.0.0.1:8000/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=sample-token" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "requested_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "scope=openid profile"
```