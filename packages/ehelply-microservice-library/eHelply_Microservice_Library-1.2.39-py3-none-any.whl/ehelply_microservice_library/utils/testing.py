from ehelply_microservice_library.service_bootstrap import ServiceBootstrap

from fastapi.testclient import TestClient

from typing import Type

import json
import os
from pathlib import Path
from pydantic import BaseModel


class TestHeaders(BaseModel):
    access_token: str
    secret_token: str
    project_uuid: str


def make_test_client(service: Type[ServiceBootstrap]) -> TestClient:
    class ServiceTest(service):
        def if_dev_launch_dev_server(self) -> bool:
            return False

    service = ServiceTest()

    app = service.fastapi_driver.instance

    client = TestClient(app)

    return client


def make_test_headers() -> TestHeaders:
    root_path = Path(os.getcwd())
    credentials_file = Path(root_path).resolve().joinpath('credentials.testing.json')

    with open(str(credentials_file)) as file:
        return TestHeaders(json.load(file))

    raise Exception("Invalid credentials file")
