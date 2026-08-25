import unittest

from app import TOKEN_EXCHANGE_GRANT_TYPE, app


class TokenExchangeEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_accepts_valid_rfc_8693_request(self) -> None:
        response = self.client.post(
            "/oauth/token",
            data={
                "grant_type": TOKEN_EXCHANGE_GRANT_TYPE,
                "subject_token": "opaque-subject-token",
                "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "audience": "native-app",
                "scope": "openid profile",
            },
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "accepted")
        self.assertEqual(payload["grant_type"], TOKEN_EXCHANGE_GRANT_TYPE)

    def test_rejects_non_exchange_grant_type(self) -> None:
        response = self.client.post(
            "/oauth/token",
            data={
                "grant_type": "client_credentials",
                "subject_token": "opaque-subject-token",
                "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
            },
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "unsupported_grant_type")

    def test_rejects_missing_required_fields(self) -> None:
        response = self.client.post(
            "/oauth/token",
            data={
                "grant_type": TOKEN_EXCHANGE_GRANT_TYPE,
                "subject_token": "opaque-subject-token",
            },
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "invalid_request")


if __name__ == "__main__":
    unittest.main()
