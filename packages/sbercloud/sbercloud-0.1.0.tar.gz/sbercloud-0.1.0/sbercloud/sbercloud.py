import requests
from settings import settings


class SA:
    AUTH_URL = f"https://iam.{settings.region}.hc.sbercloud.ru/v3/auth/tokens"
    AUTH_TOKEN = None

    @property
    def auth_token(self):

        if not self.AUTH_TOKEN:

            response = requests.request(
                "POST",
                self.AUTH_URL,
                json={
                    "auth": {
                        "identity": {
                            "methods": ["password"],
                            "password": {
                                "user": {
                                    "name": settings.username,
                                    "domain": {"name": settings.domain},
                                    "password": settings.password,
                                }
                            },
                        },
                        "scope": {"project": {"id": settings.project_id}},
                    }
                },
            )
            self.AUTH_TOKEN = response.headers["X-Subject-Token"]

        return self.AUTH_TOKEN
