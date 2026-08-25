from http import HTTPStatus

from flask import Flask, jsonify, request

TOKEN_EXCHANGE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"

app = Flask(__name__)


@app.post("/oauth/token")
def token_exchange() -> tuple:
    if request.content_type is None or not request.content_type.startswith("application/x-www-form-urlencoded"):
        return (
            jsonify(
                {
                    "error": "invalid_request",
                    "error_description": "token exchange requests must use form encoding",
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    form = request.form

    if form.get("grant_type") != TOKEN_EXCHANGE_GRANT_TYPE:
        return (
            jsonify(
                {
                    "error": "unsupported_grant_type",
                    "error_description": "grant_type must be token-exchange",
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    missing_fields = [name for name in ("subject_token", "subject_token_type") if not form.get(name)]
    if missing_fields:
        return (
            jsonify(
                {
                    "error": "invalid_request",
                    "error_description": f"missing required fields: {', '.join(missing_fields)}",
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    return (
        jsonify(
            {
                "status": "accepted",
                "grant_type": TOKEN_EXCHANGE_GRANT_TYPE,
                "requested_token_type": form.get("requested_token_type"),
                "audience": form.get("audience"),
                "resource": form.get("resource"),
                "scope": form.get("scope"),
            }
        ),
        HTTPStatus.OK,
    )


if __name__ == "__main__":
    app.run()
