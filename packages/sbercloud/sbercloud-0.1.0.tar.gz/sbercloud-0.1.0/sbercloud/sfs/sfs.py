import requests

from sbercloud import SA
from settings import settings
from sfs.exceptions import InitSFSException


class SFS(SA):
    URL = f"https://sfs.{settings.region}.hc.sbercloud.ru"

    @property
    def url(self):
        return f"{self.URL}/v2/{settings.project_id}/shares"

    @property
    def headers(self):
        return {"x-auth-token": self.auth_token, "X-Project-Id": settings.project_id, "x-stage": "RELEASE"}

    def create(self, workspace_id):
        """Создать SFS под workspace_id"""
        now = self.get(workspace_id)
        if now:
            # sfs с таким именем уже существует, нужно вернуть его
            return now

        resp = requests.request(
            "POST",
            self.url,
            headers=self.headers,
            json={
                "share": {
                    "share_type": "default",
                    "name": workspace_id,
                    "share_proto": "NFS",
                    "size": settings.sfs_default_size,
                    "is_public": False,
                }
            },
        )
        if not resp.ok:
            raise InitSFSException
        return resp.json()["share"]

    def create_vpc_access_rule(self, workspace_id):
        """Подключить SFS к VPC"""

    def list(self):
        """Получить список воркспейсов, где подключен SFS"""
        resp = requests.request("GET", self.url, headers=self.headers)
        if not resp.ok:
            raise InitSFSException
        return resp.json().get("shares")

    def get(self, workspace_id):
        """Получить список воркспейсов, где подключен SFS"""
        for share in self.list():
            if share["name"] == workspace_id:
                return share

    def check(self, workspace_id):
        """Проверить существование SFS по workspace_id"""
        return bool(self.get(workspace_id))

    def delete(self, workspace_id):
        """Удаление SFS по workspace_id"""
        _object = self.get(workspace_id)
        resp = requests.request("DELETE", self.url + f"/{_object['id']}", headers=self.headers)
        if not resp.ok:
            raise InitSFSException
        return bool(resp.status_code == 202)
